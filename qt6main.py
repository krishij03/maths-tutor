import sys,os
from PyQt6.QtWidgets import (QApplication,QWidget,QVBoxLayout,QLabel,QLineEdit,QMessageBox,QComboBox,QMainWindow,QToolBar)
from PyQt6.QtCore import Qt,QTimer,QTime
from PyQt6.QtGui import QFont,QMovie
from PyQt6.QtWidgets import QFileDialog
import shutil

class MathTutorApp(QMainWindow):  
    def __init__(self):
        super().__init__()
        self.questions=[]
        self.currentQuestionIndex=0
        self.lessonFiles=[]
        self.score=0
        self.initUI()
        #timer config
        self.timer=QTimer(self)
        self.timer.timeout.connect(self.updateStopwatch)
        self.startTime=QTime(0,0)
        #default lesson is addition easy
        self.loadQuestions("addition_easy.txt")
        self.showFullScreen()
    def initUI(self):
        #question and answer widget
        centralWidget=QWidget()
        self.setCentralWidget(centralWidget)
        mainLayout=QVBoxLayout(centralWidget)
        #toolbar for lesson,theme,score and stopwatch
        topToolBar=QToolBar("Top Toolbar")
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea,topToolBar)
        #lesson dropdown
        self.lessonSelector=QComboBox()
        self.lessonSelector.addItem("Addition (Easy)","addition_easy.txt")
        self.lessonSelector.addItem("Addition (Medium)","addition_medium.txt")
        self.lessonSelector.addItem("Add More")
        self.lessonSelector.currentIndexChanged.connect(self.onLessonChange)
        #add to toolbar
        topToolBar.addWidget(self.lessonSelector)
        #theme dropdown
        self.themeSelector=QComboBox()
        self.themeSelector.addItem("High Contrast")
        self.themeSelector.addItem("Low Contrast")
        self.themeSelector.currentIndexChanged.connect(self.changeTheme)
        #add to toolbar
        topToolBar.addWidget(self.themeSelector)
        #score display  
        self.scoreDisplay=QLabel(f"Score: {self.score}")  
        topToolBar.addWidget(self.scoreDisplay)
        #stopwatch display
        self.stopwatchDisplay=QLabel("Time: 00:00")
        topToolBar.addWidget(self.stopwatchDisplay) 
        #central widget layout
        self.centralWidgetLayout=QVBoxLayout()
        self.centralWidgetLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.questionLabel=QLabel("Question will appear here")
        self.questionLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.centralWidgetLayout.addWidget(self.questionLabel)
        self.answerInput=QLineEdit()
        self.answerInput.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.answerInput.returnPressed.connect(self.checkAnswer)
        self.centralWidgetLayout.addWidget(self.answerInput)
        self.gifLabel=QLabel()
        self.gifLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.updateGif("welcome-1.gif")
        self.centralWidgetLayout.addWidget(self.gifLabel)
        mainLayout.addLayout(self.centralWidgetLayout)
        self.adjustFontsAndLayout()
    
    #stopwatch functions
    def startStopwatch(self):
        self.startTime=QTime(0,0)  
        self.timer.start(1000) 
    def updateStopwatch(self):
        self.startTime=self.startTime.addSecs(1)  
        self.stopwatchDisplay.setText(f"Time: {self.startTime.toString('mm:ss')}") 
    def resetStopwatch(self):
        self.timer.stop()  
        self.startTime.setHMS(0,0,0)  
        self.stopwatchDisplay.setText("Time: 00:00")
    
    #lesson functions
    def onLessonChange(self, index):
        #add more lessons
        if self.lessonSelector.currentText()=="Add More":
            self.addMoreLessons()
            return  
        lessonFile=self.lessonSelector.currentData()
        if lessonFile:
            self.loadQuestions(lessonFile)
            self.updateGif("start.gif")
    def addMoreLessons(self):
        files,_=QFileDialog.getOpenFileNames(self,"Select Lesson Files","","Text Files (*.txt)")
        for file_path in files:
            #copying the file to lessons folder and updating dropdown
            try:
                base_name=os.path.basename(file_path)
                dest_path=os.path.join("lessons",base_name)
                shutil.copy(file_path,dest_path)
                #if not present then add
                if base_name not in self.lessonFiles:
                    self.lessonSelector.insertItem(self.lessonSelector.count()- 1,base_name.replace(".txt",""),base_name)
                    self.lessonFiles.append(base_name)
            except Exception as e:
                QMessageBox.critical(self,"Error",f"Failed to add lesson:{e}")
        #reset
        if files:
            self.lessonSelector.setCurrentIndex(0)
    def loadQuestions(self,filename):
            filePath=os.path.join("lessons",filename) 
            try:
                with open(filePath,"r") as file:
                    self.questions=[line.strip().split('=') for line in file.readlines()]
                self.currentQuestionIndex=0
                #reset score
                self.score=0
                self.updateScoreDisplay()
                self.showQuestion()
                self.startStopwatch()
                
            except Exception as e:
                QMessageBox.critical(self,"Error",f"Failed to load questions: {e}")
    def showQuestion(self):
        if self.currentQuestionIndex<len(self.questions):
            question,_=self.questions[self.currentQuestionIndex]
            self.questionLabel.setText(question)
            self.readQuestionAloud()
            self.answerInput.clear()
            self.answerInput.setEnabled(True)
            self.answerInput.show()
        else:
            #font size reduced from base because of screen size glitch
            self.setLabelFontSize(self.questionLabel,84,bold=True)
            self.questionLabel.setWordWrap(True)
            elapsedTimeStr=self.startTime.toString('mm:ss')
            self.questionLabel.setText(f"Congratulations, you've completed all the questions!\nYour final score is: {self.score}\nTime taken: {elapsedTimeStr}")
            self.updateGif("congratulations.gif")
            self.answerInput.setEnabled(False)
            self.answerInput.hide()
            self.resetStopwatch()
    def checkAnswer(self):
        if self.currentQuestionIndex<len(self.questions):
            _,correctAnswer=self.questions[self.currentQuestionIndex]
            userAnswer=self.answerInput.text().strip()
            if userAnswer==correctAnswer.strip():
                self.currentQuestionIndex+=1
                self.updateGif("correct.gif" if self.currentQuestionIndex < len(self.questions) else "congratulations.gif")
                self.speakFeedback("Excellent")
                self.score+=5  
                self.updateScoreDisplay()  
                self.showQuestion()
            else:
                self.updateGif("wrong.gif")
                self.speakFeedback("Try again")
                self.score-=2  
                self.updateScoreDisplay()  
            self.answerInput.clear()
    
    #layouts,fonts,theme,keypress functions
    def setLabelFontSize(self,label,size,bold=False):
        font=label.font()  
        font.setPointSize(size)  
        font.setBold(bold) 
        label.setFont(font) 
    def changeTheme(self,index):
        if index==0:
            self.setStyleSheet("QWidget { background-color: #000000; color: #FFFFFF; }")
        else:
            self.setStyleSheet("QWidget { background-color: #F0F0F0; color: #333333; }")
    def adjustFontsAndLayout(self):
            #font size adjustment
            baseFontSize=max(self.width()//10,24)
            self.questionLabel.setFont(QFont("Arial", baseFontSize, QFont.Weight.Bold))
            self.answerInput.setFont(QFont("Arial", baseFontSize))
    def resizeEvent(self,event):
        super().resizeEvent(event)
        self.adjustFontsAndLayout()   
    def updateScoreDisplay(self):
        self.scoreDisplay.setText(f"Score:{self.score}") 
    def updateGif(self,gifName):
        imagePath=os.path.join("images",gifName)  
        self.gifLabel.setMovie(None)
        self.gifMovie=QMovie(imagePath)
        self.gifLabel.setMovie(self.gifMovie)
        self.gifMovie.start()
    def keyPressEvent(self,event):
        if event.key()==Qt.Key.Key_Shift:
            self.readQuestionAloud()
    
    #speech functions
    def readQuestionAloud(self):
        if self.currentQuestionIndex<len(self.questions):
            question,_=self.questions[self.currentQuestionIndex]
            question_to_read=question.split('=')[0].strip()
            if sys.platform.startswith('darwin'):
                os.system(f'say "{question_to_read}"')
            elif sys.platform.startswith('linux') or sys.platform.startswith('linux2') or sys.platform.startswith('win32') or sys.platform.startswith('cygwin'):
                os.system(f'espeak "{question_to_read}"')
    def speakFeedback(self,feedback):
        if sys.platform.startswith('darwin'):
            os.system(f'say "{feedback}"')
        elif sys.platform.startswith('linux') or sys.platform.startswith('linux2') or sys.platform.startswith('win32') or sys.platform.startswith('cygwin'):
            os.system(f'espeak "{feedback}"')     
#driver
if __name__=='__main__':
    app = QApplication(sys.argv)
    mathTutorApp = MathTutorApp()
    mathTutorApp.show()
    sys.exit(app.exec())