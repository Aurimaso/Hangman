import unittest
from unittest.mock import Mock
import flask_app.hangman as hangman


class TestHangman(unittest.TestCase):
    def test_masking_word(self):
        self.assertEqual("____", hangman.masking_word("test"))
        self.assertRaises(TypeError, hangman.masking_word, 2)
        self.assertEqual("__", hangman.masking_word("tt"))

    def test_letter_in_string(self):
        self.assertTrue(hangman.letter_in_string("a", "America"))
        self.assertFalse(hangman.letter_in_string("v", "America"))

    def test_check_winner(self):
        self.assertTrue(hangman.check_winner("America", "America"))
        self.assertFalse(hangman.check_winner("Americ_", "America"))

    def test_revealing_letters(self):
        self.assertEqual(
            "_meric_", hangman.revealing_letters("america", "_me_ic_", "r")
        )
        self.assertEqual(
            "_me_ic_", hangman.revealing_letters("america", "_me_ic_", "x")
        )

    def test_converting_string_to_list(self):
        self.assertEqual(
            ["w", "o", "r", "d"], hangman.converting_string_to_list("word")
        )
        self.assertEqual(
            ["h", "a", "n", "g"], hangman.converting_string_to_list("hang")
        )

    def test_get_all_guesses_from_db(self):
        first_mock = Mock()
        first_mock.guesses_made = "ABC"
        second_mock = Mock()
        second_mock.guesses_made = "BCD"
        self.assertTrue(
            {"A": 1, "B": 2, "C": 2, "D": 1},
            hangman.get_all_guesses_from_db([first_mock, second_mock]),
        )


if __name__ == "__main__":
    unittest.main()
