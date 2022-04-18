# main
#Author: Michael Drobot
#https://github.com/mdrobot7

import sys
import random

allowProfane = False

solution = ["", "", "", "", ""]

nonLetters = ["", "", "", "", ""] #letters that are NOT in the appropriate slots (nonLetters[0] will contain letters NOT in slot 0)

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
    for i in range(len(dict)):
        if i.find(let) != -1: #if it finds the letter ANYWHERE in the dict word, remove the dict word
            dict.pop(i)
            i -= 1
            
def removeWordsWithLetterNotInPos(let, pos): #removes words from dict that don't have the letter 'let' in position 'pos'
    global dict
    for i in range(len(dict)):
        if dict[i][pos] != let:
            dict.pop(i)
            i -= 1

def countUnknownLetters(word): #counts the number of "unknown" letters (letters that are not in 'solution') in 'word'
    global nonLetters
    global solution
    
    tempSolution = solution

    numUnknownLetters = 0
    for i in word:
        if tempSolution.find(i) == -1: numUnknownLetters += 1
        elif tempSolution.find(i) != -1: tempSolution.pop(tempSolution.find(i)) #remove letters that are found, fixes double letters
    return numUnknownLetters

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

    if len(dict) == 1: return dict[0]
    if numLettersMissing == 0:
        result = ""
        for i in solution: result += i #concatenate all letters of 'solution' into 'result'
        return result
    elif numLettersMissing == 1:
        return random.choice(dict)
    elif numLettersMissing > 1:
        numUnknownLetters = 0
        mostUnknownLetters = 0
        mostUnknownLettersWord = ""

        for i in dict:
            numUnknownLetters = countUnknownLetters(i)
            if numUnknownLetters > mostUnknownLetters:
                mostUnknownLetters = numUnknownLetters
                mostUnknownLettersWord = i
        return mostUnknownLettersWord

def checkInput(_word, _result): #parses the inputted word, and its result. removes bad words from the dictionary list.
    global dict
    global solution
    global nonLetters

    for i in range(5): #parse the input, eliminate dict words that CAN'T be the solution
        if _result[i] == 0:
            removeWordsWithLetter(_word[i])
        elif _result[i] == 1:
            nonLetters[i] = _word[i]
        elif _result[i] == 2:
            solution[i] = _word[i]
            removeWordsWithLetterNotInPos(_word[i], i)
            if _word[i] == 'q': #handle q-u combinations, just a bit of optimization
                solution[i + 1] = 'u'
                removeWordsWithLetterNotInPos('u', i + 1)
    
    foundEmptyIndexFlag = False
    for i in range(5): #check nonLetters for 'process of elimination' cases - where there is only one place a letter can be.
        for ii in nonLetters[i]:
            for iii in range(i + 1, 5):
                if nonLetters[iii].find(ii) == -1 and len(solution[iii]) == 0: foundEmptyIndexFlag = True
                if nonLetters[iii].find(ii) == -1 and len(solution[iii]) == 0 and foundEmptyIndexFlag: break #break if it finds two indices that could be a possible slot for 'ii'
            else: #found a slot that works!
                solution[iii] = ii
                removeWordsWithLetterNotInPos(ii, iii) #eliminate bad words
            foundEmptyIndexFlag = False
    
    pickNextInput()

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

checkInput(word, result)

if solution.count("") == 0:
    print("Solution: ", end = "")
    for i in solution:
        print(i, end = "") #print out the final solution



for i in range(5): #5 more attempts to find the word
    word = input("What is your input word? ")
    while len(word) != 5:
        if len(word) != 5: print("Input words should be 5 letters.")
        word = input("What is your input word? ")

    result = input("Result: ")
    while len(result) != 5:
        if len(result) != 5: print("Result should be 5 characters.")
        result = input("Result: ")

    print("Next word: " + checkInput(word, result))
