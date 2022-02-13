# main
#Author: Michael Drobot
#https://github.com/mdrobot7

import time
import sys

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

def checkInput(_word, _result): #parses the inputted word, and its result. removes bad words from the dictionary list.
    global dict
    global solution
    global nonLetters

    for i in range(5):
        if _result[i] == "0": #if the i'th character in _word is NOT in the solution word AT ALL
            count = 0
            while True:
                if count >= len(dict):
                    break
                if dict[count].find(_word[i]) != -1: #if the current dict word has the bad letter AT ALL, remove the dict word.)
                    dict.pop(count)
                    continue
                count += 1 #only increments the count if it does not pop an index
        elif _result[i] == "1": #if the i'th letter is correct, but in the WRONG place
            nonLetters[i] += _word[i]
            count = 0
            while True:
                if count >= len(dict):
                    break
                if dict[count].find(_word[i]) == -1: #if the current dict word DOES NOT have the letter, then it will not work -- remove it.
                    dict.pop(count)
                    continue
                count += 1
        elif _result[i] == "2": #if the i'th letter is correct AND in the right place
            solution[i] = _word[i] #put the known good letters in the solution string/array
            count = 0
            while True:
                if count >= len(dict):
                    break
                if dict[count].find(_word[i]) != i: #if the current dict word has the bad letter in ANY PLACE OTHER THAN THE GOOD ONE, remove the dict word.
                    dict.pop(count)
                    continue
                count += 1
    """
    #check everything down here with prints, I'm not sure this algorithm works
    for a in range(5): #for loop through the nonLetters list
        if solution[a] != "-": continue
        for b in range(5): #for loop through the REST of the nonLetters list (skip over nonLetters[a])
            if b == a: continue
            if solution[b] != "-": continue

            for c in nonLetters[b]: #for loop through EACH LETTER in nonLetters[b]
                for d in nonLetters: #for loop through nonLetters again, trying to find nonLetters[b][c]
                    if d.find(c) == -1: break
                else:
                    solution[a] = c #if a particular letter IS in every index other than nonLetters[a], it's a solution
    
    count = 0
    for i in range(5): #go over the dict again, get rid of any words that don't match the solution string
        while True:
            if count >= len(dict):
                break
            if dict[count].find(solution[i]) != i: #if the current dict word has the bad letter in ANY PLACE OTHER THAN THE GOOD ONE, remove the dict word.
                dict.pop(count)
                continue
            count += 1"""
                

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

word = input("What is your starting word? (Recommended starting word: \'roate\') ")
while len(word) != 5:
    if len(word) != 5: print("Input words should be 5 letters.")
    word = input("What is your starting word? (Recommended starting word: \'roate\') ")

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

    checkInput(word, result)

    if solution.count("") == 0:
        print("Solution: ", end = "")
        for i in solution:
            print(i, end = "") #print out the final solution
        break

#for i in dict:
#    print(i)