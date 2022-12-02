import random


def get_word(path: str) -> str:
    with open(path, "r") as file:
        allText = file.read()
        words = list(map(str, allText.split()))
        return random.choice(words)


def masking_word(word: str) -> str:
    masked_word = []
    for _ in word:
        masked_word.append("_")
    return "".join(masked_word)


def letter_in_string(guess: str, word: str) -> bool:
    if guess in word:
        return True
    else:
        return False


def check_winner(word: str, progress: str) -> bool:
    if word == progress:
        return True
    else:
        return False


def revealing_letters(word: str, progress: str, guess: str) -> str:
    listed_progrress = converting_string_to_list(progress)
    i = 0
    while i < len(word):
        if guess == word[i]:
            listed_progrress[i] = guess
            i += 1
        else:
            i += 1
    return "".join(listed_progrress)


def converting_string_to_list(word: str) -> list:
    list = []
    for x in word:
        list.append(x)
    return list


def get_all_guesses_from_db(game_from_db: object) -> dict:
    list_of_guesses = []
    dict = {}
    for x in game_from_db.all():
        list_of_guesses.append(x.guesses_made)

    for x in list_of_guesses:
        for i in x:
            try:
                dict[i] += 1
            except:
                dict[i] = 1
    return dict


def from_dictionary_to_string(dict: dict) -> str:
    new_string = ""
    for x in range(len(dict)):
        new_string += f"{str(list(dict.keys())[x])}: {str(list(dict.values())[x])}; "
    return new_string
