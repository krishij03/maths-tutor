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
import os
import sys
from PyQt6.QtWidgets import(
    QApplication,QWidget,QVBoxLayout,QHBoxLayout,QLabel,
    QComboBox, QPushButton,QFileDialog,QDialog,QCheckBox,
    QMessageBox,QHeaderView,QLineEdit)
from PyQt6.QtGui import QIcon,QPixmap,QDesktopServices
from PyQt6.QtCore import Qt,QUrl
from PyQt6.QtMultimedia import QMediaPlayer,QAudioOutput
# from MathsTutor.tutor import MathsTutorBin
import sys
import os
from tutor import MathsTutorBin
import global_var
import preferences
# from MathsTutor.tutor import MathsTutorBin
# from MathsTutor import preferences
# from MathsTutor import global_var
import gettext
gettext.bindtextdomain(global_var.app_name,global_var.locale_dir)
gettext.textdomain(global_var.app_name)
_ = gettext.gettext
language_dict = {"en": "English", "hi": "Hindi", "ar": "Arabic", "ta": "Tamil", "ml": "Malayalam", "sa": "Sanskrit"}

#need to create this instance of QApplication to use the _() function
app= QApplication(sys.argv)

class LanguageSelectionDialog(QDialog):
    def __init__(self, parent=None, language=0):
        super().__init__(parent)
        self.setWindowTitle(_("Maths-Tutor"))
        self.setModal(True)

        layout = QVBoxLayout()

        label_language = QLabel(_("Select Language"))
        self.combobox = QComboBox()
        self.combobox.addItems(language_dict.values())
        self.combobox.setCurrentIndex(language)
        label_language.setBuddy(self.combobox)

        hbox1 = QHBoxLayout()
        hbox1.addWidget(label_language)
        hbox1.addWidget(self.combobox)

        self.remember_checkbox = QCheckBox(_("Remember Selection"))

        layout.addLayout(hbox1)
        layout.addWidget(self.remember_checkbox)

        buttons = QHBoxLayout()
        ok_button = QPushButton(_("OK"))
        ok_button.clicked.connect(self.accept)
        cancel_button = QPushButton(_("Cancel"))
        cancel_button.clicked.connect(self.reject)
        buttons.addWidget(ok_button)
        buttons.addWidget(cancel_button)

        layout.addLayout(buttons)

        self.setLayout(layout)

    def get_selected_language(self):
        return list(language_dict.keys())[self.combobox.currentIndex()]

    def get_remember_selection(self):
        return self.remember_checkbox.isChecked()


