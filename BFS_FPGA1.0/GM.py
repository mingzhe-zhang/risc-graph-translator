import json
import os
import re
import numpy as np
import operator
import random

def read_vector(a):
    a = a.lstrip('[').rstrip(']')
    a = a.split(',')
    return [int(x) for x in a]

def read_matrix(b):
    b = b.lstrip('[').rstrip(']')
    b = b.split(', ')
    matrix_b = list()
    for a in b:
        matrix_b.append(read_vector(a))
    return matrix_b

with open(os.path.dirname(__file__) + '\\pe_module.json', "r") as f:
    res = json.load(f)
expression = res['Expression']
op = re.findall(r"[A-z]", expression)
op1 = []
vector_a = list()
matrix_b = list()
for i in range(len(op)-1):        
    m1_height = res[str(i+1)]['m1_height']
    m1_width = res[str(i+1)]['m1_width']
    m2_height = res[str(i+1)]['m2_height']
    m2_width = res[str(i+1)]['m2_width']
    PE_num = res[str(i+1)]['PE_num']
    exeblock_per_PE = res[str(i+1)]['exeblock_per_PE']
    col_tiling = res[str(i+1)]['column_tiling']
    col_tiling = [int(x) for x in col_tiling.split(',')]
    col_per_node = int(PE_num/col_tiling[0]) * col_tiling[1]
    reload_num = int(m2_height/(PE_num/col_tiling[0]*col_tiling[1]))
    # node_num = res[str(i+1)]['node']
    node_num = reload_num
    is_random = res[str(i+1)]['is_random']
    sparse_degree = res[str(i+1)]['sparse_degree']
    sparse_degree_max = res[str(i+1)]['sparse_degree_max']
    vector_a = res[str(i+1)][op[0]]
    matrix_b = res[str(i+1)][op[1]]
    vector_a = read_matrix(vector_a)
    matrix_b = read_matrix(matrix_b)
    
output = ''
# for x in matrix_b:
#     for z in x:
#         print((z),end="")
#         output += str(z)
#     print('\n')
#     output += '\n'

tile_m1 = list()
tile_m2 = list()
counter = 0
for i in range(reload_num*reload_num):
    tile_m1_array = list()
    tile_m2_array = list()
    for j in range(int(PE_num/col_tiling[0])):
        tile_m1_array.append((vector_a[0][int(i/reload_num)*col_per_node : int(i/reload_num+1)*col_per_node]))
        if (i+j) % reload_num != 0 or j != 0:
            tile_m2_array.append(([x[counter%(int(PE_num/col_tiling[0])*reload_num)*col_tiling[1] : (counter%(int(PE_num/col_tiling[0])*reload_num))*col_tiling[1]+col_tiling[1]] for x in matrix_b[int(i/reload_num)*col_per_node : int(i/reload_num+1)*col_per_node]]))
            
        else:
            tile_m2_array.append(([x[0 : col_tiling[1]] for x in matrix_b[int(i/reload_num)*col_per_node : int(i/reload_num+1)*col_per_node]]))
        #print((counter%(int(PE_num/col_tiling[0])*reload_num))*col_tiling[1]+col_tiling[1])    
        #print(int(i/reload_num)*col_per_node)
        counter += 1
    tile_m1.append(tile_m1_array)
    tile_m2.append(tile_m2_array)    


result = list()
result.append(1)
for i in range(m1_width-1):
    result.append(0)
result_temp = result.copy()
level_counter = 1
#for i in range(6):

