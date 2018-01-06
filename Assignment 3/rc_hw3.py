'''
Created on Oct 20

@author: helloRC
'''
import numpy as np
import matplotlib.pyplot as plt
from astropy.io.fits.util import first
from dask.array.chunk import arange

## Q1
try:
    f = open("CEE_220_Scores.txt","r")
    #f = open("CEE_220_AlternativeList.txt","r")
    lines = f.readlines()
except IOError:
    print "Could not open the file!"
except:
    print "Other error"

###Q2
firstline = lines[0].split('\t')
assignment = []
lab = []
midterm = []
final = []

for i in range(1,len(firstline)):
    if firstline[i].find('Assignment')>=0:
        assignment.append(i)
    elif firstline[i].find('Lab')>=0:
        lab.append(i)
    elif firstline[i].find('Midterm')>=0:
        midterm.append(i)
    elif firstline[i].find('Final')>=0:
        final.append(i)

print assignment,lab,midterm,final
dictionary = dict(AS = assignment, LB = lab, MID = midterm, FN = final)
print dictionary
tar = dict()

## Q3
targetline = lines[1].split('\t')
for j in dictionary.keys():
    s = 0
    for m in dictionary.get(j):
        try:
            s = s + float(targetline[m])
        except ValueError:
            print "Data error"
        print "Score for group ", j,"is ",s
        tar[j] = s
        
for j in range(1,len(targetline)):
    if firstline[j].find('Bonus Assignment') >= 0:
        tar['AS'] -= float(targetline[j])
print tar
print tar['AS'],tar['LB']   

##Q4
weights1 = dict(AS = 0.25, LB = 0.05, MID = 0.4, FIN = 0.3)
student = []
result = dict()
for i in np.arange(2,len(lines)):
    l = lines[i].split('\t')
    target_as = 0
    target_mt = 0
    target_lab = 0
    target_fin = 0
    for j in assignment:
        try:
            target_as = target_as + float(l[j])
        except ValueError:
            print "missing data for column", j,'of',l[0]
    for j in lab:
        try:
            target_lab = target_lab + float(l[j])
        except ValueError:
            print "missing data for column", j,'of',l[0]
    for j in midterm:
        try:
            target_mt = target_mt + float(l[j])
        except ValueError:
            print "missing data for column", j,'of',l[0]
    for j in final:
        try:
            target_fin = target_fin + float(l[j])
        except ValueError:
            print "missing data for column", j,'of',l[0]   
    weighted_score = target_as/tar['AS']*0.25 + target_lab/tar['LB']*0.05 + target_mt/tar['MID']*0.40 + target_fin/tar['FN']*0.30
    grade = (weighted_score-0.2)/0.20
    if grade<0.7:
        grade = 0
    else:
        grade = round(grade,1)
    result = dict(student = l[0], AS_result = target_as, LB_result = target_lab, MID_result = target_mt, FN_result = target_fin, Weightedscore = weighted_score, Grade=grade)
    student.append(result)

print student
grade_list = []

for s in student:
    grade_list.append(s.get('Grade'))
print grade_list

plt.hist(grade_list, bins=np.arange(0.05, 4.1, 0.1))
plt.xlabel('assigned numberic grade')
plt.ylabel('number of students')
plt.title('Grade Distribution for CEE200')
plt.savefig('plot.pdf')
plt.show()


    
