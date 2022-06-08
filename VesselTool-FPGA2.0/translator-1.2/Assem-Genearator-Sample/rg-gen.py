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

def CPU_result(data_width, host_a, host_b):
    data = list()
    r = np.zeros(shape=(1, len(host_b[0][0])))
    for i in range(len(host_a)):
        a = np.array(host_a[i])
        b = np.array(host_b[i])
        c = np.dot(a, b)
        data.append(host_a[i]+host_b[i])
        r += c
    return [str(opr_ext(data_width, str(z)))+'\n' for m in data for n in m for z in n], [str(int(x))+' ' for x in r[0]]
        

def matrix_gen(height: int, width: int, exeb_start: int, dram_start: int, min_data: int, max_data: int):
    a = list()
    v_a = list()
    k = 0
    for i in range(height):
        array = list()
        v_array = list()
        for j in range(width):
            value = random.randint(min_data, max_data)
            dram_addr = k + dram_start
            exeb_addr = k + exeb_start
            if exeb_addr % 256 >= 192:
                x = [value, dram_addr, exeb_addr+256-192]
            else:
                x = [value, dram_addr, exeb_addr]
            
            #print(x)
            array.append(x)
            v_array.append(value)
            k += 1
        a.append(array)
        v_a.append(v_array)
    return a, v_a
        
def LD_stage(matrix):
    LD_stage_assem = list()
    count = 0
    for array in matrix:
        for x in array:
            a = 'LD ' + str(x[2]) + ', ' + '0, ' + str(x[1])
            LD_stage_assem.append(a)
            count += 1
    return LD_stage_assem

def CAL_stage(matrix1, matrix2):
    CAL_stage_assem = list()
    result_addr = list()
    for i in range(len(matrix2[0])):
        for j in range(len(matrix1[0])):
            
            if int(matrix1[0][j][2]/256)==int(matrix2[len(matrix1[0])-j-1][i][2]/256):
                c = 'PREREAD0 ' + str(matrix1[0][j][2]) +', 0, 0' 
                # d = 'PREREAD1 ' + '0, '+ str(matrix2[len(matrix1[0])-j-1][i][2]) +', 0'
                CAL_stage_assem.append(c)
                # CAL_stage_assem.append(d)
            a = 'MUL ' + str(matrix1[0][j][2]) + ', ' +  str(matrix2[j][i][2]) + ', ' + str(matrix2[j][i][2])
            CAL_stage_assem.append(a)
        for j in range(len(matrix1[0])-1):
            if int(matrix2[j][i][2]/256)==int(matrix2[j+1][i][2]/256):
                c = 'PREREAD0 ' + str(matrix2[j][i][2]) +', 0, 0' 
                # d = 'PREREAD1 ' + '0, '+ str(matrix2[j+1][i][2]) +', 0'
                CAL_stage_assem.append(c)
                # CAL_stage_assem.append(d)
            b = 'ADD ' + str(matrix2[j][i][2]) + ', ' +  str(matrix2[j+1][i][2]) + ', ' + str(matrix2[j+1][i][2])
            CAL_stage_assem.append(b)
        result_addr.append(matrix2[len(matrix1[0])-1][i][2])
    return CAL_stage_assem, result_addr

def FLOW_stage(PE1_num, addr1, PE2_num, addr2, PE2_start, exeblock_per_PE):
    FLOW_stage_assem1 = list()
    FLOW_stage_assem2 = list()
    result_addr2 = list()
    if int(PE1_num/exeblock_per_PE) == int(PE2_num/exeblock_per_PE):
        for i in range(len(addr1)):
            if int(addr2[i]/256) == int(addr1[i]/256):
                c = 'PREREAD0 ' + str(addr2[i]) +', 0, 0' 
                FLOW_stage_assem2.append(c)
            b = 'ADD ' + str(addr2[i]) + ', ' + str(addr1[i]) + ', ' + str(addr2[i])
            FLOW_stage_assem2.append(b)
            result_addr2.append(addr2[i])
        return FLOW_stage_assem1, FLOW_stage_assem2, result_addr2
    for i in range(len(addr1)):
        a = 'COPY ' + str(addr1[i]) + ', ' + str(PE2_start+i) + ', ' + str(int(PE2_num / exeblock_per_PE))
        FLOW_stage_assem1.append(a)
        if(len(addr2)==0):
            result_addr2.append(PE2_start+i)
    for i in range(len(addr2)):
        b = 'ADD ' + str(addr2[i]) + ', ' + str(PE2_start+i) + ', ' + str(addr2[i])
        FLOW_stage_assem2.append(b)
        result_addr2.append(addr2[i])
    return FLOW_stage_assem1, FLOW_stage_assem2, result_addr2

