import random
import json
import requests
import curses

# Global variables
count = 0
score = 0
word_list = {'easy': ['which', 'there', 'about', 'write', 'first'],
             'medium': ['water', 'after', 'where', 'think', 'three'],
             'hard': ['study', 'night', 'light', 'paper', 'large']}
difficulty = 'easy'
x = random.choice(word_list[difficulty])
l = []

# Function to choose the difficulty level
def choose_difficulty(stdscr):
    global difficulty
    stdscr.clear()
    stdscr.addstr(0, 0, "Choose difficulty (easy, medium, hard): ")
    stdscr.refresh()
    difficulty = stdscr.getstr(1, 0).decode().lower()
    if difficulty not in word_list:
        stdscr.addstr(2, 0, "Invalid difficulty. Defaulting to easy.")
        stdscr.refresh()
        difficulty = 'easy'

# Function to fetch the definition of a word using the Oxford Dictionaries API
def get_word_definition(word):
    app_id = "ccc28cad"
    app_key = "5000c84ad7d2c2776572066bea7cc792"
    endpoint = "entries"
    language_code = "en-us"
    url = f"https://od-api.oxforddictionaries.com/api/v2/{endpoint}/{language_code}/{word.lower()}"
    r = requests.get(url, headers={"app_id": app_id, "app_key": app_key})
    data = r.json()
    if 'results' in data and data['results']:
        return data['results'][0]['lexicalEntries'][0]['entries'][0]['senses'][0]['definitions'][0]
    else:
        return "No definition available."

# Function to check if a word is in the dictionary using the Oxford Dictionaries API
def api(a):
    app_id = "ccc28cad"
    app_key = "5000c84ad7d2c2776572066bea7cc792"
    endpoint = "entries"
    language_code = "en-us"
    url = f"https://od-api.oxforddictionaries.com/api/v2/{endpoint}/{language_code}/{a.lower()}"
    r = requests.get(url, headers={"app_id": app_id, "app_key": app_key})
    return a in r.text

# Function to check if a letter is in the correct position of the word
def check_word_in_position(user_input, letter):
    a = user_input.index(letter)
    if user_input[a] == x[a]:
        l.append(letter)
        return f"{letter} is in the word and in the correct position"

# Function to check if a letter is in the word but in the wrong position
def check_letter_in_word(a):
    for i in a:
        if i in l:
            pass
        elif i in x:
            w = i
            return f"{w} is in the word but in the wrong position"

# Function to check if the entered word is correct
def check_if_word_is_correct(a):
    return "The word is correct" if a == x else None

# Function to save the game data to a JSON file
def save_game():
    data = {'difficulty': difficulty, 'score': score, 'count': count, 'word_list': word_list, 'x': x, 'l': l}
    with open('save_game.json', 'w') as file:
        json.dump(data, file)

# Function to load the game data from a saved JSON file
def load_game():
    global difficulty, score, count, word_list, x, l
    try:
        with open('save_game.json', 'r') as file:
            data = json.load(file)
            difficulty = data['difficulty']
            score = data['score']
            count = data['count']
            word_list = data['word_list']
            x = data['x']
            l = data['l']
        print("Game loaded successfully.")
    except FileNotFoundError:
        print("No saved game found.")

# Function to display the current progress of the word
def display_word_progress(stdscr):
    progress = ''.join([letter if letter in l else '_' for letter in x])
    stdscr.addstr(4, 0, f"Current progress: {progress}")
    stdscr.refresh()

