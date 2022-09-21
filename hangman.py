import random
import json

attempts = []
maxAttempts = 10

print(f'Welcome to the hangman game. Your max attempts to guess a single word: {maxAttempts}')

word_file = 'hangman\words.txt'
words = json.loads(open(word_file).read())
word = random.choice(words)

print('Little hint about the word: ' + word['hint'])

guessingData = {
    'word': word,
    'guessedWords': [],
}

for i in range(0, len(word['word'])):
    guessingData['guessedWords'].append(False)

money_file = 'money.txt'
money_file_element = open(money_file)
money = int(money_file_element.read()) or 0
money_file_element.close()

print(f'Your current cash: {money}')

def showWord():
    global word 
    global guessingData 

    text = 'The word is: '
    for i in range(0, len(word['word'])):
        if guessingData['guessedWords'][i]:
            text+= word['word'][(i):(i + 1)] + " "
        else:
            text+= "_ "

    print(text)
showWord()


def checkWord(letter):
    global word
    global guessingData 
    global money

    letters = []
    for i in range(0, len(word['word'])):
        if not guessingData['guessedWords'][i]:
            letters.append(word['word'][(i):(i + 1)].lower())

    print(f'Your guess: {letter}')

    if (letter in attempts):
        print(f'You already tried the word {letter}, try a new one!')

        requestWord()

        return
    elif (letter.lower() in letters):
        for i in range(0, len(word['word'])):
            if not guessingData['guessedWords'][i]:
                if (word['word'][(i):(i + 1)].lower() == letter.lower()):
                    guessingData['guessedWords'][i] = True
                    break

        remaining = 0
        for i in range(0, len(word['word'])):
            if not guessingData['guessedWords'][i]:
                remaining+= 1
                break 

        if (remaining == 0):
            print(f'You done it! You guessed the right word, which is: ' + word['word'])

            print('The game restarts.')
            
            money+= 100
            money_file_element = open(money_file, "w")
            money_file_element.write(str(money))
            money_file_element.close()
            print(f'Your current cash: {money}')

            generateWord()
            return 
    else: 
        attempts.append(letter)

        print("You missed the letter, try again!")
        print(f'Remaining attempts: {maxAttempts - len(attempts)}')

    showWord()

    if (len(attempts) >= maxAttempts):
        print("You couldn't guess the correct letters, the game restarts with a new one!")
        generateWord()

        return

    requestWord()

def requestWord():
    letter = input('Enter a character: ')

    if (len(letter) != 1):
        print('The character length must be 1!')

        requestWord()
        return

    checkWord(letter)

def generateWord():
    global words
    global word 
    global guessingData 

    word = random.choice(words)

    print('Little hint about the word: ' + word['hint'])

    guessingData = {
        'word': word,
        'guessedWords': [],
    }

    for i in range(0, len(word['word'])):
        guessingData['guessedWords'].append(False)

    attempts.clear()

    requestWord()

requestWord()