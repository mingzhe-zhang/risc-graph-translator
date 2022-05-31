import json
import os

with open(os.path.dirname(os.path.abspath(__file__)) + '\\pe_module_input.json', "r") as f:
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

tile_num = reload_num**2    #这个是总的tile数量

with open(os.path.dirname(os.path.abspath(__file__)) + '\\local_title.loc', "r") as title:
    til = title.readlines()

with open(os.path.dirname(os.path.abspath(__file__)) + '\\local.v', "w") as locv:
    
    til_split = list()  #根据约定的标志拆分local.v不变部分，约定格式为‘//-----------*split*-------'
    til_temp = list()
    for x in til:
        
        if '*split*' in x:
            til_split.append(til_temp)
            til_temp = list()
        else:
            til_temp.append(x)
    til_split.append(til_temp)
########################################################################################################   
    # fixed content 0
    locv.writelines(til_split[0])     
    # flexible content 0  
    loop_str = ''
    for i in range(tile_num+1):    #可变部分循环
        loop_str += '\tlogic riscv_start_'+ str(i) + ';\n' #示例，一定要加\n换行
    loop_str += '\n\tlogic cfg_end;\n'
    for i in range(tile_num+1):    #可变部分循环
        loop_str += '\tlogic task_end_'+ str(i) + ';\n' 
    loop_str += '\tlogic task_end_'+ str(tile_num) + '_to_1;\n'       
    locv.writelines((loop_str))
