import os
import sys
import time

def file_name(file_dir):

    fileList = []

    for root, dirs, files in os.walk(file_dir):

        for file in files:

            if os.path.splitext(file)[1] == '.txt': # os.path.splitext()函数将路径拆分为文件名+扩展名

                fileList.append(os.path.join(root, file))

    return fileList

#获取pe代码
def get_code(filename):
    fcode = open(filename, 'r')
    code = list()
    try:
        code = fcode.readlines()
    finally:
        fcode.close()
    
    addr_list = list()
    code2d = list()
    temp = list()
    for x in code:
        if '//' in x:
            addr_list.append(x)
            if len(temp)!=0:
                code2d.append(temp)
            temp = list()
            
        else:
            temp.append(x)
    code2d.append(temp)
    
    re_code2d = list()
    for k in code2d:
        re_code = list()
        for i in range(0, len(k)-1, 2):
            re_code.append(k[i+1].replace('', ''))
            re_code.append(k[i].replace('', ''))
        re_code2d.append(re_code)
    return re_code2d, addr_list

#获取data数据
def get_data(filename):
    fdata = open(filename, 'r')
    data = list()
    try:
        data = fdata.readlines()
    finally:
        fdata.close()
    
    addr_list = list()
    data_2d = list()
    temp = list()
    for x in data:
        if '//' in x:
            addr_list.append(x)
            if len(temp)!=0:
                data_2d.append(temp)
            temp = list()
            
        else:
            temp.append(x)
    data_2d.append(temp)
    re_data_2d = list()
    #data[-1] += '\n'
    for k in data_2d:
        re_data = list()
        while(len(k) % 4 != 0):
            k.append('0'*32+'\n')
            
        for i in range(0, len(k)-3, 4):
            re_data.append(k[i])
            re_data.append(k[i+1])
            re_data.append(k[i+2])
            re_data.append(k[i+3])  
        re_data_2d.append(re_data)
    return re_data_2d, addr_list

#获取配置信息
def get_config(filename):
    fconf = open(filename, 'r')
    conf = list()
    
    try:
        conf = fconf.readlines()
    finally:
        fconf.close()
         
    return [x for x in conf]

def get_data_copy_func():
    data_copy_fun = ('#---------------------------------------\n',
                    '# data数据专用搬运函数，调用参数：\n',
                    '# a0: 源首地址\n',
                    '# a1: 源末地址\n',
                    '# a2: 目首地址\n',
                    'datacopy:\n',
                    '	mv t0, a0     # 当前读地址\n',
                    '    mv t1, a2     # 当前写地址\n',
                    'datacopyloop:\n',
                    '    blt a1, t0, datacopyreturn   # 若读地址越界，跳转\n',
                    '    lw t2, 0(t0)\n',
                    '    sw t2, 0(t1)\n',                                  
                    '    addi t0, t0, 4\n',
                    '    addi t1, t1, 4\n',
                    '    j datacopyloop\n',
                    'datacopyreturn:\n',
                    '	ret\n',
                    '\n',
                    '#---------------------------------\n')
    return ''.join(data_copy_fun)


def get_copy_func():
    copy_fun = ('#---------------------------------------\n',
                '# 搬运函数，调用参数：\n',
                '# a0: 源首地址\n',
                '# a1: 源末地址\n',
                '# a2: 目首地址\n',
                'copy:\n',
                '	mv t0, a0     # 当前读地址\n',
                '    mv t1, a2     # 当前写地址\n',
                'copyloop:\n',
                '    blt a1, t0, copyreturn   # 若读地址越界，跳转\n',
                '    lw t2, 0(t0)\n',
                '    sw t2, 0(t1)\n',
                '    addi t0, t0, 4\n',
                '    addi t1, t1, 4\n',
                '    j copyloop\n',
                'copyreturn:\n',
                '	ret\n',
                '\n',
                '#---------------------------------\n')
    return ''.join(copy_fun)
