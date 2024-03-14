import sys
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib
from core_logic import QuestionManager, ScoreManager, Timer

class MathTutorGUI(Gtk.Window):
    def __init__(self):
        super().__init__(title="Math Tutor")
        self.set_default_size(800,600)
        self.set_border_width(10)
        self.questionManager=QuestionManager()
        self.scoreManager=ScoreManager()
        self.timer =Timer()
        self.initUI()

        GLib.timeout_add_seconds(1,self.updateStopwatchDisplay)
        self.questionManager.loadQuestions("addition_easy.txt")
        self.showQuestion()
    def initUI(self):
        vbox =Gtk.Box(orientation=Gtk.Orientation.VERTICAL,spacing=6)
        self.add(vbox)
        self.lessonSelector= Gtk.ComboBoxText()
        self.lessonSelector.append_text("Addition (Easy)")
        self.lessonSelector.append_text("Addition (Medium)")
        self.lessonSelector.connect("changed",self.onLessonChange)
        vbox.pack_start(self.lessonSelector,False, False,0)
        self.scoreDisplay =Gtk.Label(label="Score: 0")
        vbox.pack_start(self.scoreDisplay, False,False,0)
        self.stopwatchDisplay= Gtk.Label(label="Time: 00:00")
        vbox.pack_start(self.stopwatchDisplay, False, False, 0)
        self.questionLabel= Gtk.Label(label="Question will appear here")
        vbox.pack_start(self.questionLabel,False, False,0)
        self.answerInput =Gtk.Entry()
        self.answerInput.connect("activate",self.checkAnswer)
        vbox.pack_start(self.answerInput, False,False, 0)
    def onLessonChange(self,combo):
        text =combo.get_active_text()
        lessonFile= "addition_easy.txt" if text == "Addition (Easy)" else "addition_medium.txt"
        self.questionManager.loadQuestions(lessonFile)
        self.timer.start()
        self.showQuestion()
    def showQuestion(self):
        question =self.questionManager.get_current_question()
        if question:
            self.questionLabel.set_text(question)
            self.scoreDisplay.set_text(f"Score: {self.scoreManager.get_score()}")
            self.answerInput.set_text("")

    def checkAnswer(self, widget):
        userAnswer= self.answerInput.get_text()
        if self.questionManager.check_answer(userAnswer):
            self.scoreManager.correct_answer()
            if not self.questionManager.advance_question():
                dialog =Gtk.MessageDialog(self,0,Gtk.MessageType.INFO,
                                           Gtk.ButtonsType.OK, "Finished")
                dialog.format_secondary_text("Congratulations, you've completed all the questions!")
                dialog.run()
                dialog.destroy()
                self.timer.stop()
        else:
            self.scoreManager.wrong_answer()
        self.showQuestion()

    def updateStopwatchDisplay(self):
        self.stopwatchDisplay.set_text(f"Time: {self.timer.get_elapsed_time()}")
        return True

if __name__=='__main__':
    app=Gtk.Application()
    win= MathTutorGUI()
    win.connect("destroy",Gtk.main_quit)
    win.show_all()
    Gtk.main()
