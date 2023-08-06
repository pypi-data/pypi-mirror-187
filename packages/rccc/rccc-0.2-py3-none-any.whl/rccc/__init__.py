bband1=input("Color of Band 1 : ")
if   band1=='Black':
    a="0"
elif band1=='Brown':
    a="1"
elif band1=='Red':
    a="2"
elif band1=='Orange':
    a="3"
elif band1=='Yellow':
    a="4"
elif band1=='Green':
    a="5"
elif band1=='Blue':
    a="6"
elif band1=='Violet':
    a="7"
elif band1=='Gray':
    a="8"


elif band1=='White':
    a="9"
    
band2=input("Color of Band 2 : ")
if band2=='Black':
    b="0"
elif band2=='Brown':
    b="1"
elif band2=='Red':
    b="2"
elif band2=='Orange':
    b="3"
elif band2=='Yellow':
    b="4"
elif band2=='Green':
    b="5"
elif band2=='Blue':
    b="6"
elif band2=='Violet':
    b="7"
elif band2=='Gray':
    b="8"
elif band2=='White':
    b="9"
    
band3=input("Color of Band 3 : ")
if band3=='Black':
    c="0"
elif band3=='Brown':
    c="1"
elif band3=='Red':
    c="2"
elif band3=='Orange':
    c="3"
elif band3=='Yellow':
    c="4"
elif band3=='Green':
    c="5"
elif band3=='Blue':
    c="6"
elif band3=='Violet':
    c="7"
elif band3=='Gray':
    c="8"
elif band3=='White':
    c="9"
elif band3=='Gold':
    c="-1"
elif band3=='Silver':
    c="-2"
    
band4=input("Color of Band 4 : ")

if band4=='Brown':
    d="1"
elif band4=='Red':
    d="2"

elif band4=='Yellow':
    d="5"
elif band4=='Green':
    d="0.5"
elif band4=='Blue':
    d="0.25"
elif band4=='Violet':
    d="0.1"
elif band4=='Gray':
    d="0.05"

elif band4=='Gold':
    d="5"
elif band4=='Silver':
    d="10"
k=int(b)
q=int(a)
p=int(c)
x=float(d)
output=(k+(q*10))*(10**p)
print("Resistor value : ", output ,"ohms","±",x,"%")
