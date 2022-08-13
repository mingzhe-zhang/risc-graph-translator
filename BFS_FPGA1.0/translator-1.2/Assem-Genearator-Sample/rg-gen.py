# coding:utf-8
import math
import random
import xmltodict
import re
import csv
import numpy as np
import os
import sys
import json

def opr_ext(width, f):
    if f=='max':
        return '0b' + '1' * int(width)
    if '0x' in f:
        x = f.replace('0x', '')
        r = bin(int(x, 16)).replace('0b', '')
    elif '0b' in f:
        x = f.replace('0b')
        
    elif '0o' in f:
        x = f.replace('0o', '')
        r = bin(int(x, 8)).replace('0b', '')
    else:
        r = bin(int(f, 10)).replace('0b', '')
        
    if(len(r) > int(width)):
        print('Warning: operand length is too long!')
        return 'error'
    e_r = '0' * (int(width)-len(r)) + r
    return e_r

def read_vector(a):
    a = a.lstrip('[').rstrip(']')
    a = a.split(',')
    return a

def read_matrix(b):
    b = b.lstrip('[').rstrip(']')
    b = b.split(', ')
    matrix_b = list()
    for a in b:
        matrix_b.append(read_vector(a))
    return matrix_b

def CPU_result(data_width, host_a, host_b):
    data = list()
    fil_length = 0
    # bitmap = list()
    #print(host_b)
    r = np.zeros(shape=(1, len(host_b[0][0])))
    for i in range(len(host_a)): 
        a = np.array(host_a[i])
        b = np.array(host_b[i])
        c = np.dot(a, b)   
        r += c
        for j in host_a[i]:
            data.append(j)
            
            # bitmap.append(1)
        length = len(host_a[i]) 
        fil_length = 0
        while length%4!=0:
            data.append(0)
            length += 1
            fil_length += 1
        for j in host_b[i]:
            for k in j:
                data.append(k)
                # if k != 0:
                #     bitmap.append(1)
                # else:
                #     bitmap.append(0)
            
    #print(fil_length)
    return [str(opr_ext(data_width, str(m)))+'\n' for m in data ], [str(int(x))+' ' for x in r[0]], fil_length
       
def tiling_gen1(matrix, value, width_start, width_end, height, exeb_start: int, dram_start: int):
    a = list()
    v_a = list()
    k = 0
    for i in range(height):
        array = list()
        v_array = list()
        for j in range(width_start, width_end):
            v = value[i][j]
            dram_addr = matrix[i][j][1]
            #dram_addr = dram_start + k
            exeb_addr = k + exeb_start
            x = [v, dram_addr, exeb_addr]
            #print(x)
            array.append(x)
            v_array.append(v)
            k += 1
        a.append(array)
        v_a += v_array
    return a, v_a

def tiling_gen2(matrix, value, height_start, height_end, width_start, width_end, exeb_start: int, dram_start: int):
    a = list()
    v_a = list()
    d_bank_count = random.randint(0, 6)
    k = 0
    for i in range(height_start, height_end):
        array = list()
        v_array = list()
        k = d_bank_count * 256
        
        for j in range(width_start, width_end):

            v = value[i][j]
            dram_addr = matrix[i][j][1]
            #dram_addr = dram_start + k
            exeb_addr = k + exeb_start
            if exeb_addr % 256 >= 192:
                d_bank_count += 1
                d_bank_count = d_bank_count % 6
                k = d_bank_count * 256
                exeb_addr = k + exeb_start
            x = [v, dram_addr, exeb_addr]
            
            #print(x)
            array.append(x)
            v_array.append(v)
            k += 1
        a.append(array)
        v_a.append(v_array)
        d_bank_count += 1
        d_bank_count = d_bank_count % 7
    return a, v_a

def matrix_gen(height: int, width: int, min_data: int, max_data: int, dram_addr_start: int, matrix):
    a = list()
    v_a = list()
    
    k = 0
    for i in range(height):
        array = list()
        v_array = list()
        for j in range(width):
            #value = random.randint(min_data, max_data)
            if height==1:
                
                value = int(matrix[0][j])
            else:
                
                value = int(matrix[i][j])
            x = [value, dram_addr_start + k, -1]
            
            #print(x)
            array.append(x)
            v_array.append(value)       
            k += 1
        a.append(array)
        v_a.append(v_array)
    return a, v_a
 
def dram_arrange(matrix_a, matrix_b, PE_num, col_tiling):
    b_fil = list()
    for pt in range(int(PE_num/col_tiling[0])):
        for c in range(pt*col_tiling[0], pt*col_tiling[0]+col_tiling[0]):
            
            k = 0
           
            for j in range(int(len(matrix_a[0])/col_tiling[0])*(c-pt*col_tiling[0]), int(len(matrix_a[0])/col_tiling[0])*(c-pt*col_tiling[0]+1)):
                
                matrix_a[0][j][1] = k
                k += 1
            # while k%4!=0:
            #     b_fil.append([0,])
            if k%4!=0:
                k = int(k/4+1)*4
            for i in range(int(len(matrix_b)/col_tiling[0])*(c-pt*col_tiling[0]), int(len(matrix_b)/col_tiling[0])*(c-pt*col_tiling[0]+1)):
                for j in range(pt*col_tiling[1], pt*col_tiling[1]+col_tiling[1]):
                    
                    matrix_b[i][j][1] = k
                    k += 1
            #print(k)
    # k = 0
    # for j in range(int(len(matrix_a[0])/PE_num), len(matrix_a[0])):
    #     matrix_a[0][j][1] = k
    #     k += 1
    # for i in range(int(len(matrix_b)/PE_num), len(matrix_b)):
    #     for j in range(len(matrix_b[i])):
    #         matrix_b[i][j][1] = k
    #         k += 1
    return matrix_a, matrix_b
       

def LD_stage_A(matrix, bitmap):

    LD_stage_assem = list()
    addr_occu = list()
    #print(ld_vector_num)
    for array in matrix:
        for x in array:
            a = 'LD ' + str(x[2]) + ', ' + '0, ' + str(x[1])
            LD_stage_assem.append(a)
            
            bitmap.append(str(opr_ext(32, '1'))+'\n')
            addr_occu.append(x[2])
           
    return LD_stage_assem, addr_occu