########################################################################################################
    # fixed content 1
    locv.writelines(til_split[1])
     # flexible content 1  
    loop_str = ''
    loop_str += '\t\tforever begin\n'
    for i in range(tile_num):    #可变部分循环
        loop_str += '\t\t\twait(riscv_start_'+ str(i+1) + ');\n' 
        loop_str += '\t\t\t# (`CLK_PERIORD*20);\n'
        loop_str += '\t\t\tirq <= 1\'b1;\n'
        loop_str += '\t\t\t# (`CLK_PERIORD*4);\n'
        loop_str += '\t\t\tirq <= 1\'b0;\n'
    loop_str += '\t\tend\n'  
    loop_str += '\tend\n'   
    loop_str += '//-------------------------------------------------------------\n'
    loop_str += '//--------------------- FPGA writes & SRAM writes -------------\n'
    loop_str += '//-------------------------------------------------------------\n' 
    for i in range(tile_num):    #可变部分循环
        loop_str += '\tlogic [31:0] dram_data_num_'+ str(i+1) + ';\n'
        loop_str += '\tlogic [31:0] sram_data_num_'+ str(i+1) + ';\n'
    loop_str += '\n\tlogic [31:0] cfg_data_num;\n\n'
    loop_str += '\tinteger file_inform;\n'
    loop_str += '\tinitial begin\n'
    loop_str += '\t\tfile_inform = $fopen("./case/<replace>/inform.txt","r");\n'
    loop_str += '\t\t$fscanf(file_inform,\"'
    for i in range(2*tile_num+1):    #可变部分循环
        loop_str += ' %d'
    loop_str += '\",'    
    for i in range(tile_num):    #可变部分循环
        loop_str += 'dram_data_num_'+ str(i+1) + ','
        loop_str += 'sram_data_num_'+ str(i+1) + ','
    loop_str += 'cfg_data_num);\n'
    loop_str += '\tend\n'
    for i in range(tile_num):    #可变部分循环
        loop_str += '\tlogic [31:0] dram_write_num_'+ str(i+1) + ';\n'
        loop_str += '\tlogic [31:0] sram_write_num_'+ str(i+1) + ';\n'
    loop_str += '\n\tlogic [31:0] cfg_write_num;\n\n'
    for i in range(tile_num):    #可变部分循环
        loop_str += '\treg [32-1:0] dram_data_file_'+ str(i+1) + ' [20000-1:0];\n'
        loop_str += '\treg [32-1:0] dram_addr_file_'+ str(i+1) + ' [20000-1:0];\n'
        loop_str += '\treg [32-1:0] sram_data_file_'+ str(i+1) + ' [4096-1:0];\n'
        loop_str += '\treg [32-1:0] sram_addr_file_'+ str(i+1) + ' [4096-1:0];\n'
    loop_str += '\n\treg [32-1:0] cfg_data_file [2048-1:0];\n'
    loop_str += '\treg [32-1:0] cfg_addr_file [2048-1:0];\n'
    loop_str += '\tinitial begin\n'
    for i in range(tile_num):    #可变部分循环
        loop_str += '\t\t$readmemh("./case/<replace>/tile' + str(i) + '/dram_data.txt", dram_data_file_'+ str(i+1) + ');\n'
        loop_str += '\t\t$readmemh("./case/<replace>/tile' + str(i) + '/dram_data_addr.txt", dram_addr_file_'+ str(i+1) + ');\n'
        loop_str += '\t\t$readmemh("./case/<replace>/tile' + str(i) + '/sram_code.txt", sram_data_file_'+ str(i+1) + ');\n'
        loop_str += '\t\t$readmemh("./case/<replace>/tile' + str(i) + '/sram_code_addr.txt", sram_addr_file_'+ str(i+1) + ');\n'
    loop_str += '\n\t\t$readmemh("./case/<replace>/riscv_code.txt", cfg_data_file);\n'
    loop_str += '\t\t$readmemh("./case/<replace>/riscv_code_addr.txt", cfg_addr_file);\n'
    loop_str += '\tend\n'
    loop_str += '//-------------------------------------------------------------\n'
    loop_str += '//--------------------- states control ------------------------\n'
    loop_str += '//-------------------------------------------------------------\n'
    loop_str += '\tlocalparam [5:0]\n'
    loop_str += '\t\tS_IDLE 		        = 6\'d0,\n'
    loop_str += '\t\tS_cfg                  = 6\'d1,\n'
    loop_str += '\t\tS_cfg_polling          = 6\'d2,\n'
    for i in range(tile_num):    #可变部分循环
        loop_str += '\t\tS_transfer_'+ str(i+1) + '        =6\'d' + str(2*i+3) + ',\n'
        loop_str += '\t\tS_polling_'+ str(i+1) + '         =6\'d' + str(2*i+4) + ',\n'
    loop_str += '\t\tS_reading_results          = 6\'d' + str(2*tile_num+3) + ',\n'
    loop_str += '\t\tS_end                      = 6\'d' + str(2*tile_num+4) + ';\n'
    loop_str += '\treg [5 : 0] S_state;\n'     
    locv.writelines((loop_str))
########################################################################################################
    # fixed content 2
    locv.writelines(til_split[2])     
    # flexible content 2  
    loop_str = ''
    for i in range(tile_num):    #可变部分循环
        loop_str += '\t\t\t\tS_transfer_'+ str(i+1) + ' : begin\n' 
        loop_str += '\t\t\t\t\tif ( (sram_write_num_'+ str(i+1) + ' < sram_data_num_' + str(i+1) + ') || (dram_write_num_' + str(i+1) + ' < dram_data_num_' + str(i+1) + ') ) begin\n' 
        loop_str += '\t\t\t\t\t\t\t\t\t\t\t\t\t\tS_state	<= S_transfer_'+ str(i+1) + ';\n'
        loop_str += '\t\t\t\t\tend\n'
        loop_str += '\t\t\t\t\telse\t\t\t\t\t\t\t\t' + 'S_state	<= S_polling_' + str(i+1) + ';\n' 
        loop_str += '\t\t\t\tend\n'
        if  i+1 != tile_num :
            loop_str += '\t\t\t\tS_polling_'+ str(i+1) + ' : begin\n'
            loop_str += '\t\t\t\t\tif (task_end_'+ str(i+1) + ') \t\t\t\t\tS_state	<= S_transfer_' + str(i+2) +';\n'
            loop_str += '\t\t\t\t\telse  \t\t\t\t\t\t\t\tS_state	<= S_polling_' + str(i+1) +';\n' 
            loop_str += '\t\t\t\tend\n'
        else :
            loop_str += '\t\t\t\tS_polling_'+ str(i+1) + ' : begin\n'
            loop_str += '\t\t\t\t\tif (task_end_'+ str(i+1) + ') \t\t\t\t\tS_state	<= S_reading_results;\n'
            loop_str += '\t\t\t\t\telse if (task_end_'+ str(i+1) + '_to_1) \t\t\tS_state	<= S_transfer_1;\n'
            loop_str += '\t\t\t\t\telse  \t\t\t\t\t\t\t\tS_state	<= S_polling_' + str(i+1) +';\n'
            loop_str += '\t\t\t\tend\n'    
    locv.writelines((loop_str))
