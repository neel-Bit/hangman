#1.3 Change log - added ascii graphic, playagain option
import random

def welcome():
    print("Hello friend!")
    while True:
        name = input("Please enter your name: ").strip()
        if name == "":
            print("You can't do that! No blank lines.")
        else:
            break
    print(f"Welcome, {name}!")

def choose_mode():
    easy_wordList = ["lion", "umbrella", "window", "computer", "glass",
                     "juice", "chair", "desktop", "laptop", "dog", "cat",
                     "lemon", "cable", "mirror", "hat"]
    
    hard_wordList = [
"necessary", "misspell", "rhythm", "pneumonia", "guarantg", "entrepreneur",
"conscientious", "chameleon", "maintenance", "supercalifragilisticexpialidocious", "pseudopseudohypoparathyroidism",
"hippopotomonstrosesquipedaliophobia", "floccinaucinihilipilification", "sesquipedalian", "incomprehensibilities", "antiestablishmentarianism",
"pneumonoultramicroscopicsilicovolcanoconiosis", "otorhinolaryngologist", "disproportionableness", "electroencephalographically", "antidisestablishmentarianism",
"accommodate", "exhilarate", "bureaucracy", "camaraderie", "embarrass", "millennium",
"parallel", "unnecessary", "vocabulary"
]


    mode = input("Choose game mode: Easy or Hard? ").lower()
    if mode == "hard":
        return hard_wordList
    return easy_wordList

stages = [
    """
      +---+
      |   |
      O   |
     /|\  |
     / \  |
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
      |   |
          |
          |
    ========
    """,
    """
      +---+
      |   |
      O   |
          |
          |
          |
    ========
    """
]

def play_hangman():

    wordList = choose_mode()
    secretWord = random.choice(wordList).lower()
    length_word = len(secretWord)
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    guess_word = ["-" for _ in range(length_word)]
    letter_storage = []
    guess_taken = 0
    current_stage = 0   
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
        nonlocal guess_taken, current_stage

        while guess_taken < 6:  # Adjusted the max guesses to 6 (as per your hangman stages)
            guess = input("Enter a letter: ").lower()

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
                if guess == secretWord[i]:
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
                print(f"The secret word was: {secretWord}")
                break

            if "-" not in guess_word:
                print("Congratulations! You won!")
                break


    # Main game loop
    welcome()
    intro()
    guessing()

    # Ask for retry
    retry = input("Do you want to play again? (yes/no): ").lower()
    if retry == "yes":
        play_hangman()
    else:
        print("Thank you for playing!")

# Start the game
play_hangman()
