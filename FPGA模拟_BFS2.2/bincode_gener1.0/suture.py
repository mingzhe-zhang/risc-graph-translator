import os
import sys
import time
import json

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
        while(len(k) % 4 != 0):
            k.append('0'*32+'\n')
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
                    
                    '    lw t2, 0x4(t0)\n',
                    '    sw t2, 0(t1)\n',
                    
                    '    lw t2, 0x8(t0)\n',
                    '    sw t2, 0(t1)\n',
                    
                    '    lw t2, 0xC(t0)\n',
                    '    sw t2, 0(t1)\n',
                    
                    '    addi t0, t0, 16\n',
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

def get_cfg_config(filename):
    cfg_config_file = open(os.path.dirname(os.path.abspath(__file__)) + "\\..\\" + filename, 'r')
    cfg_config = list()
    try:
        cfg_config = cfg_config_file.readlines()
    finally:
        cfg_config_file.close()
    return cfg_config



def get_wait_result_code(ST_addr_start, ST_addr_end, vector_addr_start, width, PE_num, tiling, height2, exeblock_per_pe, data_list, Label_no):
    code = ('#---------------------------------------\n',
            '# 等待结果：\n',
            '# t1: 结果dram首地址\n',
            '# t3: 结果sram首地址\n'
            'wait'+Label_no+':\n',
            '    li t1, '+hex(ST_addr_start)+'     # 当前写地址\n',
            '    li a1, '+hex(ST_addr_end)+ '    # 末地址\n',
            '    li a2, -1 \n'
            '    li t3, 0x1600 \n',
            '    li t4, 0x1800 \n',
            '    li a3, '+str(width)+'\n',
            'wait_loop'+Label_no+':\n',

            '    lw s0, 0(t1)\n',
            '    lw s1, 0(t1)\n',
            '    lw s2, 0(t1)\n',
            '    lw s3, 0(t1)\n',

            '    addi a3, a3, -1\n',
            '    beqz a3, buffer0_'+Label_no+'    \n',
            '    addi a3, a3, 1\n',
            
            '    addi a3, a3, -2\n',
            '    beqz a3, buffer1_'+Label_no+'    \n',
            '    addi a3, a3, 2\n',
            
            '    addi a3, a3, -3\n',
            '    beqz a3, buffer2_'+Label_no+'    \n',
            '    addi a3, a3, 3\n',
            
            '    addi a3, a3, -4\n',
            '    beqz a3, buffer3_'+Label_no+'    \n',
            'buffer3_'+Label_no+':    \n',
            '    lw t5, 0xc(t4) \n',
            '    snez t5, t5 \n',
            '    xori t5, t5, 1\n',
            '    and s3, s3, t5\n',
            '    sw s3, 0xc(t3)\n',

            '    beq s3, x0, buffer2_'+Label_no+' \n',
            '    sw s11, 0xc(t4)    #s11存放当前level\n',
            '    li s10, 1\n',
            
            'buffer2_'+Label_no+':    \n',
            '    lw t5, 8(t4) \n',
            '    snez t5, t5 \n',
            '    xori t5, t5, 1\n',
            '    and s2, s2, t5\n',
            '    sw s2, 8(t3)\n',

            '    beq s2, x0, buffer1_'+Label_no+' \n',
            '    sw s11, 8(t4)    #s11存放当前level\n',
            '    li s10, 1\n',

            
            'buffer1_'+Label_no+':    \n',
            '    lw t5, 4(t4) \n',
            '    snez t5, t5 \n',
            '    xori t5, t5, 1\n',
            '    and s1, s1, t5\n',
            '    sw s1, 4(t3)\n',

            '    beq s1, x0, buffer0_'+Label_no+' \n',
            '    sw s11, 4(t4)    #s11存放当前level\n',           
            '    li s10, 1\n',
            
            'buffer0_'+Label_no+':    \n',
            '    lw t5, 0(t4) \n',
            '    snez t5, t5 \n',
            '    xori t5, t5, 1\n',
            '    and s0, s0, t5\n',
            '    sw s0, 0(t3)\n',

            '    beq s0, x0, next'+Label_no+' \n',
            '    sw s11, 0(t4)    #s11存放当前level\n',
            '    li s10, 1\n',

            'next'+Label_no+':    \n',
            '    blt a1, t1, wait_return'+Label_no+'   # 若读地址越界，跳转\n',
            '    beqz a3, wait_return'+Label_no+'   # 若读取数量超出范围，跳转\n',
            '    addi t1, t1, 4\n',
            '    addi t3, t3, 16 \n',
            '    addi t4, t4, 16 \n',
            '    j wait_loop'+Label_no+'\n',
            'wait_return'+Label_no+':\n',
            '\n')
    start = 5632
    for i in range(PE_num):
        if i!= PE_num-1:
            copy = ('    li a0, '+hex(start)+'\n',
                    '    li a1, '+hex(start+tiling*exeblock_per_pe*4-4)+'\n',
                    '    li a2, '+hex(int(vector_addr_start))+'\n'
                    '    jal copy\n',
                    '#---------------------------------\n')   
            code += (copy)
            start = start+tiling*exeblock_per_pe*4
            vector_addr_start += len(data_list[i])*4
        else:
            copy = ('    li a0, '+hex(start)+'\n',
                    '    li a1, '+hex(start+(tiling+height2%tiling)*exeblock_per_pe*4-4)+'\n',
                    '    li a2, '+hex(int(vector_addr_start))+'\n'
                    '    jal copy\n',
                    '#---------------------------------\n')   
            code += (copy)
            start = start+(tiling+height2%tiling)*exeblock_per_pe*4
            vector_addr_start += len(data_list[i])*4

    return ''.join(code)