def ST_stage(exeb_addr_table, dram_addr_start):
    ST_stage_assem = list()
    k = 0
    for i in exeb_addr_table:
        a = 'ST ' + str(i) + ', ' + '0' ', ' + str(dram_addr_start+k)
        ST_stage_assem.append(a)
        k += 1
    return ST_stage_assem

def Exeblock_init(assem, exeblock_no, PE_no, exeblock_per_PE, PE_num, data, data_num):
    r = os.path.abspath(__file__)
    file = open(os.path.dirname(r)+'\\EXEBLOCK-INIT-SAMPLE.xml', encoding = 'utf-8')
    try:
        all_xml = file.read()
    finally:
        file.close()
    xml_inf = xmltodict.parse(all_xml)
    xml_inf = xml_inf['exeblock']
    
    
    Inst_DRAM_Address = int(64 * 1024 *1024 / 8 / exeblock_per_PE / PE_num / 4 * (exeblock_no + PE_no * exeblock_per_PE ) / 4 + 1) * 4      #每一个exeblock的代码段分配分配给每个exeblock的一半
    inst_addr = Inst_DRAM_Address
    Starting_PC_loader = int(256) * (exeblock_no)
    # ST_Base, LD_Base = int(256 * 1024 *1024 / 8 / exeblock_per_PE / PE_num / 4 * (0 + PE_no * exeblock_per_PE) / 4  + 1) * 4 + 1024, int(256 * 1024 *1024 / 8 / exeblock_per_PE / PE_num / 4 * (0 + PE_no * exeblock_per_PE) / 4  + 1 ) * 4 + 1024     #数据段基地址在代码段之后，每个exeblock分配分配给每个exeblock的一半
    LD_Base, ST_Base = int(64 * 1024 *1024 / 8 / exeblock_per_PE / PE_num / 4 * (0 + PE_no * exeblock_per_PE) / 4  + 1) * 4 + 1024, 0    #数据段基地址在代码段之后，每个exeblock分配分配给每个exeblock的一半，ST地址默认从0开始

    if exeblock_no == 0:
        data.insert((data_num)*(exeblock_per_PE*PE_no)+(PE_no), '//'+str(LD_Base)+'\n')
        #print((data_num)*(exeblock_per_PE*PE_no+exeblock_no)+(max(0, PE_no-1)))
    PE = PE_no
    Sparse = 0
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
 
    inf['Starting_PC_loader'] = Starting_PC_loader
    inf['Ending_PC_ld'], inf['Starting_PC_ld'], inf['Ending_PC_loader'] = Ending_PC_ld,Starting_PC_ld,Ending_PC_loader
    inf['Starting_PC_flow'], inf['Ending_PC_cal'], inf['Starting_PC_cal'] = Starting_PC_flow,Ending_PC_cal,Starting_PC_cal
    inf['Ending_PC_st'], inf['Starting_PC_st'], inf['Ending_PC_flow'] = Ending_PC_st,Starting_PC_st,Ending_PC_flow
    
    inf.items()
    r = os.path.abspath(__file__)
    filename1 = os.path.dirname(r)+'\\b_exeblock'+str(PE_no)+ '_' + str(exeblock_no) + '.txt'
    filename2 = os.path.dirname(r)+'\\inf_exeblock' +str(PE_no)+ '_' + str(exeblock_no) + '.txt'
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
    return inst_addr
    