i = 0
while(1):
    temp = list()
    level_counter += 1
    print('\n'+str(i)+' time round')
    output += '\n'+str(i)+' time round\n'
    for j in range(reload_num*reload_num):
        print('tile'+str(j)+':')
        output += 'tile'+str(j)+':\n'
        for k in range(int(PE_num/col_tiling[0])):
            #print(tile_m2[j][k])
            #print(tile_m1[j][k])
            t = np.array(tile_m1[j][k])@np.array(tile_m2[j][k])
            t[t>=1]= 1
            # temp.append(t)
            # print('node'+str(int(j%reload_num))+',pe'+str(col_tiling[0]*k+col_tiling[0]-1)+',st: ')
            # print(t)
            real_t = list()
            for x in range(len(t)):
                #print(k*col_tiling[1]+int(j%reload_num)*int(m2_width/node_num)+x)
                if result[k*col_tiling[1]+int(j%reload_num)*int(m2_width/node_num)+x]==0:
                    if t[x] != 0:
                        result[k*col_tiling[1]+int(j%reload_num)*int(m2_width/node_num)+x] = level_counter
                        real_t.append(1)
                    else:
                        real_t.append(0)
                else:
                    real_t.append(0)
            temp.append(t)
            print('node'+str(int(j%reload_num))+',pe'+str(col_tiling[0]*k+col_tiling[0]-1)+',st: ')
            output += 'node'+str(int(j%reload_num))+',pe'+str(col_tiling[0]*k+col_tiling[0]-1)+',st: \n'
            print(tile_m1[j][k])
            output += ''.join([str(x)+' ' for x in tile_m1[j][k]])
            output += '\n'
            print(t)
            output += ''.join([str(x)+' ' for x in t]) + '\n'
    if operator.eq(result_temp, result):
        break
    else:
        result_temp = result.copy()
        i += 1

    tile_m1_copy = tile_m1.copy()
    tile_m1_copy = np.array(tile_m1_copy)
    tile_m1_copy[tile_m1_copy>=1] = 2
    tile_m1_copy[tile_m1_copy==0] = 1
    tile_m1_copy[tile_m1_copy>=2] = 0

    for j in range(reload_num*reload_num):
        for k in range(int(PE_num/col_tiling[0])):
            for m in range(int(PE_num/col_tiling[0])):
                tile_m1[j][k][m*col_tiling[1] : m*col_tiling[1]+col_tiling[1]] = np.array(tile_m1[j][k][m*col_tiling[1] : m*col_tiling[1]+col_tiling[1]]) | np.array(temp[int(j/reload_num)*int(PE_num/col_tiling[0])+m]) | np.array(temp[int(j/reload_num)*int(PE_num/col_tiling[0])+int(PE_num/col_tiling[0])*reload_num+m])
                tile_m1[j][k][m*col_tiling[1] : m*col_tiling[1]+col_tiling[1]] = np.array(tile_m1[j][k][m*col_tiling[1] : m*col_tiling[1]+col_tiling[1]]) & (np.array(tile_m1_copy[j][k][m*col_tiling[1] : m*col_tiling[1]+col_tiling[1]]))

print("\n硬件最终结果:")
output += "\n硬件最终结果:\n"
real_result = ''
for j in range(len(result)):
    print('SRAM Addr: '+hex(j).replace('0x', ''), end="")
    output += 'SRAM Addr: '+hex(j).replace('0x', '')
    real_result += 'SRAM Addr: '+'0'*(8-len(hex(j+1).replace('0x', '')))+hex(j+1).replace('0x', '')
    print(',Results Data: '+str(result[j])+'\n')
    output += ',Results Data: '+str(result[j])+'\n'
    real_result += ',Results Data: '+'0'*(8-len(str(result[j])))+str(result[j])+'\n'
print("所需迭代次数: " + str(i))
output += "所需迭代次数: " + str(i) + '\n'

level_vector = list()
for j in range(m1_width):
    level_vector.append(0)
level_vector[0] = 1
level_counter = 1
for i in range(4):
    temp = list()
    level_counter += 1
    t = np.array(vector_a[0])@np.array(matrix_b)
    t[t>=1] = 1
    for x in range(len(t)):
        if level_vector[x] ==0:
            if t[x]!=0:
                level_vector[x] = level_counter
    vector_a[0] = np.array(vector_a[0]) | np.array(t)
print('\n软件真实结果：')  
output +=  '\n软件真实结果：\n'
print(level_vector)
output += ''.join([str(x)+' ' for x in level_vector])

with open(os.path.dirname(__file__) + '\\result.txt', "w") as r:
    r.writelines(output)
with open(os.path.dirname(__file__) + '\\compare1.txt', "w") as c1:
    c1.writelines(real_result)