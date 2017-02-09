import unittest
from hypothesis import given
from hypothesis.strategies import none
from hypothesis.strategies import text
from hypothesis.strategies import characters

from hangman.hangman import Hangman

VALID_LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
KNOWN_WORD = "SECRETWORD"


class HangmanHypothesisTests(unittest.TestCase):
    # setUp() is only called once per test, not once per choice
    def setUp(self):
        self.hangman = Hangman()
        self.hangman_with_known_word = Hangman([KNOWN_WORD])

    @given(none())
    def test_picks_a_different_word_for_each_game(self, s):
        w1 = self.hangman._pick_word()
        w2 = self.hangman._pick_word()
        assert w1 != w2

    @given(text(alphabet=VALID_LETTERS, min_size=1, max_size=1))
    def test_valid_guesses(self, letter):
        assert self.hangman.is_valid_letter(letter)

    @given(characters(blacklist_characters=VALID_LETTERS))
    def test_invalid_guesses(self, letter):
        assert not self.hangman.is_valid_letter(letter)

    @given(text(alphabet=VALID_LETTERS, min_size=1, max_size=1))
    def test_is_already_guessed(self, letter):
        # We need a new Hangman object for each test
        h = Hangman(['SOME', 'RANDOM', 'WORDS'])
        assert not h.is_already_guessed(letter)
        h.guess_letter(letter)
        assert h.is_already_guessed(letter)

    @given(text(alphabet=KNOWN_WORD, min_size=1, max_size=1))
    def test_status_contains_underscores_spaces_and_correct_guesses(self, letter):
        h = self.hangman_with_known_word
        assert all(c in KNOWN_WORD+' _' for c in h.current_guess())
        assert len(h.current_guess()) == len(KNOWN_WORD)*2-1

    @given(text(alphabet=KNOWN_WORD, min_size=1, max_size=1))
    def test_correct_guesses_show_up_in_status(self, letter):
        h = self.hangman_with_known_word
        h.guess_letter(letter)
        assert letter in h.current_guess()

    @given(text(alphabet=KNOWN_WORD, min_size=1, max_size=1))
    def test_correct_guesses_do_not_show_up_in_discards(self, letter):
        h = self.hangman_with_known_word
        h.guess_letter(letter)
        assert letter not in h.discards()

    @given(characters(blacklist_characters=KNOWN_WORD))
    def test_incorrect_guesses_show_up_in_discards(self, letter):
        h = self.hangman_with_known_word
        h.guess_letter(letter)
        assert letter in h.discards()

    @given(characters(blacklist_characters=KNOWN_WORD+' _'))
    def test_incorrect_guesses_do_not_show_up_in_status(self, letter):
        h = self.hangman_with_known_word
        h.guess_letter(letter)
        assert letter not in h.current_guess()

    @given(text(alphabet=VALID_LETTERS, min_size=1, max_size=1))
    def test_discards_are_sorted(self, letter):
        h = self.hangman_with_known_word
        h.guess_letter(letter)
        assert ''.join(sorted(h.discards())) == h.discards()

    @given(text(alphabet=VALID_LETTERS, min_size=1))
    def test_when_all_letters_are_guessed_the_puzzle_is_solved(self, text):
        h = Hangman([text])
        assert not h.is_solved()
        for letter in text:
            h.guess_letter(letter)
        assert h.is_solved()