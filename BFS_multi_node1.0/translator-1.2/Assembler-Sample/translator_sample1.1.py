import xmltodict
import re
import sys
import os
from optparse import OptionParser

#操作数位扩展函数，支持十六、十、八、二进制
def opr_ext(width, f):
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
    e_r = '0' * (int(width)-len(r)) + r
    return e_r

#翻译函数，默认isa定义的xml文件以及对应指令集表的xml文件
def translator(filename, isa_def_filename=os.path.dirname(os.path.abspath(__file__))+'\\risc-graph-isa-def1.1.xml', inst_table_filename=os.path.dirname(os.path.abspath(__file__))+'\\risc-graph-inst-table.xml'):
    #file = open('risc-graph-isa-def.xml', encoding = 'utf-8')
    file = open(isa_def_filename, encoding = 'utf-8')
    try:
        all_xml = file.read()
    finally:
        file.close()
        
    #file2 = open('risc-graph-inst-table.xml', encoding = 'utf-8')
    file2 = open(inst_table_filename, encoding = 'utf-8')
    try:
        inst_table_xml = file2.read()
    finally:
        file2.close()
        
    file3 = open(filename, encoding = 'utf-8')
    try:
        inst_list = file3.readlines()
    finally:
        file3.close()
        
    inst_list = [x.rstrip('\n') for x in inst_list]
    b_inst_list = list()
    
    
    
    isa_ = xmltodict.parse(all_xml)
    inst_table = xmltodict.parse(inst_table_xml)
    isa_def = isa_['risc-graph']['inst']
    
    
    

    #print(isa_def[int(inst_table['inst-table'][a]['num'])])
    #print(result['risc-graph']['inst'])
        
    for inst in inst_list:
        if '#' in inst :
            b_inst = inst.replace('#', '//')
            b_inst += '\n'
            #binary_inst = ''.join(b_inst)
            #b_inst_list.append(b_inst)
        elif '//' in inst:
            b_inst_list.append(inst+'\n')
        else:
            inst_width = int(isa_def[0]['op']['start'])                             #指令最高位位置
            inst = re.split('[, ]+', inst)  #分隔符为逗号或空格
            b_inst = list()     #当前指令二进制形式
            num = int(inst_table['inst-table'][inst[0]]['num'])
            
    
            
            opt = inst[0]       #操作符
            
            F0 = inst[1]        #操作数F0
            
            F1 = inst[2]        #操作数F1
            
            F2 = inst[3]        #操作数F2
            
            b_inst = list()     #当前指令二进制形式
            
            num = int(inst_table['inst-table'][opt]['num'])
            
            b_opt = isa_def[num]['op']['bin']
            b_inst.insert(inst_width - int(isa_def[num]['op']['start']), b_opt)
            
            b_F0 = opr_ext(isa_def[num]['F0']['width'], F0)
            b_inst.insert(inst_width - int(isa_def[num]['F0']['start']), b_F0)
            
            b_F1 = opr_ext(isa_def[num]['F1']['width'], F1)
            b_inst.insert(inst_width - int(isa_def[num]['F1']['start']), b_F1)
            
            b_F2 = opr_ext(isa_def[num]['F2']['width'], F2)
            b_inst.insert(inst_width - int(isa_def[num]['F2']['start']), b_F2)
            
            k = 0
            keys = isa_def[num]['ctrl'].keys()
            keys = list(keys)
            
            for k in range(len(keys)):
                if k + 4 >= len(inst):
                    b_inst.insert(inst_width - int(isa_def[num]['ctrl'][keys[k]]['start']), '0'*int(isa_def[num]['ctrl'][keys[k]]['width']))
                    k += 1
                else:
                    ctrl = inst[k+4]
                    b_ctrl = opr_ext(int(isa_def[num]['ctrl'][keys[k]]['width']), ctrl)
                    #print(ctrl)
                    #print(b_ctrl)
                    b_inst.insert(inst_width - int(isa_def[num]['ctrl'][keys[k]]['start']), b_ctrl)
                    k += 1
            
            # for i in range(4, len(inst)):
            #     ctrl = inst[i]
            #     b_ctrl = opr_ext(int(isa_def[num]['ctrl'][keys[k]]['width']), ctrl)
            #     b_inst.insert(inst_width - int(isa_def[num]['ctrl'][keys[k]]['start']), b_ctrl)
            #     k += 1
            # if(len(inst) == 5):                     #如果ctrl域的所有操作数被写在一个操作数里
            #     ctrl = inst[4]
            #     width = int(isa_def[num]['ctrl']['sparse_pc_inc']['width']) + int(isa_def[num]['ctrl']['in-dram-lookup-type']['width'])
            #     b_ctrl = opr_ext(width, ctrl)
            #     b_inst.insert(inst_width - int(isa_def[num]['ctrl']['sparse_pc_inc']['start']), b_ctrl)
            # else:
            #     sparse_pc_inc = inst[4]
            #     b_sparse_pc_inc = opr_ext(int(isa_def[num]['ctrl']['sparse_pc_inc']['width']), sparse_pc_inc)
            #     b_inst.insert(inst_width - int(isa_def[num]['ctrl']['sparse_pc_inc']['start']), b_sparse_pc_inc)
                
            #     in_dram_lookup_type = inst[5]
            #     b_in_dram_lookup_type = opr_ext(int(isa_def[num]['ctrl']['in-dram-lookup-type']['width']), in_dram_lookup_type)
            #     b_inst.insert(inst_width - int(isa_def[num]['ctrl']['in-dram-lookup-type']['start']), b_in_dram_lookup_type)
            
            b_inst += '\n'
            binary_inst = ''.join(b_inst)
            binary_inst = list(binary_inst)
            binary_inst.insert(16, '\n')
            binary_inst = ''.join(binary_inst)
            b_inst_list.append(binary_inst)
    return b_inst_list

def main(filename, output_filename):
    dir_list = os.listdir(filename)
    for x in dir_list:
        if 'tile' in x:
            inst_list = translator(filename+'\\'+x+'\\assem_inst.txt')
            #output = open('binary_inst.txt', 'w')   #默认输出文件
            output = open(output_filename+'\\'+x+'\\pe_code.txt', 'w')
            try:
                output.writelines(inst_list)
            finally:
                output.close()

if __name__ == "__main__":
#    if(len(sys.argv) < 2):
#        main('insts.txt')   #默认输入文件
#    else:
#        main(sys.argv[1])   #需要从命令行输入文件名

    parser = OptionParser()
    parser.add_option("-o", "--output", dest="out_filename",
                      help="write to output OUT_FILE", metavar="OUT_FILE")
    parser.add_option("-i", "--input", dest="in_filename",
                      help="read from input IN_FILE", metavar="OUT_FILE")
    
    (options, args) = parser.parse_args()
    if(options.in_filename!=None and options.out_filename!=None):
        main(options.in_filename, options.out_filename)
    else:
        main(os.path.dirname(os.path.abspath(__file__))+'\\rg_gen', os.path.dirname(os.path.abspath(__file__))+'\\rg_gen')    #默认输入输出文件
    