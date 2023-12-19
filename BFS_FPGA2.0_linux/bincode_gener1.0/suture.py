# coding:utf-8
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

#获取bitmap数据
def get_bitmap(filename):
    fbitmap = open(filename, 'r')
    bitmap = list()
    try:
        bitmap = fbitmap.readlines()
    finally:
        fbitmap.close()
    
    addr_list = list()
    bitmap_2d = list()
    temp = list()
    for x in bitmap:
        if '//' in x:
            addr_list.append(x)
            if len(temp)!=0:
                bitmap_2d.append(temp)
            temp = list()
            
        else:
            temp.append(x)
    bitmap_2d.append(temp)
    re_bitmap_2d = list()
    #bitmap[-1] += '\n'
    for k in bitmap_2d:
        re_bitmap = list()
        while(len(k) % 4 != 0):
            k.append('0'*32+'\n')
            
        for i in range(0, len(k)-3, 4):
            re_bitmap.append(k[i])
            re_bitmap.append(k[i+1])
            re_bitmap.append(k[i+2])
            re_bitmap.append(k[i+3])  
        re_bitmap_2d.append(re_bitmap)
    return re_bitmap_2d, addr_list

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
                    '   li t3, 0\n'
                    
                      '    addi s0, s5, 0\n',
                      'addr_add2_:\n',
                      '    beqz s0, sram_addr_add\n',
                      '    add t3, t3, s8\n',
                      '    addi s0, s0, -1\n',
                      '    j addr_add2_\n',
                      'sram_addr_add:\n',
                      '    add t0, t0, t3\n',
                    '    add a1, a1, t3\n',
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

def get_config_copy():
    copy_fun = ('#---------------------------------------\n',
                '# 配置信息专用搬运函数，调用参数：\n',
                '# a0: 源首地址\n',
                '# a1: 源末地址\n',
                '# a2: 目首地址\n',
                'config_copy:\n',
                '	mv t0, a0     # 当前读地址\n',
                '    mv t1, a2     # 当前写地址\n',
                '    mv t3, a3\n',
                'config_copyloop:\n',
                '    blt a1, t0, config_copyreturn   # 若读地址越界，跳转\n',
                '    lw t2, 0(t0)\n',
                '    sw t2, 0(t1)\n',
                '    addi t0, t0, 4\n',
                '    addi t1, t1, 4\n',
                '    addi t3, t3, -1\n',
                '    bnez t3, n_next\n',
                '    mv t1, a2\n',
                '    mv t3, a3\n',
                'n_next:\n'
                '    j config_copyloop\n',
                'config_copyreturn:\n',
                '	ret\n',
                '\n',
                '#---------------------------------\n')
    return ''.join(copy_fun)

def get_sendsingle_code():
    code = ('#-------------------------------------------------------\n',
            '#send单数据到FPGA\n',
            '#a0: 源数据\n',
            '\n',
            'sendSingle2FPGA:\n',
            '  li  t2, 0x00001308  #buffer地址R2H\n',

            '  sw a0, 0(t2)  #写入数据\n',
            '  ret\n')
    return ''.join(code)

def get_cfg_config(filename):
    cfg_config_file = open(os.path.dirname(os.path.abspath(__file__)) + "/../" + filename, 'r')
    cfg_config = list()
    try:
        cfg_config = cfg_config_file.readlines()
    finally:
        cfg_config_file.close()
    return cfg_config