def get_set_first_level_code(width, vector_addr_start):
    code = ('#---------------------------------------\n',
            '# level过程：\n',
            '# t1: 结果sram首地址\n',
            'select:\n',
            '    li t1, 0x1800     # 当前写地址\n',
            '    li t3, '+hex(int(vector_addr_start))+'    # 当前写地址\n',
            '    li a1, '+str(width) +'     # 末地址\n',
            '    li t2, 1 \n'
            'select_loop:\n',
            '    sw t2, 0(t1)\n',
            '    sw t2, 0(t3)\n',
            '    addi t1, t1, 4\n',
            '    addi t3, t3, 4\n',
            '    addi a1, a1, -1\n',
            '    li t2, 0 \n'
            '    bnez a1, select_loop\n',
            '\n',
            '#---------------------------------\n') 
    return ''.join(code)

def get_wait_end_code(Label_no):
    code = ('#---------------------------------------\n',
            '# 等待结束过程：\n',
            '# s10: 结束标志，为0表示结束\n',
            'wait_end'+Label_no+':\n',
            '    beqz s10, quit \n',
            '    li s10, 0 \n'
            '    addi s11, s11, 1\n'
            '    j load_data \n',
            '\n',
            '\n',
            '#---------------------------------\n') 
    return ''.join(code)

def get_switch2riscv_code(ST_exeblock_no, PE_num, exeblock_per_pe, width, Label_no):
    flag = 0
    for i in range(PE_num):
        for j in range(exeblock_per_pe):
            flag <<= 1
            flag += 1
    code = ('#---------------------------------------\n',
            '# 切换mem_ctrl到riscv过程：\n',
            '# t0: 切换需要的地址\n',
            'li t0, '+hex(int('e0000000', 16)+int(ST_exeblock_no/32)*4) +'\n',
            'li t2, '+hex((int('e0000000', 16)+int(ST_exeblock_no/32)*4)|0b10000000) +'\n',
            'li a2, '+str(flag)+'\n',
            'li a3, '+str(width)+'\n',
            'wait_exe'+Label_no+':\n',
            '    lw t1, 0(t0) \n',
            '    bne t1, a2, wait_exe'+Label_no+' \n',
            'wait_st'+Label_no+':\n',
            '    lw t1, 0(t2) \n',
            '    bne t1, a3, wait_st'+Label_no+' \n',
            '    li a0, 0x10000000\n',
            '    li a1, 0\n',
            '    sw a1, 0(a0)\n'
            '\n',
            '\n',
            '#---------------------------------\n') 
    return ''.join(code)

def get_new_vector_copy(width):
    data_copy_fun = ('#---------------------------------------\n',
                    '# 后续vector数据专用搬运函数，调用参数：\n',
                    '# a0: 源首地址\n',
                    '# a1: 源末地址\n',
                    '# a2: 目首地址\n',
                    'vectorcopy:\n',
                    '	mv t0, a0     # 当前读地址\n',
                    '    mv t1, a2     # 当前写地址\n',
                    '    li a3, '+width+'\n'
                    'vectorcopyloop:\n',
                    '    blt a1, t0, vectorcopyreturn   # 若读地址越界，跳转\n',
                    '    lw t2, 0(t0)\n',
                    '    sw t2, 0(t1)\n',
                    '    addi a3, a3, -1\n',
                    '    beqz a3, vectorcopyreturn\n',
                    
                    '    lw t2, 0x4(t0)\n',
                    '    sw t2, 0(t1)\n',
                    '    addi a3, a3, -1\n',
                    '    beqz a3, vectorcopyreturn\n',
                    
                    '    lw t2, 0x8(t0)\n',
                    '    sw t2, 0(t1)\n',
                    '    addi a3, a3, -1\n',
                    '    beqz a3, vectorcopyreturn\n',
                    
                    '    lw t2, 0xC(t0)\n',
                    '    sw t2, 0(t1)\n',
                    '    addi a3, a3, -1\n',
                    '    beqz a3, vectorcopyreturn\n',
                    
                    '    addi t0, t0, 16\n',
                    '    addi t1, t1, 4\n',
                    '    j vectorcopyloop\n',
                    'vectorcopyreturn:\n',
                    '	ret\n',
                    '\n',
                    '#---------------------------------\n')
    return ''.join(data_copy_fun)

