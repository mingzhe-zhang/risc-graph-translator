# coding:utf-8
import os
import sys
import shutil
print(sys.executable)

if os.path.exists(os.path.dirname(os.path.abspath(__file__))+'\\translator-1.2\\Assem-Genearator-Sample\\rg_gen')==1:
    ret = shutil.rmtree(os.path.dirname(os.path.abspath(__file__))+'\\translator-1.2\\Assem-Genearator-Sample\\rg_gen')
    if ret == None:
        print(ret)
    else:
        print(ret)
        exit(1)

if os.path.exists(os.path.dirname(os.path.abspath(__file__))+'\\bincode_gener1.0\\test\\rg_gen')==1:
    ret = shutil.rmtree(os.path.dirname(os.path.abspath(__file__))+'\\bincode_gener1.0\\test\\rg_gen')
    if ret == None:
        print(ret)
    else:
        print(ret)
        exit(1)

if os.path.exists(os.path.dirname(os.path.abspath(__file__))+'\\bincode_gener1.0\\structure_gen')==1:
    ret = shutil.rmtree(os.path.dirname(os.path.abspath(__file__))+'\\bincode_gener1.0\\structure_gen')
    if ret == None:
        print(ret)
    else:
        print(ret)
        exit(1)        

if os.path.exists(os.path.dirname(os.path.abspath(__file__))+'\\translator-1.2\\Assembler-Sample\\rg_gen')==1:
    ret = shutil.rmtree(os.path.dirname(os.path.abspath(__file__))+'\\translator-1.2\\Assembler-Sample\\rg_gen')
    if ret == None:
        print(ret)
    else:
        print(ret)
        exit(1)

# ret = os.system('del /F /S /Q ' +os.path.dirname(os.path.abspath(__file__))+'\\bincode_gener1.0\\*')
# if ret == 0:
#     print(ret)
# else:
#     print(ret)
#     exit(1)

# ret = os.system('del /F /S /Q ' +os.path.dirname(os.path.abspath(__file__))+'\\*.txt')
# if ret == 0:
#     print(ret)
# else:
#     print(ret)
#     exit(1)

ret = os.system(sys.executable + ' '+os.path.dirname(os.path.abspath(__file__))+'\\translator-1.2\\Assem-Genearator-Sample\\rg-gen.py')
if ret == 0:
    print(ret)
else:
    print(ret)
    exit(1)



ret = shutil.copytree(os.path.dirname(os.path.abspath(__file__))+'\\translator-1.2\\Assem-Genearator-Sample\\rg_gen', os.path.dirname(os.path.abspath(__file__))+'\\translator-1.2\\Assembler-Sample\\rg_gen')


# ret = os.system('copy '+os.path.dirname(os.path.abspath(__file__))+'\\translator-1.2\\Assem-Genearator-Sample\\result.txt '+ os.path.dirname(os.path.abspath(__file__))+'\\bincode_gener1.0\\test\\result.txt')
# if ret == 0:
#     print(ret)
# else:
#     print(ret)
#     exit(1)

ret =  os.system(sys.executable + ' '+os.path.dirname(os.path.abspath(__file__))+'\\translator-1.2\\Assembler-Sample\\translator_sample1.1.py')
if ret == 0:
    print(ret)
else:
    print(ret)
    exit(1)

ret = shutil.copytree(os.path.dirname(os.path.abspath(__file__))+'\\translator-1.2\\Assembler-Sample\\rg_gen', os.path.dirname(os.path.abspath(__file__))+'\\bincode_gener1.0\\test\\rg_gen')


if os.path.exists(os.path.dirname(os.path.abspath(__file__))+'\\bincode_gener1.0\\test\\rg_gen') == 0:
    ret = shutil.copytree(os.path.dirname(os.path.abspath(__file__))+'\\translator-1.2\\Assembler-Sample\\rg_gen', os.path.dirname(os.path.abspath(__file__))+'\\bincode_gener1.0\\test\\rg_gen')