#def get_wait_result_code(ST_addr_start, ST_addr_end, vector_addr_start, width, PE_num, tiling, height2, exeblock_per_pe, data_list, vector_buffer_addr, level_addr, Label_no):
def get_wait_result_code():
    code = ('#---------------------------------------\n',
            '# 等待结果：\n',
            '# t1: ST_addr_start\n',
            '# a1: ST_addr_end\n',
            '# t3: vector_buffer_addr\n',
            '# t4: level_addr\n',
            '# a3: width\n', 
            '# a4: 为标志寄存器，若为0，则不是最后一行，不存\n',
            'wait:\n',
            # '    li t1, '+hex(ST_addr_start)+'     # 当前写地址\n',
            # '    li a1, '+hex(ST_addr_end)+ '    # 末地址\n',
            '    li a2, -1 \n'
            '    add t1, t1, s6\n',
            '    add a1, a1, s6\n',
            # '    li t3, '+hex(vector_buffer_addr)+ '    # sram用于暂存向量地址\n',
            # '    li t4, '+hex(level_addr)+ '    # sram用于暂存向量地址\n',
            # '    li a3, '+str(width)+'\n',
            '    addi s0, s9, 0\n',
            'addr_add1:\n',
            '    beqz s0, wait_loop\n'
            '    add t3, t3, s8\n',
            '    add t4, t4, s8\n',
            '    addi s0, s0, -1\n',
            '    j addr_add1\n',
            
            'wait_loop:\n',

            '    lw s0, 0(t1)\n',
            '    lw s1, 0(t1)\n',
            '    lw s2, 0(t1)\n',
            '    lw s3, 0(t1)\n',

            '    addi a3, a3, -1\n',
            '    beqz a3, buffer0    \n',
            '    addi a3, a3, 1\n',
            
            '    addi a3, a3, -2\n',
            '    beqz a3, buffer1   \n',
            '    addi a3, a3, 2\n',
            
            '    addi a3, a3, -3\n',
            '    beqz a3, buffer2   \n',
            '    addi a3, a3, 3\n',
            
            '    addi a3, a3, -4\n',
            '    beqz a3, buffer3   \n',
            'buffer3:    \n',
            '    lw t5, 0xc(t4) \n',
            '    snez t5, t5 \n',
            '    xori t5, t5, 1\n',
            '    and s3, s3, t5\n',
            '    lw a0, 0xc(t3)\n',
            '    or a0, a0, s3\n',
            '    beqz a4, jump_st_3\n', #a4为标志寄存器，若为0，则不是最后一行，不存
            '    lw t5, 0xc(t4) \n',
            '    snez t5, t5 \n',
            '    or a0, a0, t5\n',
            '    sw a0, 0xc(t3)\n',
            'jump_st_3:\n'
            '    beq s3, x0, buffer2 \n',
            '    sw s11, 0xc(t4)    #s11存放当前level\n',
            '    li s10, 1\n',
            
            'buffer2:    \n',
            '    lw t5, 8(t4) \n',
            '    snez t5, t5 \n',
            '    xori t5, t5, 1\n',
            '    and s2, s2, t5\n',
            '    lw a0, 8(t3)\n',
            '    or a0, a0, s2\n',
            '    beqz a4, jump_st_2\n', #a4为标志寄存器，若为0，则不是最后一行，不存
            '    lw t5, 8(t4) \n',
            '    snez t5, t5 \n',
            '    or a0, a0, t5\n',
            '    sw a0, 8(t3)\n',
            'jump_st_2:\n'
            '    beq s2, x0, buffer1 \n',
            '    sw s11, 8(t4)    #s11存放当前level\n',
            '    li s10, 1\n',

            
            'buffer1:    \n',
            '    lw t5, 4(t4) \n',
            '    snez t5, t5 \n',
            '    xori t5, t5, 1\n',
            '    and s1, s1, t5\n',
            '    lw a0, 4(t3)\n',
            '    or a0, a0, s1\n',
            '    beqz a4, jump_st_1\n', #a4为标志寄存器，若为0，则不是最后一行，不存
            '    lw t5, 4(t4) \n',
            '    snez t5, t5 \n',
            '    or a0, a0, t5\n',
            '    sw a0, 4(t3)\n',
            'jump_st_1:\n'
            '    beq s1, x0, buffer0 \n',
            '    sw s11, 4(t4)    #s11存放当前level\n',           
            '    li s10, 1\n',
            
            'buffer0:   \n',
            '    lw t5, 0(t4) \n',
            '    snez t5, t5 \n',
            '    xori t5, t5, 1\n',
            '    and s0, s0, t5\n',
            '    lw a0, 0(t3)\n',
            '    or a0, a0, s0\n',
            '    beqz a4, jump_st_0\n', #a4为标志寄存器，若为0，则不是最后一行，不存
            '    lw t5, 0(t4) \n',
            '    snez t5, t5 \n',
            '    or a0, a0, t5\n',
            '    sw a0, 0(t3)\n',
            'jump_st_0:\n'
            '    beq s0, x0, next \n',
            '    sw s11, 0(t4)    #s11存放当前level\n',
            '    li s10, 1\n',

            'next:    \n',
            '    blt a1, t1, wait_return   # 若读地址越界，跳转\n',
            '    beqz a3, wait_return   # 若读取数量超出范围，跳转\n',
            '    addi t1, t1, 4\n',
            '    addi t3, t3, 16 \n',
            '    addi t4, t4, 16 \n',
            '    j wait_loop\n',
            'wait_return:\n',
            '    ret'
            '\n')
    return ''.join(code)
def get_new_data_load(PE_num, tiling, height2, exeblock_per_pe, vector_addr_start, data_list, col_tiling, data_addr_list, data_dir_base_addr, Label_no):
    
    start = 8192
    code = ''
    count = 0
    
    # code += CI_MEM_offset_code
    #code += ''.join(next_row_addr)
    for pt in range(int(PE_num/col_tiling[0])):
        start = 8192
        for i in range(pt*col_tiling[0], pt*col_tiling[0]+col_tiling[0]):
            if i!= pt*col_tiling[0]+col_tiling[0]-1:
                data_dir = data_dir_base_addr + int(data_addr_list[count].replace('//', ''))
                copy = ('    li a0, '+hex(start)+'\n',
                        '    li a1, '+hex(start+tiling*exeblock_per_pe*4-4)+'\n',
                        '    li a2, '+hex(data_dir)+'\n',
                        '    add a2, a2, s6\n',
                        # '    add a0, a0, a6\n',
                        # '    add a1, a1, a6\n',
                        '    jal datacopy\n',
                        '#---------------------------------\n')   
                code += ''.join(copy)
                start = start+tiling*exeblock_per_pe*4
                #vector_addr_start += len(data_list[i])*4
                count += 1
            else:
                data_dir = data_dir_base_addr + int(data_addr_list[count].replace('//', ''))
                copy = ('    li a0, '+hex(start)+'\n',
                        '    li a1, '+hex(start+(tiling+height2%tiling)*exeblock_per_pe*4-4)+'\n',
                        '    li a2, '+hex(data_dir)+'\n',
                        '    add a2, a2, s6\n',
                        # '    add a0, a0, a6\n',
                        # '    add a1, a1, a6\n',
                        '    jal datacopy\n',
                        '#---------------------------------\n')   
                code += ''.join(copy)
                start = start+(tiling+height2%tiling)*exeblock_per_pe*4
                #vector_addr_start += len(data_list[i])*4
                count += 1

    return ''.join(code)

