# coding:utf-8
import os
import json
import re

with open(os.path.dirname(os.path.abspath(__file__))+'/vec_ind_example.txt', 'r') as vec_ind_input:
    vec_inds = vec_ind_input.readlines()

vec_inds = [v_i.rstrip('\n') for v_i in vec_inds]

dirlist = os.listdir(os.path.dirname(os.path.abspath(__file__))+'/../TILE/')

for tile in dirlist:
    tile_file_name = os.path.dirname(os.path.abspath(__file__))+'/../TILE/'+tile

    with open(tile_file_name+'/dram_data_temp.txt', 'r') as dram_data_input:
        dram_data_list = dram_data_input.readlines()        

    with open(tile_file_name+'/dram_data.txt', 'w') as dram_data_output:
        for dram_data in dram_data_list:
            if 'vec' in dram_data:
                if dram_data.rstrip('\n').replace("vec", "") in vec_inds:
                    dram_data_output.write('1\n')
                else:
                    dram_data_output.write('0\n')
            else:
                dram_data_output.write(dram_data)

with open(os.path.dirname(os.path.abspath(__file__))+'/iter_limit_example.txt', 'r') as iter_limit_input:
    iter_limit = iter_limit_input.readlines()
iter_limit[-1] = iter_limit[-1].strip('\n') + '\n'

with open(os.path.dirname(os.path.abspath(__file__))+'/../riscv_code_addr.txt', 'r') as addr_file:
    addr = addr_file.readlines()
with open(os.path.dirname(os.path.abspath(__file__))+'/../riscv_code.txt', 'r') as code_file:
    code = code_file.readlines()

index = -1
if '4C0\n' in addr and iter_limit != code[-1]:
    index = addr.index('4C0\n')
    code[index] = iter_limit[0]
 
    with open(os.path.dirname(os.path.abspath(__file__))+'/../riscv_code.txt', 'w') as code_file:
        code_file.writelines(code)
elif '4C0\n' in addr and iter_limit == code[-1]:
    index = addr.index('4C0\n')
else:
    addr.append('4C0\n')
    # index = addr.index('4C0\n')
    index = len(addr)-1
    print(index)
    print(addr[index])
    with open(os.path.dirname(os.path.abspath(__file__))+'/../riscv_code_addr.txt', 'w') as addr_file:
        addr_file.writelines(addr)

    code += iter_limit
    with open(os.path.dirname(os.path.abspath(__file__))+'/../riscv_code.txt', 'w') as code_file:
        code_file.writelines(code)



with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..') + '/pe_module.json', "r") as f:
    res = json.load(f)
    width = res['1']['m1_width']
    height2 = res['1']['m2_height']
    width2 = res['1']['m2_width']

vec_list = []
vec_addr = []
vec_temp_base = int('800', 16)
vec_base = int('C00', 16)
for i in range(width):
    if str(i) in vec_inds:
        vec_list.append('1\n')
        vec_list.append('1\n')
    else:
        vec_list.append('0\n')
        vec_list.append('0\n')
    vec_addr.append(hex(vec_base).replace('0x', '')+'\n')
    vec_addr.append(hex(vec_temp_base).replace('0x', '')+'\n')
    vec_temp_base += 1
    vec_base += 1

code[index+1:] = []
addr[index+1:] = []
for item in reversed(vec_list):
    code.insert(index+1, item)
for item in reversed(vec_addr):
    addr.insert(index+1, item)
with open(os.path.dirname(os.path.abspath(__file__))+'/../riscv_code_addr.txt', 'w') as addr_file:
    addr_file.writelines(addr)

with open(os.path.dirname(os.path.abspath(__file__))+'/../riscv_code.txt', 'w') as code_file:
    code_file.writelines(code)

with open(os.path.dirname(os.path.abspath(__file__))+'/../inform.txt', 'r') as inform_input:
    inform = inform_input.readlines()
inform[-1] = str(len(code))+'\n'
with open(os.path.dirname(os.path.abspath(__file__))+'/../inform.txt', 'w') as inform_output:
    inform_output.writelines(inform)