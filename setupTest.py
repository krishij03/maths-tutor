from cx_Freeze import setup, Executable
import os
maths_tutor_dir= os.path.join(os.path.dirname(os.path.abspath(__file__)), 'MathsTutor')
# icon_dir= os.path.join(os.path.dirname(os.path.abspath(__file__)), 'icon.png')
setup(
    name="Maths-Tutor",
    version="1.0",
    description="A PyQt6 Application for Maths Tutoring",
    executables=[Executable("maths-tutor", base="MacOSGUI")],
    options={
        "build_exe": {
            "packages": ["PyQt6"], 
            "include_files": [
                os.path.join(maths_tutor_dir, "tutor.py"),
                os.path.join(maths_tutor_dir, "preferences.py"),
                os.path.join(maths_tutor_dir, "global_var.py"),
                os.path.join(maths_tutor_dir, "speech.py"),
                os.path.join(maths_tutor_dir, "main.py"),
                os.path.join(maths_tutor_dir, "__init__.py"),
                os.path.join(os.path.dirname(os.path.abspath(__file__)), "images"),
                os.path.join(os.path.dirname(os.path.abspath(__file__)), "sounds"),
                os.path.join(os.path.dirname(os.path.abspath(__file__)), "lessons"),
                os.path.join(os.path.dirname(os.path.abspath(__file__)), "locale"),
            ],
            # "icon":"",
        }
    },
)
