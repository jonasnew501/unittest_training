# Purpose of this project

The purpose of this project is to practice the use of try-except-finally in Python,  
also in conjunction with Unit tests (using pytest).  

The idea for the project came from Uncle Bob´s book *"Clean Code"*  
from Chapter 7: "Error Handling" -> section "Write Your Try-Catch-Finally Statement First" (pages 105-106).  
He claims that a Try-Except-Finally (resp. Try-Catch-Finally (in Java)) should be written first and  
the actual code/algorithm should be incorporated into that structure from the beginning on,  
as opposed to first writing the algorithm and only then, when problems arise, adding try-except-finally-  
block(s) to it.  

Additionally he claims that (unit) tests shall be written right away, with the goal of forcing the exceptions  
in the source code. By doing that, one is pushed towards implementing the right exception handling in 'except'  
and cleanup in 'finally'.  

A basic example where this procedure can be practiced is creating a text-file and writing some text to it.  
This was done is this project.  

A rollback (here: deleting the file if it exists) is done in the 'except'-part, and a cleanup (here: closing the file-handle)  
is done in the 'finally'-part. Of course, those two parts are only necessary when for the file-creation and writing  
no context-mananger is used.  
To practice the context-manager-use too, both ways were implemented in this project.  