def get_set_first_level_code(width, vector_addr_start):
    code = ('#---------------------------------------\n',
            '# level过程：\n',
            '# t1: 结果sram首地址\n',
            'select:\n',
            '    li t1, 0x3000     # 当前写地址\n',
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

def get_wait_end_code(total_tile_num, Label_no):
    code = ('#---------------------------------------\n',
            '# 等待结束过程：\n',
            '# s10: 结束标志，为0表示结束\n',
            'wait_end'+Label_no+':\n',
            '    li a0, '+str(total_tile_num)+'\n',
            '    bne s7, a0, load_data\n',
            '    beqz s10, quit \n',
            '    li s10, 0 \n'
            '    addi s11, s11, 1\n',
            '    li s7, 0\n',
            '    li s5, 0\n',
            '    li s9, 0\n',
            '    j load_data \n',
            '\n',
            '\n',
            '#---------------------------------\n') 
    return ''.join(code)

def get_switch2riscv_code(ST_exeblock_no, PE_num, exeblock_per_pe, width, Label_no):
    flag = 0
    l_no = 0
    addr = 0
    code = ''
    for i in range(PE_num):
        for j in range(exeblock_per_pe):
            flag <<= 1
            flag += 1
            if flag>=4294967295:
                code += '# t0: 切换需要的地址\n'
                code += 'li t0, '+hex(int('e0000000', 16)+addr) +'\n'
                code += 'add t0, t0, s6\n'
                code += 'li a2, '+hex(flag)+'\n'
                code += 'wait_exe'+str(l_no)+'_'+Label_no+':\n'
                code += '    lw t1, 0(t0) \n'
                code += 'bne t1, a2, wait_exe'+str(l_no)+'_'+Label_no+' \n'
                flag = 0
                addr += 4
                l_no += 1
    if flag!=0:
        code += '# t0: 切换需要的地址\n'
        code += 'li t0, '+hex(int('e0000000', 16)+addr) +'\n'
        code += 'add t0, t0, s6\n'
        code += 'li a2, '+hex(flag)+'\n'
        code += 'wait_exe'+str(l_no)+'_'+Label_no+':\n'
        code += '    lw t1, 0(t0) \n'
        code += 'bne t1, a2, wait_exe'+str(l_no)+'_'+Label_no+' \n'
    wait_st_code = ('#---------------------------------------\n',
            '# 切换mem_ctrl到riscv过程：\n',
            '# t0: 切换需要的地址\n',
            'li t2, '+hex((int('e0000000', 16)+int(ST_exeblock_no/32)*4)|0b10000000) +'\n',
            'add t2, t2, s6\n',
            'li a3, '+str(width)+'\n',
            'wait_st'+Label_no+':\n',
            '    lw t1, 0(t2) \n',
            '    bne t1, a3, wait_st'+Label_no+' \n',
            '    li a0, 0x10000000\n',
            '    mv a1, s4\n',
            'ni_sel_add1'+Label_no+':\n',
            '    beqz a1, conti_send_config1'+Label_no+'\n'
            '    addi a0, a0, 4\n'
            '    addi a1, a1, -1\n'
            '    j ni_sel_add1'+Label_no+'\n'
            'conti_send_config1'+Label_no+':\n'
            
            '    li a1, 0\n',
            '    sw a1, 0(a0)\n'
            '\n',
            '\n',
            '#---------------------------------\n') 
    return code+''.join(wait_st_code)

def get_new_vector_copy(width):
    data_copy_fun = ('#---------------------------------------\n',
                    '# 后续vector数据专用搬运函数，调用参数：\n',
                    '# a0: 源首地址\n',
                    '# a1: 源末地址\n',
                    '# a2: 目首地址\n',
                    'vectorcopy:\n',
                    '	mv t0, a0     # 当前读地址\n',
                    '    mv t1, a2     # 当前写地址\n',
                    '    li a3, '+str(width)+'\n'
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

# def get_CI_offset_code(row_tile_per_node):
#     code = ('    li s6, 0\n',
#             '    li a1, '+str(row_tile_per_node)+'\n',
#             '    bne s5, a1, conti_cur_node\n',
#             '    mv a0, s6\n',
#             '    mv a1, s4\n',
#             'CI_addr_add:\n',
#             '    li a2, 0x0800000\n',
#             '    add s6, s6, a2\n',
#             '    addi a1, a1, -1\n',
#             '    bnez a1, CI_addr_add\n',
#             'conti_cur_node:\n')
#     return ''.join(code)

#主函数
def main():
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..') + '/pe_module.json', "r") as f:
        res = json.load(f)
    width = res['1']['m1_width']
    height2 = res['1']['m2_height']
    width2 = res['1']['m2_width']
    col_tiling = res['1']['column_tiling']
    PE_num = res['1']['PE_num']
    exeblock_per_PE = res['1']['exeblock_per_PE']
    node_num = res['1']['node']
    col_tiling = [int(x) for x in col_tiling.split(',')]
    tile = int(PE_num/col_tiling[0]*col_tiling[1])
    reload_num = int(height2/(PE_num/col_tiling[0]*col_tiling[1]))
    #tile_per_node = int(reload_num/node_num)
    
    vector_addr_start = '8192'     #后续新向量在sram中暂时存储的地址
    level_addr_start = '12288'
    warning = ''
    dirlist = os.listdir(os.path.dirname(os.path.abspath(__file__))+'/test/rg_gen')
    dirlist.sort(key=lambda x: int(x[4:]))
    tile_num = 0
    node_count = 0
    for i in dirlist:
        
        filelist = file_name(os.path.dirname(os.path.abspath(__file__))+'/test/rg_gen/'+i)
        pe_code_start_pos = '00000C00'
        pe_code_start_pos = int(pe_code_start_pos, 16)
        #config_start_pos = '0000112C'
        #data_start_pos = ''
        pe_code_base_dir = 'F0000000'
        pe_code_base_dir = int(pe_code_base_dir, 16)
        data_dir_base_addr = 'F0000000'
        data_dir_base_addr = int(data_dir_base_addr, 16)
        bitmap_dir_base_addr = 'F0000000'
        bitmap_dir_base_addr = int(bitmap_dir_base_addr, 16)
        config_dir_list = 'E0000000'
        pe_total_num = 256
        
        config_list = dict()
        for name in filelist:
            if 'pe' in name:
                pe_code_list, code_addr_list = get_code(name)
            elif 'b_exe' in name:
                pe_num = int(name[-7:-6])
                if pe_num not in config_list:
                    config_list[pe_num] = list()
                    config_list[pe_num].append(get_config(name))
                else:
                    config_list[pe_num].append(get_config(name))
            elif 'data' in name:
                data_list, data_addr_list = get_data(name)
            elif 'bitmap' in name:
                bitmap_list, bitmap_addr_list = get_bitmap(name)
        
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
                dram_data_addr += hex(pe_code_dir + 8388608*(node_count%node_num)).replace('0x', '')+'\n'
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
                        # temp = ('    li a0, '+(hex(config_start_pos))+'\n',
                        #         '    li a1, '+hex((len(x)-1)*4 + int(config_start_pos))+'\n',
                        #         '    li a2, 0x'+config_dir_list+'\n',
                        #         '    jal copy\n')
                        temp = [hex(config_start_pos), hex((len(x)-1)*4 + int(config_start_pos)), config_dir_list]
                        config_copy_list.append(temp)
                        if i not in config_start_pos_list:
                            config_start_pos_list[i] = list()
                            config_start_pos_list[i].append(config_start_pos)
                        else:
                            config_start_pos_list[i].append(config_start_pos)
                        config_start_pos = (config_start_pos+len(x)*4)
        
        PE_num = len(config_list)
        exeblock_per_pe = int(len(config_copy_list)/PE_num)
    
        re_config_copy_list = list()
        for i in range(PE_num):
            #for j in range(exeblock_per_pe):
            load_config = ('    li a0, '+config_copy_list[(PE_num-i-1)*(exeblock_per_pe)+0][0]+'\n',
                           '    li a1, '+config_copy_list[(PE_num-i-1)*(exeblock_per_pe)+exeblock_per_pe-1][1]+'\n',
                           '    li a2, 0x'+config_copy_list[(PE_num-i-1)*(exeblock_per_pe)+0][2]+'\n',
                           '    add a2, a2, s6\n',
                           '    li a3, '+str(int((int(config_copy_list[(PE_num-i-1)*(exeblock_per_pe)+0][1],16)+4-int(config_copy_list[(PE_num-i-1)*(exeblock_per_pe)+0][0],16))/4))+'\n',
                           '    jal config_copy\n')
            #re_config_copy_list.append(config_copy_list[(PE_num-i-1)*(exeblock_per_pe)+0][0])
            re_config_copy_list.append(load_config)
        config_copy_list = re_config_copy_list
        #config_copy_list.reverse()
        
        data_start_pos = config_start_pos + 4
        #data数据copy
        data_copy_total = ''
        data_start_pos_t = data_start_pos
        
        for k in range(len(data_list)):
            data_dir = data_dir_base_addr + int(data_addr_list[k].replace('//', ''))
            for j in range(len(data_list[k])):
                if data_list[k][j]=='\n':
                    dram_data_addr += '\n'
                    dram_data += '\n'
                    continue
                dram_data_addr += hex(data_dir + 8388608*(node_count%node_num)).replace('0x', '')+'\n'
                #print(hex(data_dir).replace('0x', '')+'\n')
                dram_data += data_list[k][j]
                if j%4 == 3:
                    data_dir += 4
        
        # for i in range(len(data_list)):
        #     data_dir = data_dir_base_addr + int(data_addr_list[i].replace('//', ''))
        #     data_copy = ('    li a0, '+hex(data_start_pos_t)+'\n',
        #                  '    li a1, '+hex(data_start_pos_t+len(data_list[i])*4-4)+'\n',
        #                  '    li a2, '+hex(data_dir)+'\n',
        #                  '    jal datacopy\n')  
        #     data_start_pos_t += len(data_list[i])*4
        #     if data_start_pos_t / 4 >= 16384:
        #         warning = 'warning: addr out of sram range(on host), this may cause error!'
        #     data_copy_total += ''.join(data_copy)
            
        bitmap_start_pos = config_start_pos + 4
        #bitmap数据copy
        bitmap_copy_total = ''
        bitmap_start_pos_t = bitmap_start_pos
        
        
        for k in range(len(bitmap_list)):
            bitmap_dir = bitmap_dir_base_addr + int(bitmap_addr_list[k].replace('//', ''))
            dram_data_per_32 = 0
            dir_counter = 0
            data_counter = 0 #记录每32个或者结尾的bitmap
            exeb_data_len = int(len(bitmap_list[k])/exeblock_per_PE)
            offset = 0
            for j in range(len(bitmap_list[k])):
                # if bitmap_list[k][j]=='\n':
                #     dram_data_addr += '\n'
                #     dram_data += '\n'
                #     continue
                
                #print(hex(bitmap_dir).replace('0x', '')+'\n')
                dram_data_per_32 += int(bitmap_list[k][j], 2)<< int(data_counter)
                data_counter += 1
                #dram_data += bitmap_list[k][j]
                #print(dram_data_per_32)
                if data_counter%32 == 0:
                    
                    dram_data += bin(dram_data_per_32).replace('0b', '')+'\n'
                    #print(dram_data_per_32)
                    dram_data_per_32 = 0
                    data_counter = 0
                    dram_data_addr += hex(bitmap_dir + 8388608*(node_count%node_num) + int(dir_counter/4)*4).replace('0x', '')+'\n'
                    dir_counter = (dir_counter + 1)
                elif ((j+1)%exeb_data_len==0):
                    dram_data += bin(dram_data_per_32).replace('0b', '')+'\n'
                    #print(dram_data_per_32)
                    dram_data_per_32 = 0
                    data_counter = 0
                    offset += exeb_data_len
                    dram_data_addr += hex(bitmap_dir + 8388608*(node_count%node_num) + int(dir_counter/4)*4).replace('0x', '')+'\n'
                    dir_counter = (dir_counter + 1)
                    
                    while(dir_counter%4!=0) :
                        dram_data += bin(0).replace('0b', '')+'\n'
                        
                        dram_data_addr += hex(bitmap_dir + 8388608*(node_count%node_num) + int(dir_counter/4)*4).replace('0x', '')+'\n'
                        dir_counter = (dir_counter + 1)
                    # dram_data += bin(0).replace('0b', '')+'\n'
                    # dir_counter = (dir_counter + 1)
                    # dram_data_addr += hex(bitmap_dir + 8388608*(node_count%node_num) + int(dir_counter/4)*4).replace('0x', '')+'\n'
                    
                  
                    # dir_counter = (dir_counter + 1)
                    
                    
                  
                
        node_count += 1
        #后续data数据copy，仅copy向量
        tiling = int(tile / col_tiling[0] / exeblock_per_pe)  #每个exeblock要运算多少行
        #print(tiling)
        vector_copy_total = ''
        vector_start_pos_t = data_start_pos
        for i in range(len(data_list)): 
            data_dir = data_dir_base_addr + int(data_addr_list[i].replace('//', ''))
            vector_copy = ('    li a0, '+hex(vector_start_pos_t)+'\n',
                         '    li a1, '+hex(vector_start_pos_t+ int((tiling*exeblock_per_pe+height2%tiling))*4-4)+'\n',
                         '    li a2, '+hex(data_dir)+'\n',
                         '    jal copy\n')  
            vector_start_pos_t += len(data_list[i])*4
            if vector_start_pos_t / 4 >= 3072:
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
        riscv_code += ''.join(cfg_config_code)
        # riscv_code += '\nli a0, 1\njal sendSingle2FPGA\n'
        # riscv_code += '\n#enable irq\n'
        # riscv_code += '      li x3, 0x7FFFFFF0			# 8\'h7ffffff0\n'
        # riscv_code += '      #.word 0x0601e00b #enable irq\n'
        # riscv_code += 'nop      #enable irq\n'
        # riscv_code += '\n#wait_irq()\n'
        # riscv_code += '      #.word 0x0800400B #wait irq\n'
        # riscv_code += 'nop      #wait irq\n'
        # riscv_code += 'init:\n'
        # riscv_code += '      li x3, 0xFFFFFFF0			# 8\'hfffffff0'
        # riscv_code += '      #.word 0x0601e00b #disable irq\n'
        # riscv_code += 'nop      #disable irq\n'
        riscv_code += '\n      li s11, 2 \n'
        riscv_code += '      li s10, 0 \n'
        riscv_code += '      li s9, 0\n'    #s9记录每一次行划分进行到第几次，目前最多两次
        riscv_code += '      li s8, '+str(tile*4)+'\n'    #s8为一次行划分所需要加上的偏移
        riscv_code += '      li s7, 0\n' #s7记录进行的总的tile次数，目前最多为4次
        riscv_code += '      li s6, 0\n' #s6记录CI地址偏移和MEM地址偏移，用于给不同的node发配置信息和数据
        riscv_code += '      li s5, 0\n' #s5记录行tile到第几行tile
        riscv_code += '      li s4, 0\n' #s4记录当前执行到第几个node
        riscv_code += '      li a7, 0\n' #a7记录执行了几个TILE，用于判断是否为第一次迭代
        
        riscv_code += '\n\n\n'
        riscv_code += get_set_first_level_code(width, vector_addr_start)
    
        ST_addr_start = list()
        ST_addr_end = list()
        for pt in range(int(PE_num/col_tiling[0])):
            t = data_dir_base_addr + int(data_addr_list[(pt*col_tiling[0]+col_tiling[0]-1)].replace('//', '')) + int(height2/reload_num/col_tiling[0]/exeblock_per_pe)*(1+col_tiling[1])*exeblock_per_pe
            
            if t %4 !=0:
                t = int(t/4+1)*4
            temp = int(col_tiling[1])
            if temp %4 !=0:
                temp = int(temp/4+1)*4
            ST_addr_start.append(t)    
            ST_addr_end.append(t + temp-4)
           # print(col_tiling[1])
        
        
        #ST_addr_start = data_dir_base_addr + int(data_addr_list[-1].replace('//', '')) + (tiling+height2%tiling)*(1+width2)*exeblock_per_pe
        
        
    
        riscv_code += '\n'
        #riscv_code += ''.join(pe_code_copy_total)
        #riscv_code += ''.join(data_copy_total)
        # switch2node = ('li a0, 0x10000000\n',
        #                 '    mv a1, s4\n',
        #                 'ni_sel_add1:\n',
        #                 '    beqz a1, conti_send_config1'
        #                 '    addi a0, a0, 4\n'
        #                 '    addi a1, a1, -1\n'
        #                 '    j ni_sel_add1\n'
        #                 'li a1, 1\n',
        #                 'sw a1, 0(a0)\n'
        #                 )
        #riscv_code += ''.join(switch2node)
        riscv_code += '    li s4, 0\n'
        riscv_code += 'send_config_loop1:\n'
        riscv_code += '\nli a0, 1\njal sendSingle2FPGA\n'
        riscv_code += '\n#enable irq\n'
        riscv_code += '      li x3, 0x7FFFFFF0			# 8\'h7ffffff0\n'
        riscv_code += '      #.word 0x0601e00b #enable irq\n'
        riscv_code += 'nop      #enable irq\n'
        riscv_code += '\n#wait_irq()\n'
        riscv_code += '      #.word 0x0800400B #wait irq\n'
        riscv_code += 'nop      #wait irq\n'
        riscv_code += 'init:\n'
        riscv_code += '      li x3, 0xFFFFFFF0			# 8\'hfffffff0'
        riscv_code += '      #.word 0x0601e00b #disable irq\n'
        riscv_code += 'nop      #disable irq\n'
        riscv_code += '    mv a1, s4\n'
        riscv_code += '    li s6, 0\n'
        riscv_code += 'CI_addr_add1:\n'
        riscv_code += '    beqz a1, conti_send_node\n'
        riscv_code += '    li a2, 0x0800000\n'
        riscv_code += '    add s6, s6, a2\n'
        riscv_code += '    addi a1, a1, -1\n'
        riscv_code += '    j CI_addr_add1\n'
        riscv_code += 'conti_send_node:\n'
        switch2node = ('li a0, 0x10000000\n',
                        '    mv a1, s4\n',
                        'ni_sel_add1:\n',
                        '    beqz a1, conti_send_config1\n'
                        '    addi a0, a0, 4\n'
                        '    addi a1, a1, -1\n'
                        '    j ni_sel_add1\n'
                        'conti_send_config1:\n'
                        'li a1, 1\n',
                        'sw a1, 0(a0)\n'
                        )
        riscv_code += ''.join(switch2node)
        
        for x in config_copy_list:
            riscv_code += ''.join(x)
        riscv_code += '    addi s7, s7, 1\n'
        riscv_code += '    addi s4, s4, 1\n'
        #riscv_code += '    addi s9, s9, 1\n'
        # riscv_code += '\nli a0, 1\njal sendSingle2FPGA\n'
        # riscv_code += '\n#enable irq\n'
        # riscv_code += '      li x3, 0x7FFFFFF0			# 8\'h7ffffff0\n'
        # riscv_code += '      #.word 0x0601e00b #enable irq\n'
        # riscv_code += 'nop      #enable irq\n'
        # riscv_code += '\n#wait_irq()\n'
        # riscv_code += '      #.word 0x0800400B #wait irq\n'
        # riscv_code += 'nop      #wait irq\n\n'
        riscv_code += '    li a0, '+str(node_num)+'\n'
        riscv_code += '    bne s4, a0, send_config_loop1\n'
        riscv_code += '    li s4, 0\n'
        riscv_code += '    li s6, 0\n'
        #riscv_code += '    li s9, 0\n'
        riscv_code += 'wait_result_loop1:\n'
        riscv_code += '    mv a1, s4\n'
        riscv_code += '    li s6, 0\n'
        riscv_code += 'CI_addr_add2:\n'
        riscv_code += '    beqz a1, conti_wait_node1\n'
        riscv_code += '    li a2, 0x0800000\n'
        riscv_code += '    add s6, s6, a2\n'
        riscv_code += '    addi a1, a1, -1\n'  
        riscv_code += '    j CI_addr_add2\n'        
        riscv_code += 'conti_wait_node1:\n'
        
        riscv_code += get_switch2riscv_code(PE_num*exeblock_per_pe-1, PE_num, exeblock_per_pe, tile,  '1')
        vector_buffer_addr = int(vector_addr_start)
        level_addr = int(level_addr_start)
        ST_addr_s = ST_addr_start[0]
        st_count = -1
        ST_addr_e = ST_addr_end[0]
        #riscv_code += get_wait_result_code(ST_addr_start, ST_addr_end, data_start_pos, height2, PE_num, tiling, height2, exeblock_per_pe,data_list, '1')
    
        for pt in range(int(PE_num/col_tiling[0])):
            st_count += 1       
            ST_addr_s = ST_addr_start[st_count]
            ST_addr_e = ST_addr_end[st_count]
            col_tile_wait = ('    li t1, '+hex(ST_addr_s)+'     # 当前写地址\n',
                              '    li a1, '+hex(ST_addr_e)+ '    # 末地址\n',
                              '    li t3, '+hex(vector_buffer_addr)+ '    # sram用于暂存向量地址\n',
                              '    li t4, '+hex(level_addr)+ '    # sram用于暂存向量地址\n',
                              '    li a3, '+str(col_tiling[1])+'\n',
                              '    li a4, '+str(reload_num-1)+'\n',
                              '    bne a4, s5, jump_flag_0_'+str(pt)+'\n',
                              '    li a4, 1\n',
                              '    j jump_2_wait_0_'+str(pt)+'\n'
                              'jump_flag_0_'+str(pt)+':\n'
                              '    li a4, 0\n'
                              'jump_2_wait_0_'+str(pt)+':\n'
                              '    jal wait\n')
            vector_buffer_addr += col_tiling[1]*4
            level_addr += col_tiling[1]*4
            
            riscv_code += ''.join(col_tile_wait)
        
        riscv_code += '    addi s9, s9, 1\n'
        riscv_code += '    addi s4, s4, 1\n'
        riscv_code += '    addi a7, a7, 1\n'
        riscv_code += '    li a0, '+str(node_num)+'\n'
        riscv_code += '    bne s4, a0, wait_result_loop1\n'
        riscv_code += '    li s4, 0\n'
        riscv_code += '    li s6, 0\n'
        
        riscv_code += 'load_data: \n'
        
        riscv_code += '    li s4, 0\n'
        riscv_code += '    li s6, 0\n'
        riscv_code += 'reload_loop1:\n'
        riscv_code += '    mv a1, s4\n'
        riscv_code += '    li s6, 0\n'
        riscv_code += 'CI_addr_add3:\n'
        riscv_code += '    beqz a1, conti_reload_node1\n'
        riscv_code += '    li a2, 0x0800000\n'
        riscv_code += '    add s6, s6, a2\n'
        riscv_code += '    addi a1, a1, -1\n'
        riscv_code += '    j CI_addr_add3\n'
        riscv_code += 'conti_reload_node1:\n'
        
        riscv_code += 'li a0, 2\n'
        riscv_code += 'beq s7, a0, FPGA_n_try_stop\n'
        
        riscv_code += '\nli a0, 1\n'
        riscv_code += 'FPGA_n_try_stop:\n'
        riscv_code += 'jal sendSingle2FPGA\n'
        riscv_code += '\n#enable irq\n'
        riscv_code += '      li x3, 0x7FFFFFF0			# 8\'h7ffffff0\n'
        riscv_code += '      #.word 0x0601e00b #enable irq\n'
        riscv_code += 'nop      #enable irq\n'
        riscv_code += '\n#wait_irq()\n'
        riscv_code += '      #.word 0x0800400B #wait irq\n'
        riscv_code += 'nop      #wait irq\n\n'
        
        #riscv_code += get_CI_offset_code(tile_per_node)
        riscv_code += '    li a0, '+str(reload_num)+'\n'
        riscv_code += '    bne s9, a0, coni_row_tile1\n'
        riscv_code += '    li s9, 0\n'
        riscv_code += '    addi s5, s5, 1\n'
        riscv_code += 'coni_row_tile1:\n'
        riscv_code += '    li a0, '+str(reload_num*reload_num)+'\n'
        riscv_code += '    blt a7, a0, jump_reload\n'
        # riscv_code += '    li a7, '+str(reload_num)+'\n'
        # riscv_code += '    li a6, 0\n'
        # riscv_code += '    li a5, 0\n'
        # riscv_code += 'reload_new_data:\n'
        riscv_code += get_new_data_load(PE_num, tiling, height2, exeblock_per_pe, int(data_start_pos), data_list, col_tiling, data_addr_list, data_dir_base_addr, '1')
        # riscv_code += '    add a6, a6, s8\n'
        # riscv_code += '    li a4, 0x0800000\n'
        # riscv_code += '    add a5, a5, a4\n'
        # riscv_code += '    addi a7, a7, -1\n'
        # riscv_code += '    bnez a7, reload_new_data\n'
        riscv_code += 'jump_reload:\n'
        #riscv_code += get_wait_end_code('1')
        
        
        
        #riscv_code += vector_copy_total
        exeb_reset = ('li a0, 0xE000007C \n',
                      'add a0, a0, s6\n',
                       'li a1, 1 \n',
                       'sw a1, 0(a0) \n',
                       'li a1, 0 \n',
                       'sw a1, 0(a0)\n')
        riscv_code += ''.join(exeb_reset)
        switch2node = ('li a0, 0x10000000\n',
                        '    mv a1, s4\n',
                        'ni_sel_add2:\n',
                        '    beqz a1, conti_send_config2\n'
                        '    addi a0, a0, 4\n'
                        '    addi a1, a1, -1\n'
                        '    j ni_sel_add2\n'
                        'conti_send_config2:\n'
                        'li a1, 1\n',
                        'sw a1, 0(a0)\n'
                        )
        riscv_code += ''.join(switch2node)
        
        # next_row_tile = ('li a0, 2\n',
        #                  'addi s9, s9, 1\n',
        #                  'bne s9, a0, jump\n',
        #                  'li s9, 0\n',
        #                  'jump:\n')
        
        
        
        for x in config_copy_list:
            riscv_code += ''.join(x)
        riscv_code += '    addi s7, s7, 1\n'
        riscv_code += '    addi s4, s4, 1\n'
        #riscv_code += '    addi s9, s9, 1\n'
            
        riscv_code += '    li a0, '+str(node_num)+'\n'
        riscv_code += '    bne s4, a0, reload_loop1\n'
        riscv_code += '    li s4, 0\n'
        riscv_code += '    li s6, 0\n'
        #riscv_code += '    li s9, 0\n'
    
        
        
        riscv_code += 'wait_result_loop2:\n'
        riscv_code += '    mv a1, s4\n'
        riscv_code += '    li s6, 0\n'
        riscv_code += 'CI_addr_add4:\n'
        riscv_code += '    beqz a1, conti_wait_node2\n'
        riscv_code += '    li a2, 0x0800000\n'
        riscv_code += '    add s6, s6, a2\n'
        riscv_code += '    addi a1, a1, -1\n'  
        riscv_code += '    j CI_addr_add4\n'
        riscv_code += 'conti_wait_node2:\n'
        
        riscv_code += get_switch2riscv_code(PE_num*exeblock_per_pe-1, PE_num, exeblock_per_pe, tile, '2')
        
        
        
        #riscv_code += get_wait_result_code(ST_addr_start, ST_addr_end, data_start_pos, height2, PE_num, tiling, height2, exeblock_per_pe,data_list, '2')
        vector_buffer_addr = int(vector_addr_start)
        level_addr = int(level_addr_start)
        ST_addr_s = ST_addr_start[0]
        st_count = -1
        ST_addr_e = ST_addr_end[0]
        #riscv_code += get_wait_result_code(ST_addr_start, ST_addr_end, data_start_pos, height2, PE_num, tiling, height2, exeblock_per_pe,data_list, '1')
        for pt in range(int(PE_num/col_tiling[0])):
            st_count += 1       
            ST_addr_s = ST_addr_start[st_count]
            ST_addr_e = ST_addr_end[st_count]
            col_tile_wait = ('    li t1, '+hex(ST_addr_s)+'     # 当前写地址\n',
                             '    li a1, '+hex(ST_addr_e)+ '    # 末地址\n',
                             '    li t3, '+hex(vector_buffer_addr)+ '    # sram用于暂存向量地址\n',
                             '    li t4, '+hex(level_addr)+ '    # sram用于暂存向量地址\n',
                             '    li a3, '+str(col_tiling[1])+'\n',
                             '    li a4, '+str(reload_num-1)+'\n',
                            '    bne a4, s5, jump_flag_1_'+str(pt)+'\n',
                            '    li a4, 1\n',
                            '    j jump_2_wait_1_'+str(pt)+'\n'
                            'jump_flag_1_'+str(pt)+':\n'
                            '    li a4, 0\n'
                            'jump_2_wait_1_'+str(pt)+':\n'
                             '    jal wait\n')
            vector_buffer_addr += (col_tiling[1])*4
            level_addr += (col_tiling[1])*4
            
            riscv_code += ''.join(col_tile_wait)
            
        riscv_code += '    addi s9, s9, 1\n'
        riscv_code += '    addi s4, s4, 1\n'
        riscv_code += '    addi a7, a7, 1\n'
        riscv_code += '    li a0, '+str(node_num)+'\n'
        riscv_code += '    bne s4, a0, wait_result_loop2\n'
        riscv_code += '    li s4, 0\n'
        riscv_code += '    li s6, 0\n'
        
        #riscv_code += get_new_data_load(PE_num, tiling, height2, exeblock_per_pe, int(data_start_pos), data_list, col_tiling, data_addr_list, data_dir_base_addr, '2')
        
        riscv_code += get_wait_end_code(reload_num*reload_num, '2')
    
        riscv_die = ('quit: \n',
                     'li a0, 0xf\n',
                     'jal sendSingle2FPGA\n'
                     '\n#wait_irq()\n'
                     '      #.word 0x0800400B #wait irq\n'
                     'nop      #wait irq\n\n'
                     'li a0, 0xf\n',
                     'li a1, 0\n',
                     'sw a1, 0(a0)\n')
        riscv_code += ''.join(riscv_die)
        
        riscv_code += '\n\n'
        riscv_code += get_wait_result_code()
        riscv_code += get_copy_func()
        riscv_code += get_data_copy_func()            
        riscv_code += get_sendsingle_code()
        riscv_code += get_config_copy()
        
        
        if os.path.exists(os.path.dirname(os.path.abspath(__file__))+'/structure_gen')==0:
            os.mkdir(os.path.dirname(os.path.abspath(__file__))+'/structure_gen')
        if os.path.exists(os.path.dirname(os.path.abspath(__file__))+'/structure_gen/tile'+str(tile_num))==0:
            os.mkdir(os.path.dirname(os.path.abspath(__file__))+'/structure_gen/tile'+str(tile_num))
            
        half_code_output = open(os.path.dirname(os.path.abspath(__file__))+'/structure_gen/tile'+str(tile_num)+'/half_code.txt', 'w')
        riscv_code_output = open(os.path.dirname(os.path.abspath(__file__))+'/structure_gen/tile'+str(tile_num)+'/riscv_code.s', 'w')
        try:
            half_code_output.writelines(total)
            riscv_code_output.writelines(riscv_code)
        finally:
            half_code_output.close()
            riscv_code_output.close()
        
        #print(os.path.dirname(os.path.abspath(__file__))+'/jupiter/bin/jupiter '+os.path.dirname(os.path.abspath(__file__))+'/riscv_code.s --dump-code '+ os.path.dirname(os.path.abspath(__file__))+'/hex_riscv_code.txt')
        #产生二进制riscv汇编
        #print(os.getcwd())
        with os.popen(os.path.dirname(os.path.abspath(__file__))+'/jupiter/bin/jupiter '+os.path.dirname(os.path.abspath(__file__))+'/structure_gen/tile'+str(tile_num)+'/riscv_code.s --dump-code '+ os.path.dirname(os.path.abspath(__file__))+'/structure_gen/tile'+str(tile_num)+'/hex_riscv_code.txt') as ret:
            print(ret)
        #hex2bin
        with open(os.path.dirname(os.path.abspath(__file__))+'/structure_gen/tile'+str(tile_num)+'/hex_riscv_code.txt', 'r') as h:
            hex_code = h.readlines()
        bin_code = [str(bin(int(x.replace('\n', ''),16))).replace('0b', '') for x in hex_code]
        bin_code = ['0'*(32-len(x))+x+'\n' for x in bin_code]
        
        code = ''.join(bin_code) + '\n' + total
        
        
                
       
            
        with open(os.path.dirname(os.path.abspath(__file__))+'/structure_gen/tile'+str(tile_num)+'/code.txt', 'w') as output:
            output.writelines(code)
        
        with open(os.path.dirname(os.path.abspath(__file__))+'/structure_gen/tile'+str(tile_num)+'/dram_data.txt', 'w') as output:
            output.writelines(dram_data)
        with open(os.path.dirname(os.path.abspath(__file__))+'/structure_gen/tile'+str(tile_num)+'/dram_data_addr.txt', 'w') as output:
            output.writelines(dram_data_addr)
        
        if len(warning) != 0:
            print(warning)
            with open(os.path.dirname(os.path.abspath(__file__))+'/structure_gen/tile'+str(tile_num)+'/warning.txt', 'w') as w:
                w.writelines(warning)
                
        tile_num += 1
        # with open(os.path.dirname(os.path.abspath(__file__))+'/test/result.txt', 'r') as result:
        #     re_num = result.readlines()
        # output_addr = list()
        # for i in range(len(re_num)):
        #     output_addr.append(str(hex(int(data_addr_list[-1].rstrip('\n').lstrip('//'))+i).replace('0x', ''))+'\n')
        # with open(os.path.dirname(os.path.abspath(__file__))+'/ST_ADDR.txt', 'w') as SA:
        #     SA.writelines(output_addr)
    
if __name__ == "__main__":
    main()
