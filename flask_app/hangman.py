import random
from typing import List
from flask_app.models import Game


def get_word(path: str) -> str:
    with open(path, "r") as file:
        all_text = file.read()
        words = list(map(str, all_text.split()))
        return random.choice(words)


def mask_word(word: str) -> str:
    masked_word = ""
    for _ in word:
        masked_word += "_"
    return masked_word


def find_letter_in_string(guess: str, word: str) -> bool:
    if guess in word:
        return True
    return False


def check_winner(actual_word: str, guessed_progress: str) -> bool:
    if actual_word == guessed_progress:
        return True
    return False


def revealing_letters(word: str, progress: str, guess: str) -> str:
    listed_progrress = converting_string_to_list(progress)
    iteration_count = 0
    while iteration_count < len(word):
        if guess == word[iteration_count]:
            listed_progrress[iteration_count] = guess
            iteration_count += 1
        else:
            iteration_count += 1
    return "".join(listed_progrress)


def converting_string_to_list(word: str) -> list:
    list = []
    for x in word:
        list.append(x)
    return list


def get_all_guesses_from_db(games: List[Game]) -> dict:
    guesses_list_from_all_games = []
    guesses_dict = {}
    for game in games:
        guesses_list_from_all_games.append(game.guesses_made)

    for guesses in guesses_list_from_all_games:
        for letter in guesses:
            try:
                guesses_dict[letter] += 1
            except:
                guesses_dict[letter] = 1
    return guesses_dict