#主函数
def main():
    warning = ''
    filelist = file_name(os.path.dirname(os.path.abspath(__file__))+'\\test\\')
    pe_code_start_pos = '00001000'
    pe_code_start_pos = int(pe_code_start_pos, 16)
    #config_start_pos = '0000112C'
    #data_start_pos = ''
    pe_code_base_dir = 'F0000000'
    pe_code_base_dir = int(pe_code_base_dir, 16)
    data_dir_base_addr = 'F0000000'
    data_dir_base_addr = int(data_dir_base_addr, 16)
    config_dir_list = 'E4000000'
    pe_total_num = 256
    
    config_list = dict()
    for name in filelist:
        if 'pe' in name:
            pe_code_list, code_addr_list = get_code(name)
        elif 'exe' in name:
            pe_num = int(name[-7:-6])
            if pe_num not in config_list:
                config_list[pe_num] = list()
                config_list[pe_num].append(get_config(name))
            else:
                config_list[pe_num].append(get_config(name))
        elif 'data' in name:
            data_list, data_addr_list = get_data(name)

    #指令copy
    pe_code_copy_total = ''
    pe_code_start_pos_t = pe_code_start_pos
    for i in range(len(pe_code_list)):
        pe_code_dir = pe_code_base_dir + int(code_addr_list[i].replace('//', ''))
        pe_code_copy = ('    li a0, '+hex(pe_code_start_pos_t)+'\n',
                        '    li a1, '+hex(pe_code_start_pos_t+len(pe_code_list[i])*4)+'\n',
                        '    li a2, '+hex(pe_code_dir)+'\n',
                        '    jal datacopy\n')
        pe_code_copy_total += ''.join(pe_code_copy)
        pe_code_start_pos_t += len(pe_code_list[i])*4
    #配置信息copy
    config_start_pos = pe_code_start_pos_t
    config_start_pos_list = dict()
    config_copy_list = []
    for i in range(pe_total_num):
        if i in config_list:
            for x in config_list[i]:
                if len(x)!=0:                   
                    temp = ('    li a0, '+(hex(config_start_pos))+'\n',
                            '    li a1, '+hex((len(x)-1)*4 + int(config_start_pos))+'\n',
                            '    li a2, 0x'+config_dir_list+'\n',
                            '    jal copy\n')
                    config_copy_list.append(temp)
                    if i not in config_start_pos_list:
                        config_start_pos_list[i] = list()
                        config_start_pos_list[i].append(config_start_pos)
                    else:
                        config_start_pos_list[i].append(config_start_pos)
                    config_start_pos = (config_start_pos+len(x)*4 + 4)
    
    PE_num = len(config_list)
    exeblock_per_pe = int(len(config_copy_list)/PE_num)

    re_config_copy_list = list()
    for i in range(PE_num):
        for j in range(exeblock_per_pe):
            re_config_copy_list.append(config_copy_list[(PE_num-i-1)*(exeblock_per_pe)+j])
    config_copy_list = re_config_copy_list
    #config_copy_list.reverse()
    
    data_start_pos = config_start_pos + 4
    #data数据copy
    data_copy_total = ''
    data_start_pos_t = data_start_pos
    for i in range(len(data_list)):
        data_dir = data_dir_base_addr + int(data_addr_list[i].replace('//', ''))
        data_copy = ('    li a0, '+hex(data_start_pos_t)+'\n',
                     '    li a1, '+hex(data_start_pos_t+len(data_list[i])*4)+'\n',
                     '    li a2, '+hex(data_dir)+'\n',
                     '    jal datacopy\n')  
        data_start_pos_t += len(data_list[i])*4
        if data_start_pos_t / 4 >= 8192:
            warning = 'warning: addr out of sram range(on host), this may cause error!'
        data_copy_total += ''.join(data_copy)
    #缝合，但riscv程序目前还未缝上
    total = ''
    total += '@' + str(hex(int(pe_code_start_pos/4)).replace('0x', ''))
    total += '\n'
    count = 0
    for x in pe_code_list:
        total += '//exeblock'+str(count)+'\n'
        total += ''.join(x)
        count += 1
    total += '\n'

    for i in range(pe_total_num):
        if i in config_start_pos_list:
            for k in range(len(config_start_pos_list[i])):
    
                total += '@' + str(hex(int(config_start_pos_list[i][k]/4)).replace('0x', ''))
                total += '\n'
                total += ''.join(config_list[i][k])
                total += '\n\n'
    
    total += '@' + str(hex(int(data_start_pos/4)).replace('0x', ''))
    total += '\n'
    count = 0
    for x in data_list:
        total += '//data for pe'+str(count)+'\n'
        total += ''.join(x)
        count += 1
    #print(total)
    
    #缝合riscv汇编
    riscv_code = ''
    riscv_code += '.globl __start\n'
    riscv_code += '.text\n'    
    riscv_code += '__start:\n'     
    riscv_code += ''.join(pe_code_copy_total)
    riscv_code += ''.join(data_copy_total)
    switch2node = ('li a0, 0x10000000\n',
                   'li a1, 1\n',
                   'sw a1, 0(a0)\n'
                    )
    riscv_code += ''.join(switch2node)
    for x in config_copy_list:
        riscv_code += ''.join(x)
    
    riscv_die = ('li a0, 0xf\n',
                'li a1, 0\n',
                'sw a1, 0(a0)\n')
    riscv_code += ''.join(riscv_die)
    
    riscv_code += '\n\n'
    riscv_code += get_copy_func()
    riscv_code += get_data_copy_func()        
    
    half_code_output = open(os.path.dirname(os.path.abspath(__file__))+'\\half_code.txt', 'w')
    riscv_code_output = open(os.path.dirname(os.path.abspath(__file__))+'\\riscv_code.s', 'w')
    try:
        half_code_output.writelines(total)
        riscv_code_output.writelines(riscv_code)
    finally:
        half_code_output.close()
        riscv_code_output.close()
    
    #print(os.path.dirname(os.path.abspath(__file__))+'\\jupiter\\bin\\jupiter '+os.path.dirname(os.path.abspath(__file__))+'\\riscv_code.s --dump-code '+ os.path.dirname(os.path.abspath(__file__))+'\\hex_riscv_code.txt')
    #产生二进制riscv汇编
    #print(os.getcwd())
    with os.popen(os.path.dirname(os.path.abspath(__file__))+'\\jupiter\\bin\\jupiter '+os.path.dirname(os.path.abspath(__file__))+'\\riscv_code.s --dump-code '+ os.path.dirname(os.path.abspath(__file__))+'\\hex_riscv_code.txt') as ret:
        print(ret)

    #hex2bin
    with open(os.path.dirname(os.path.abspath(__file__))+'\\hex_riscv_code.txt', 'r') as h:
        hex_code = h.readlines()
    bin_code = [str(bin(int(x.replace('\n', ''),16))).replace('0b', '') for x in hex_code]
    bin_code = ['0'*(32-len(x))+x+'\n' for x in bin_code]
    
    code = ''.join(bin_code) + '\n' + total
    
    with open(os.path.dirname(os.path.abspath(__file__))+'\\code.txt', 'w') as output:
        output.writelines(code)
    
    if len(warning) != 0:
        print(warning)
        with open(os.path.dirname(os.path.abspath(__file__))+'\\warning.txt', 'w') as w:
            w.writelines(warning)
    # with open(os.path.dirname(os.path.abspath(__file__))+'\\test\\result.txt', 'r') as result:
    #     re_num = result.readlines()
    # output_addr = list()
    # for i in range(len(re_num)):
    #     output_addr.append(str(hex(int(data_addr_list[-1].rstrip('\n').lstrip('//'))+i).replace('0x', ''))+'\n')
    # with open(os.path.dirname(os.path.abspath(__file__))+'\\ST_ADDR.txt', 'w') as SA:
    #     SA.writelines(output_addr)
    
if __name__ == "__main__":
    main()
