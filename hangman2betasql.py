from faker import Faker as fake
import random
import pymysql.cursors

password = None

def welcome():
    global name , password
    print("Hello friend!")
    while True:
        name = input("Please enter your name: ").strip()
        if name == "":
            print("You can't do that! No blank lines.")
        else:
            break
    password = input("Please enter your database password: ")
    print(f"Welcome, {name}!")

def create_database():
    con = pymysql.connect(
        host='localhost',
        user='root',
        password=password,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

    try:
        with con.cursor() as cursor:
            cursor.execute('CREATE DATABASE IF NOT EXISTS hangman')
            cursor.execute('USE hangman')
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS w_l (
                name VARCHAR(255) PRIMARY KEY,
                win INT,
                lose INT
            )
            ''')
        con.commit()
    finally:
        con.close()


def display_stats():
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password=password,
        db='hangman',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

    try:
        with connection.cursor() as cursor:
            cursor.execute('SELECT * FROM w_l')
            all_stats = cursor.fetchall()

            if all_stats:
                print("Player Statistics:  (if you are a first time player your Statistics will not be showed first time)")
                for stats in all_stats:
                    print(f"Player: {stats['name']}, Wins: {stats['win']}, Losses: {stats['lose']}")
            else:
                print("No stats found.")
    finally:
        connection.close()

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

def play_hangman():

    secretWord = fake().word()
    length_word = len(secretWord)
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    guess_word = ["-" for _ in range(length_word)]
    letter_storage = []
    guess_taken = 0
    current_stage = 0   
    hint_used = 0
    won = 0
    lost = 0

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
        print("Type 'hint' to reveal a random letter")
        print("Good luck!")
        print("Devoloped by Neelarko")

    # Guessing loop
    def guessing():
        nonlocal guess_taken, current_stage, hint_used, won, lost
        
        def update_stats_in_db():
            con = pymysql.connect(
                host='localhost',
                user='root',
                password=password,
                db='hangman',
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )

            try:
                with con.cursor() as cursor:
                    if guess_taken == 6 and not correct:
                        # Player lost, update 'lose' column in the database
                        cursor.execute('''
                        INSERT INTO w_l (name, win, lose)
                        VALUES (%s, 0, 1)
                        ON DUPLICATE KEY UPDATE lose = lose + 1
                        ''', (name,))
                        con.commit()
                    elif "-" not in guess_word:
                        # Player won, update 'win' column in the database
                        cursor.execute('''
                        INSERT INTO w_l (name, win, lose)
                        VALUES (%s, 1, 0)
                        ON DUPLICATE KEY UPDATE win = win + 1
                        ''', (name,))
                        con.commit()
            finally:
                con.close()

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
                update_stats_in_db()
                print(f"The secret word was: {secretWord}")
                break

            if "-" not in guess_word:
                print("Congratulations! You won!")
                update_stats_in_db()
                break

    def reveal_letter():
        nonlocal secretWord, guess_word
        indices = [i for i, letter in enumerate(guess_word) if letter == "-"]
        if indices:
            index_to_reveal = random.choice(indices)
            guess_word[index_to_reveal] = secretWord[index_to_reveal]
            print(f"A random letter has been revealed: {' '.join(guess_word)}")
        else:
            print("No letters to reveal.")
    

    # Main game loop
    welcome()
    create_database()
    display_stats()
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