def LD_stage_B(matrix, bitmap):

    LD_stage_assem = list()
    addr_occu = list()
    #print(ld_vector_num)
    for array in matrix:
        for x in array:
            a = 'LD ' + str(x[2]) + ', ' + '0, ' + str(x[1])
            LD_stage_assem.append(a)
            addr_occu.append(x[2])

            if x[0] == 0:
                bitmap.append(str(opr_ext(32, '0'))+'\n')
            else:
                bitmap.append(str(opr_ext(32, '1'))+'\n')
    return LD_stage_assem, addr_occu

def CAL_stage(matrix1, matrix2, cal_op1, cal_op2):
    CAL_stage_assem = list()
    result_addr = list()
    for i in range(len(matrix2[0])):
        for j in range(len(matrix1[0])):
            
            if int(matrix1[0][j][2]/256)==int(matrix2[len(matrix1[0])-j-1][i][2]/256):
                c = 'PREREAD0 ' + str(matrix1[0][j][2]) +', 0, 0' 
                # d = 'PREREAD1 ' + '0, '+ str(matrix2[len(matrix1[0])-j-1][i][2]) +', 0'
                CAL_stage_assem.append(c)
                # CAL_stage_assem.append(d)
            
            if cal_op1 == '+':
                a = 'ADD ' + str(matrix1[0][j][2]) + ', ' +  str(matrix2[j][i][2]) + ', ' + str(matrix2[j][i][2])
            elif cal_op1 == '-':
                a = 'SUB ' + str(matrix1[0][j][2]) + ', ' +  str(matrix2[j][i][2]) + ', ' + str(matrix2[j][i][2])
            elif cal_op1 == '*':
                a = 'MUL ' + str(matrix1[0][j][2]) + ', ' +  str(matrix2[j][i][2]) + ', ' + str(matrix2[j][i][2])
            elif cal_op1 == '#':
                a = 'MIN ' + str(matrix1[0][j][2]) + ', ' +  str(matrix2[j][i][2]) + ', ' + str(matrix2[j][i][2])
            elif cal_op1 == '$':
                a = 'MAX ' + str(matrix1[0][j][2]) + ', ' +  str(matrix2[j][i][2]) + ', ' + str(matrix2[j][i][2])                       
            elif cal_op1 == '&':
                a = 'BITAND ' + str(matrix1[0][j][2]) + ', ' +  str(matrix2[j][i][2]) + ', ' + str(matrix2[j][i][2])
            elif cal_op1 == '|':
                a = 'BITOR ' + str(matrix1[0][j][2]) + ', ' +  str(matrix2[j][i][2]) + ', ' + str(matrix2[j][i][2])
            elif cal_op1 == '^':
                a = 'XNOR ' + str(matrix1[0][j][2]) + ', ' +  str(matrix2[j][i][2]) + ', ' + str(matrix2[j][i][2])
            
            
            CAL_stage_assem.append(a)
        for j in range(len(matrix1[0])-1):
            if int(matrix2[j][i][2]/256)==int(matrix2[j+1][i][2]/256):
                c = 'PREREAD0 ' + str(matrix2[j][i][2]) +', 0, 0' 
                # d = 'PREREAD1 ' + '0, '+ str(matrix2[j+1][i][2]) +', 0'
                CAL_stage_assem.append(c)
                # CAL_stage_assem.append(d)

            if cal_op2 == '+':
                b = 'ADD ' + str(matrix2[j][i][2]) + ', ' +  str(matrix2[j+1][i][2]) + ', ' + str(matrix2[j+1][i][2])
            elif cal_op2 == '-':
                b = 'SUB ' + str(matrix2[j][i][2]) + ', ' +  str(matrix2[j+1][i][2]) + ', ' + str(matrix2[j+1][i][2])
            elif cal_op2 == '*':
                b = 'MUL ' + str(matrix2[j][i][2]) + ', ' +  str(matrix2[j+1][i][2]) + ', ' + str(matrix2[j+1][i][2])
            elif cal_op2 == '#':
                b = 'MIN ' + str(matrix2[j][i][2]) + ', ' +  str(matrix2[j+1][i][2]) + ', ' + str(matrix2[j+1][i][2])
            elif cal_op2 == '$':
                b = 'MAX ' + str(matrix2[j][i][2]) + ', ' +  str(matrix2[j+1][i][2]) + ', ' + str(matrix2[j+1][i][2])
            elif cal_op2 == '&':
                b = 'BITAND ' + str(matrix2[j][i][2]) + ', ' +  str(matrix2[j+1][i][2]) + ', ' + str(matrix2[j+1][i][2])
            elif cal_op2 == '|':
                b = 'BITOR ' + str(matrix2[j][i][2]) + ', ' +  str(matrix2[j+1][i][2]) + ', ' + str(matrix2[j+1][i][2])
            elif cal_op2 == '^':
                b = 'XNOR ' + str(matrix2[j][i][2]) + ', ' +  str(matrix2[j+1][i][2]) + ', ' + str(matrix2[j+1][i][2])


            CAL_stage_assem.append(b)
        result_addr.append(matrix2[len(matrix1[0])-1][i][2])
    return CAL_stage_assem, result_addr

def conflict_predict(PE1_num, addr1, PE2_num, addr2, PE2_start, exeblock_per_PE, cal_op1, cal_op2, bias, addr_occu):
 
    while(1):
        flag = 0
        for i in range(len(addr1)*(exeblock_per_PE)):
            if PE2_start+i+256-bias in addr_occu[int(PE2_num / exeblock_per_PE)]:
                PE2_start += 1
                flag = 1
        if flag == 0:
            break
    return PE2_start