########################################################################################################
    # fixed content 3
    locv.writelines(til_split[3])     
    # flexible content 3  
    loop_str = ''
    for i in range(tile_num+1):    #可变部分循环
        loop_str += '\t\t\t\triscv_start_'+ str(i) + ' <= 0;\n'
    loop_str += '\tend\n'          
    locv.writelines((loop_str))
########################################################################################################
    # fixed content 4
    locv.writelines(til_split[4])     
    # flexible content 4  
    loop_str = ''
    for i in range(tile_num):    #可变部分循环
        loop_str += '\t\t\tif ( (S_state == S_polling_'+ str(i+1) + ') ) begin\n'
        loop_str += '\t\t\t\triscv_start_'+ str(i+1) + ' <= 1;\n'
        loop_str += '\t\t\tend\n'
        loop_str += '\t\t\telse begin\n'
        loop_str += '\t\t\t\triscv_start_'+ str(i+1) + ' <= 0;\n'
        loop_str += '\t\t\tend\n'
    loop_str += '\t\tend\n'  
    loop_str += '\tend\n'  
    locv.writelines((loop_str))
########################################################################################################
    # fixed content 5
    locv.writelines(til_split[5])     
    # flexible content 5  
    loop_str = ''
    for i in range(tile_num):    #可变部分循环
        loop_str += '\t\t\tsram_write_num_'+ str(i+1) + '   <= 0;\n'
    for i in range(tile_num):    #可变部分循环
        loop_str += '\t\t\ttask_end_'+ str(i+1) + '         <= 0;\n'
    loop_str += '\t\t\ttask_end_'+ str(i+1) + '_to_1    <= 0;\n' 
    loop_str += '\t\tend\n'  
    locv.writelines((loop_str))
