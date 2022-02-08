# main
#Author: Michael Drobot
#https://github.com/mdrobot7

import time
import sys

allowProfane = False

global solution = "-----" #using strings here in place of arrays, since in python strings pretty much are arrays. makes it easier.

try:
    dictFile = open("dictionary.txt", 'r')
    if allowProfane: #if profane is allowed
        dictFile = open("dictionary-profane.txt", 'r') #combine the dict and prof files into one large file
except FileNotFoundError:
    print("Dictionary files not found!")
    raise SystemExit

#====================================================================================================================================================================================#

def checkInput(_word, _result):
    for i in range(5):
        if _result[i] == 0: #if the i'th character in _word is NOT in the solution word AT ALL
            count = 0
            while True: #"rough cut" of the dictionary - remove any dict words that are not 5 letters, extra \n chars, spaces, etc
                if count >= len(dict):
                    break
                if dict[count].find(_word[i]) != -1: #if the current dict word has the bad letter AT ALL, remove the dict word.
                    dict.pop(count)
                    continue
                count += 1 #only increments the count if it does not pop an index
        elif _result[i] == 1:
            count = 0
            while True: #"rough cut" of the dictionary - remove any dict words that are not 5 letters, extra \n chars, spaces, etc
                if count >= len(dict):
                    break
                if dict[count].find(_word[i]) == -1: #if the current dict word DOES NOT have the letter, then it will not work -- remove it.
                    dict.pop(count)
                    continue
                count += 1 #only increments the count if it does not pop an index
        elif _result[i] == 2:
            solution[i] = word[i] #put the known good letters in the solution string/array
            count = 0
            while True: #"rough cut" of the dictionary - remove any dict words that are not 5 letters, extra \n chars, spaces, etc
                if count >= len(dict):
                    break
                if dict[count].find(_word[i]) != i: #if the current dict word has the bad letter in ANY PLACE OTHER THAN THE GOOD ONE, remove the dict word.
                    dict.pop(count)
                    continue
                count += 1 #only increments the count if it does not pop an index

#====================================================================================================================================================================================#

dict = dictFile.readlines() #read all lines into a list
count = 0

while True: #"rough cut" of the dictionary - remove any dict words that are not 5 letters, extra \n chars, spaces, etc
    if count >= len(dict):
        break
    dict[count] = dict[count].strip("\n")
    if len(dict[count]) != 5: #get rid of less than 4 character words (rules of spelling bee)
        dict.pop(count)
        continue
    count += 1 #only increments the count if it does not pop an index

print("Wordle Solver")
print("-------------")
word = input("What is your starting word? (Recommended starting word: \'roate\') ")

print("Input your starting word into the Wordle website. Enter the result below, in this form: ")
print(
    """0 for \"Not in word at all\"
    1 for \"In word, but in the wrong place\"
    2 for \"In word, and in the right place\" """)

result = input("Result: ")

checkInput(word, result)
