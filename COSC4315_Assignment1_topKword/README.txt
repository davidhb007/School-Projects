Name: David Herrera
PSID: 1570639
--------

How to run the code:
python topkword.py "input=<file name>;k=<positive integer>;output=<file name>"

--------
A brief description of how you implement the program. How the recursion works. etc:

Two major components, the main function that processes the command line arguments and calls the second major component; which is 
the script responsible for calling all the necessary functions to find the top k most repeated words.

The main idea for recursions was to extract the first word from the list of all words and call another recursive function to 
compare with the first word of a slice of the same list starting with the next index