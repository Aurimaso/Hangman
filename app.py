import random

class Hangman:
    def __init__(self, word_list: list):
        self.word_list = word_list
        self.random_word = random.choice(self.word_list)
        self.masked_word = self.masking_word()

    def masking_word(self) -> str:
        masked_word = []
        for _ in self.random_word:
            masked_word.append('_')
        return masked_word

    def guessing_letters(self) -> str:
        guesses = 0
        used_letters = ""
        print(''.join(self.masking_word()))

        while guesses < 10:
            if self.check_answer() == 'You won':
                print(self.check_answer())
                break
            
            guess = input('Guess a letter: ')

            if guess in self.random_word and guess not in used_letters:
                used_letters += guess
                self.masked_word = self.revealing_letters(self.masked_word, guess)
                print(''.join(self.masked_word))
                guesses += 1
                self.check_answer()
            elif guess in used_letters:
                print('already used letter, try again')
            elif guess not in self.random_word and guess not in used_letters:
                used_letters += guess
                guesses +=1
                self.masked_word = self.revealing_letters(self.masked_word, guess)
                print(''.join(self.masked_word))
    def check_answer(self):

        if self.random_word == ''.join(self.masked_word):
            return 'You won'
        else:
            return 'You lost'
        
    
    def revealing_letters(self, masked_word, guess = '') -> str:
        i = 0
        while i < len(self.random_word):
            if guess == self.random_word[i]:
                masked_word[i] = guess
                i+=1
            else:
                i+=1
        return masked_word

            
def run_app() -> None:
    list_of_words = ['apple', 'orange', 'python', 'computer', 'testing', 'hangman']
    first_player = Hangman(list_of_words)
    print(first_player.guessing_letters())

if __name__=="__main__":
    run_app()