# ret =  os.system('copy '+os.path.dirname(os.path.abspath(__file__))+'\\translator-1.2\\Assem-Genearator-Sample\\data.txt '+ os.path.dirname(os.path.abspath(__file__))+'\\bincode_gener1.0\\test\\data.txt')
# if ret == 0:
#     print(ret)
# else:
#     print(ret)
#     exit(1)

ret =  os.system(sys.executable+' '+os.path.dirname(os.path.abspath(__file__))+'\\bincode_gener1.0\\suture.py')
if ret == 0:
    print(ret)
else:
    print(ret)
    exit(1)
    
# ret =  os.system('copy '+os.path.dirname(os.path.abspath(__file__))+'\\bincode_gener1.0\\code.txt '+ os.path.dirname(os.path.abspath(__file__))+'\\b_code.txt')
# if ret == 0:
#     print(ret)
# else:
#     print(ret)
#     exit(1)

warning = list()
if os.path.exists(os.path.dirname(os.path.abspath(__file__))+'\\bincode_gener1.0\\warning.txt'):
    with open(os.path.dirname(os.path.abspath(__file__))+'\\bincode_gener1.0\\warning.txt', 'r') as w:
        warning = w.readlines()

# ret =  os.system('copy '+os.path.dirname(os.path.abspath(__file__))+'\\bincode_gener1.0\\ST_ADDR.txt '+ os.path.dirname(os.path.abspath(__file__))+'\\ST_ADDR.txt')
# if ret == 0:
#     print(ret)
# else:
#     print(ret)
#     exit(1)

# ret =  os.system('copy '+os.path.dirname(os.path.abspath(__file__))+'\\translator-1.2\\Assem-Genearator-Sample\\result.txt '+ os.path.dirname(os.path.abspath(__file__))+'\\result.txt')
# if ret == 0:
#     print(ret)
# else:
#     print(ret)
#     exit(1)
dirlist = os.listdir(os.path.dirname(os.path.abspath(__file__))+'\\bincode_gener1.0\\structure_gen')

dirname = (os.path.dirname(os.path.abspath(__file__))+'\\bincode_gener1.0\\structure_gen\\tile0')
with open(dirname+'\\code.txt', 'r') as code:
    h_code = code.readlines()
    
if os.path.exists(os.path.dirname(os.path.abspath(__file__))+'\\irqprog.bin')==0:    
    with os.popen(os.path.dirname(os.path.abspath(__file__))+'\\bincode_gener1.0\\jupiter\\bin\\jupiter '+os.path.dirname(os.path.abspath(__file__))+'\\irqprog.s --dump-code '+ os.path.dirname(os.path.abspath(__file__))+'\\irqprog.bin') as ret:
        print(ret)    
with open(os.path.dirname(os.path.abspath(__file__))+'\\irqprog.bin', 'r') as irq_hex:
    irq_h = irq_hex.readlines()    
    
o_code = list()

for x in h_code:
    if '@' in x or '//' in x:
        o_code.append(x)
    elif x == '\n':
        continue
    else:
        temp = hex(int(x.rstrip('\n'),2))
        o_code.append('0'*(8-len(str(temp).replace('0x', '')))+str(temp).replace('0x', '')+'\n')

#o_code = ''.join(o_code)
o_code += ['\n@480\n']

o_code += [x.replace('0x', '') for x in irq_h]

#print(o_code)
# with open(dirname+'\\h_code.txt', 'w') as output:
#     output.writelines(o_code)
sram_data = ''
sram_data_addr = ''
sram_addr = 0
irq_code = ['0601e00b\n', '0800400B\n', '0601e00b\n','0601e00b\n', '0800400B\n', '0601e00b\n', '0400000B\n']
count = 0
for x in o_code:
    if x == '\n':
        continue
    if x == '':
        continue
    if '@480' in x:
        sram_addr = (int(x.rstrip('\n').replace('@', ''), 16))
        
        continue
    if '@' in x and '@480' not in x:
        sram_addr = (int(x.rstrip('\n').replace('@', ''), 16))
        continue
    if '00000013' in x and (count < 5 or sram_addr >= 1152):
        sram_data_addr += hex(sram_addr).replace('0x', '')+'\n'
        sram_data += irq_code[count]
        sram_addr += 1
        count += 1
       
        continue
    if sram_addr < 768 or sram_addr >= 1152:
        sram_data_addr += hex(sram_addr).replace('0x', '')+'\n'
        sram_data += x
        sram_addr += 1
    
