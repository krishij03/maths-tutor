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
from PyQt6.QtCore import Qt, QUrl, QTimer,QLocale
from PyQt6.QtGui import QFont, QImage, QPixmap, QMovie
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QWidget, QSpacerItem, QSizePolicy
from PyQt6.QtMultimedia import QMediaPlayer,QAudioOutput
from MathsTutor import global_var
from PyQt6.QtTextToSpeech import QTextToSpeech
# import global_var
import re
import os
import threading
import math
import random
import time
import subprocess
import platform
listing_symbol = ","
range_symbol = ":"
multiplier_symbol = ";"

class MathsTutorBin(QWidget):
    def __init__(self, gettext, language='en_US'):
        super().__init__()
        
        self.player = QMediaPlayer()
        global _;
        _ = gettext
        self.player = QMediaPlayer()
        self.audioOutput = QAudioOutput()
        #set audio output device
        self.player.setAudioOutput(self.audioOutput)
        self.audioOutput.setVolume(0.5)
        self.text_to_speech= QTextToSpeech()
        self.text_to_speech.setLocale(QLocale(language))
        available_voices= self.text_to_speech.availableVoices()
        selected_voice= available_voices[0] if available_voices else None
        if selected_voice:
            self.text_to_speech.setVoice(selected_voice)
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
        self.label.setWordWrap(True)
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
        default_lesson_path = os.path.join(global_var.data_dir, "lessons", "add_easy.txt")
        self.load_question_file(default_lesson_path)

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

    
    def speak(self, text):
        self.text_to_speech.say(text)
   
    #Function to read the questions from the file
    def load_question_file(self, file_path):
        self.list = []
        self.current_question_index = -1
        self.wrong = False
        self.number_of_questions_attended = 0

        #check if the file is a word problem file based on the prefix 'wp'
        is_word_problem= os.path.basename(file_path).startswith('wp')

        with open(file_path, "r") as file:
            for line in file:
                stripped_line = line.strip()
                if is_word_problem:
                    #split each line into question and answer
                    question_text, answer_text = stripped_line.split(" === ")
                    self.list.append((question_text, answer_text))
                else:
                    self.list.append(stripped_line)

        self.label.setText(self.welcome_message)
        self.set_image("welcome", 3)
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
        if self.game_over:
            self.game_over_callback_function()
        elif self.current_question_index== -1:
            self.starting_time = time.time()
            self.wrong= False
            self.current_performance_rate= 0
            self.final_score= 0
            self.incorrect_answer_count= 0
            self.next_question()
        else:
            user_answer= self.entry.text().strip()
            question= self.list[self.current_question_index]
            
            #checking if this is a word problem
            if isinstance(question, tuple):
                #word problem logic
                
                question_text,correct_answer= question
                if user_answer== correct_answer:
                    self.final_score += 10 
                    text = random.choice(self.appreciation_dict["Excellent"])
                    self.set_image("excellent", 3)
                    self.play_file("excellent", 3)
                else:
                    self.incorrect_answer_count += 1
                    text = _("Sorry! The correct answer is ") + correct_answer
                    self.final_score -= 5  
                
                #need to add hint logic and time logic above
                
            else:
                #pre-existing numeric problem logic
                correct_answer = self.answer
                if user_answer == correct_answer:
                    time_end = time.time()
                    time_taken = time_end - self.time_start
                    time_alotted = int(question.split("===")[1])
                    appreciation_index = random.randint(0, 4)
                    if time_taken < time_alotted - (time_alotted * 50 / 100):
                        self.current_performance_rate += 4
                        self.final_score += 50
                        text = self.appreciation_dict["Excellent"][appreciation_index]
                        self.set_image("excellent", 3)
                        self.play_file("excellent", 3)
                    elif time_taken < time_alotted - (time_alotted * 25 / 100):
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
                    elif time_taken < time_alotted + (time_alotted * 25 / 100):
                        self.final_score += 20
                        text = self.appreciation_dict["Fair"][appreciation_index]
                        self.set_image("not-bad", 3)
                        self.play_file("not-bad", 3)
                    else:
                        self.current_performance_rate -= 1
                        self.final_score += 10
                        text = self.appreciation_dict["Okay"][appreciation_index]
                        self.set_image("okay", 3)
                        self.play_file("okay", 3)
                else:
                    self.wrong = True
                    self.current_performance_rate -= 3
                    self.final_score -= 10
                    self.incorrect_answer_count += 1
                    if self.incorrect_answer_count == 3:
                        text = _("Sorry! The correct answer is ") + correct_answer
                        self.incorrect_answer_count = 0
                    else:
                        text = _("Sorry! Let's try again")
                        self.label.setText(text) 
                        self.speak(text)
                        self.set_image("wrong-anwser", 3)
                        self.play_file("wrong-anwser", 3)
            # Set the label and speak the text
            self.label.setText(text + "!")
            self.speak(text)
            if self.incorrect_answer_count == 3 and not isinstance(question, tuple):  # only show image if it's a repeated wrong answer
                self.set_image("wrong-answer-repeated", 2)
                self.play_file("wrong-answer-repeated", 3)

            QTimer.singleShot(3000, self.next_question)
            self.entry.setText("")

    # Function to set next question        
    def next_question(self):
        self.time_start = time.time()
        self.entry.setFocus()

        if self.wrong:
            self.label.setText(self.question)
            self.announce_question_using_thread()
            self.set_image("wrong-answer", 3) 
            self.wrong = False
        else:
            next_question_index = self.current_question_index + math.floor(self.current_performance_rate / 10) + 1
            if next_question_index >= 0:
                self.current_question_index = next_question_index

            if self.current_question_index < len(self.list):
                current_entry = self.list[self.current_question_index]

                font = QFont("Arial", 100)  #default font size for traditional problems
                if isinstance(current_entry, tuple):  #handling word problems
                    self.question, self.answer = current_entry
                    self.make_sound = '0'
                    font.setPointSize(50)  #reduce font size for word problems to fix word wrap
                    self.set_image("question", 2)
                else:  #handling traditional problems below
                    question_to_pass = current_entry.split("===")[0]
                    self.question = self.make_question(question_to_pass)
                    question_to_evaluate = self.question
                    if "%" in self.question:
                        digit_one, digit_two = self.question.split("%")
                        question_to_evaluate = f"({digit_one}*{digit_two})/100"

                    number = eval(question_to_evaluate)
                    self.answer = str(math.trunc(number)) if number == math.trunc(number) else str(round(number, 2))
                    self.make_sound = current_entry.split("===")[2]
                    self.set_image("question", 2)

                self.label.setFont(font)
                self.label.setText(self.question)
                self.announce_question_using_thread()
                self.entry.setText("")
                self.number_of_questions_attended += 1
            else:
                self.finish_session()

    #separated function of a session finish below
    def finish_session(self):
        minute, seconds = divmod(round(time.time() - self.starting_time), 60)
        score = round((self.final_score * 100) / (50 * self.number_of_questions_attended))
        text = _("Successfully finished! Your mark is ") + str(score) + \
            "!\n" + _("Time taken ") + str(minute) + " " + _("minutes and ") + str(seconds) + " " + _("seconds!")
        self.speak(text)

       
        font= QFont("Arial", 30) #smaller font size for better readability in wrap mode
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