from string import ascii_lowercase
import random


def no_of_attempts():
    while True:
        attempts = input('How many incorrect attempts do you want? [1-25] ')
        try:
            attempts = int(attempts)
            if 1 <= attempts <= 25:
                return attempts
            else:
                print('{} is not between 1 to 25 '.format(attempts))
        except ValueError:
            print('{} is not an integer between 1 and 25 '.format(attempts))


def get_length():
    while True:
        min_length = input('What minimum word length do you want? [4-16] ')
        try:
            min_length = int(min_length)
            if 4 <= min_length <= 16:
                return min_length
            else:
                print('{} is not between 4 and 16'.format(min_length))
        except ValueError:
            print('{} is not an integer between 4 and 16'.format(min_length))


def get_random_word(min_length):
    curr_word = None
    with open(r'C:\Users\ReBeL Roar\Desktop\WordList.txt') as l:
        word = random.choice(l.readlines())
        if len(word) > min_length:
            return word
        else:
            get_random_word(min_length)


def get_display_word(word, correctly_guessed_state):
    """Get the word suitable for display."""
    if len(word) != len(correctly_guessed_state):
        raise ValueError('Word length and indices length are not the same')
    displayed_word = ''.join([letter if correctly_guessed_state[i] else '*' for i, letter in enumerate(word)])
    return displayed_word.strip()


def get_next_letter(remaining_letters):
    """Get the user-inputted next letter."""
    if len(remaining_letters) == 0:
        raise ValueError('There are no remaining letters')
    while True:
        next_letter = input('Choose the next letter: ').lower()
        if len(next_letter) != 1:
            print('{} is not a single character'.format(next_letter))
        elif next_letter not in ascii_lowercase:
            print('{} is not a letter'.format(next_letter))
        elif next_letter not in remaining_letters:
            print('{} has been guessed before'.format(next_letter))
        else:
            remaining_letters.remove(next_letter)
        return next_letter


def play_hangman():
    """Play a game of hangman.At the end of the game, returns if the player wants to retry."""

    # Let player specify difficulty
    print('Starting the game of Hangman...')
    attempts_remaining = no_of_attempts()
    min_length = get_length()
    # Randomly select a word
    print('Selecting a word...')
    word = get_random_word(min_length)
    print()
    # Initialize game state variables
    correctly_guessed_state = [letter not in ascii_lowercase for letter in word]
    remaining_letters = set(ascii_lowercase)
    wrong_letters = []
    word_solved = False
    # Main game loop
    while attempts_remaining > 0 and not word_solved:
        # Print current game state
        print('Word: {}'.format(get_display_word(word, correctly_guessed_state)))
        print('Attempts Remaining: {}'.format(attempts_remaining))
        print('Previous Guesses: {}'.format(','.join(wrong_letters)))

        # Get player's next letter guess
        next_letter = get_next_letter(remaining_letters)

        # Check if letter guess is in word
        if next_letter in word:
            # Guessed correctly
            print('{} is in the word '.format(next_letter))

            # Reveal letters
            for i in range(len(word)):
                if word[i] == next_letter:
                    correctly_guessed_state[i] = True
        else:
            # Guessed incorrectly
            if next_letter in ascii_lowercase:
                print('{} is Not in the word '.format(next_letter))
                attempts_remaining -= 1
                wrong_letters.append(next_letter)

        # Check if word is completely solved
        if False not in correctly_guessed_state:
            word_solved = True
        print()

    print("The word is {} ".format(word))

    if word_solved:
        print('Congratulation! You won!')
    else:
        print('Try again! Good Luck')

    try_again = input('Would you like to try again? [Y/y] ')
    return try_again.lower() == 'y'


if __name__ == '__main__':
    while play_hangman():
        print()


