import random
import string
import pkg_resources


class Hangman:
    def __init__(self, words=None):
        self._words = words or self._load_words()
        self._secret_word = self._pick_word()
        self._picked = set()
        self._guess = [None] * len(self._secret_word)

    def _load_words(self):
#        filename = 'sowpods.txt'
#        with open(filename, 'r') as f:
        with pkg_resources.resource_stream(__name__, 'sowpods.txt') as f:
            words = [line.strip() for line in f.readlines()]
        return words

    def _pick_word(self):
        return random.choice(self._words)

    def is_valid_letter(self, letter):
        return len(letter) == 1 and letter in string.ascii_uppercase

    def is_already_guessed(self, letter):
        return letter in self._picked

    def guess_letter(self, letter):
        self._picked.add(letter)

    def discards(self):
        return ''.join((sorted(letter for letter in self._picked if letter not in self._secret_word)))

    def current_guess(self):
        guess = [letter if letter in self._picked else '_' for letter in self._secret_word]
        return ' '.join(guess)

    def is_solved(self):
        return not any(c == '_' for c in self.current_guess())


def main():
    h = Hangman()
    while True:
        print(h.current_guess())
        print(h.discards())
        if h.is_solved():
            break
        letter = input("Pick a letter: ")
        if not h.is_valid_letter(letter) or h.is_already_guessed(letter):
            print("Pick exactly one new letter please")
            continue
        h.guess_letter(letter)

if __name__ == '__main__':
    main()
