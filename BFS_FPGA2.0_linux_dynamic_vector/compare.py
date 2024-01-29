# coding:utf-8
import sys
import os

with open(os.path.dirname(__file__) + 'compare1.txt', "r") as c1:
    real = c1.readlines()

with open(os.path.dirname(__file__) + 'compare2.cmp', "r") as c2:
    hard = c2.readlines()
    
flag = 0    
if len(real) != len(hard):
    flag = 1
for i in range(len(real)):
    temp1 = real[i].rstrip('\n')
    temp2 = hard[i].rstrip('\n')
    if temp1 != temp2:       
        flag = 1
        print(temp1)
        print(temp2)
        
        
if flag != 0:
    print('compare error!')
else:
    print('compare pass!')    