def main(height1, width1, height2, width2, PE_num, exeblock_per_PE, min_data, max_data):
    #PE_num = 8
    #PE_size = 12
    host_a = list()
    host_b = list()
    assem = list()
    PE_inter_result_addr = list()
    #PE_result_addr = list()
    for i in range(PE_num):
        exeblock_inter_result_addr = list()
        a = list()
        b = list()
        for j in range(exeblock_per_PE):
            PE_assem = list()
            if len(a) ==0 and len(b)==0 :    
                m, n = 0, 0
            else:
                m += len(a) * len(a[-1])
                n += len(b) * len(b[-1])
            
            # a, v_a = matrix_gen(height1, width1, m, (height1*width1+height2*width2)*(i*exeblock_per_PE+j))
            # b, v_b = matrix_gen(height2, width2, height1*width1+512+n, (height1*width1+height2*width2)*(i*exeblock_per_PE+j)+(height1*width1))
            
            a, v_a = matrix_gen(height1, width1, m, (height1*width1+height2*width2)*(j), min_data, max_data)
            b, v_b = matrix_gen(height2, width2, height1*width1+512+n, (height1*width1+height2*width2)*(j)+(height1*width1), min_data, max_data)
            
            
            host_a.append(v_a)
            host_b.append(v_b)
            PE_assem.append(LD_stage(a))
            PE_assem.append(LD_stage(b))
            cal_assem, inter_result_addr = CAL_stage(a, b)    
            exeblock_inter_result_addr.append(inter_result_addr)
            PE_assem.append(cal_assem)
            assem.append(PE_assem)
        PE_inter_result_addr.append(exeblock_inter_result_addr)
    data, host_r = CPU_result(32, host_a, host_b)

    
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
    
    final_in_pe_inter_result_addr = list()
    last_inter_result_addr = list()
    for i in range(PE_num):
        
        for j in range(exeblock_per_PE-1):
            flow_assem1, flow_assem2, result_addr = FLOW_stage(i*exeblock_per_PE+j, PE_inter_result_addr[i][j],(i+1)*exeblock_per_PE-1, PE_inter_result_addr[i][exeblock_per_PE-1], (j) * (len(PE_inter_result_addr[i][exeblock_per_PE-1])) + (len(a) * len(a[0]) + len(b)*len(b[0]) ), exeblock_per_PE )
            assem[i*exeblock_per_PE+j].append(flow_assem1)
            final_in_pe_inter_result_addr.append(result_addr)
            assem[(i+1)*exeblock_per_PE-1].append(flow_assem2)  
            
        #flow_assem1, flow_assem2, result_addr = FLOW_stage(None, [],(i+1)*exeblock_per_PE-1, PE_inter_result_addr[i][PE_num-1], len(a)*len(a[0])+len(b)*len(b[0])) #每个pe内部最后一个exeb负责前面的累加
        #assem[(i+1)*exeblock_per_PE-1].append(flow_assem2)    
        if i != PE_num-1:
            flow_assem1, flow_assem2, result_addr = FLOW_stage((i+1)*exeblock_per_PE-1, final_in_pe_inter_result_addr[i],(PE_num)*exeblock_per_PE-1, PE_inter_result_addr[PE_num-1][exeblock_per_PE-1], i*len(final_in_pe_inter_result_addr[i]) + (exeblock_per_PE-1) * (len(PE_inter_result_addr[i][exeblock_per_PE-1])) + (len(a) * len(a[0]) + len(b)*len(b[0]) ), exeblock_per_PE) #每个pe内部最后一个exeb负责将结果数据copy到最最后一个exeb
            assem[(i+1)*exeblock_per_PE-1].append(flow_assem1)
            assem[(PE_num)*exeblock_per_PE-1].append(flow_assem2)
            last_inter_result_addr += result_addr
            
    last_inter_result_addr = sorted(list(set(last_inter_result_addr)))
    assem[-1].append(ST_stage(last_inter_result_addr, 0))
    #print(last_inter_result_addr)
    
    inst_addr_list = list()
    for i in range(PE_num):     
        for j in range(exeblock_per_PE):
            temp = Exeblock_init(assem,  j, i, exeblock_per_PE, PE_num, data, m1_height*m2_height + m2_height*m2_width)  
            inst_addr_list.append(temp)
            
    r = os.path.abspath(__file__)            
    output = open(os.path.dirname(r)+'\\assem_inst.txt', 'w')
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
    data_filename = open(os.path.dirname(r)+'\\data.txt', 'w')
    result_filename = open(os.path.dirname(r)+'\\result.txt', 'w')
    try:
        data_filename.writelines(data)
        result_filename.writelines(host_r)
    finally:
        data_filename.close()
        result_filename.close()
        


if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..\\..') + '\\pe_module.json', "r") as f:
        res = json.load(f)
    PE_num = res['PE_num']
    exeblock_per_PE = res['exeblock_per_PE']
    m1_height = res['m1_height']
    m1_width = res['m1_width']
    m2_height = res['m2_height']
    m2_width = res['m2_width']
    min_data = res['min_data']
    max_data = res['max_data']
    main(m1_height, m2_height, m2_height, m2_width, PE_num, exeblock_per_PE, min_data, max_data)
