import json
import os
import re

with open(os.path.dirname(__file__) + '\\pe_module_input.json', "r") as f:
    res = json.load(f)
expression = res['Expression']
op = re.findall(r"[A-z]", expression)
op1 = []
for i in range(len(op)-1):        
    m1_height = res[str(i+1)]['m1_height']
    m1_width = res[str(i+1)]['m1_width']
    m2_height = res[str(i+1)]['m2_height']
    m2_width = res[str(i+1)]['m2_width']

    res[str(i+1)][op[0]] = '['
    for j in range(m1_width):
        if j ==0:
            res[str(i+1)][op[0]] += '1,'
        else:
            res[str(i+1)][op[0]] += '0,'
    res[str(i+1)][op[0]] = res[str(i+1)][op[0]].rstrip(',')
    res[str(i+1)][op[0]] += ']'
    
    res[str(i+1)][op[1]] = '['
    for j in range(m2_height):
        res[str(i+1)][op[1]] += '['
        for k in range(m2_width):
           
            if j*12 <= k-1 and j*12 >= k-12 and j==0:
                res[str(i+1)][op[1]] += '1,'
            elif (j) <= k-1 and (j) >= k-12 and j == 12:
                res[str(i+1)][op[1]] += '1,'  
            elif j <= k-1 and j >= k-12 and j == 24:
                res[str(i+1)][op[1]] += '1,'  
            elif j <= k-1 and j >= k-12 and j == 36:
                res[str(i+1)][op[1]] += '1,'  
            elif j <= k-1 and j >= k-12 and j == 48:
                res[str(i+1)][op[1]] += '1,'  
            elif j <= k-1 and j >= k-12 and j == 60:
                res[str(i+1)][op[1]] += '1,'  
            else:
                res[str(i+1)][op[1]] += '0,'
        res[str(i+1)][op[1]] = res[str(i+1)][op[1]].rstrip(',')        
        res[str(i+1)][op[1]] += '], '
    res[str(i+1)][op[1]] = res[str(i+1)][op[1]].rstrip(', ')         
    res[str(i+1)][op[1]] += ']'
print(res[str(i+1)][op[1]])
with open(os.path.dirname(__file__) + '\\pe_module.json', "w") as f:
    json.dump(res, f)
