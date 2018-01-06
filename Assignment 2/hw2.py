'''

@author: helloRC
'''
import q3 as p
from docutils.io import InputError
from anaconda_project.internal.conda_api import result

class GenBase(object):
    
    def __init__(self,base1,value1):
        if (base1>=2 and base1<=16 and type(base1)==int):
            self.value = dict(base=base1,value = p.tobase(base1,int(value1)))
        elif(type(value1)!=int):
            print "The input is not a integer"   
        else:
            print "invalid input"
            raise InputError
    
    def base(self):
        return self.value['base']
    
    
    def __add__(self,x):
        if type(x)==GenBase:
            summ = p.frombase(self.value['base'],self.value['value']) + p.frombase(x.value['base'], x.value['value'])
            return GenBase(self.value['base'], summ)
        else:
            raise TypeError
    
    def __sub__(self,x):
        if type(x)==GenBase:
            subt = p.frombase(self.value['base'],self.value['value'])-p.frombase(x.value['base'],x.value['value'])
            if subt<0:
                print "subtraction is less than 0"
            else:
                return GenBase(self.value['base'], subt)
        else:
            raise TypeError
    
    def __mul__(self,x):
        if type(x)==GenBase:
            pro = p.frombase(self.value['base'],self.value['value'])*p.frombase(x.value['base'],x.value['value'])
            return GenBase(self.value['base'], pro)
        else:
            raise TypeError
    
    def __div__(self,x):
        if type(x)==GenBase:
            if p.frombase(x.value['base'],x.value['value'])==0:
                print "The divisor can't be zero!"
            else:        
                div=p.frombase(self.value['base'],self.value['value'])/p.frombase(x.value['base'],x.value['value'])
                return GenBase(self.value['base'],div)
        else:
            raise TypeError
    
    def modulo(self,x):
        if type(x)==GenBase:    
            res = p.frombase(self.value['base'],self.value['value'])%p.frombase(x.value['base'],x.value['value'])
            return GenBase(self.value['base'],res)
        else:
            raise TypeError
        
    def __str__(self):
        s = '%s (base %s)' % (self.value['value'], self.value['base'])
        return s
    
    def changebase(self,base_new):
        n = p.frombase(self.value['base'],self.value['value'])
        m = p.tobase(base_new,n)
        self.value=dict(base=base_new,value=m)
        


if (__name__=="__main__"):
    m = GenBase(16, 255)
    print "Genbase(16,255):", m
    a = GenBase(4, 237)
    print "GenBase(4,237) base:", a.base()
    a.changebase(7)
    print "changebase to 7:", a.base()

    x = GenBase(16,255)
    y = GenBase(4,237)

    print "x+y:",x.__add__(y)
    print "y+x:",y.__add__(x)
    print "x-y:",x.__sub__(y)
    print "y-x:",y.__sub__(x)
    print "x*y:",x.__mul__(y)
    print "y*x:",y.__mul__(x)
    print "x/y:",x.__div__(y)
    print "y/x:",y.__div__(x)
    print "x%y:",x.modulo(y)
    print "y%x:",y.modulo(x)
   
