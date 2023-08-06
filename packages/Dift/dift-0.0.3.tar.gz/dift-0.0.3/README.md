# Installation
``` pip install Dift```
# Introduction
Dift is a python library that allows you to read data from a file and convert it into a dictionary that can be used by your Python script, and it can be configured to your needs
# Usage
You can import Dift into your script by adding
```import Dift```
To read a data from a file you can use the ```readData()``` function
The ```readData()``` function takes one main arguments and three optional arguments
# 1.file
the main argument that ```readData()``` function takes is the file to read the data fron and the file should be like this
```
Student's Name : Alex Corey
Mother's Name : Branda Corey
Father's Name : John Corey
```
And the it doesn't require ```""``` to set the name of the key and its syntax can be customized
Example of code using the ```readData()``` function
```
import Dift
file = open('details.txt','r')
dict = Dift.readData(file)
```
<h3>2.ctype</h3>
This is an optional argument that you can enable to store int values as int and disable to store int values as str in the dictionary
Enabled by default

Example:-
```
d = readData(file,ctype=False)
```
<h3>3.seperator</h3>

It is a string argument which requires a sign to be used by the library to seperate keys from values the default is ```:```
```
d = readData(file,seperator=":")
```
# 4.ignore
This optional arguments is used to enable or disable the error that occurs when you didn't used the right seperator in the file
True by default

``` 

d = readData(file,ignore=True)
```