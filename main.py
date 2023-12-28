import random
import json
import requests

# Global variables
count = 0
score = 0
word_list = {'easy': ['which', 'there', 'about', 'write', 'first'],
             'medium': ['water', 'after', 'where', 'think', 'three'],
             'hard': ['study', 'night', 'light', 'paper', 'large']}
difficulty = 'easy'
x = random.choice(word_list[difficulty])
l = []

def choose_difficulty():
    global difficulty
    difficulty = input("Choose difficulty (easy, medium, hard): ").lower()
    if difficulty not in word_list:
        print("Invalid difficulty. Defaulting to easy.")
        difficulty = 'easy'

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

def api(a):
    app_id = "ccc28cad"
    app_key = "5000c84ad7d2c2776572066bea7cc792"
    endpoint = "entries"
    language_code = "en-us"
    url = f"https://od-api.oxforddictionaries.com/api/v2/{endpoint}/{language_code}/{a.lower()}"
    r = requests.get(url, headers={"app_id": app_id, "app_key": app_key})
    return a in r.text

def check_word_in_position(user_input, letter):
    a = user_input.index(letter)
    if user_input[a] == x[a]:
        l.append(letter)
        return f"{letter} is in the word and in the correct position"

def check_letter_in_word(a):
    for i in a:
        if i in l:
            pass
        elif i in x:
            w = i
            return f"{w} is in the word but in the wrong position"

def check_if_word_is_correct(a):
    return "The word is correct" if a == x else None

# Save and load game functions
def save_game():
    data = {'difficulty': difficulty, 'score': score, 'count': count, 'word_list': word_list, 'x': x, 'l': l}
    with open('save_game.json', 'w') as file:
        json.dump(data, file)

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

def display_word_progress():
    progress = ''.join([letter if letter in l else '_' for letter in x])
    print(f"Current progress: {progress}")

def multiplayer_mode():
    players = int(input("Enter the number of players: "))
    player_scores = {f"Player {i + 1}": 0 for i in range(players)}

    while True:
        for player in player_scores:
            print(f"\n{player}'s turn:")
            a = input('Enter the word: ')
            count += 1

            z = api(a)
            if z:
                print(f'The word is in the dictionary')
                if len(a) != len(x):
                    print(f"The word does not contain {len(x)} letters")
                else:
                    for i in a:
                        p = check_word_in_position(a, i)
                        if p:
                            print(p)
                    q = check_letter_in_word(a)
                    if q:
                        print(q)
                    r = check_if_word_is_correct(a)
                    if r:
                        print(r)
                        player_scores[player] += score

                # Add scoring system
                score += len(l) + len(set(a) & set(x)) - len(l)
                print(f"Current Score: {score}")

                if count == 6:
                    print('You have used up your 6 tries')
                    print('The correct word is', x)
                    break
            else:
                print('The word is not in the dictionary')

            # Add hint system
            hint = get_word_definition(x)
            print(f"Hint: {hint}")

            display_word_progress()

        # Display scores after each round
        print("\nCurrent Scores:")
        for player, player_score in player_scores.items():
            print(f"{player}: {player_score}")

        if count == 6:
            break

# Main game loop
while True:
    a = input('Enter the word: ')
    count += 1

    # Choose difficulty at the start of the game
    if count == 1:
        choice = input("Do you want to load a saved game? (yes/no): ").lower()
        if choice == 'yes':
            load_game()
        else:
            choose_difficulty()
            x = random.choice(word_list[difficulty])

    z = api(a)
    if z:
        print('The word is in the dictionary')
        if len(a) != len(x):
            print(f"The word does not contain {len(x)} letters")
        else:
            for i in a:
                p = check_word_in_position(a, i)
                if p:
                    print(p)
            q = check_letter_in_word(a)
            if q:
                print(q)
            r = check_if_word_is_correct(a)
            if r:
                print(r)
                break

        # Add scoring system
        score += len(l) + len(set(a) & set(x)) - len(l)
        print(f"Current Score: {score}")

        if count == 6:
            print('You have used up your 6 tries')
            print('The correct word is', x)
            break
    else:
        print('The word is not in the dictionary')

    # Add hint system
    hint = get_word_definition(x)
    print(f"Hint: {hint}")

    display_word_progress()

    # Save game option
    if count == 3:  # Save the game every 3 rounds
        choice = input("Do you want to save the game? (yes/no): ").lower()
        if choice == 'yes':
            save_game()