import os
import shutil
from datetime import datetime, timedelta

class QuestionManager:
    def __init__(self):
        self.questions=[]
        self.currentQuestionIndex=0
        self.lessonFiles=[]

    def loadQuestions(self,filename):
        filePath=os.path.join("lessons",filename)
        with open(filePath,"r") as file:
            self.questions=[line.strip().split('=') for line in file.readlines()]
        self.currentQuestionIndex=0

    def get_current_question(self):
        if self.currentQuestionIndex<len(self.questions):
            question,_=self.questions[self.currentQuestionIndex]
            return question
        return None

    def check_answer(self,userAnswer):
        if self.currentQuestionIndex<len(self.questions):
            _,correctAnswer=self.questions[self.currentQuestionIndex]
            return userAnswer.strip()==correctAnswer.strip()

    def advance_question(self):
        if self.currentQuestionIndex<len(self.questions)-1:
            self.currentQuestionIndex+=1
            return True
        return False

    def add_lesson(self,file_path):
        try:
            base_name=os.path.basename(file_path)
            dest_path= os.path.join("lessons",base_name)
            shutil.copy(file_path,dest_path)
            if base_name not in self.lessonFiles:
                self.lessonFiles.append(base_name)
                return True
        except Exception as e:
            print(f"Failed to add lesson: {e}")
        return False

class ScoreManager:
    def __init__(self):
        self.score =0

    def correct_answer(self):
        self.score+= 5

    def wrong_answer(self):
        self.score -=2

    def get_score(self):
        return self.score

class Timer:
    def __init__(self):
        self.start_time= datetime.min
        self.running= False

    def start(self):
        self.start_time= datetime.now()
        self.running= True

    def stop(self):
        self.running= False

    def get_elapsed_time(self):
        if not self.running:
            return "00:00"
        elapsed =datetime.now()- self.start_time
        return str(timedelta(seconds=elapsed.seconds))

