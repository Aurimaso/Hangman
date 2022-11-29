import unittest
import hangman

class TestAritmetika(unittest.TestCase):
   
    def test_masking_word(self):
        self.assertEqual('____', hangman.masking_word('test'))
        self.assertRaises(TypeError, hangman.masking_word, 2)
        self.assertEqual('__', hangman.masking_word('tt'))

    def test_letter_in_word(self):
        self.assertTrue(hangman.letter_in_word('a', 'America'))
        self.assertFalse(hangman.letter_in_word('v', 'America'))

    def test_check_winner(self):
        self.assertTrue(hangman.check_winner('America', 'America'))
        self.assertFalse(hangman.check_winner('Americ_', 'America'))

    def test_revealing_letters(self):
        self.assertEqual('_meric_', hangman.revealing_letters('america', '_me_ic_', 'r'))
        self.assertEqual('_me_ic_', hangman.revealing_letters('america', '_me_ic_', 'x'))

    def test_converting_string_to_list(self):
        self.assertEqual(['w', 'o', 'r', 'd'], hangman.converting_string_to_list('word'))
        self.assertEqual(['h', 'a', 'n', 'g'], hangman.converting_string_to_list('hang'))

    def test_from_dictionary_to_string(self):
        self.assertEqual('a: 1; b: 2; c: 3; ', hangman.from_dictionary_to_string({'a':1, 'b':2, 'c': 3}))
        self.assertEqual('a: a; b: b; c: c; ', hangman.from_dictionary_to_string({'a':'a', 'b':'b', 'c': 'c'}))

if __name__ == '__main__':
    unittest.main()