import re

#getting a feel for python regex library
#not going to use it but may take inspo


#Starts with "The", ends with "Spain"
txt = "The rain in Spain"
x = re.search("^The.*Spain$", txt)

if x:
  print("YES! We have a match!")
else:
  print("No match")


#Return list containing ever "ai"
x = re.findall("ai", txt)
print(x)


#Return empty list if no match is found
x = re.findall("Portugal", txt)
print(x)
if (x):
  print("Yes, there is at least one match!")
else:
  print("No match")


#Search for the first white-space(ws) char
x = re.search("\s", txt)
print("The first white-space character is located in position:", x.start())


#Split string at ws char
x = re.split("\s", txt)
print(x)


#Split string only at the first ws char
x = re.split("\s", txt, 1)
print(x)


#Replace ws char with "9"
x = re.sub("\s", "9", txt) 
print(x)


#Replace first two ws chars
x = re.sub("\s", "9", txt, 2)
print(x)


#Search that will return a Match Object
x = re.search("ai", txt)
print(x)


#Print (start & end) pos for the first match
x = re.search(r"\bS\w+", txt)
print(x.span())


#Print the string passed into a funct
print(x.string)


#Print the part of the string with the match
print(x.group())
