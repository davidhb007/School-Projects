"""
David Herrera
The following is a program to find the top k highest frequency
words in a file given as input, based on a user entered
key value. For example, if user enters a k == 4; the output
will be a file consisting the 4 most repeated words in the input
file, including words with same frequency, which will be sorted
by said frequency starting with the largest number
"""

import sys
import re


class Word:

    def __init__(self, word, freq):
        self.word = word
        self.freq = freq

    def get(self):
        return str(self.word + " " + str(self.freq))


def cleanLine(line):
    """A function that gets rid of all unnecessary characters in an line
       of strings and returns a all the 'cleaned' words in it"""

    extra = re.compile(r'[^a-z\s]')
    cleanedLine = str.lower(line)
    for match in re.findall(extra, cleanedLine):
        cleanedLine = cleanedLine.replace(match, '')
    return cleanedLine


def isUnique(word, uniqueWords):
    """Function to determine is a word already belongs in the unique words
    list by using recursion"""
    if len(uniqueWords) == 0:
        return 0
    if uniqueWords[0].word == word:
        return 1 + isUnique(word, uniqueWords[1:])
    else:
        return 0 + isUnique(word, uniqueWords[1:])


def countCurrentWord(list, word):
    """Recursive function that counts the number of times a certain
       word appears in a list"""
    if len(list) == 0:
        return 0
    if list[0] == word:
        return 1 + countCurrentWord(list[1:], word)
    else:
        return 0 + countCurrentWord(list[1:], word)


def findUnique(wordsList, uniqueWords):
    """Find unique finds all unique words in a list of words (strings)
       Finds the ones that are repeated counting their frequency
       and finally returns a list of every word and their frequency"""

    if len(wordsList) == 0:
        return

    else:
        newWord = wordsList[0]
        word = Word(newWord, countCurrentWord(wordsList, newWord))
        if isUnique(newWord, uniqueWords) == 0:
            uniqueWords.append(word)
        return findUnique(wordsList[1:], uniqueWords)


def sortUnique(uniqueWords):
    """An implementation of the quick sort algorith to sort the list of unique
       words in decreasing order"""
    large = []
    equal = []
    small = []
    if len(uniqueWords) > 1:
        pivot = uniqueWords[0]
        for word in uniqueWords:
            if word.freq < pivot.freq:
                small.append(word)
            elif word.freq == pivot.freq:
                equal.append(word)
            elif word.freq > pivot.freq:
                large.append(word)
        return sortUnique(large) + equal + sortUnique(small)
    else:
        return uniqueWords


def topK(uniqueWords, k, top):
    if len(uniqueWords) < 2:
        # Only one elemnent in unique words list
        top.append[uniqueWords[0]]
        return

    else:
        # loop through to find the frequency of the k highest word
        uniqueFreq = []
        for word in uniqueWords:
            freq = word.freq
            if freq not in uniqueFreq:
                uniqueFreq.append(freq)
            if len(uniqueFreq) == k:
                break

        for i in uniqueWords:
            if i.freq >= uniqueFreq[-1]:
                top.append(i)
            if i.freq < uniqueFreq[-1]:
                break
        return


def findTopKWord(inputF, k, outputF):
    """The following is the script responsible for calling all necessary
       functions to clean an input file and extract all the properly formatted
       words, find the ones that are repeated and output the results to
       a user provided output file"""

    wordsList = []
    uniqueWords = []
    try:
        with open(inputF, "r") as inFile:
            for line in inFile:
                line = cleanLine(line)
                wordsInALine = line.split()
                for word in wordsInALine:
                    wordsList.append(word)

            inFile.close()

            if len(wordsList) == 0:
                print("ERROR: Input file is empty. Please provide a valid input file")
                exit(1)
            findUnique(wordsList, uniqueWords)
            uniqueWords = sortUnique(uniqueWords)

            top = []
            topK(uniqueWords, k, top)

            with open(outputF, "w") as outFile:
                for word in top:
                    outFile.write(word.get() + "\n")
                outFile.close()

    except FileNotFoundError as notFoundErr:
        print(notFoundErr)


if __name__ == '__main__':

    """
        The following section of code focuses on processing the command line arguments.
        First, the program deals with any instance of the program being run with the incorrect amount
        of parameters (should be exactly 2; the script name followed by a string containing the
        input file name, the key, and the output file name). It then deals with any user entered string
        that isnot in the propper format; it has to be exactly "input=<file_name>;k=<integer > 0>;output=<file_name>"
        And lastly, it processes the user string to extract the necessary values to be used by the script.
    """

    # Make sure user enters 2 arguments: the name of the script and the parameters to be passed. Else: print help message
    if len(sys.argv) != 2:
        print('Usage: python|python3 topkword.py "input=<input file name>;k=<key>;output=<output file name>"')
        exit(1)

    # Capture user parameters as a string to be processed
    usrString = str(sys.argv[1])
    # Separate the different components of the parameters
    commands = usrString.split(";")
    if len(commands) != 3:
        # Make sure the user passes exactly 3 parameters to the program. Else: print a help message
        print("Error: You must enter exactly 3 parameters as a string")
        print('Usage: python|python3 topkword.py "input=<input file name>;k=<key>;output=<output file name>"')
        print('Parameters entered: "' + usrString + '"')
        exit(1)

    if ("input=" not in commands[0]) | ("k=" not in commands[1]) | ("output=" not in commands[2]):
        # Make sure the user enters the parameters in the right format. Else: print a help message
        print("Error: You must enter exactly 3 parameters as a string")
        print('Usage: python|python3 topkword.py "input=<input file name>;k=<key>;output=<output file name>"')
        print('Parameters entered: "' + usrString + '"')
        exit(1)

    # Values to be passed to the findTopKWord function
    inputF = ""
    key = 0
    outputF = ""

    try:
        # Capture file names safelly
        inputF += str(commands[0].split("=")[1])
        outputF += str(commands[2].split("=")[1])
    except Exception:
        print("Error! Input file name is not valid")
        raise
    except Exception:
        print("Error! Output file name is not valid")
        raise

    try:
        # Validate the key entered by user
        key += int(commands[1].split("=")[1])
        if key <= 0:
            print("Error! Invalid key. Key must be a number greater than 0")
            exit(1)
    except ValueError:
        print("Error! Invalid key. Key must be a number greater than 0")
        raise

    """
        End of first section of code. Up to the point, all command line arguments entered by the user
        have been properly validated and extracted to then be used for the purpose of the program.
    """

    # Call the text file processing function
    findTopKWord(inputF, key, outputF)
