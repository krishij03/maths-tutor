
# math-tutor

this is the qt6plug branch


## Improvements

- Cross platform accessible gui (tested using VoiceOver for MacOS)
- Self reliant framework
- Language translation in regional languages such as  Malayalam, Sanskrit, Tamil, Hindi, Arabic
- Multilingual speech available
- Word problems support
- Updated test setup.py file to package the application into Windows and MacOS 
- Complete original migrated code to the latest Qt6 framework





## Installation
1. Clone project and navigate to project directory.

2. Create a python env and activate it

For Mac and Debian:-
```bash
  python3 -m venv qttutor
  cd qttutor
  source bin/activate

```
For Windows:-
```bash
  python3 -m venv qttutor
  cd qttutor
  qttutor\Scripts\activate

```
3. Install dependencies
```bash
  pip3 install -r requirements.txt
```
4. Navigate to root directory of project and run
```bash
  python3 maths-tutor
```