def FLOW_stage(PE1_num, addr1, PE2_num, addr2, PE2_start, exeblock_per_PE, cal_op1, cal_op2, bias, addr_occu):
    FLOW_stage_assem1 = list()
    FLOW_stage_assem2 = list()
    result_addr2 = list()
    if int(PE1_num/exeblock_per_PE) == int(PE2_num/exeblock_per_PE):
        for i in range(len(addr1)):
            if int(addr2[i]/256) == int(addr1[i]/256):
                c = 'PREREAD0 ' + str(addr2[i]) +', 0, 0' 
                FLOW_stage_assem2.append(c)
            if cal_op2 == '+':
                b = 'ADD ' + str(addr2[i]) + ', ' + str(addr1[i]) + ', ' + str(addr2[i])
            elif cal_op2 == '-':
                b = 'SUB ' + str(addr2[i]) + ', ' + str(addr1[i]) + ', ' + str(addr2[i])
            elif cal_op2 == '*':
                b = 'MUL ' + str(addr2[i]) + ', ' + str(addr1[i]) + ', ' + str(addr2[i])
            elif cal_op2 == '#':
                b = 'MIN ' + str(addr2[i]) + ', ' + str(addr1[i]) + ', ' + str(addr2[i])
            elif cal_op2 == '$':
                b = 'MAX ' + str(addr2[i]) + ', ' + str(addr1[i]) + ', ' + str(addr2[i])
            elif cal_op2 == '&':
                b = 'BITAND ' + str(addr2[i]) + ', ' + str(addr1[i]) + ', ' + str(addr2[i])
            elif cal_op2 == '|':
                b = 'BITOR ' + str(addr2[i]) + ', ' + str(addr1[i]) + ', ' + str(addr2[i])
            elif cal_op2 == '^':
                b = 'XNOR ' + str(addr2[i]) + ', ' + str(addr1[i]) + ', ' + str(addr2[i])

            FLOW_stage_assem2.append(b)
            result_addr2.append(addr2[i])
        return FLOW_stage_assem1, FLOW_stage_assem2, result_addr2
    
    # for i in range(len(addr1)):
    #     while PE2_start+i+256-bias in addr_occu[int(PE2_num / exeblock_per_PE)]:
    #         PE2_start += 1
    
    # while(1):
    #     flag = 0
    #     for i in range(len(addr1)):
    #         if PE2_start+i+256-bias in addr_occu[int(PE2_num / exeblock_per_PE)]:
    #             PE2_start += 1
    #             flag = 1
    #     if flag == 0:
    #         break
    
    for i in range(len(addr1)):
        
        # if (PE2_start+i) < 192:
            
        #     a = 'COPY ' + str(addr1[i]) + ', ' + str(PE2_start+i) + ', ' + str(int(PE2_num / exeblock_per_PE))
        # else:
            
        #     a = 'COPY ' + str(addr1[i]) + ', ' + str(PE2_start+i-192+256) + ', ' + str(int(PE2_num / exeblock_per_PE))
        
        a = 'COPY ' + str(addr1[i]) + ', ' + str(PE2_start+i+256-bias) + ', ' + str(int(PE2_num / exeblock_per_PE))
        addr_occu[int(PE2_num / exeblock_per_PE)].append(PE2_start+i+256-bias)
        FLOW_stage_assem1.append(a)
        if(len(addr2)==0):
            #result_addr2.append(PE2_start+i)
            result_addr2.append(PE2_start+i+256-bias)

    for i in range(len(addr2)):
        # if PE2_start+i < 192:
        #     PE2_exe_addr = PE2_start+i
        # else:
        #     PE2_exe_addr = PE2_start+i-192+256
        PE2_exe_addr = PE2_start+i+256-bias
        if int(addr2[i]/256) == int(PE2_exe_addr/256):
            e = 'PREREAD0 ' + str(addr2[i]) +', 0, 0' 
            FLOW_stage_assem2.append(e)
        if cal_op2 == '+':
            b = 'ADD ' + str(addr2[i]) + ', ' + str(PE2_exe_addr) + ', ' + str(addr2[i])
        elif cal_op2 == '-':
            b = 'SUB ' + str(addr2[i]) + ', ' + str(PE2_exe_addr) + ', ' + str(addr2[i])
        elif cal_op2 == '*':
            b = 'MUL ' + str(addr2[i]) + ', ' + str(PE2_exe_addr) + ', ' + str(addr2[i])
        elif cal_op2 == '#':
            b = 'MIN ' + str(addr2[i]) + ', ' + str(PE2_exe_addr) + ', ' + str(addr2[i])
        elif cal_op2 == '$':
            b = 'MAX ' + str(addr2[i]) + ', ' + str(PE2_exe_addr) + ', ' + str(addr2[i])
        elif cal_op2 == '&':
            b = 'BITAND ' + str(addr2[i]) + ', ' + str(PE2_exe_addr) + ', ' + str(addr2[i])
        elif cal_op2 == '|':
            b = 'BITOR ' + str(addr2[i]) + ', ' + str(PE2_exe_addr) + ', ' + str(addr2[i])
        elif cal_op2 == '^':
            b = 'XNOR ' + str(addr2[i]) + ', ' + str(PE2_exe_addr) + ', ' + str(addr2[i])
        FLOW_stage_assem2.append(b)
        result_addr2.append(addr2[i])
    return FLOW_stage_assem1, FLOW_stage_assem2, result_addr2, addr_occu

def ST_stage(exeb_addr_table, dram_addr_start):
    ST_stage_assem = list()
    k = 0
    for i in exeb_addr_table:
        a = 'ST ' + str(i) + ', ' + '0' ', ' + str(dram_addr_start+k)
        ST_stage_assem.append(a)
        k += 1
    return ST_stage_assem

