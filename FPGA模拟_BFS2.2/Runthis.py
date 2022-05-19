import os
import sys
print(sys.executable)

ret = os.system('del /F /S /Q ' +os.path.dirname(os.path.abspath(__file__))+'\\translator-1.2\\Assem-Genearator-Sample\\*.txt')
if ret == 0:
    print(ret)
else:
    print(ret)
    exit(1)

ret = os.system('del /F /S /Q ' +os.path.dirname(os.path.abspath(__file__))+'\\bincode_gener1.0\\test\\*.txt')
if ret == 0:
    print(ret)
else:
    print(ret)
    exit(1)

ret = os.system('del /F /S /Q ' +os.path.dirname(os.path.abspath(__file__))+'\\bincode_gener1.0\\*.txt')
if ret == 0:
    print(ret)
else:
    print(ret)
    exit(1)

ret = os.system('del /F /S /Q ' +os.path.dirname(os.path.abspath(__file__))+'\\*.txt')
if ret == 0:
    print(ret)
else:
    print(ret)
    exit(1)

ret = os.system(sys.executable + ' '+os.path.dirname(os.path.abspath(__file__))+'\\translator-1.2\\Assem-Genearator-Sample\\rg-gen.py')
if ret == 0:
    print(ret)
else:
    print(ret)
    exit(1)

ret = os.system('copy '+os.path.dirname(os.path.abspath(__file__))+'\\translator-1.2\\Assem-Genearator-Sample\\b_exeblock* '+ os.path.dirname(os.path.abspath(__file__))+'\\bincode_gener1.0\\test\\exeblock*')
if ret == 0:
    print(ret)
else:
    print(ret)
    exit(1)

ret =  os.system('copy '+os.path.dirname(os.path.abspath(__file__))+'\\translator-1.2\\Assem-Genearator-Sample\\assem_inst.txt '+ os.path.dirname(os.path.abspath(__file__))+'\\translator-1.2\\Assembler-Sample\\insts.txt')
if ret == 0:
    print(ret)
else:
    print(ret)
    exit(1)

ret = os.system('copy '+os.path.dirname(os.path.abspath(__file__))+'\\translator-1.2\\Assem-Genearator-Sample\\result.txt '+ os.path.dirname(os.path.abspath(__file__))+'\\bincode_gener1.0\\test\\result.txt')
if ret == 0:
    print(ret)
else:
    print(ret)
    exit(1)

ret =  os.system(sys.executable + ' '+os.path.dirname(os.path.abspath(__file__))+'\\translator-1.2\\Assembler-Sample\\translator_sample1.1.py')
if ret == 0:
    print(ret)
else:
    print(ret)
    exit(1)

ret =  os.system('copy '+os.path.dirname(os.path.abspath(__file__))+'\\translator-1.2\\Assembler-Sample\\binary_inst.txt '+ os.path.dirname(os.path.abspath(__file__))+'\\bincode_gener1.0\\test\\pe_code.txt')
if ret == 0:
    print(ret)
else:
    print(ret)
    exit(1)

ret =  os.system('copy '+os.path.dirname(os.path.abspath(__file__))+'\\translator-1.2\\Assem-Genearator-Sample\\data.txt '+ os.path.dirname(os.path.abspath(__file__))+'\\bincode_gener1.0\\test\\data.txt')
if ret == 0:
    print(ret)
else:
    print(ret)
    exit(1)

ret =  os.system(sys.executable+' '+os.path.dirname(os.path.abspath(__file__))+'\\bincode_gener1.0\\suture.py')
if ret == 0:
    print(ret)
else:
    print(ret)
    exit(1)
    
ret =  os.system('copy '+os.path.dirname(os.path.abspath(__file__))+'\\bincode_gener1.0\\code.txt '+ os.path.dirname(os.path.abspath(__file__))+'\\b_code.txt')
if ret == 0:
    print(ret)
else:
    print(ret)
    exit(1)

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

ret =  os.system('copy '+os.path.dirname(os.path.abspath(__file__))+'\\translator-1.2\\Assem-Genearator-Sample\\result.txt '+ os.path.dirname(os.path.abspath(__file__))+'\\result.txt')
if ret == 0:
    print(ret)
else:
    print(ret)
    exit(1)
ret =  os.system('copy '+os.path.dirname(os.path.abspath(__file__))+'\\bincode_gener1.0\\dram_data.txt '+ os.path.dirname(os.path.abspath(__file__))+'\\dram_data.txt')
if ret == 0:
    print(ret)
else:
    print(ret)
    exit(1)
ret =  os.system('copy '+os.path.dirname(os.path.abspath(__file__))+'\\bincode_gener1.0\\dram_data_addr.txt '+ os.path.dirname(os.path.abspath(__file__))+'\\dram_data_addr.txt')
if ret == 0:
    print(ret)
else:
    print(ret)
    exit(1)
with open(os.path.dirname(os.path.abspath(__file__))+'\\b_code.txt', 'r') as code:
    h_code = code.readlines()
o_code = list()
for x in h_code:
    if '@' in x or '//' in x:
        o_code.append(x)
    elif len(x.rstrip('\n')) == 0:
        o_code.append(x)
    else:
        temp = hex(int(x.rstrip('\n'),2))
        o_code.append('0'*(8-len(str(temp).replace('0x', '')))+str(temp).replace('0x', '')+'\n')

with open(os.path.dirname(os.path.abspath(__file__))+'\\dram_data.txt', 'r') as data:
    b_data = data.readlines()
o_data = list()
for x in b_data:
    if len(x.rstrip('\n')) == 0:
        o_data.append(x)
    else:
        temp = hex(int(x.rstrip('\n'),2))
        o_data.append('0'*(8-len(str(temp).replace('0x', '')))+str(temp).replace('0x', '')+'\n')
with open(os.path.dirname(os.path.abspath(__file__))+'\\dram_data_h.txt', 'w') as data:
    data.writelines(''.join(o_data))
    
sram_data = ''
sram_data_addr = ''
sram_addr = 0
for x in o_code:
    if '@' in x:
        sram_addr = (int(x.rstrip('\n').replace('@', ''), 16))
        continue
    if x == '\n':
        continue
    sram_data_addr += hex(sram_addr).replace('0x', '')+'\n'
    sram_data += x
    sram_addr += 1

o_code = ''.join(o_code)

with open(os.path.dirname(os.path.abspath(__file__))+'\\sram_code.txt', 'w') as output:
    output.writelines(sram_data)
with open(os.path.dirname(os.path.abspath(__file__))+'\\sram_code_addr.txt', 'w') as output:
    output.writelines(sram_data_addr)    
    
if len(warning) != 0:
    print('🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺\n'+''.join(warning)+'\n🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺\n')