########################################################################################################
    # fixed content 6
    locv.writelines(til_split[6])     
    # flexible content 6  
    loop_str = ''
    for i in range(tile_num):    #可变部分循环
        loop_str += '\t\t\telse if ( (S_state == S_transfer_'+ str(i+1) + ') && (sram_write_num_'+ str(i+1) + ' < sram_data_num_'+ str(i+1) + ') ) begin\n'
        if i == 0 :
            loop_str += '\t\t\t\ttask_end_'+ str(tile_num) + '			<= 0;\n'
            loop_str += '\t\t\t\ttask_end_'+ str(tile_num) + '_to_1		<= 0;\n'
        else :
            loop_str += '\t\t\t\ttask_end_'+ str(i) + '			 <= 0;\n'
        loop_str += '\t\t\t\tCENA            	<= 1\'b1;\n'
        loop_str += '\t\t\t\tWENA            	<= 1;\n'
        loop_str += '\t\t\t\tAA              	<= sram_addr_file_'+ str(i+1) + '[sram_write_num_'+ str(i+1) + '][11:0];\n'
        loop_str += '\t\t\t\tDA              	<= sram_data_file_'+ str(i+1) + '[sram_write_num_'+ str(i+1) + '];\n'
        loop_str += '\t\t\t\tsram_write_num_'+ str(i+1) + '  	<= sram_write_num_'+ str(i+1) + ' + 1;\n'
        loop_str += '\t\t\t\tR_ok 				<= 0;\n'
        loop_str += '\t\t\t\tend\n'
        if i+1 != tile_num :
            loop_str += '\t\t\telse if ( S_state == S_polling_'+ str(i+1) + ' ) begin\n'
            loop_str += '\t\t\t\tif (R_ok && QA != 0) begin\n'
            loop_str += '\t\t\t\t\tCENA			<= 1\'b0;\n'
            loop_str += '\t\t\t\t\ttask_end_'+ str(i+1) + '		<= 1;\n'
            loop_str += '\t\t\t\tend\n'
            loop_str += '\t\t\t\telse if (task_end_'+ str(i+1) + ' == 1) begin\n'
            loop_str += '\t\t\t\t\tCENA			<= 1\'b0;\n'
            loop_str += '\t\t\t\tend\n'
            loop_str += '\t\t\t\telse begin\n'
            loop_str += '\t\t\t\t\tCENA			<= 1\'b1;\n'
            loop_str += '\t\t\t\t\tAA				<= 11\'h4c2;\n'
            loop_str += '\t\t\t\t\ttask_end_'+ str(i+1) + '		<= 0;\n'
            loop_str += '\t\t\t\tend\n'
            loop_str += '\t\t\t\tR_ok 				<= CENA;\n'
            loop_str += '\t\t\t\tsram_write_num_'+ str(i+1) + '  	<= 0;\n'
            loop_str += '\t\t\tend\n'
        else :
            loop_str += '\t\t\telse if ( S_state == S_polling_'+ str(i+1) + ' ) begin\n'
            loop_str += '\t\t\t\tif (R_ok && QA == 32\'hf) begin\n'
            loop_str += '\t\t\t\t\tCENA			<= 1\'b0;\n'
            loop_str += '\t\t\t\t\ttask_end_'+ str(i+1) + '		<= 1;\n'
            loop_str += '\t\t\t\tend\n'
            loop_str += '\t\t\t\telse if (task_end_'+ str(i+1) + ' != 0) begin\n'
            loop_str += '\t\t\t\t\tCENA			<= 1\'b0;\n'
            loop_str += '\t\t\t\t\ttask_end_'+ str(i+1) + '_to_1	<= 1;\n'
            loop_str += '\t\t\t\tend\n'
            loop_str += '\t\t\t\telse if ((task_end_'+ str(i+1) + ' == 1) || (task_end_'+ str(i+1) + '_to_1 == 1)) begin\n'
            loop_str += '\t\t\t\t\tCENA			<= 1\'b0;\n'
            loop_str += '\t\t\t\tend\n'
            loop_str += '\t\t\t\telse begin\n'
            loop_str += '\t\t\t\t\tCENA			<= 1\'b1;\n'
            loop_str += '\t\t\t\t\tAA				<= 11\'h4c2;\n'
            loop_str += '\t\t\t\t\ttask_end_'+ str(i+1) + '		<= 0;\n'
            loop_str += '\t\t\t\t\ttask_end_'+ str(i+1) + '_to_1	<= 0;\n'
            loop_str += '\t\t\t\tend\n'
            loop_str += '\t\t\t\tR_ok 				<= CENA;\n'
            loop_str += '\t\t\t\tsram_write_num_'+ str(i+1) + '  	<= 0;\n'
            loop_str += '\t\t\tend\n'
    locv.writelines((loop_str))