def Exeblock_init(assem, exeblock_no, PE_no, exeblock_per_PE, PE_num, data, bitmap, data_num, gen_no, fil_length, is_sparse):
    r = os.path.abspath(__file__)
    if is_sparse == 1:
        file = open(os.path.dirname(r)+'\\EXEBLOCK-INIT-SAMPLE.xml', encoding = 'utf-8')
    else:
        file = open(os.path.dirname(r)+'\\EXEBLOCK-INIT-SAMPLE_with_nosparse.xml', encoding = 'utf-8')
    try:
        all_xml = file.read()
    finally:
        file.close()
    xml_inf = xmltodict.parse(all_xml)
    xml_inf = xml_inf['exeblock']
    
    
    Inst_DRAM_Address = int(64 * 1024 *1024 / 8 / 4 / PE_num / 4 * (exeblock_no + PE_no * exeblock_per_PE ) / 4 + 1) * 4      #每一个exeblock的代码段分配分配给每个exeblock的一半
    inst_addr = Inst_DRAM_Address
    Starting_PC_loader = int(256) * (exeblock_no)
    # ST_Base, LD_Base = int(256 * 1024 *1024 / 8 / exeblock_per_PE / PE_num / 4 * (0 + PE_no * exeblock_per_PE) / 4  + 1) * 4 + 1024, int(256 * 1024 *1024 / 8 / exeblock_per_PE / PE_num / 4 * (0 + PE_no * exeblock_per_PE) / 4  + 1 ) * 4 + 1024     #数据段基地址在代码段之后，每个exeblock分配分配给每个exeblock的一半
    temp = int(64 * 1024 *1024 / 8 / 4 / PE_num / 4 * (0 + PE_no * exeblock_per_PE))
    if temp % 4!=0:
        temp = int(temp/4+1)*4
    LD_Base =  1024 + temp    #数据段基地址在代码段之后，每个exeblock分配分配给每个exeblock的一半
    temp = data_num * exeblock_per_PE
    if temp % 4!=0:
        temp = int(temp/4+1)*4
    #print(temp)
    ST_Base = LD_Base + temp
    if exeblock_no == 0:
        data.insert((data_num)*(exeblock_per_PE*PE_no)+(PE_no)+fil_length*PE_no, '//'+str(LD_Base)+'\n')
        #print((data_num)*(exeblock_per_PE*PE_no+exeblock_no)+(max(0, PE_no-1)))
    PE = PE_no
    Sparse = is_sparse  #启用稀疏功能
    Bitmap_Addr = LD_Base + 1024 + (exeblock_no % 4) * 4 + int(data_num/128) * 4
    Bitmap_length = int(data_num/32)
    if data_num%32!=0:
        Bitmap_length += 1
    if exeblock_no == 0:
        bitmap.insert((data_num)*(exeblock_per_PE*PE_no)+(PE_no), '//'+str(Bitmap_Addr)+'\n')
    R_N = 0     

    
    Need_Flow_Num = 0       
    Need_Flow_Index = int(opr_ext(xml_inf['Need_Flow_Index']['width'], 'max'), 2)
    ExeblockID = PE_no*exeblock_per_PE+exeblock_no

    # for i in range(int(exeblock_no/exeblock_per_PE)*exeblock_per_PE, exeblock_no):
    #     for k in range(len(assem[i])):
    #         Starting_PC_loader += len(assem[i][k])
    Ending_PC_ld, Starting_PC_ld, Ending_PC_loader = Starting_PC_loader,Starting_PC_loader,Starting_PC_loader
    Starting_PC_flow, Ending_PC_cal, Starting_PC_cal = Starting_PC_loader,Starting_PC_loader,Starting_PC_loader
    Ending_PC_st, Starting_PC_st, Ending_PC_flow = Starting_PC_loader,Starting_PC_loader,Starting_PC_loader
    for i in range(len(assem[exeblock_no + PE_no*exeblock_per_PE])):
        for j in range(len(assem[exeblock_no + PE_no*exeblock_per_PE][i])):
            if 'LD' in assem[exeblock_no + PE_no*exeblock_per_PE][i][j]:
                Ending_PC_ld += 1
                Starting_PC_flow += 1
                Ending_PC_flow += 1
                Starting_PC_cal += 1
                Ending_PC_cal += 1
                Starting_PC_st += 1
                Ending_PC_st += 1
                Ending_PC_loader += 1
            elif ('LD' not in assem[exeblock_no + PE_no*exeblock_per_PE][i][j]) and ('COPY' not in assem[exeblock_no + PE_no*exeblock_per_PE][i][j]) and ('ST' not in assem[exeblock_no + PE_no*exeblock_per_PE][i][j]):
                Ending_PC_cal += 1
                Starting_PC_flow += 1
                Ending_PC_flow += 1
                Starting_PC_st += 1
                Ending_PC_st += 1
                Ending_PC_loader += 1
            elif 'COPY' in assem[exeblock_no + PE_no*exeblock_per_PE][i][j]:
                Ending_PC_flow += 1
                Starting_PC_st += 1
                Ending_PC_st += 1
                Ending_PC_loader += 1
                
                # inst = re.split('[, ]+', assem[exeblock_no + PE_no*exeblock_per_PE][i][j])
                # Need_Flow_Index = min(Need_Flow_Index, int(inst[2]))
                # Need_Flow_Num += 1  
            else:
                Ending_PC_st += 1
                Ending_PC_loader += 1
            
    
    for i in assem:
        for j in i:
            for k in j:
                inst = re.split('[, ]+', k)
                
                if int(inst[3])==PE_no and exeblock_no==exeblock_per_PE-1 and inst[0] == 'COPY':
                    
                    Need_Flow_Index = min(Need_Flow_Index, int(inst[2]))
                    
                    Need_Flow_Num += 1                    

    b_inf = list('0' * int(xml_inf['bit_num']))
    b_num = int(xml_inf['bit_num'])-1
    if(xml_inf['Priority']!=None):
        #b_inf.insert(int(xml_inf['Priority']['start']), opr_ext(int(xml_inf['Priority']['width']), str(int(exeblock_no%exeblock_per_PE))))
        begin = b_num - int(xml_inf['Priority']['start'])
        end = int(xml_inf['Priority']['width']) + begin
        b_inf[begin:end] = opr_ext(int(xml_inf['Priority']['width']), str(int(exeblock_no%exeblock_per_PE)))
    
    if(xml_inf['Starting_PC_loader']!=None):
        #b_inf.insert(int(xml_inf['Starting_PC_loader']['start']), opr_ext(xml_inf['Starting_PC_loader']['width'], str(Starting_PC_loader)))
        begin = b_num - int(xml_inf['Starting_PC_loader']['start'])
        end = int(xml_inf['Starting_PC_loader']['width']) + begin
        b_inf[begin:end] = opr_ext(int(xml_inf['Starting_PC_loader']['width']), str(Starting_PC_loader))
    if(xml_inf['ST_Base']!=None):
        #b_inf.insert(int(xml_inf['ST_Base']['start']), opr_ext(xml_inf['ST_Base']['width'], str(ST_Base)))
        begin = b_num - int(xml_inf['ST_Base']['start'])
        end = int(xml_inf['ST_Base']['width']) + begin
        b_inf[begin:end] = opr_ext(int(xml_inf['ST_Base']['width']), str(ST_Base))
        
    if(xml_inf['LD_Base']!=None):
        #b_inf.insert(int(xml_inf['LD_Base']['start']), opr_ext(xml_inf['LD_Base']['width'], str(LD_Base)))
        begin = b_num - int(xml_inf['LD_Base']['start'])
        end = int(xml_inf['LD_Base']['width']) + begin
        b_inf[begin:end] = opr_ext(int(xml_inf['LD_Base']['width']), str(LD_Base))
    
    if(xml_inf['PE']!=None):
        #b_inf.insert(int(xml_inf['PE']['start']), opr_ext(xml_inf['PE']['width'], str(PE)))
        begin = b_num - int(xml_inf['PE']['start'])
        end = int(xml_inf['PE']['width']) + begin
        b_inf[begin:end] = opr_ext(int(xml_inf['PE']['width']), str(PE))

    if(xml_inf['Ending_PC_ld']!=None):
        #b_inf.insert(int(xml_inf['Ending_PC_ld']['start']), opr_ext(xml_inf['Ending_PC_ld']['width'], str(Ending_PC_ld)))
        begin = b_num - int(xml_inf['Ending_PC_ld']['start'])
        end = int(xml_inf['Ending_PC_ld']['width']) + begin
        b_inf[begin:end] = opr_ext(int(xml_inf['Ending_PC_ld']['width']), str(Ending_PC_ld))
    
    if(xml_inf['Starting_PC_ld']!=None):
        #b_inf.insert(int(xml_inf['Starting_PC_ld']['start']), opr_ext(xml_inf['Starting_PC_ld']['width'], str(Starting_PC_ld)))
        begin = b_num - int(xml_inf['Starting_PC_ld']['start'])
        end = int(xml_inf['Starting_PC_ld']['width']) + begin
        b_inf[begin:end] = opr_ext(int(xml_inf['Starting_PC_ld']['width']), str(Starting_PC_ld))
    
    if(xml_inf['Ending_PC_loader']!=None):
        #b_inf.insert(int(xml_inf['Ending_PC_loader']['start']), opr_ext(xml_inf['Ending_PC_loader']['width'], str(Ending_PC_loader)))
        begin = b_num - int(xml_inf['Ending_PC_loader']['start'])
        end = int(xml_inf['Ending_PC_loader']['width']) + begin
        b_inf[begin:end] = opr_ext(int(xml_inf['Ending_PC_loader']['width']), str(Ending_PC_loader))
    
    if(xml_inf['Starting_PC_flow']!=None):
        #b_inf.insert(int(xml_inf['Starting_PC_flow']['start']), opr_ext(xml_inf['Starting_PC_flow']['width'], str(Starting_PC_flow)))
        begin = b_num - int(xml_inf['Starting_PC_flow']['start'])
        end = int(xml_inf['Starting_PC_flow']['width']) + begin
        b_inf[begin:end] = opr_ext(int(xml_inf['Starting_PC_flow']['width']), str(Starting_PC_flow))
    
    if(xml_inf['Ending_PC_cal']!=None):
        #b_inf.insert(int(xml_inf['Ending_PC_cal']['start']), opr_ext(xml_inf['Ending_PC_cal']['width'], str(Ending_PC_cal)))
        begin = b_num - int(xml_inf['Ending_PC_cal']['start'])
        end = int(xml_inf['Ending_PC_cal']['width']) + begin
        b_inf[begin:end] = opr_ext(int(xml_inf['Ending_PC_cal']['width']), str(Ending_PC_cal))
    
    if(xml_inf['Starting_PC_cal']!=None):
        #b_inf.insert(int(xml_inf['Starting_PC_cal']['start']), opr_ext(xml_inf['Starting_PC_cal']['width'], str(Starting_PC_cal)))
        begin = b_num - int(xml_inf['Starting_PC_cal']['start'])
        end = int(xml_inf['Starting_PC_cal']['width']) + begin
        b_inf[begin:end] = opr_ext(int(xml_inf['Starting_PC_cal']['width']), str(Starting_PC_cal))
    
    if(xml_inf['Sparse']!=None):
        #b_inf.insert(int(xml_inf['Sparse']['start']), opr_ext(xml_inf['Sparse']['width'], str(Sparse)))
        begin = b_num - int(xml_inf['Sparse']['start'])
        end = int(xml_inf['Sparse']['width']) + begin
        b_inf[begin:end] = opr_ext(int(xml_inf['Sparse']['width']), str(Sparse))
    
    if(xml_inf['Ending_PC_st']!=None):
        #b_inf.insert(int(xml_inf['Ending_PC_st']['start']), opr_ext(xml_inf['Ending_PC_st']['width'], str(Ending_PC_st)))
        begin = b_num - int(xml_inf['Ending_PC_st']['start'])
        end = int(xml_inf['Ending_PC_st']['width']) + begin
        b_inf[begin:end] = opr_ext(int(xml_inf['Ending_PC_st']['width']), str(Ending_PC_st))
    
    if(xml_inf['Starting_PC_st']!=None):
        #b_inf.insert(int(xml_inf['Starting_PC_st']['start']), opr_ext(xml_inf['Starting_PC_st']['width'], str(Starting_PC_st)))
        begin = b_num - int(xml_inf['Starting_PC_st']['start'])
        end = int(xml_inf['Starting_PC_st']['width']) + begin
        b_inf[begin:end] = opr_ext(int(xml_inf['Starting_PC_st']['width']), str(Starting_PC_st))

    
    if(xml_inf['Ending_PC_flow']!=None):
        #b_inf.insert(int(xml_inf['Ending_PC_flow']['start']), opr_ext(xml_inf['Ending_PC_flow']['width'], str(Ending_PC_flow)))
        begin = b_num - int(xml_inf['Ending_PC_flow']['start'])
        end = int(xml_inf['Ending_PC_flow']['width']) + begin
        b_inf[begin:end] = opr_ext(int(xml_inf['Ending_PC_flow']['width']), str(Ending_PC_flow))

    
    if(xml_inf['Inst_DRAM_Address']!=None):
        #b_inf.insert(int(xml_inf['Inst_DRAM_Address']['start']), opr_ext(xml_inf['Inst_DRAM_Address']['width'], str(Inst_DRAM_Address)))
        begin = b_num - int(xml_inf['Inst_DRAM_Address']['start'])
        end = int(xml_inf['Inst_DRAM_Address']['width']) + begin
        b_inf[begin:end] = opr_ext(int(xml_inf['Inst_DRAM_Address']['width']), str(Inst_DRAM_Address))

    
    if(xml_inf['Need_Flow_Num']!=None):
        #b_inf.insert(int(xml_inf['Need_Flow_Num']['start']), opr_ext(xml_inf['Need_Flow_Num']['width'], str(Need_Flow_Num)))
        begin = b_num - int(xml_inf['Need_Flow_Num']['start'])
        end = int(xml_inf['Need_Flow_Num']['width']) + begin
        b_inf[begin:end] = opr_ext(int(xml_inf['Need_Flow_Num']['width']), str(Need_Flow_Num))

    
    if(xml_inf['Need_Flow_Index']!=None):
        #b_inf.insert(int(xml_inf['Need_Flow_Index']['start']), opr_ext(xml_inf['Need_Flow_Index']['width'], str(Need_Flow_Index)))
        begin = b_num - int(xml_inf['Need_Flow_Index']['start'])
        end = int(xml_inf['Need_Flow_Index']['width']) + begin
        b_inf[begin:end] = opr_ext(int(xml_inf['Need_Flow_Index']['width']), str(Need_Flow_Index))
    
    
    if(xml_inf['ExeblockID']!=None):
        #b_inf.insert(int(xml_inf['ExeblockID']['start']), opr_ext(xml_inf['ExeblockID']['width'], str(ExeblockID))   ) 
        begin = b_num - int(xml_inf['ExeblockID']['start'])
        end = int(xml_inf['ExeblockID']['width']) + begin
        b_inf[begin:end] = opr_ext(int(xml_inf['ExeblockID']['width']), str(ExeblockID))

    
    if(xml_inf['Reuse_Num']!=None):
        #b_inf.insert(int(xml_inf['Reuse_Num']['start']), opr_ext(xml_inf['Reuse_Num']['width'], str(R_N)) )
        begin = b_num - int(xml_inf['Reuse_Num']['start'])
        end = int(xml_inf['Reuse_Num']['width']) + begin
        b_inf[begin:end] = opr_ext(int(xml_inf['Reuse_Num']['width']), str(R_N))
    if is_sparse == 1:
        if(xml_inf['Bitmap_Addr']!=None):
            #b_inf.insert(int(xml_inf['Reuse_Num']['start']), opr_ext(xml_inf['Reuse_Num']['width'], str(R_N)) )
            begin = b_num - int(xml_inf['Bitmap_Addr']['start'])
            end = int(xml_inf['Bitmap_Addr']['width']) + begin
            b_inf[begin:end] = opr_ext(int(xml_inf['Bitmap_Addr']['width']), str(Bitmap_Addr))
        
        if(xml_inf['Bitmap_length']!=None):
            #b_inf.insert(int(xml_inf['Reuse_Num']['start']), opr_ext(xml_inf['Reuse_Num']['width'], str(R_N)) )
            begin = b_num - int(xml_inf['Bitmap_length']['start'])
            end = int(xml_inf['Bitmap_length']['width']) + begin
            b_inf[begin:end] = opr_ext(int(xml_inf['Bitmap_length']['width']), str(Bitmap_length))   
        
    temp = list()
    out_b_inf = list()
    for i in range(len(b_inf)):
        if(i%32!=31):
            temp.append(b_inf[i])
        else:
            temp.append(b_inf[i])
            temp.append('\n')
            out_b_inf.append(temp)
            temp = list()
    
    out_b_inf.reverse()
    inf = dict()
    
    inf['Starting_PC_loader'] = Starting_PC_loader
    inf['ST_Base'], inf['LD_Base'] = ST_Base, LD_Base
    inf['PE'] = PE
    inf['Sparse'] = Sparse
    inf['Reuse_Num'] =R_N
    inf['Inst_DRAM_Address'] = Inst_DRAM_Address
    inf['Need_Flow_Num'] = Need_Flow_Num
    inf['Need_Flow_Index'] =Need_Flow_Index
    inf['ExeblockID'] = ExeblockID
    if is_sparse == 1:
        inf['Bitmap_Addr'] = Bitmap_Addr
        inf['Bitmap_length'] = Bitmap_length
    
    inf['Starting_PC_loader'] = Starting_PC_loader
    inf['Ending_PC_ld'], inf['Starting_PC_ld'], inf['Ending_PC_loader'] = Ending_PC_ld,Starting_PC_ld,Ending_PC_loader
    inf['Starting_PC_flow'], inf['Ending_PC_cal'], inf['Starting_PC_cal'] = Starting_PC_flow,Ending_PC_cal,Starting_PC_cal
    inf['Ending_PC_st'], inf['Starting_PC_st'], inf['Ending_PC_flow'] = Ending_PC_st,Starting_PC_st,Ending_PC_flow
    
    inf.items()
    r = os.path.abspath(__file__)
    if os.path.exists(os.path.dirname(r)+'\\rg_gen\\tile'+str(gen_no))==0:
        os.mkdir(os.path.dirname(r)+'\\rg_gen\\tile'+str(gen_no))
    filename1 = os.path.dirname(r)+'\\rg_gen\\tile'+str(gen_no)+'\\b_exeblock' +str(PE_no)+ '_' + str(exeblock_no) + '.txt'
    filename2 = os.path.dirname(r)+'\\rg_gen\\tile'+str(gen_no)+'\\inf_exeblock' +str(PE_no)+ '_' + str(exeblock_no) + '.txt'
    output = open(filename1, 'w')
    output2 = open(filename2, 'w')
    try:
        for row in out_b_inf:
            output.writelines(row)
        writer = csv.writer(output2)
        for key, value in inf.items():
            
            writer.writerow([key, ' '+str(value)])
        
    finally:
        output.close()
        output2.close()
    
    if Ending_PC_loader - Starting_PC_loader > 256:
        print('Warning: instruction per exeblock is too long!')
        return 'error'
    return inst_addr
    
