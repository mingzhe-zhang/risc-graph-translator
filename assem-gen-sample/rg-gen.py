import math
import random

def matrix_gen(height: int, width: int, exeb_size: int, exeb_start: int, dram_start: int):
    a = list()
    k = 0
    for i in range(height):
        array = list()
        for j in range(width):
            value = random.randint(0, 1)
            dram_addr = k + dram_start
            exeb_addr = k + exeb_start
            x = (value, dram_addr, exeb_addr)
            #print(x)
            array.append(x)
            k += 1
        a.append(array)
    return a
        
def LD_stage(matrix):
    LD_stage_assem = list()
    for array in matrix:
        for x in array:
            a = 'LD ' + str(x[2]) + ', ' + '0, ' + str(x[1])
            LD_stage_assem.append(a)
    return LD_stage_assem

def CAL_stage(matrix1, matrix2):
    CAL_stage_assem = list()
    result_addr = list()
    for i in range(len(matrix2[0])):
        for j in range(len(matrix1[0])):
            a = 'MUL ' + str(matrix1[0][j][2]) + ', ' +  str(matrix2[i][len(matrix1[0])-j-1][2]) + ', ' + str(matrix2[i][len(matrix1[0])-j-1][2])
            CAL_stage_assem.append(a)
        for j in range(len(matrix1[0])-1):
            b = 'ADD ' + str(matrix2[i][j][2]) + ', ' +  str(matrix2[i][j+1][2]) + ', ' + str(matrix2[i][j+1][2])
            CAL_stage_assem.append(b)
        result_addr.append(matrix2[i][len(matrix1[0])-1][2])
    return CAL_stage_assem, result_addr

def FLOW_stage(PE1_num, addr1, PE2_num, addr2, PE2_start):
    FLOW_stage_assem1 = list()
    FLOW_stage_assem2 = list()
    result_addr2 = list()
    for i in range(len(addr1)):
        a = 'COPY ' + str(addr1[i]) + ', ' + str(PE2_start+i) + ', ' + str(PE2_num)
        FLOW_stage_assem1.append(a)
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

def main(height1, width1, height2, width2, PE_num, PE_size):
    #PE_num = 8
    #PE_size = 12
    assem = list()
    PE_inter_result_addr = list()
    #PE_result_addr = list()
    for i in range(PE_num):
        PE_assem = list()
        a = matrix_gen(height1, width1, PE_size, 0, 2*i)
        b = matrix_gen(height2, width2, PE_size, height1*width1, 2*i+height1*width1)
        PE_assem.append(LD_stage(a))
        PE_assem.append(LD_stage(b))
        cal_assem, inter_result_addr = CAL_stage(a, b)    
        PE_inter_result_addr.append(inter_result_addr)
        PE_assem.append(cal_assem)
        assem.append(PE_assem)
        
    #print(PE_result_addr[-1])
    min = 0
    for j in range(0, int(math.log(PE_num, 2)), 1):
        #stride += k
        for i in range(min, PE_num, 2**(j+1)):
            if i + 2**j < PE_num:
                flow_assem1, flow_assem2, result_addr  = FLOW_stage(i, PE_inter_result_addr[i], i+2**j, PE_inter_result_addr[i+2**j], 0)
                #print(result_addr)
                assem[i].append(flow_assem1)
                assem[i+2**j].append(flow_assem2)
                #PE_result_addr.append(result_addr)
                Final_result_addr = result_addr
        min += 2**j
    #print(PE_inter_result_addr[-1])
    assem[-1].append(ST_stage(Final_result_addr, 0))
    
    output = open('assem_inst.txt', 'w')
    count=-1
    try:
        for i in assem: 
            count += 1
            #print('#PE'+str(count)+':')
            str1 = '#PE'+str(count)+':'+'\n'
            output.writelines([str1])
            for j in i:
                for k in j:
                   # print(k)
                   str2 = k+'\n'
                   output.writelines([str2])
    finally:
        output.close()
        

if __name__ == "__main__":
    PE_num = 8
    PE_size = 12
    m1_height = 1
    m1_width = 3
    m2_height = m1_width
    m2_width = 3
    main(m1_height, m2_height, m2_height, m2_width, PE_num, PE_size)