sram_data += '0\n'
sram_data_addr += '4C2\n'     

with open(os.path.dirname(os.path.abspath(__file__))+'\\riscv_code.txt', 'w') as output:
    output.writelines(sram_data)
with open(os.path.dirname(os.path.abspath(__file__))+'\\riscv_code_addr.txt', 'w') as output:
    output.writelines(sram_data_addr)    

infor = ''
for i in dirlist:
    
        
    dirname = (os.path.dirname(os.path.abspath(__file__))+'\\bincode_gener1.0\\structure_gen\\'+i)
    with open(dirname+'\\code.txt', 'r') as code:
        h_code = code.readlines()
    o_code = list()
    
    for x in h_code:
        if '@' in x or '//' in x:
            o_code.append(x)
        elif x == '\n':
            continue
        else:
            temp = hex(int(x.rstrip('\n'),2))
            o_code.append('0'*(8-len(str(temp).replace('0x', '')))+str(temp).replace('0x', '')+'\n')

    #o_code = ''.join(o_code)
    
    # with open(dirname+'\\h_code.txt', 'w') as output:
    #     output.writelines(o_code)
    sram_data = ''
    sram_data_addr = ''
    sram_addr = 0
    for x in o_code:
        if x == '\n':
            continue
        if x == '':
            continue
        if '@' in x:
            sram_addr = (int(x.rstrip('\n').replace('@', ''), 16))
            continue
        if sram_addr != 0:
            sram_data_addr += hex(sram_addr).replace('0x', '')+'\n'
            sram_data += x
            sram_addr += 1
    sram_data += '0\n'
    sram_data_addr += '4C2\n'        
    if  os.path.exists(os.path.dirname(os.path.abspath(__file__))+'\\'+i)==0:
        os.mkdir(os.path.dirname(os.path.abspath(__file__))+'\\'+i)
    with open(os.path.dirname(os.path.abspath(__file__))+'\\'+i+'\\sram_code.txt', 'w') as output:
        output.writelines(sram_data)
    with open(os.path.dirname(os.path.abspath(__file__))+'\\'+i+'\\sram_code_addr.txt', 'w') as output:
        output.writelines(sram_data_addr)    
      
    
    ret = os.system('copy ' +os.path.dirname(os.path.abspath(__file__))+'\\bincode_gener1.0\\structure_gen\\'+i+'\\dram_data_addr.txt '+os.path.dirname(os.path.abspath(__file__))+'\\'+i+'\\dram_data_addr.txt')    
    if ret == 0:
        print(ret)
    else:
        print(ret)
        exit(1)  
        
    with open(os.path.dirname(os.path.abspath(__file__))+'\\bincode_gener1.0\\structure_gen\\'+i+'\\dram_data.txt', 'r') as data:
        b_data = data.readlines()
    o_data = list()
    for x in b_data:
        if len(x.rstrip('\n')) == 0:
            o_data.append(x)
        else:
            temp = hex(int(x.rstrip('\n'),2))
            o_data.append('0'*(8-len(str(temp).replace('0x', '')))+str(temp).replace('0x', '')+'\n')
    with open(os.path.dirname(os.path.abspath(__file__))+'\\'+i+'\\dram_data.txt', 'w') as data:
        data.writelines(''.join(o_data))
    with open(os.path.dirname(os.path.abspath(__file__))+'\\'+i+'\\dram_data.txt', 'r') as data:
        x = data.readlines()
        infor += str(len(x))+'\n'
        infor += '325\n'

with open(os.path.dirname(os.path.abspath(__file__))+'\\riscv_code.txt', 'r') as data:
    x = data.readlines()
    infor += str(len(x))+'\n'

with open(os.path.dirname(os.path.abspath(__file__))+'\\inform.txt', 'w') as data:
    data.writelines(infor)
        

if len(warning) != 0:
    print('🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺\n'+''.join(warning)+'\n🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺\n')
