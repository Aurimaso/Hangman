# import random

# list_of_words = ['apple', 'orange', 'python', 'computer', 'testing', 'hangman']

# def choose_random_word(my_list: list) -> str:
#     return (random.choice(my_list))

# print(choose_random_word(list_of_words))

# progress = ['_','_', 'a', 's', '_']
# print(''.join(progress))

# word = 'bananasssssssss'

# masked_word = ''
# for x in word:
#     masked_word += '_'

# print(masked_word)

# for x in range(6):
#     print('test')


word = 'banana'
masked = ['_', '_', '_', '_', '_', '_']


def revealing_letters(guess, random_word, masked_word):
        i = 0
        while i < len(random_word):
            if guess == random_word[i]:
                masked_word[i] = guess
                i+=1
            else:
                i+=1
        return ''.join(masked_word)

print(revealing_letters('n', word, masked))