#主函数
def main():
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..') + '\\pe_module.json', "r") as f:
        res = json.load(f)
    width = res['1']['m1_width']
    height2 = res['1']['m2_height']
    width2 = res['1']['m2_width']
    
    vector_addr_start = '5632'     #后续新向量在sram中暂时存储的地址
    warning = ''
    filelist = file_name(os.path.dirname(os.path.abspath(__file__))+'\\test\\')
    pe_code_start_pos = '00000680'
    pe_code_start_pos = int(pe_code_start_pos, 16)
    #config_start_pos = '0000112C'
    #data_start_pos = ''
    pe_code_base_dir = 'F0000000'
    pe_code_base_dir = int(pe_code_base_dir, 16)
    data_dir_base_addr = 'F0000000'
    data_dir_base_addr = int(data_dir_base_addr, 16)
    config_dir_list = 'E0000000'
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
    
    cfg_config_code = get_cfg_config("cfg_config.fig")


    #指令copy
    pe_code_copy_total = ''
    pe_code_start_pos_t = pe_code_start_pos
    
    
    dram_data = ''
    dram_data_addr = ''
    for i in range(len(pe_code_list)):
        pe_code_dir = pe_code_base_dir + int(code_addr_list[i].replace('//', ''))
        for j in range(len(pe_code_list[i])):
            if pe_code_list[i][j]=='\n':
                dram_data_addr += '\n'
                dram_data += '\n'
                continue
            dram_data_addr += hex(pe_code_dir).replace('0x', '')+'\n'
            dram_data += pe_code_list[i][j]
            if j%4 == 3:
                pe_code_dir += 4
            
    
    # for i in range(len(pe_code_list)):
    #     pe_code_dir = pe_code_base_dir + int(code_addr_list[i].replace('//', ''))
    #     pe_code_copy = ('    li a0, '+hex(pe_code_start_pos_t)+'\n',
    #                     '    li a1, '+hex(pe_code_start_pos_t+len(pe_code_list[i])*4-4)+'\n',
    #                     '    li a2, '+hex(pe_code_dir)+'\n',
    #                     '    jal datacopy\n')
    #     pe_code_copy_total += ''.join(pe_code_copy)
    #     pe_code_start_pos_t += len(pe_code_list[i])*4
    
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
        for j in range(len(data_list[i])):
            if data_list[i][j]=='\n':
                dram_data_addr += '\n'
                dram_data += '\n'
                continue
            dram_data_addr += hex(data_dir).replace('0x', '')+'\n'
            dram_data += data_list[i][j]
            if j%4 == 3:
                data_dir += 4
    # for i in range(len(data_list)):
    #     data_dir = data_dir_base_addr + int(data_addr_list[i].replace('//', ''))
    #     data_copy = ('    li a0, '+hex(data_start_pos_t)+'\n',
    #                  '    li a1, '+hex(data_start_pos_t+len(data_list[i])*4-4)+'\n',
    #                  '    li a2, '+hex(data_dir)+'\n',
    #                  '    jal datacopy\n')  
    #     data_start_pos_t += len(data_list[i])*4
    #     if data_start_pos_t / 4 >= 12288:
    #         warning = 'warning: addr out of sram range(on host), this may cause error!'
    #     data_copy_total += ''.join(data_copy)
        
    #后续data数据copy，仅copy向量
    tiling = int(width / (PE_num * exeblock_per_pe))  #每个exeblock要运算多少行
    vector_copy_total = ''
    vector_start_pos_t = data_start_pos
    for i in range(len(data_list)): 
        data_dir = data_dir_base_addr + int(data_addr_list[i].replace('//', ''))
        vector_copy = ('    li a0, '+hex(vector_start_pos_t)+'\n',
                     '    li a1, '+hex(vector_start_pos_t+ int((tiling*exeblock_per_pe+height2%tiling))*4-4)+'\n',
                     '    li a2, '+hex(data_dir)+'\n',
                     '    jal datacopy\n')  
        vector_start_pos_t += len(data_list[i])*4
        if vector_start_pos_t / 4 >= 12288:
            warning = 'warning: addr out of sram range(on host), this may cause error!'
        vector_copy_total += ''.join(vector_copy)  
        
    #缝合，但riscv程序目前还未缝上

    total = ''
    # total += '@' + str(hex(int(pe_code_start_pos/4)).replace('0x', ''))
    # total += '\n'
    # count = 0
    # for x in pe_code_list:
    #     total += '//exeblock'+str(count)+'\n'
    #     total += ''.join(x)
    #     count += 1
    # total += '\n'

    for i in range(pe_total_num):
        if i in config_start_pos_list:
            for k in range(len(config_start_pos_list[i])):
    
                total += '@' + str(hex(int(config_start_pos_list[i][k]/4)).replace('0x', ''))
                total += '\n'
                total += ''.join(config_list[i][k])
                total += '\n\n'
    
    # total += '@' + str(hex(int(data_start_pos/4)).replace('0x', ''))
    # total += '\n'
    # count = 0
    # for x in data_list:
    #     total += '//data for pe'+str(count)+'\n'
    #     total += ''.join(x)
    #     count += 1
    #print(total)
    
    #缝合riscv汇编
    riscv_code = ''
    riscv_code += '.globl __start\n'
    riscv_code += '.text\n'    
    riscv_code += '__start:\n' 
    riscv_code += 'init:\n'
    riscv_code += '      li s11, 2 \n'
    riscv_code += '      li s10, 0 \n'
    #riscv_code += ''.join(cfg_config_code)
    riscv_code += '\n\n\n'
    riscv_code += get_set_first_level_code(width, vector_addr_start)
    if tiling %(int(4/exeblock_per_pe)) !=0:
        ST_addr_start = data_dir_base_addr + int(data_addr_list[-1].replace('//', '')) + ((int(tiling/int(4/exeblock_per_pe))+1)*int(4/exeblock_per_pe)+tiling*width2)*exeblock_per_pe

    else:
        ST_addr_start = data_dir_base_addr + int(data_addr_list[-1].replace('//', '')) + (tiling)*(1+width2)*exeblock_per_pe
    
    if ST_addr_start %4 !=0:
        ST_addr_start = int(ST_addr_start/4+1)*4
    temp = width2
    if temp %4 !=0:
        temp = int(temp/4+1)*4
    ST_addr_end = ST_addr_start + temp-4

    riscv_code += '\n'
    #riscv_code += ''.join(pe_code_copy_total)
    #riscv_code += ''.join(data_copy_total)
    switch2node = ('li a0, 0x10000000\n',
                   'li a1, 1\n',
                   'sw a1, 0(a0)\n'
                    )
    riscv_code += ''.join(switch2node)
    for x in config_copy_list:
        riscv_code += ''.join(x)
    
   
    riscv_code += get_switch2riscv_code(PE_num*exeblock_per_pe-1, PE_num, exeblock_per_pe, width,  '1')
    riscv_code += get_wait_result_code(ST_addr_start, ST_addr_end, data_start_pos, height2, PE_num, tiling, height2, exeblock_per_pe,data_list, '1')
    riscv_code += get_wait_end_code('1')
    
    
    riscv_code += 'load_data: \n'
    riscv_code += vector_copy_total
    exeb_reset = ('li a0, 0xE000005C \n',
                   'li a1, 1 \n',
                   'sw a1, 0(a0) \n',
                   'li a1, 0 \n',
                   'sw a1, 0(a0)\n')
    riscv_code += ''.join(exeb_reset)
    riscv_code += ''.join(switch2node)
    for x in config_copy_list:
        riscv_code += ''.join(x)
    riscv_code += get_switch2riscv_code(PE_num*exeblock_per_pe-1, PE_num, exeblock_per_pe, width, '2')
    riscv_code += get_wait_result_code(ST_addr_start, ST_addr_end, data_start_pos, height2, PE_num, tiling, height2, exeblock_per_pe,data_list, '2')
    riscv_code += get_wait_end_code('2')

    riscv_die = ('quit: \n',
                 'li a0, 0xf\n',
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
    
    with open(os.path.dirname(os.path.abspath(__file__))+'\\dram_data.txt', 'w') as output:
        output.writelines(dram_data)
    with open(os.path.dirname(os.path.abspath(__file__))+'\\dram_data_addr.txt', 'w') as output:
        output.writelines(dram_data_addr)
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
