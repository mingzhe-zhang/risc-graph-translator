import json
import os
import re
import numpy as np
import operator
import random

with open(os.path.dirname(__file__) + '\\pe_module_input.json', "r") as f:
    res = json.load(f)
expression = res['Expression']
op = re.findall(r"[A-z]", expression)
op1 = []
data1 = list()
data2 = list()
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
    #print(reload_num)
    node_num = res[str(i+1)]['node']
    is_random = res[str(i+1)]['is_random']
    sparse_degree = res[str(i+1)]['sparse_degree']
    sparse_degree_max = res[str(i+1)]['sparse_degree_max']
    
    if col_tiling[1] % col_tiling[0] != 0:
        print("Error: 分配给pe的列不均匀!\n")
        exit(1)
    if int(col_tiling[1]/col_tiling[0])%exeblock_per_PE!= 0:
        print("Error: 分配给exeblock的数据不均匀!\n")
        exit(1)
    if PE_num % col_tiling[0]!=0:
        print("Error: 分配给一个分块的pe数目不均匀!\n")
        exit(1)
    if node_num > 1:
        print("Error: 当前FPGA版本仅限一个node工作!\n")
        exit(1)
    
    res[str(i+1)][op[0]] = '['
    for j in range(m1_width):
        if j ==0:
            res[str(i+1)][op[0]] += '1,'
            data1.append(1)
        else:
            res[str(i+1)][op[0]] += '0,'
            data1.append(0)
    res[str(i+1)][op[0]] = res[str(i+1)][op[0]].rstrip(',')
    res[str(i+1)][op[0]] += ']'
    
    res[str(i+1)][op[1]] = '['
    for j in range(m2_height):
        res[str(i+1)][op[1]] += '['
        temp = list()
        for k in range(m2_width):
            if is_random==0:
                if j*12 <= k-1 and j*12 >= k-12 and j==0:
                    res[str(i+1)][op[1]] += '1,'
                    temp.append(1)
                elif (j) <= k-1 and (j) >= k-12 and j == 12:
                    res[str(i+1)][op[1]] += '1,'  
                    temp.append(1)
                elif j <= k-1 and j >= k-12 and j == 24:
                    res[str(i+1)][op[1]] += '1,'  
                    temp.append(1)
                elif j <= k-1 and j >= k-12 and j == 36:
                    res[str(i+1)][op[1]] += '1,'  
                    temp.append(1)
                elif j <= k-1 and j >= k-12 and j == 48:
                    res[str(i+1)][op[1]] += '1,'  
                    temp.append(1)
                elif j <= k-1 and j >= k-12 and j == 60:
                    res[str(i+1)][op[1]] += '1,'  
                    temp.append(1)
                else:
                    res[str(i+1)][op[1]] += '0,'
                    temp.append(0)
            else:
                a = random.randint(0, int(sparse_degree_max/sparse_degree))
                if a%int(sparse_degree_max/sparse_degree)==0:
                    a = 1
                else:
                    a = 0
                res[str(i+1)][op[1]] += str(a)+','
                if a == 0:
                    temp.append(0)
                else:
                    temp.append(1)
                
        res[str(i+1)][op[1]] = res[str(i+1)][op[1]].rstrip(',')        
        res[str(i+1)][op[1]] += '], '
        data2.append(temp)
    res[str(i+1)][op[1]] = res[str(i+1)][op[1]].rstrip(', ')         
    res[str(i+1)][op[1]] += ']'
#print(res[str(i+1)][op[1]])

# for i in range(4):
#     if i < 2:
#         print([x[i*16:(i+1)*16] for x in data2[0:32]])
#         print()
#     else:
#         print([x[i*16:(i+1)*16] for x in data2[32:64]])
#         print()
tile_m1 = list()
tile_m2 = list()
counter = 0
for i in range(reload_num*reload_num):
    tile_m1_array = list()
    tile_m2_array = list()
    for j in range(int(PE_num/col_tiling[0])):
        tile_m1_array.append((data1[int(i/reload_num)*col_per_node : int(i/reload_num+1)*col_per_node]))
        if (i+j) % reload_num != 0 or j != 0:
            tile_m2_array.append(([x[counter%(int(PE_num/col_tiling[0])*reload_num)*col_tiling[1] : (counter%(int(PE_num/col_tiling[0])*reload_num))*col_tiling[1]+col_tiling[1]] for x in data2[int(i/reload_num)*col_per_node : int(i/reload_num+1)*col_per_node]]))
            
        else:
            tile_m2_array.append(([x[0 : col_tiling[1]] for x in data2[int(i/reload_num)*col_per_node : int(i/reload_num+1)*col_per_node]]))
        #print((counter%(int(PE_num/col_tiling[0])*reload_num))*col_tiling[1]+col_tiling[1])    
        #print(int(i/reload_num)*col_per_node)
        counter += 1
    tile_m1.append(tile_m1_array)
    tile_m2.append(tile_m2_array)    


# result = list()
# result.append(1)
# for i in range(m1_width-1):
#     result.append(0)
# result_temp = result.copy()
# level_counter = 1

# i = 0
# while(1):
#     temp = list()
#     level_counter += 1
#     print('\n'+str(i)+' time round')
#     for j in range(reload_num*reload_num):
#         for k in range(int(PE_num/col_tiling[0])):
#             #print(tile_m2[j][k])
#             t = np.array(tile_m1[j][k])@np.array(tile_m2[j][k])
#             t[t>=1]= 1
#             temp.append(t)
#             print('node'+str(int(j%reload_num))+',pe'+str(col_tiling[0]*k+col_tiling[0]-1)+',st: ')
#             print(t)
#             for x in range(len(t)):
#                 #print(k*col_tiling[1]+int(j%reload_num)*int(m2_width/node_num)+x)
#                 if result[k*col_tiling[1]+int(j%reload_num)*int(m2_width/node_num)+x]==0:
#                     if t[x] != 0:
#                         result[k*col_tiling[1]+int(j%reload_num)*int(m2_width/node_num)+x] = level_counter
#     if operator.eq(result_temp, result):
#         break
#     else:
#         result_temp = result.copy()
#         i += 1

    
    # for j in range(reload_num*reload_num):
    #     for k in range(int(PE_num/col_tiling[0])):
    #         for m in range(int(PE_num/col_tiling[0])):
    #             #print(int(j/reload_num)*int(PE_num/col_tiling[0])+m)
    #             tile_m1[j][k][m*col_tiling[1] : m*col_tiling[1]+col_tiling[1]] = np.array(tile_m1[j][k][m*col_tiling[1] : m*col_tiling[1]+col_tiling[1]]) | np.array(temp[int(j/reload_num)*int(PE_num/col_tiling[0])+m]) | np.array(temp[int(j/reload_num)*int(PE_num/col_tiling[0])+int(PE_num/col_tiling[0])*reload_num+m])

# print("最终结果:")
# print(result)
#print("所需迭代次数: " + str(i))
with open(os.path.dirname(__file__) + '\\pe_module.json', "w") as f:
    json.dump(res, f)

