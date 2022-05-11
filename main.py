# main
#Author: Michael Drobot
#https://github.com/mdrobot7

import sys
import random

allowProfane = False

solution = ["", "", "", "", ""]

nonLetters = ["", "", "", "", ""] #letters that are NOT in the appropriate slots (nonLetters[0] will contain letters NOT in slot 0)

letterRank = "eariotnslcudpmhgbfywkvxzjq" #most common letters in english, in order

try:
    dictFile = open("dictionary.txt", 'r')
    if allowProfane: #if profane is allowed
        dictFile = open("dictionary-profane.txt", 'r') #combine the dict and prof files into one large file
except FileNotFoundError:
    print("Dictionary files not found!")
    raise SystemExit

#====================================================================================================================================================================================#

def removeWordsWithLetter(let): #removes words from dict containing the letter 'let'
    global dict
    for i in range(len(dict) - 1, -1, -1):
        if dict[i].find(let) != -1: #if it finds the letter ANYWHERE in the dict word, remove the dict word
            dict.pop(i)

def removeWordsWithoutLetter(let):
    global dict
    for i in range(len(dict) - 1, -1, -1):
        if dict[i].find(let) == -1: #if the letter is not found in the dict word, remove it
            dict.pop(i)
            
def removeWordsWithLetterNotInPos(let, pos): #removes words from dict that don't have the letter 'let' in position 'pos'
    global dict
    for i in range(len(dict) - 1, -1, -1):
        if dict[i][pos] != let:
            dict.pop(i)

def removeWordsWithLetterInPos(let, pos): #removes words from dict that have the letter 'let' in position 'pos'
    global dict
    for i in range(len(dict) - 1, -1, -1):
        if dict[i][pos] == let:
            dict.pop(i)

def searchNonLetters(let): #searches nonLetters for a letter, returns true/false if it found/didn't find it
    global nonLetters
    for i in nonLetters:
        if i.find(let) != -1: return True
    return False

def wordRankScore(word): #computes the "score" of a word, aka how good of a guess it is.
    #closer to 0 is better.
    #letters that repeat within 'word' are automatically 26. letters that are already in solution or nonletters are also 26
    #should prioritize words with less found letters, and with more common letters
    
    global nonLetters
    global solution
    global letterRank

    score = 0

    for i, let in enumerate(word):
        if word.find(let, i + 1) != -1: score += 26 #repeat letters
        elif searchNonLetters(let) == True or solution.count(let) != 0: score += 26
        else: score += letterRank.find(let)
    return score

def pickNextInput(): #selects the next input word
    #How the algorithm works:
    #If the solution array is missing more than 1 letter, it picks the word from dict with the most unknown letters
    #If the solution array is missing 1 letter, it starts guessing from the available words left
    #If the solution array is full, or if there is only 1 choice left in dict, it outputs the resulting word.

    global dict
    global solution
    global nonLetters
    
    numLettersMissing = 0
    for i in solution: #count the number of letters missing from 'solution'
        if len(i) == 0: numLettersMissing += 1

    #if dict.index("gecko") != -1: print("have it")
    if len(dict) < 10:
        print(dict)
        print(nonLetters)
        print(solution)

    if len(dict) == 0:
        print("No words found that match the result scores entered. Check your results, and rerun.")
        raise SystemExit
    if len(dict) == 1: return dict[0]
    if numLettersMissing == 0:
        result = ""
        for i in solution: result += i #concatenate all letters of 'solution' into 'result'
        return result
    elif numLettersMissing == 1:
        return random.choice(dict)
    elif numLettersMissing > 1:
        currentScore = 0
        leastScore = wordRankScore(dict[0])
        leastScoreWord = dict[0]

        for i in dict:
            currentScore = wordRankScore(i)
            if currentScore < leastScore:
                leastScore = currentScore
                leastScoreWord = i
        return leastScoreWord

def checkInput(_word, _result): #parses the inputted word, and its result. removes bad words from the dictionary list.
    global dict
    global solution
    global nonLetters

    for i in range(5): #parse the input, eliminate dict words that CAN'T be the solution
        if _result[i] == "0":
            removeWordsWithLetter(_word[i])
        elif _result[i] == "1":
            nonLetters[i] += _word[i]
            removeWordsWithLetterInPos(_word[i], i)
            removeWordsWithoutLetter(_word[i]) #the letter has to be somewhere in the word, so get rid of everything that doesn't have it
        elif _result[i] == "2":
            solution[i] = _word[i]
            removeWordsWithLetterNotInPos(_word[i], i)
            if _word[i] == 'q': #handle q-u combinations, just a bit of optimization
                solution[i + 1] = 'u'
                removeWordsWithLetterNotInPos('u', i + 1)
    
    #for loop through each of the indices-letters in nonLet, grab a letter, and then search for it through nonLet
    """foundEmptyIndexFlag = False
    emptyIndex = 0
    for ind in nonLetters:
        for let in ind:
            for i, searchInd in enumerate(nonLetters):
                if searchInd.find(let) == -1 and len(solution[i]) == 0:
                    foundEmptyIndexFlag = True
                    emptyIndex = i
                if searchInd.find(let) == -1 and len(solution[i]) == 0 and foundEmptyIndexFlag: break #break if it finds two indices that could be a possible slot for 'ii'
            else: #found a slot that works!
                solution[emptyIndex] = let
                removeWordsWithLetterNotInPos(let, emptyIndex) #eliminate bad words
            foundEmptyIndexFlag = False"""
    
    return pickNextInput()

#====================================================================================================================================================================================#

dict = dictFile.readlines() #read all lines into a list

count = 0
while True: #rough cut of the dictionary -- remove bad words, spaces, carriage returns...
    if count >= len(dict):
        break
    dict[count] = dict[count].strip("\n")
    if len(dict[count]) != 5: #get rid of non-5-character words (rules of wordle)
        dict.pop(count)
        continue
    if not dict[count].isalpha(): #remove words with apostrophes, spaces, etc
        dict.pop(count)
        continue
    count += 1 #only increments the count if it does not pop an index

print("Wordle Solver")
print("-------------")

word = input("What is your starting word? (Recommended starting word: \'salet\') ")
while len(word) != 5:
    if len(word) != 5: print("Input words should be 5 letters.")
    word = input("What is your starting word? (Recommended starting word: \'salet\') ")

print("Input your starting word into the Wordle website. Enter the result below, in this form: ")
print("""
    0 for \"Not in word at all\"
    1 for \"In word, but in the wrong place\"
    2 for \"In word, and in the right place\" """)

result = input("Result: ")
while len(result) != 5:
    if len(result) != 5: print("Result should be 5 characters.")
    result = input("Result: ")

for i in range(5): #5 more attempts to find the word
    word = checkInput(word, result)
    print("Next word: " + word)

    while True:
        yesno = input("Was that the solution? [Y/N] ")
        if yesno == "Y" or yesno == "y": raise SystemExit
        elif yesno == "N" or yesno == "n": break
        else: print("Not a valid input.")

    result = input("Result: ")
    while len(result) != 5:
        if len(result) != 5: print("Result should be 5 characters.")
        result = input("Result: ")