###########################################################################
#    Maths-Tutor
#
#    Copyright (C) 2022-2023 Roopasree A P <roopasreeap@gmail.com>    
#    Copyright (C) 2023-2024 Greeshna Sarath <greeshnamohan001@gmail.com>
#    Copyright (C) 2024-2025 Nalin Sathyan <nalin.x.linux@gmail.com>
#
#    This project is Supervised by Zendalona(2022-2023)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
###########################################################################
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt, QUrl, QTimer
from PyQt6.QtGui import QFont, QImage, QPixmap, QMovie
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QWidget, QSpacerItem, QSizePolicy
from PyQt6.QtMultimedia import QMediaPlayer,QAudioOutput
# from MathsTutor import global_var
import global_var
import re
import os
import threading
import math
import random
import time
listing_symbol = ","
range_symbol = ":"
multiplier_symbol = ";"

class MathsTutorBin(QWidget):
    def __init__(self, speech_object, gettext):
        super().__init__()
        self.speech = speech_object
        self.player = QMediaPlayer()
        global _;
        _ = gettext
        self.player = QMediaPlayer()
        self.audioOutput = QAudioOutput()
        #set audio output device
        self.player.setAudioOutput(self.audioOutput)
        self.audioOutput.setVolume(0.5)
        vbox = QVBoxLayout()
        vbox2 = QVBoxLayout()
        self.setLayout(vbox)
        self.welcome_message = _("Welcome!")+" "+_("Press enter to start")

        """An appreciation dictionary is used here to help non-English
        translators understand things more easily. Also, there is not
        always a one-to-one word correspondence in every language."""
        self.appreciation_dict = {
        "Excellent" : [ _('Excellent-1'), _('Excellent-2'), _('Excellent-3'), _('Excellent-4'), _('Excellent-5')],
        "Very good" : [_('Very good-1'), _('Very good-2'), _('Very good-3'), _('Very good-4'), _('Very good-5')],
        "Good" : [_('Good-1'), _('Good-2'), _('Good-3'), _('Good-4'), _('Good-5')],
        "Fair" : [_('Fair-1'), _('Fair-2'), _('Fair-3'), _('Fair-4'), _('Fair-5')],
        "Okay" : [_('Okay-1'), _('Okay-2'), _('Okay-3'), _('Okay-4'), _('Okay-5')]
        }
        self.label= QLabel()
        self.label.setFont(QFont("Arial",100))
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        vbox2.addWidget(self.label)
        hbox= QHBoxLayout()
        vbox2.addLayout(hbox)
        self.entry= QLineEdit()
        font= QFont()
        font.setPointSize(100) #font size 100
        self.entry.setFont(font)
        self.entry.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        #imp connecting returnPressed signal of entry widget to the self.on_entry_activated method
        self.entry.returnPressed.connect(self.on_entry_activated)
        hbox.addWidget(self.entry)
        
        #creating multiple instances of QLabel and adding them to the vbox2 layout
        self.image = QLabel()
        self.image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        vbox2.addWidget(self.image)
        vbox.addLayout(vbox2)
        self.current_question_index = -1
        self.wrong=False
        self.current_performance_rate=0
        self.final_score=0
        self.incorrect_answer_count=0
        self.number_of_questions_attended = 0
        
        #creatng QMediaPlayer instance
        self.player = QMediaPlayer()

    def grab_focus_on_entry(self):
        self.entry.setFocus()

    def connect_game_over_callback_function(self, function):
        self.game_over_callback_function = function

    # Function to play sounds
    def play_file(self, name, rand_range=1):
        self.player = QMediaPlayer()
        self.audioOutput = QAudioOutput()
        self.player.setAudioOutput(self.audioOutput)
        
        if rand_range == 1:
            file_name = name + ".ogg"
        else:
            value = str(random.randint(1, rand_range))
            file_name = f"{name}-{value}.ogg"
        file_path_and_name = os.path.join(global_var.data_dir, 'sounds', file_name)
        self.player.setSource(QUrl.fromLocalFile(file_path_and_name))
        self.audioOutput.setVolume(0.5)
        self.player.play()

    #function to set gif from file using Qmovie thereby removing dependency on pygame
    def set_image(self, name, rand_range):
        value = str(random.randint(1, rand_range))
        gif_path = os.path.join(global_var.data_dir, "images", f"{name}-{value}.gif")
        movie = QMovie(gif_path)
        self.image.setMovie(movie)
        movie.start()

    def speak(self, text, enqueue=False):
        # if(enqueue == False):
        #     self.speech.cancel();
        # self.speech.speak(text)
        return
   
    #Function to read the questions from the file
    def load_question_file(self, file_path):
        # Resetting all game variables
        self.list = []
        self.current_question_index = -1
        self.wrong=False
        self.number_of_questions_attended = 0

        # Loading questions from file
        with open(file_path, "r") as file:
            for line in file:
                stripped_line = line.strip()
                self.list.append(stripped_line)

        # Set the text of the label to the value of welcome_message
        self.label.setText(self.welcome_message)

        self.set_image("welcome", 3)

        # Playing starting sound
        self.play_file('welcome')

        self.speak(self.welcome_message)

        self.entry.setFocus()

        self.game_over = False

    
    # Function to covert the signs to text
    def convert_signs(self, text):
        return text.replace("+", " " + _("plus") + " ") \
                   .replace("-", " " + _("minus") + " ") \
                   .replace("*", " " + _("multiply") + " ") \
                   .replace("/", " " + _("divided by") + " ") \
                   .replace("%", " " + _("percentage of") + " ")

    def convert_to_verbose(self, text):
        return ", ".join(text)


    def keyPressEvent(self, event):
        keyval = event.key()
        if keyval == Qt.Key.Key_Space: # Space
            self.announce_question_using_thread()
            return
        elif keyval in (Qt.Key.Key_Shift, Qt.Key.Key_Shift): # Shift
            self.announce_question_using_thread(True)
            return
        elif keyval == Qt.Key.Key_Semicolon: # Semicolon
            self.speech.set_speech_rate(int(self.speech.get_speech_rate()) - 10)
            self.announce_question_using_thread()
            return
        elif keyval == Qt.Key.Key_Apostrophe: # Apostrophe
            self.speech.set_speech_rate(int(self.speech.get_speech_rate()) + 10)
            self.announce_question_using_thread()
            return

    # Function to display the question and corresponding images and sounds
    def on_entry_activated(self):
        if (self.game_over):
            self.game_over_callback_function()
        elif (self.current_question_index == -1):
            self.starting_time = time.time()
            self.wrong = False
            self.current_performance_rate = 0
            self.final_score = 0
            self.incorrect_answer_count = 0
            self.next_question()
        else:
            answer = self.entry.text() 
            correct_answer = self.answer
            
            if answer == correct_answer:                
                time_end = time.time()

                time_taken = time_end - self.time_start

                time_alotted = int(self.list[self.current_question_index].split("===")[1])

                print(
                    f"\n### Time Allotted ###\n"
                    f"Excellent: {time_alotted - (time_alotted * 50) / 100}\n"
                    f"Very Good: {time_alotted - (time_alotted * 25) / 100}\n"
                    f"Good: {time_alotted}\n"
                    f"Fair: {time_alotted + (time_alotted * 25) / 100}\n"
                    f"### Time Taken: {time_taken}\n\n"
                )

                self.incorrect_answer_count = 0

                appreciation_index = random.randint(0, 4)

                if time_taken < time_alotted - ((time_alotted * 50) / 100):
                    self.current_performance_rate += 4
                    self.final_score += 50
                    text = self.appreciation_dict["Excellent"][appreciation_index]
                    self.set_image("excellent", 3)
                    self.play_file("excellent", 3)
                elif time_taken < time_alotted - ((time_alotted * 25) / 100):
                    self.current_performance_rate += 2
                    self.final_score += 40
                    text = self.appreciation_dict["Very good"][appreciation_index]
                    self.set_image("very-good", 3)
                    self.play_file("very-good", 3)
                elif time_taken < time_alotted:
                    self.current_performance_rate += 1
                    self.final_score += 30
                    text = self.appreciation_dict["Good"][appreciation_index]
                    self.set_image("good", 3)
                    self.play_file("good", 3)
                elif time_taken < time_alotted + ((time_alotted * 25) / 100):
                    # No changes to self.current_performance_rate
                    self.final_score += 20
                    text = self.appreciation_dict["Fair"][appreciation_index]
                    self.set_image("not-bad", 3)
                    self.play_file('not-bad', 3)
                    
                else:
                    self.current_performance_rate -= 1
                    self.final_score += 10
                    text = self.appreciation_dict["Okay"][appreciation_index]
                    self.set_image("okay", 3)
                    self.play_file('okay', 3)
                text = text + "!"
                self.speak(text)
                self.label.setText(text)

            else:
                self.wrong = True
                self.current_performance_rate -= 3
                self.final_score -= 10
                self.incorrect_answer_count = self.incorrect_answer_count + 1
                if self.incorrect_answer_count == 3:
                    self.set_image("wrong-anwser-repeted", 2)
                    self.play_file("wrong-anwser-repeted", 3)
                    self.incorrect_answer_count = 0
                    text = _("Sorry! The correct answer is ")
                    self.label.setText(text + self.answer) 
                    if(len(self.answer.split(".")) > 1):
                        li = list(self.answer.split(".")[1])
                        self.speak(text + self.answer.split(".")[0] + " " + _("point") + " " + " ".join(li))
                    else:
                        self.speak(text + self.answer)
                    
                else:
                    text = _("Sorry! Let's try again")
                    self.label.setText(text) 
                    self.speak(text)
                    self.set_image("wrong-anwser", 3)
                    self.play_file("wrong-anwser", 3)
            QTimer.singleShot(3000, self.next_question)
            self.entry.setText("") 

    # Function to set next question        
    def next_question(self):
        self.time_start = time.time()
        self.entry.setFocus()


        if self.wrong==True:
            self.label.setText(self.question)
            self.announce_question_using_thread()
            self.set_image("wrong-anwser", 3)
            self.wrong=False
        else:
            print("Current Performance Rate = "+str(self.current_performance_rate)+
            " Question index shift = " + str(math.floor(self.current_performance_rate/10)+1))
            next_question = self.current_question_index + math.floor(self.current_performance_rate/10)+1;
            if(next_question >= 0):
                self.current_question_index = next_question

            if self.current_question_index < len(self.list)-1:
                question_to_pass = self.list[self.current_question_index].split("===")[0]
                self.question = self.make_question(question_to_pass)
                question_to_evaluate = self.question
                if("%" in self.question):
                    digit_one, digit_two = self.question.split("%")
                    question_to_evaluate = "("+digit_one+"*"+digit_two+")/100"

                number = eval(question_to_evaluate)
                if number==math.trunc(number):
                    self.answer = str(math.trunc(number))
                else:
                    num= round(eval(str(number)),2)
                    self.answer = str(num)

                self.make_sound = self.list[self.current_question_index].split("===")[2]
                self.label.setText(self.question)                
                self.announce_question_using_thread()
                
                self.entry.setText("")
                self.set_image("question", 2)

                self.number_of_questions_attended += 1

            else:
                minute, seconds = divmod(round(time.time()-self.starting_time), 60)
                score = round((self.final_score*100)/(50*self.number_of_questions_attended))
                text = _("Successfully finished! Your mark is ")+str(score)+\
                "!\n"+_("Time taken ")+str(minute)+" "+_("minutes and")+" "+str(seconds)+" "+_("seconds!");
                self.speak(text)

                #enabling word wrap for the congrats message but decreasing the font size to prevent overflow issues 
                font = QFont()
                font.setPointSize(30)
                self.label.setFont(font)
                self.label.setWordWrap(True)
                self.label.setText(text)
                self.set_image("finished", 3)
                self.play_file("finished", 3)
                self.game_over = True
                
    # Create random numbers
    def get_randome_number(self, value1, value2):
        if(int(value1) < int(value2)):
            return str(random.randint(int(value1),int(value2)))
        else:
            return str(random.randint(int(value2),int(value1)))

    """
    Question maker for creating questions by randomly selecting an operand
    from a list of numbers separated by a listing_symbol, or a number between
    two numbers separated by a range_symbol, or multiples of a number from
    range start to end separated by a multiplier_symbol.
    """
    def make_question(self, question):
        # adding $ symbol to notify end
        question = question + "$"
        output = ""
        start = 0
        for i in range(0, len(question)):
            item = question[i]

            if(item.isdigit() or item == listing_symbol or item == range_symbol or item == multiplier_symbol or item == "."):
                pass
            else:
                number_content = question[start:i]
                start = i+1

                if(listing_symbol in number_content):
                    number_list = number_content.split(listing_symbol)
                    selected = number_list[random.randint(0,len(number_list)-1)]
                    output = output + str(selected) + item

                elif (range_symbol in number_content):
                    digit_one, digit_two = number_content.split(range_symbol)
                    selected = self.get_randome_number(digit_one, digit_two)
                    output = output + str(selected) + item

                elif (multiplier_symbol in number_content):
                    digit, num_start, num_end = number_content.split(multiplier_symbol)
                    num = random.randint(int(num_start),int(num_end))
                    selected = int(digit)*num;
                    output = output + str(selected) + item

                else:
                    output = output + str(number_content) + item

        # [:-1] for removing $ symbol before returning
        return output[:-1]

    def announce_question_using_thread(self, verbose=False):
        try:
           threading.Thread(target=self.announce_question,args=[self.question,
            self.make_sound, self.current_question_index, verbose]).start()
        except AttributeError:
           self.speak(_("Press enter to start"))
    
    # Function for announcing a question with or without a bell sound.
    def announce_question(self, question, make_sound, announcing_question_index, verbose):
        if(make_sound == '1'):
            item_list = re.split(r'(\d+)', question)[1:-1]

            if(self.question == self.answer):
                self.speak(_("Enter the number of bells rung!"))
                time.sleep(1.8)

            for item in item_list:
                # To prevent announcement on user answer
                if(announcing_question_index != self.current_question_index):
                    return;
                if item.isnumeric():

                    num = int(item)
                    while(num > 0):
                        num = num-1;
                        self.play_file("coin")
                        time.sleep(0.7)
                else:
                    self.speak(self.convert_signs(item))
                    time.sleep(0.7)
            if(announcing_question_index != self.current_question_index):
                self.speak(_("equals to?"))
        else:
            self.play_file("question")
            time.sleep(0.7)
            if(verbose):
                if(self.question == self.answer):
                    self.speak(_("Enter ")+self.convert_to_verbose(self.answer))
                else:
                    self.speak(self.convert_signs(self.convert_to_verbose(self.question))+" "+_("equals to?"))
            else:
                if(self.question == self.answer):
                    self.speak(_("Enter ")+self.answer)
                else:
                    self.speak(self.convert_signs(self.question)+" "+_("equals to?"))

    def on_quit(self):
        pass

if __name__ == "__main__":
    win = MathsTutorWindow()

