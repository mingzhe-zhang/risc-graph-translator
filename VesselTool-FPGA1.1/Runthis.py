import os
import sys

print(sys.executable)

ret = os.system('del /F /S /Q ' +os.path.dirname(os.path.abspath(__file__))+'\\translator-1.2\\Assem-Generator-Sample\\*.txt')
if ret == 0:
    print(ret)
else:
    print(ret)
    #exit(1)

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

ret = os.system(sys.executable + ' '+os.path.dirname(os.path.abspath(__file__))+'\\translator-1.2\\Assem-Generator-Sample\\rg-gen.py')
if ret == 0:
    print(ret)
else:
    print(ret)
    exit(1)

ret = os.system('copy '+os.path.dirname(os.path.abspath(__file__))+'\\translator-1.2\\Assem-Generator-Sample\\b_exeblock* '+ os.path.dirname(os.path.abspath(__file__))+'\\bincode_gener1.0\\test\\exeblock*')
if ret == 0:
    print(ret)
else:
    print(ret)
    exit(1)

ret =  os.system('copy '+os.path.dirname(os.path.abspath(__file__))+'\\translator-1.2\\Assem-Generator-Sample\\assem_inst.txt '+ os.path.dirname(os.path.abspath(__file__))+'\\translator-1.2\\Assembler-Sample\\insts.txt')
if ret == 0:
    print(ret)
else:
    print(ret)
    exit(1)

ret = os.system('copy '+os.path.dirname(os.path.abspath(__file__))+'\\translator-1.2\\Assem-Generator-Sample\\result.txt '+ os.path.dirname(os.path.abspath(__file__))+'\\bincode_gener1.0\\test\\result.txt')
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

ret =  os.system('copy '+os.path.dirname(os.path.abspath(__file__))+'\\translator-1.2\\Assem-Generator-Sample\\data.txt '+ os.path.dirname(os.path.abspath(__file__))+'\\bincode_gener1.0\\test\\data.txt')
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

ret =  os.system('copy '+os.path.dirname(os.path.abspath(__file__))+'\\translator-1.2\\Assem-Generator-Sample\\result.txt '+ os.path.dirname(os.path.abspath(__file__))+'\\result.txt')
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

o_code = ''.join(o_code)

with open(os.path.dirname(os.path.abspath(__file__))+'\\code.txt', 'w') as output:
    output.writelines(o_code)
    
if len(warning) != 0:
    print('🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺\n'+''.join(warning)+'\n🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺\n')
