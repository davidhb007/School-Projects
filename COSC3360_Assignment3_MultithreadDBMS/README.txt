This is a program written in C language to simulate exclusive access to a hypothetical DataBase by the
use of mutexes and threads. The program uses input redirection in order to read from an input file
containing informationabout virtual users (each line is a new user) separated by groups. The virtual
DB is composed of different positions that can only be accessed by a user at a time The format of 
the input file is as follows:

Initial group with acces to the DataBase
<user group> <position requested> <arrival time of user> <excecution time>
.
.
.
.
End of input file

To run the program after compilation run command:
./Main < <input file name>

where Main is the name if the compiled program (can be changed)