def gen(height1, width1, height2, width2, PE_num, exeblock_per_PE, min_data, max_data, op1, gen_no, cal_op1, cal_op2, vector_a, matrix_b, col_tiling, ld_vector_length, is_sparse):
    #PE_num = 8
    #PE_size = 12
    host_a = list()
    host_b = list()
    assem = list()
    PE_inter_result_addr = list()
    bitmap = list()
    
    matrix_a, value_a = matrix_gen(height1, width1,  min_data, max_data, 0, vector_a)
 
    matrix_b, value_b = matrix_gen(height2, width2, min_data, max_data, height1 * width1, matrix_b)
    tiling = 0
    while(tiling==0):
        tiling = int(width1 / (col_tiling[0] * exeblock_per_PE))  #每个exeblock要运算多少行
        if(tiling==0):
            PE_num -= 1
    matrix_a, matrix_b = dram_arrange(matrix_a, matrix_b, PE_num, col_tiling)
    #print(matrix_a)
    addr_occu = list()
    for pt in range(int(PE_num/col_tiling[0])):
        #PE_result_addr = list()
        t1_width, t2_height = 0, 0
        
        for i in range(pt*col_tiling[0], pt*col_tiling[0]+col_tiling[0]):
            exeblock_inter_result_addr = list()
            a = list()
            b = list()
            PE_a = list()
            PE_b = list()
            addr_occu_pe = list()
            for j in range(exeblock_per_PE):
                PE_assem = list()
                if len(a) ==0 and len(b)==0 :    
                    m, n = 0, 0
                    #t1_width, t2_height = 0, 0
                else:
                    m += len(a) * len(a[-1])
                    n += len(b) * len(b[-1])
                
                
                
                # a, v_a = matrix_gen(height1, width1, m, (height1*width1+height2*width2)*(i*exeblock_per_PE+j))
                # b, v_b = matrix_gen(height2, width2, height1*width1+512+n, (height1*width1+height2*width2)*(i*exeblock_per_PE+j)+(height1*width1))
                
                #a, v_a = matrix_gen(height1, width1, m, (height1*width1+height2*width2)*(j), min_data, max_data)
                #b, v_b = matrix_gen(height2, width2, height1*width1+512+n, (height1*width1+height2*width2)*(j)+(height1*width1), min_data, max_data)
                if t1_width+ 2 * tiling > width1:
                    a, v_a = tiling_gen1(matrix_a, value_a, t1_width, width1, height1, m, (tiling)*(j))
                    #b, v_b = tiling_gen2(matrix_b, value_b, t2_height, height2, width2, t1_width*height1+512+n, (height1*width1+height2*width2)*(j)+(height1*width1))
                    b, v_b = tiling_gen2(matrix_b, value_b, t2_height, height2, pt*col_tiling[1],pt*col_tiling[1]+col_tiling[1], 256+n, (height1*width1+height2*width2)*(j)+(height1*width1))
    
                else:
                    a, v_a = tiling_gen1(matrix_a, value_a, t1_width, t1_width+tiling, height1, m, (tiling)*(j))
                    #b, v_b = tiling_gen2(matrix_b, value_b, t2_height, t2_height+tiling, width2, t1_width*height1+512+n, (height1*width1+height2*width2)*(j)+(height1*width1))               
                    b, v_b = tiling_gen2(matrix_b, value_b, t2_height, t2_height+tiling, pt*col_tiling[1],pt*col_tiling[1]+col_tiling[1], 256+n, (height1*width1+height2*width2)*(j)+(height1*width1))                          
                t1_width += len(a[-1])
                t2_height += len(b)
                #print(b)
    
                PE_a += v_a
                #print(v_b)
                PE_b += v_b
                ta, addr_occu_a = LD_stage_A(a, bitmap)
                tb, addr_occu_b = LD_stage_B(b, bitmap)
                PE_assem.append(ta)
                PE_assem.append(tb)
                addr_occu_pe += addr_occu_a + addr_occu_b
                cal_assem, inter_result_addr = CAL_stage(a, b, cal_op1, cal_op2)    
                exeblock_inter_result_addr.append(inter_result_addr)
                PE_assem.append(cal_assem)
                assem.append(PE_assem)
            PE_inter_result_addr.append(exeblock_inter_result_addr)
            host_a.append(PE_a)
            host_b.append(PE_b)
            addr_occu.append(addr_occu_pe)
            
        data, host_r, fil_length = CPU_result(32, host_a, host_b)
        #print(pt)
        
        #print(PE_result_addr[-1])
        # min = 0
        # for j in range(0, int(math.log(PE_num, 2)), 1):
        #     #stride += k
        #     for i in range(min, PE_num, 2**(j+1)):
        #         if i + 2**j < PE_num:
        #             flow_assem1, flow_assem2, result_addr  = FLOW_stage(i, PE_inter_result_addr[i], i+2**j, PE_inter_result_addr[i+2**j], 0)
        #             #print(result_addr)
        #             assem[i].append(flow_assem1)
        #             assem[i+2**j].append(flow_assem2)
        #             #PE_result_addr.append(result_addr)
        #             Final_result_addr = result_addr
        #     min += 2**j
        #print(PE_inter_result_addr[-1])
        #assem[-1].append(ST_stage(Final_result_addr, 0))
        
        
        last_inter_result_addr = list()
        for i in range(pt*col_tiling[0], pt*col_tiling[0]+col_tiling[0]):
            final_in_pe_inter_result_addr = list()
            for j in range(exeblock_per_PE-1):
                
                flow_assem1, flow_assem2, result_addr = FLOW_stage(i*exeblock_per_PE+j, PE_inter_result_addr[i][j],(i+1)*exeblock_per_PE-1, PE_inter_result_addr[i][exeblock_per_PE-1], (j) * (len(PE_inter_result_addr[i][exeblock_per_PE-1])) + (len(a) * len(a[0]) + len(b)*len(b[0]) ), exeblock_per_PE, cal_op1, cal_op2, (len(a) * len(a[0]) + len(b)*len(b[0]) ), addr_occu )
                assem[i*exeblock_per_PE+j].append(flow_assem1)
                final_in_pe_inter_result_addr.append(result_addr)
                assem[(i+1)*exeblock_per_PE-1].append(flow_assem2)  
                
            #flow_assem1, flow_assem2, result_addr = FLOW_stage(None, [],(i+1)*exeblock_per_PE-1, PE_inter_result_addr[i][PE_num-1], len(a)*len(a[0])+len(b)*len(b[0])) #每个pe内部最后一个exeb负责前面的累加
            #assem[(i+1)*exeblock_per_PE-1].append(flow_assem2)    
            if i != pt*col_tiling[0]+col_tiling[0]-1:
                #此处final_in_pe_inter_result_addr[i-pt*col_tiling[0]]改为final_in_pe_inter_result_addr[-1]待测试
                if i == pt*col_tiling[0]:
                    PE2_start = conflict_predict((i+1)*exeblock_per_PE-1, final_in_pe_inter_result_addr[-1],(pt*col_tiling[0]+col_tiling[0])*exeblock_per_PE-1, PE_inter_result_addr[pt*col_tiling[0]+col_tiling[0]-1][exeblock_per_PE-1], i*len(final_in_pe_inter_result_addr[-1]) + (exeblock_per_PE-1) * (len(PE_inter_result_addr[i][exeblock_per_PE-1])) + (len(a) * len(a[0]) + len(b)*len(b[0]) ), exeblock_per_PE, cal_op1, cal_op2, (exeblock_per_PE-1) * (len(PE_inter_result_addr[0][exeblock_per_PE-1])) + (len(a) * len(a[0]) + len(b)*len(b[0]) ), addr_occu)
                    flow_assem1, flow_assem2, result_addr, addr_occu = FLOW_stage((i+1)*exeblock_per_PE-1, final_in_pe_inter_result_addr[-1],(pt*col_tiling[0]+col_tiling[0])*exeblock_per_PE-1, PE_inter_result_addr[pt*col_tiling[0]+col_tiling[0]-1][exeblock_per_PE-1], PE2_start, exeblock_per_PE, cal_op1, cal_op2, (exeblock_per_PE-1) * (len(PE_inter_result_addr[0][exeblock_per_PE-1])) + (len(a) * len(a[0]) + len(b)*len(b[0]) ), addr_occu) #每个pe内部最后一个exeb负责将结果数据copy到最最后一个exeb
                else:
                    flow_assem1, flow_assem2, result_addr, addr_occu = FLOW_stage((i+1)*exeblock_per_PE-1, final_in_pe_inter_result_addr[-1],(pt*col_tiling[0]+col_tiling[0])*exeblock_per_PE-1, PE_inter_result_addr[pt*col_tiling[0]+col_tiling[0]-1][exeblock_per_PE-1], PE2_start+(i-pt*col_tiling[0]) * (len(PE_inter_result_addr[i][exeblock_per_PE-1])), exeblock_per_PE, cal_op1, cal_op2, (exeblock_per_PE-1) * (len(PE_inter_result_addr[0][exeblock_per_PE-1])) + (len(a) * len(a[0]) + len(b)*len(b[0]) ), addr_occu) #每个pe内部最后一个exeb负责将结果数据copy到最最后一个exeb
                assem[(i+1)*exeblock_per_PE-1].append(flow_assem1)
                assem[(pt*col_tiling[0]+col_tiling[0])*exeblock_per_PE-1].append(flow_assem2)
                last_inter_result_addr += result_addr
                
        last_inter_result_addr = sorted(list(set(last_inter_result_addr)))
        assem[-1].append(ST_stage(last_inter_result_addr, 0))
        #print(last_inter_result_addr)
    
    inst_addr_list = list()
    for i in range(PE_num):     
        for j in range(exeblock_per_PE):                
            temp = Exeblock_init(assem,  j, i, exeblock_per_PE, PE_num, data, bitmap, (tiling+height2%tiling)*(height1+col_tiling[1]), gen_no, fil_length, is_sparse)  
            inst_addr_list.append(temp)
            
    r = os.path.abspath(__file__)        
    if os.path.exists(os.path.dirname(r)+'\\rg_gen\\tile'+str(gen_no))==0:
        os.mkdir(os.path.dirname(r)+'\\rg_gen\\tile'+str(gen_no))
    output = open(os.path.dirname(r)+'\\rg_gen\\tile'+str(gen_no)+'\\assem_inst'+'.txt', 'w')
    count=-1
    try:
        for i in assem: 
            count += 1
            #print('#PE'+str(count)+':')
            str1 = '#EXEBLOCK'+str(count)+':'+'\n'
            output.writelines([str1])
            output.writelines('//'+str(inst_addr_list[count])+'\n')
            for j in i:
                for k in j:
                   # print(k)
                   str2 = k+'\n'
                   output.writelines([str2])
    finally:
        output.close()
        
    host_r = [x+'\n' for x in host_r]
    r = os.path.abspath(__file__)    
    data_filename = open(os.path.dirname(r)+'\\rg_gen\\tile'+str(gen_no)+'\\data'+'.txt', 'w')
    result_filename = open(os.path.dirname(r)+'\\rg_gen\\tile'+str(gen_no)+'\\result'+'.txt', 'w')
    bitmap_filename = open(os.path.dirname(r)+'\\rg_gen\\tile'+str(gen_no)+'\\bitmap'+'.txt', 'w')
    try:
        data_filename.writelines(data)
        result_filename.writelines(host_r)
        bitmap_filename.writelines(bitmap)
    finally:
        data_filename.close()
        result_filename.close()
        bitmap_filename.close()
        
