import random
import json
import requests

word_list = ['which','there','their','about','would','these','other','words','could','write','first',
    'water','after','where','right','think','three','years','place','sound','great','again','still','every',
    'small','found','those','never','under','might','while','house','world','below','asked','going','large',
    'until','along','shall','being','often','earth','began','since','study','night','light','above','paper']

count = 0
x = random.choice(word_list)
l = []

def api(a):
    app_id  = "ccc28cad"
    app_key  = "5000c84ad7d2c2776572066bea7cc792"
    endpoint = "entries"
    language_code = "en-us"
    url = "https://od-api.oxforddictionaries.com/api/v2/" + endpoint + "/" + language_code + "/" + a.lower()
    r = requests.get(url, headers = {"app_id": app_id, "app_key": app_key})
    
    if a in r.text:
        return True
    else:
        return False

def check_word_in_position(user_input,letter):
    a = user_input.index(letter)
    if user_input[a] == x[a]:
        l.append(letter)
        return letter+" is in the word and in the correct position"

def check_letter_in_word(a):
    for i in a:
        if i in l:
            pass
        else:
            if i in x:
                w = i
                return w+" is in the word but in the wrong position"

def check_if_word_is_correct(a):
    if a == x:
        return "The word is correct"

while True:
    a = input('Enter the word : ')
    count += 1
    z = api(a)
    if z == True:
        print('The word is in the dictionary')
        if len(a) != 5:
            print("The word does not contain 5 letters")
        else:
            for i in a:
                p = check_word_in_position(a,i)
                if p is None:
                    pass
                else:
                    print(p)
            q = check_letter_in_word(a)
            if q is None:
                pass
            else:
                print(q)
            r = check_if_word_is_correct(a)
            if r is None:
                pass
            else:
                print(r)
                break
            
        if count == 6:
            print('You have used up your 6 tries')
            print('The correct word is',x)
            break
    else:
        print('The word is not in the dictionary')