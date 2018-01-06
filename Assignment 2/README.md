Problem Statement
Expand Assignment #1 (problem #3) into a class
 
class GeneralBase (object): 

which holds the internal variables in a dictionary as 

    self.value = dict(base=…, value=…)

Use the procedures developed under problem #3 through

   import problem3 as p

where problem3 needs to be replaced by your filename.
overload the operators add (+), subtract (-), multiply (*), integer divide (floordiv, //), and modulo (rest of integer division, %). Assume the second value can be given in any general base (2-16), possibly different from the first object base.

Provide a suitable implementation of __str__(self) , to be tested via the print statement

>>> x = GenBase( 16, 255 )
>>> print x
ff (base 16)

Add a method which returns the base of an instance of the class (here the variable x) as an integer:

>>> x = GenBase( 4, 237 )
>>> x.Base()
4

Add a method ChangeBase(base) to convert an instance of the class to a different base:

>>> x = GenBase( 4, 237 )
>>> x.Base()
4
>>> x.ChangeBase( 7 )
>>> x.Base()
7

All functions shall accept numbers in any arbitrary base (2-16) and return an object of type GeneralBase()

Provide reliable error recognition and handling (warning, feedback)

Develop a test procedure which generates alternative representation of a series of different decimal values and performs the following operations on them:

x = GenBase( some_base, some_value)
y = GenBase( other_base, other_value )
x + y
x - y
y - x
x * y
x // y
x % y
y // x
y % x

Provide a report which describes the implementation details, the class interface, the testing procedure, and its outcome.  It is sufficient to upload a single PDF file including all requested sections. 
A copy of your python source may be requested if the documentation is lacking sufficient information.  10 points will be deducted if this becomes necessary.
remarks: 
ad 1. the value may be given as decimal number (integer) or as a string representing th evalue in the provided base.  The first option makes testing for a valid input trivial, while the latter requires some smarts in handling the input.

add 8. you need to think about the result of your operation. It should be of type GenBase or you won't be able to do further computations with your class objects.  For mixed base computations, I suggest using the base of self as the target representation.
