import nltk
from nltk.corpus import words as nltk_words, wordnet
import random
nltk.download('words')

def filter_words():
    print("Loading... This may take a few seconds :)")
    filtered_words = [word.lower() for word in nltk_words.words() if wordnet.synsets(word)]
    return filtered_words

def welcome():
    print("Hello friend!")
    while True:
        name = input("Please enter your name: ").strip()
        if name == "":
            print("You can't do that! No blank lines.")
        else:
            break
    print(f"Welcome, {name}!")


stages = [
"""
      +---+
      |   |
      O   |
          |
          |
          |
    ========
    """,
    """
      +---+
      |   |
      O   |
      |   |
          |
          |
    ========
    """,
    """
      +---+
      |   |
      O   |
     /|   |
          |
          |
    ========
    """,
    """
    +---+
      |   |
      O   |
     /|\  |
          |
          |
    ========
    """,
    """
    +---+
      |   |
      O   |
     /|\  |
     /    |
          |
    ========
    """,
    """
    +---+
      |   |
      O   |
     /|\  |
     / \  |
          |
    ========
    """
]

def get_word_meaning(word):
    synsets = wordnet.synsets(word)
    if synsets:
        return synsets[0].definition()
    return " No definition found :/ "

def play_hangman():

    word_list = filter_words()

    def generate_secret_word():
        secretword = random.choice(word_list)
        length_word = len(secretword)
        return secretword, length_word


    secretword, length_word = generate_secret_word()
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    guess_word = ["-" for _ in range(length_word)]
    letter_storage = []
    guess_taken = 0
    current_stage = 0   
    hint_used = 0

    # Game introduction
    def intro():
        print('''
    ██╗░░██╗░█████╗░███╗░░██╗░██████╗░███╗░░░███╗░█████╗░███╗░░██╗
    ██║░░██║██╔══██╗████╗░██║██╔════╝░████╗░████║██╔══██╗████╗░██║
    ███████║███████║██╔██╗██║██║░░██╗░██╔████╔██║███████║██╔██╗██║
    ██╔══██║██╔══██║██║╚████║██║░░╚██╗██║╚██╔╝██║██╔══██║██║╚████║
    ██║░░██║██║░░██║██║░╚███║╚██████╔╝██║░╚═╝░██║██║░░██║██║░╚███║
    ╚═╝░░╚═╝╚═╝░░╚═╝╚═╝░░╚══╝░╚═════╝░╚═╝░░░░░╚═╝╚═╝░░╚═╝╚═╝░░╚══╝
    ''') #ART FROM https://www.asciiartcopy.com/hangman-ascii.html
        print("Let's play Hangman!")
        print(f"The word has {length_word} letters.")
        print("Guess one letter at a time.")
        print("Good luck!")
        print("Devoloped by Neelarko")

    # Guessing loop
    def guessing():
        nonlocal guess_taken, current_stage, hint_used

        while guess_taken < 6:  
            guess = input("Enter a letter: ").lower()

            if guess == "hint":
                if hint_used < 2:
                    hint_used += 1
                    reveal_letter()
                    continue
                else:
                    print("You've used all available hints!")
                    continue

            # Check for valid input
            if not guess or len(guess) > 1 or guess not in alphabet:
                print("Please enter a single letter from a-z.")
                continue
            elif guess in letter_storage:
                print("You already guessed that letter!")
                continue

            # Process guess
            letter_storage.append(guess)
            correct = False

            for i in range(length_word):
                if guess == secretword[i]:
                    guess_word[i] = guess
                    correct = True

            # Update game state
            if correct:
                print("Correct!")
            else:
                print("Incorrect.")
                guess_taken += 1
                current_stage += 1

            # Display progress
            print(' '.join(guess_word))
            print(f"Guesses remaining: {6 - guess_taken}")
            if current_stage < len(stages):
                print(stages[current_stage])
            else:
                print(stages[-1])  # Display the last stage if current_stage exceeds stages length

            # Check for win or lose
            if guess_taken == 6 and not correct:
                print("Sorry, you ran out of guesses.")
                print(f"The secret word was:  {secretword} ")
                print("Meaning of word is loading...... Please Wait")
                meaning = get_word_meaning(secretword)
                print(f"Meaning of the word:  {meaning} ")
                break

            if "-" not in guess_word:
                print("Congratulations! You won!")
                print(f"The secret word was:  {secretword}")
                print("Meaning of word is loading...... Please Wait")
                meaning = get_word_meaning(secretword)
                print(f"Meaning of the word:  {meaning} ")
                break

    def reveal_letter():
        nonlocal secretword, guess_word
        indices = [i for i, letter in enumerate(guess_word) if letter == "-"]
        if indices:
            index_to_reveal = random.choice(indices)
            guess_word[index_to_reveal] = secretword[index_to_reveal]
            print(f"A random letter has been revealed: {' '.join(guess_word)}")
        else:
            print("No letters to reveal.")

    # Main game loop
    welcome()
    intro()
    guessing()

    # Ask for retry
    retry = input("Do you want to play again? (y/n): ").lower()
    if retry in ["y", "yes"]:
        play_hangman()
    else:
        print("Thank you for playing!")

# Start the game
play_hangman()
