import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QMessageBox, QComboBox, QMainWindow, QToolBar, QPushButton)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont
from core_logic import QuestionManager, ScoreManager, Timer

class MathTutorGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.questionManager=QuestionManager()
        self.scoreManager=ScoreManager()
        self.timer =Timer()
        self.initUI()
        self.timer_qt =QTimer(self)
        self.timer_qt.timeout.connect(self.updateStopwatchDisplay)
        self.timer_qt.start(1000)
        self.questionManager.loadQuestions("addition_easy.txt")
        self.showQuestion()

    def initUI(self):
        self.setWindowTitle("Math Tutor")
        self.setGeometry(100,100,800,600)
        centralWidget= QWidget()
        self.setCentralWidget(centralWidget)
        mainLayout =QVBoxLayout(centralWidget)
        self.lessonSelector= QComboBox()
        self.lessonSelector.addItem("Addition (Easy)","addition_easy.txt")
        self.lessonSelector.addItem("Addition (Medium)", "addition_medium.txt")
        self.lessonSelector.currentIndexChanged.connect(self.onLessonChange)
        mainLayout.addWidget(self.lessonSelector)
        self.scoreDisplay =QLabel("Score: 0")
        mainLayout.addWidget(self.scoreDisplay)

        self.stopwatchDisplay= QLabel("Time: 00:00")
        mainLayout.addWidget(self.stopwatchDisplay)
        self.questionLabel= QLabel("Question will appear here")
        self.questionLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        mainLayout.addWidget(self.questionLabel)
        self.answerInput= QLineEdit()
        self.answerInput.returnPressed.connect(self.checkAnswer)
        mainLayout.addWidget(self.answerInput)
    def onLessonChange(self,index):
        lessonFile =self.lessonSelector.currentData()
        if lessonFile:
            self.questionManager.loadQuestions(lessonFile)
            self.timer.start()
            self.showQuestion()
    def showQuestion(self):
        question =self.questionManager.get_current_question()
        if question:
            self.questionLabel.setText(question)
            self.scoreDisplay.setText(f"Score: {self.scoreManager.get_score()}")
            self.answerInput.clear()
    def checkAnswer(self):
        userAnswer=self.answerInput.text()
        if self.questionManager.check_answer(userAnswer):
            self.scoreManager.correct_answer()
            if not self.questionManager.advance_question():
                QMessageBox.information(self, "Finished", "Congratulations, you've completed all the questions!")
                self.timer.stop()
        else:
            self.scoreManager.wrong_answer()
        self.showQuestion()

    def updateStopwatchDisplay(self):
        self.stopwatchDisplay.setText(f"Time: {self.timer.get_elapsed_time()}")

if __name__=='__main__':
    app=QApplication(sys.argv)
    mainWindow=MathTutorGUI()
    mainWindow.show()
    sys.exit(app.exec())