def main(res):
    expression = res['Expression']
    op = re.findall(r"[A-z]", expression)
    op1 = []
    for i in range(len(op)-1):
        
        r = os.path.abspath(__file__)        
        if os.path.exists(os.path.dirname(r)+'\\rg_gen')==0:
            os.mkdir(os.path.dirname(r)+'\\rg_gen')
        
        PE_num = res[str(i+1)]['PE_num']
        exeblock_per_PE = res[str(i+1)]['exeblock_per_PE']
        col_tiling = res[str(i+1)]['column_tiling']
        m1_height = res[str(i+1)]['m1_height']
        m1_width = res[str(i+1)]['m1_width']
        m2_height = res[str(i+1)]['m2_height']
        m2_width = res[str(i+1)]['m2_width']
        min_data = res[str(i+1)]['min_data']
        max_data = res[str(i+1)]['max_data']
        is_sparse = res[str(i+1)]['sparse']
        vector_a = res[str(i+1)][op[0]]
        matrix_b = res[str(i+1)][op[1]]
        vector_a = read_matrix(vector_a)
        matrix_b = read_matrix(matrix_b)
        MB = np.array(matrix_b)
        
                
        col_tiling = [int(x) for x in col_tiling.split(',')]
        tile = int(PE_num/col_tiling[0]*col_tiling[1])
        reload_num = int(m2_height/(PE_num/col_tiling[0]*col_tiling[1]))
        for j in range(reload_num):
            for k in range(reload_num):
                vector_a_t = list()
                matrix_b_t = list()
                vector_a_t.append(vector_a[0][(j)*tile:(j+1)*(tile)])
                matrix_b_t = (MB[j*tile:(j+1)*(tile), k*tile:(k+1)*tile].tolist())
                #print(vector_a_t)
                #print(matrix_b_t)
                gen(1, tile, tile, tile, PE_num, exeblock_per_PE, min_data, max_data, op1, j*reload_num+k, expression[1], expression[2], vector_a_t, matrix_b_t, col_tiling, int(m1_width/PE_num/exeblock_per_PE), is_sparse) #op1表示当连续运算时的前一个操作数向量


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..\\..') + '\\pe_module.json', "r") as f:
        res = json.load(f)
        main(res)