########################################################################################################
    # fixed content 7
    locv.writelines(til_split[7])     
    # flexible content 7 
    loop_str = ''
    for i in range(tile_num-1):    #可变部分循环
        loop_str += '\t\t\telse if ( (S_state == S_transfer_'+ str(i+2) + ') ) begin\n'
        loop_str += '\t\t\t\tif (~m1_AWVALID && ~s_awv_awr_flag && ~s_arv_arr_flag && (dram_write_num_'+ str(i+2) + ' <dram_data_num_'+ str(i+2) + ') ) begin\n'
        loop_str += '\t\t\t\t\tm1_AWVALID <= 1\'b1;\n'
        loop_str += '\t\t\t\t\tm1_AWADDR <= dram_addr_file_'+ str(i+2) + '[dram_write_num_'+ str(i+2) + '];\n'
        loop_str += '\t\t\t\tend\n'
        loop_str += '\t\t\t\telse if(m1_AWVALID && m1_AWREADY) begin\n' 
        loop_str += '\t\t\t\t\tm1_AWVALID <= 1\'b0;\n' 
        loop_str += '\t\t\t\tend\n'	
        loop_str += '\t\t\tend\n'     
    locv.writelines((loop_str))
########################################################################################################
    # fixed content 8
    locv.writelines(til_split[8])     
    # flexible content 8 
    loop_str = ''
    for i in range(tile_num-1):    #可变部分循环
        loop_str += '\t\t\telse if ( (S_state == S_transfer_'+ str(i+2) + ') ) begin\n'
        loop_str += '\t\t\t\tif (~m1_WVALID && ~s_awv_awr_flag && ~s_arv_arr_flag && (dram_write_num_'+ str(i+2) + ' <dram_data_num_'+ str(i+2) + ') ) begin\n'
        loop_str += '\t\t\t\t\tm1_WVALID <= 1\'b1;\n'
        loop_str += '\t\t\t\t\tm1_WDATA <= dram_data_file_'+ str(i+2) + '[dram_write_num_'+ str(i+2) + '];\n'
        loop_str += '\t\t\t\t\tm1_WSTRB <= {(AXI_DATA_WIDTH/8){1\'b1}};\n'
        loop_str += '\t\t\t\tend\n'
        loop_str += '\t\t\t\telse if(m1_WVALID && m1_WREADY) begin\n' 
        loop_str += '\t\t\t\t\tm1_WVALID <= 1\'b0;\n' 
        loop_str += '\t\t\t\tend\n'	
        loop_str += '\t\t\tend\n'     
    locv.writelines((loop_str))
########################################################################################################
    # fixed content 9
    locv.writelines(til_split[9])     
    # flexible content 9 
    loop_str = ''
    for i in range(tile_num):    #可变部分循环
        loop_str += '\t\t\tdram_write_num_'+ str(i+1) + ' <= 0;\n'
    loop_str += '\t\tend\n' 
    loop_str += '\t\telse begin\n' 
    loop_str += '\t\t\tif (~m1_BREADY && m1_BVALID ) begin\n'   
    loop_str += '\t\t\t\tm1_BREADY <= 1\'b1;\n' 
    for i in range(tile_num):    #可变部分循环
        if i == 0 :
            loop_str += '\t\t\t\tif  ( (S_state == S_transfer_'+ str(i+1) + ') ) begin\n'
        else :
            loop_str += '\t\t\t\telse if  ( (S_state == S_transfer_'+ str(i+1) + ') ) begin\n'
        for j in range(tile_num):    #可变部分循环
            if i == j :
                loop_str += '\t\t\t\t\tdram_write_num_'+ str(j+1) + ' <= dram_write_num_'+ str(j+1) + ' + 1;\n'
            else :
                loop_str += '\t\t\t\t\tdram_write_num_'+ str(j+1) + ' <= 0;\n'
        loop_str += '\t\t\t\tend\n'
    loop_str += '\t\t\tend\n' 
    locv.writelines((loop_str))
########################################################################################################
    # fixed content 10
    locv.writelines(til_split[10]) 
########################################################################################################