# Multiplayer mode function
def multiplayer_mode():
    def multiplayer_mode(stdscr):
        global count, score, x, l
        players = int(stdscr.getstr(1, 0).decode())
        player_scores = {f"Player {i + 1}": 0 for i in range(players)}

    while True:
        for player in player_scores:
            stdscr.clear()
            stdscr.addstr(0, 0, f"{player}'s turn:")
            stdscr.refresh()
            a = stdscr.getstr(1, 0).decode()
            count += 1

            z = api(a)
            if z:
                stdscr.addstr(2, 0, 'The word is in the dictionary')
                stdscr.refresh()
                if len(a) != len(x):
                    stdscr.addstr(3, 0, f"The word does not contain {len(x)} letters")
                    stdscr.refresh()
                else:
                    for i in a:
                        p = check_word_in_position(a, i)
                        if p:
                            stdscr.addstr(4, 0, p)
                            stdscr.refresh()
                    q = check_letter_in_word(a)
                    if q:
                        stdscr.addstr(5, 0, q)
                        stdscr.refresh()
                    r = check_if_word_is_correct(a)
                    if r:
                        stdscr.addstr(6, 0, r)
                        stdscr.refresh()
                        player_scores[player] += score

                    # Add scoring system
                    score += len(l) + len(set(a) & set(x)) - len(l)
                    stdscr.addstr(7, 0, f"Current Score: {score}")
                    stdscr.refresh()

                    if count == 6:
                        stdscr.addstr(8, 0, 'You have used up your 6 tries')
                        stdscr.addstr(9, 0, f'The correct word is {x}')
                        stdscr.refresh()
                        return player_scores
            else:
                stdscr.addstr(2, 0, 'The word is not in the dictionary')
                stdscr.refresh()

            # Add hint system
            hint = get_word_definition(x)
            stdscr.addstr(10, 0, f"Hint: {hint}")
            stdscr.refresh()

            display_word_progress(stdscr)

            # Display scores after each round
        stdscr.addstr(11, 0, "\nCurrent Scores:")
        for idx, (player, player_score) in enumerate(player_scores.items(), start=12):
            stdscr.addstr(idx, 0, f"{player}: {player_score}")
            stdscr.refresh()

        if count == 6:
            break

def main(stdscr):
    global count, score, x, l
    # Main game loop
    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, 'Enter the word: ')
        stdscr.refresh()
        a = stdscr.getstr(1, 0).decode()
        count += 1

        # Choose difficulty at the start of the game
        if count == 1:
            stdscr.addstr(2, 0, "Do you want to load a saved game? (yes/no): ")
            stdscr.refresh()
            choice = stdscr.getstr(3, 0).decode().lower()
            if choice == 'yes':
                load_game()
            else:
                choose_difficulty(stdscr)
                x = random.choice(word_list[difficulty])

        z = api(a)
        if z:
            stdscr.addstr(2, 0, 'The word is in the dictionary')
            stdscr.refresh()
            if len(a) != len(x):
                stdscr.addstr(3, 0, f"The word does not contain {len(x)} letters")
                stdscr.refresh()
            else:
                for i in a:
                    p = check_word_in_position(a, i)
                    if p:
                        stdscr.addstr(4, 0, p)
                        stdscr.refresh()
                q = check_letter_in_word(a)
                if q:
                    stdscr.addstr(5, 0, q)
                    stdscr.refresh()
                r = check_if_word_is_correct(a)
                if r:
                    stdscr.addstr(6, 0, r)
                    stdscr.refresh()
                    break

                # Add scoring system
                score += len(l) + len(set(a) & set(x)) - len(l)
                stdscr.addstr(7, 0, f"Current Score: {score}")
                stdscr.refresh()

                if count == 6:
                    stdscr.addstr(8, 0, 'You have used up your 6 tries')
                    stdscr.addstr(9, 0, f'The correct word is {x}')
                    stdscr.refresh()
                    break
        else:
            stdscr.addstr(2, 0, 'The word is not in the dictionary')
            stdscr.refresh()

        # Add hint system
        hint = get_word_definition(x)
        stdscr.addstr(10, 0, f"Hint: {hint}")
        stdscr.refresh()

        display_word_progress(stdscr)

        # Save game option
        if count == 3:
            stdscr.addstr(11, 0, "Do you want to save the game? (yes/no): ")
            stdscr.refresh()
            choice = stdscr.getstr(12, 0).decode().lower()
            if choice == 'yes':
                save_game()

    # Multiplayer mode
    if count > 6: # Allow multiplayer mode only after a single-player round
        stdscr.addstr(13, 0, "\nStarting Multiplayer Mode:")
        stdscr.refresh()
        multiplayer_scores = multiplayer_mode(stdscr)

        # Display final scores for multiplayer mode
        stdscr.addstr(15, 0, "\nFinal Scores:")
        stdscr.refresh()
        for idx, (player, player_score) in enumerate(multiplayer_scores.items(), start=16):
            stdscr.addstr(idx, 0, f"{player}: {player_score}")
            stdscr.refresh()

    # End of the game
    stdscr.addstr(18, 0, "Game Over. Thanks for playing!")
    stdscr.refresh()
    stdscr.getch()

if __name__ == "__main__":
    curses.wrapper(main)