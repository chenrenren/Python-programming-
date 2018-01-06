'''
Created on Oct 7, 2017

@author: helloRC
'''
## change char to number
def char_to_num(a):
    dict_char = {'0': 0, '1': 1, '2' : 2, '3' : 3, '4': 4, '5': 5, '6' : 6, '7' : 7, '8': 8, '9': 9, 'a' : 10, 'b' : 11, 'c': 12, 'd': 13, 'e' : 14, 'f' : 15}
    if a not in dict_char:
        print 'invalid input charactor'
    else:
        return dict_char.get(a)

## change number to char
def num_to_char(c):
    dict_num={0:'0', 1:'1', 2:'2', 3: '3', 4:'4', 5:'5', 6:'6', 7: '7', 8:'8', 9:'9', 10:'a', 11: 'b', 12:'c', 13:'d', 14:'e', 15: 'f'}
    if c not in dict_num:
        print " invalid input charactor"
    else:
        return dict_num.get(c)
## binary to decimal number
def frombin(s):
    i=0
    a=0
    l=len(s)
    while i<l:
        a=a+int(s[i])*2**(l-i-1)
        i=i+1
    return a
# test
#print frombin('1101')

## hexadecimal number to decimal number
def fromhex(s):
    l=len(s)
    b=0
    for j in s:
        j=char_to_num(j)
        b=b+int(j)*16**(l-1)
        l=l-1
    return b
# test 
#print fromhex('a7dc')

#decimal to binary
def tobin(val):
    if val==0:
        return ''
    else:
        return tobin(val/2)+num_to_char(val%2)
#test
#print tobin(54)

#decimal to hexadecimal
def tohex(val):
    if val==0:
        return ''
    else:
        return tohex(val/16)+num_to_char(val%16)
# test
#print tohex(42972)
    
def tobase(base,val):
    if val==0:
        return ''
    else:
        return tobase(base,val/base)+num_to_char(val%base)

def frombase(base,x):
    length=len(x)
    re=0
    for a in x:
        a=char_to_num(a)
        re=re+a*base**(length-1)
        length=length-1
    return re

