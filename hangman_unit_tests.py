import unittest
import random
import string

from hangman import Hangman


class HangmanTests(unittest.TestCase):
    def setUp(self):
        self.h = Hangman("SOME RANDOM WORDS TO USE FOR TESTING PURPOSES AVOIDING LOADING FROM FILE SYSTEM".split())

    def test_load_words(self):
        self.assertEqual(len(self.h._load_words()), 267751)

    def test_pick_word(self):
        w1 = self.h._pick_word()
        w2 = self.h._pick_word()
        self.assertTrue(len(w1) > 0)
        self.assertTrue(len(w2) > 0)
        self.assertTrue(w1 != w2)

    def test_valid_letter(self):
        self.assertTrue(self.h.is_valid_letter('A'))
        self.assertTrue(self.h.is_valid_letter('Z'))

    def test_invalid_letter(self):
        self.assertFalse(self.h.is_valid_letter('z'))
        self.assertFalse(self.h.is_valid_letter('z'))
        self.assertFalse(self.h.is_valid_letter('AB'))

    def test_is_already_guessed(self):
        self.assertFalse(self.h.is_already_guessed('A'))
        self.h.guess_letter('A')
        self.assertTrue(self.h.is_already_guessed('A'))

    def test_guess_letter(self):
        self.assertFalse(self.h.is_already_guessed('A'))
        self.h.guess_letter('A')
        self.assertTrue(self.h.is_already_guessed('A'))

    def test_letters_in_word_do_not_count_as_discards(self):
        letter_in_word = random.choice(self.h._secret_word)
        self.h.guess_letter(letter_in_word)
        self.assertEqual('', self.h.discards())

    def test_discards_are_sorted(self):
        letters_not_in_word = [c for c in string.ascii_uppercase if c not in self.h._secret_word]
        guesses = sorted(letters_not_in_word, reverse=True)
        self.h.guess_letter(guesses[0])
        self.h.guess_letter(guesses[1])
        self.assertEqual(guesses[1] + guesses[0], self.h.discards())

    def test_no_correct_guesses(self):
        self.assertTrue(all(c == '_' or c == ' ' for c in self.h.current_guess()))

    def test_guess_letter_in_word(self):
        letter = random.choice(self.h._secret_word)
        self.h.guess_letter(letter)
        self.assertTrue(letter in self.h.current_guess())

    def test_guess_all_letters_in_word(self):
        self.assertFalse(self.h.is_solved())
        for c in self.h._secret_word:
            self.h.guess_letter(c)
        self.assertTrue(self.h.is_solved())
        self.assertFalse(any(c == '_' for c in self.h.current_guess()))