class SelectGame(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(_("Maths-Tutor"))

        #init media player
        self.player= QMediaPlayer()
        self.audioOutput= QAudioOutput()

        #output device setup
        self.player.setAudioOutput(self.audioOutput)

        #load bg music
        url = QUrl.fromLocalFile(os.path.join(global_var.data_dir,'sounds','backgroundmusic.ogg'))
        self.player.setSource(url)

        #setting volume
        self.audioOutput.setVolume(0.5) #50% volume

        self.player.play()
        

        self.pref = preferences.Preferences()
        self.pref.load_preferences_from_file(global_var.user_preferences_file_path)

        previous_language = self.pref.language

        if self.pref.language == -1:
            self.pref.language = 0
        
        lang_dialog = LanguageSelectionDialog(self, self.pref.language)
        result = lang_dialog.exec()
        if result == QDialog.accepted:
            selected_language = lang_dialog.get_selected_language()
            self.pref.language = list(language_dict.keys()).index(selected_language)
            if lang_dialog.get_remember_selection():
                self.pref.remember_language = 1
        else:
            #setting default language for now (eng) which is at index 0
            self.pref.language = 0 
            
        # if self.pref.remember_language == 1:
        #     selected_language = list(language_dict)[self.pref.language]
        # else:
        #     # Create and show the language selection dialog
        #     lang_dialog = LanguageSelectionDialog(self, self.pref.language)
        #     result = lang_dialog.exec()

        #     if result == QDialog.accepted:
        #         selected_language = lang_dialog.get_selected_language()
        #         self.pref.language = list(language_dict.keys()).index(selected_language)
        #         if lang_dialog.get_remember_selection():
        #             self.pref.remember_language = 1
        #     else:
        #         return

        # try:
        #     global _
        #     lang1 = gettext.translation(global_var.app_name, languages=[selected_language])
        #     lang1.install()
        #     _ = lang1.gettext
        # except:
        #     self.pref.language = 0

        if previous_language != self.pref.language:
            self.pref.speech_language = -1

        self.operator_mapping = {
            _('Addition (+)'): {
                _('Simple'): 'add_simple.txt',
                _('Easy'): 'add_easy.txt',
                _('Medium'): 'add_med.txt',
                _('Hard'): 'add_hard.txt',
                _('Challenging'): 'add_chlg.txt',
            },
            _('Subtraction (-)'): {
                _('Simple'): 'sub_simple.txt',
                _('Easy'): 'sub_easy.txt',
                _('Medium'): 'sub_med.txt',
                _('Hard'): 'sub_hard.txt',
                _('Challenging'): 'sub_chlg.txt',
            },
            _('Multiplication (*)'): {
                _('Simple'): 'mul_simple.txt',
                _('Easy'): 'mul_easy.txt',
                _('Medium'): 'mul_med.txt',
                _('Hard'): 'mul_hard.txt',
                _('Challenging'): 'mul_chlg.txt',
            },
            _('Division (/)'): {
                _('Simple'): 'div_simple.txt',
                _('Easy'): 'div_easy.txt',
                _('Medium'): 'div_med.txt',
                _('Hard'): 'div_hard.txt',
                _('Challenging'): 'div_chlg.txt',
            },
            _('Percentage (%)'): {
                _('Simple'): 'per_simple.txt',
                _('Easy'): 'per_easy.txt',
                _('Medium'): 'per_med.txt',
            },
        }

        #window icon
        icon_pixmap= QPixmap(os.path.join(global_var.data_dir,"icon.png"))
        self.setWindowIcon(QIcon(icon_pixmap))

        #main layout stuff
        main_layout= QVBoxLayout()
        self.setLayout(main_layout)

        #hbox for show/hide settings, about, user-guide, and quit
        hbox2= QHBoxLayout()

        #settings button
        self.show_controls_button= QPushButton(_("Show Settings"))
        self.show_controls_button.clicked.connect(self.show_controls)
        self.show_controls_button.setFixedSize(100, 30)
        hbox2.addWidget(self.show_controls_button)

        #about button
        about_button= QPushButton(_("About"))
        about_button.clicked.connect(self.show_about_dialog)
        about_button.setFixedSize(100,30)
        hbox2.addWidget(about_button)

        #user guide button
        user_guide_button= QPushButton(_("Help"))
        user_guide_button.clicked.connect(self.on_help_clicked)
        user_guide_button.setFixedSize(100,30)
        hbox2.addWidget(user_guide_button)

        #quit button
        quit_button= QPushButton(_("Quit"))
        quit_button.clicked.connect(self.close)
        quit_button.setFixedSize(100,30)
        hbox2.addWidget(quit_button)

        #create a QWidget to contain all the controls so that visbility can be toggled
        self.controls_widget= QWidget()
        self.vbox_controls= QVBoxLayout()
        self.controls_widget.setLayout(self.vbox_controls)

        #hbox for the operator labels and comboBox
        operator_box= QHBoxLayout()
        select_operator_label= QLabel(_("Select Operation:"))
        operator_box.addWidget(select_operator_label)

        self.operator_combobox= QComboBox()
        self.operator_combobox.addItems(self.operator_mapping.keys())
        self.operator_combobox.currentIndexChanged.connect(self.on_operator_combobox_changed)
        operator_box.addWidget(self.operator_combobox)
        select_operator_label.setBuddy(self.operator_combobox)

        #hbox for the level labels and comboBox
        level_box= QHBoxLayout()
        select_mode_label= QLabel(_("Select Difficulty Level:"))
        level_box.addWidget(select_mode_label)
        self.mode_combobox= QComboBox()
        level_box.addWidget(self.mode_combobox)
        select_mode_label.setBuddy(self.mode_combobox)
        self.operator_combobox.setCurrentIndex(self.pref.operator)
        self.mode_combobox.setCurrentIndex(self.pref.level)
        #add operator and level boxes to controls layout
        self.vbox_controls.addLayout(operator_box)
        self.vbox_controls.addLayout(level_box)

        #create start,load and reset settings buttons
        start_button= QPushButton(_("Start"))
        start_button.clicked.connect(self.on_start_button_clicked)
        self.vbox_controls.addWidget(start_button)
        load_button= QPushButton(_("Load Questions"))
        load_button.clicked.connect(self.on_load_button_clicked)
        self.vbox_controls.addWidget(load_button)
        button_reset_settings= QPushButton(_("Reset Settings"))
        button_reset_settings.clicked.connect(self.on_button_reset_settings_clicked)
        button_reset_settings.setFixedSize(100, 30)
        self.vbox_controls.addWidget(button_reset_settings)

        #create game_bin widget (takes 2 empty positional argumentss) and add it to the vbox_game_and_controls layout
        self.game_bin= MathsTutorBin(_, _)
        self.game_bin.connect_game_over_callback_function(self.move_game_to_next_level)
        vbox_game_and_controls= QVBoxLayout()
        vbox_game_and_controls.addWidget(self.game_bin)

        #add controls widget to the vbox_game_and_controls layout
        vbox_game_and_controls.addWidget(self.controls_widget)

        #add label and hbox2 to the vbox_game_and_controls layout
        label= QLabel(_(
            "Note: Adjust the speech rate by pressing the apostrophe or semicolon key, "
            "which are located to the left of the Enter key. Use the Space key to replay "
            "the question, and employ the Shift key to hear the question in verbose mode. "
            "Utilize settings to change arithmetic operation, difficulty, load questions, "
            "speech language, voice, etc. Press Alt+S to open or hide settings."
        ))
        label.setWordWrap(True)
        label.setAlignment(Qt.AlignmentFlag.AlignJustify)
        vbox_game_and_controls.addWidget(label)

        vbox_game_and_controls.addLayout(hbox2)

        #add vbox_game_and_controls layout to the main layout
        main_layout.addLayout(vbox_game_and_controls)

        self.showMaximized()
        self.on_start_button_clicked()

    def move_game_to_next_level(self):
        if self.pref.level+ 1< self.mode_combobox.count():
            self.pref.level+= 1
        else:
            if self.pref.operator+ 1< self.operator_combobox.count():
                self.pref.level= 0
                self.pref.operator+= 1
            else:
                self.pref.level= 0
                self.pref.operator= 0

        self.operator_combobox.setCurrentIndex(self.pref.operator)
        self.mode_combobox.setCurrentIndex(self.pref.level)

        self.on_start_button_clicked()

    def on_button_reset_settings_clicked(self):
        self.pref.set_default_preferences()

        # This won't set the GameBin to the default operator and level,
        # nor will it start the game. Users have to start it using the 'Start Game' option.
        self.operator_combobox.setCurrentIndex(self.pref.operator)
        self.mode_combobox.setCurrentIndex(self.pref.level)

    def on_start_button_clicked(self):
        selected_operator = self.operator_combobox.currentText()
        self.pref.operator = self.operator_combobox.currentIndex()

        selected_mode = self.mode_combobox.currentText()
        self.pref.level = self.mode_combobox.currentIndex()

        file_path = self.operator_mapping[selected_operator].get(selected_mode)

        # Check if file_path is None and handle it
        if file_path is None:
            QMessageBox.warning(self, _("Error"), _("File path not found for the selected operator and mode."))
            return

        # Proceed with the original operation now that we've ensured file_path is not None
        self.start_game(os.path.join(global_var.data_dir, "lessons", file_path))

    def start_game(self, file_path):
        self.game_bin.load_question_file(file_path)
        # Assuming self.controls_widget is the parent widget of self.vbox_controls
        self.controls_widget.setVisible(False)
        self.game_bin.show()
        self.show_controls_button.setText(_("Show Settings"))
        self.repaint()

    def on_operator_combobox_changed(self, index):
        self.mode_combobox.clear()

        for difficulty in self.operator_mapping[self.operator_combobox.itemText(index)].keys():
            self.mode_combobox.addItem(difficulty)

        self.mode_combobox.setCurrentIndex(0)

    def on_load_button_clicked(self):
        # Create a file dialog to choose a file
        dialog = QFileDialog(self, _("Please choose a lesson file"), "", _("Text files (*.txt)"))
        dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        if dialog.exec() == QFileDialog.accepted:
            # Get the selected file
            selected_file = dialog.selectedFiles()[0]
            self.start_game(selected_file)

    def show_controls(self):
        if self.controls_widget.isVisible():
            self.controls_widget.setVisible(False)
            self.game_bin.show()
            self.game_bin.grab_focus_on_entry()
            self.show_controls_button.setText(_("Show Settings"))
        else:
            self.show_controls_button.setText(_("Hide Settings"))
            self.controls_widget.setVisible(True)
            self.game_bin.hide()
            self.operator_combobox.setFocus()
        self.repaint()

    def show_about_dialog(self):
        about_dialog = QMessageBox(self)
        about_dialog.setWindowTitle(_("About Maths-Tutor"))
        about_dialog.setIconPixmap(QPixmap(os.path.join(global_var.data_dir, "icon.png")))
        about_dialog.setText(_("Maths-Tutor"))
        about_dialog.setInformativeText(_("Maths-Tutor is a game designed to enhance "
                                          "one's calculation abilities in mathematics and enable them to self-assess."))
        about_dialog.setDetailedText(_(
            "Copyright (C) 2022-2023 Roopasree A P roopasreeap@gmail.com\n"
"Copyright (C) 2022-2023 Greeshna Sarath greeshnamohan001@gmail.com\n\n"
"Supervised by Zendalona(2022-2024)\n\n"
"License: GNU General Public License - GPL-2.0\n\n"
"Website: http://wwww,zendalona.com/maths-tutor\n\n"
"Authors: Roopasree A P, Greeshna Sarath\n"
"Documenters: Roopasree A P, Greeshna Sarath\n"
"Artists: Nalin Sathyan, Dr. Saritha Namboodiri, K. Sathyaseelan, Mukundhan Annamalai, "
"Ajayakumar A, Subha I N, Bhavya P V, Abhirami T, Ajay Kumar M, Saheed Aslam M, "
"Dr. Rajakrishnan V. K., Girish KK, Suresh S"
))
        about_dialog.exec()
        
    def on_help_clicked(self):
        url= QUrl.fromLocalFile(global_var.user_guide_file_path)
        QDesktopServices.openUrl(url)

    def closeEvent(self, event):
        self.game_bin.on_quit()
        event.accept()

if __name__=="__main__":
    print("Before SelectGame")
    win = SelectGame()
    win.show()
    print("After SelectGame")
    app.exec()