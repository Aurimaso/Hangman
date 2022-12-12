## Welcome to hangman game

## About the project:

- This is classic hangman game, where you have to try guessing random generated word.
- This is web application built with flask. Game can be played by many users at the same time. All the data is saved in SQLite database.
- Users can register their unique account, login, play unfinished games and view their game statistics.

## Settings

To have same settings please do steps below:

1. Install Python(for this project, I used Python 3.10.4).
2. Create vitual environment:
   ```bash
   python -m venv venv
   ```
3. Install all packages from requirements.txt:
   ```bash
   pip install -r requirements.txt
   ```
4. Activate vitual environment

## Usage

Run the game:

```bash
   python run.py
```

## Testing

- Main functions for Hangman game functionality can be found in /flask_app/handmanp.py <br />
- Testing was made using Unittest module. <br />
- To run the test:

```bash
   python test_handman.py
```

## Customize

Create your own words:

1. Go to /flask_app/static/dictionary
2. Upload new txt file with your own words.
3. Change PATH_OF_FUN_WORDS in routes.py

## Author

Aurimas Gaidamavičius <br />
Github: @Aurimaso <br />
Email: aurimas.gaidamavicius@gmail.com
