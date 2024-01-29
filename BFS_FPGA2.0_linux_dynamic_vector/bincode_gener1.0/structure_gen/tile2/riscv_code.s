.globl __start
.text
__start:
li x10, 0x20000000
li x11, 0x30000000
li x5, 0x16E360

################## PHY cfg ##################

# cfg_dly_cc_bnksel_n
sw x0, 0(x10)

# cfg_dly_gcas_wr
addi x1 x0 1
sw x1, 4(x10)

# cfg_dly_gcas_rd
addi x1 x0 1
sw x1, 8(x10)

# cfg_dly_g_wrrdy_n
sw x0, 12(x10)

# cfg_dly_gcadd_rd
sw x0, 16(x10)

# cfg_dly_gcadd_wr
sw x0, 20(x10)

# cfg_pulse_gcas_wr
sw x0, 24(x10)

################## mc_ctrl cfg ##################

# mc_active_cfg 
addi x1 x0 7
sw x1, 0(x11)

# mc_precharge_cfg
addi x1 x0 6
sw x1, 4(x11)

# mc_act2pre_cfg
addi x1 x0 9
sw x1, 8(x11)

# mc_rd2pre_cfg 
addi x1 x0 1
sw x1, 12(x11)

# mc_wr2pre_cfg 
addi x1 x0 7
sw x1, 16(x11)

# mc_rf_start_time_0 
addi x1 x0 0xff
sw x1, 20(x11)

# mc_rf_start_time_1 
add x1 x1 x5
sw x1, 24(x11)

# mc_rf_start_time_2 
add x1 x1 x5
sw x1, 28(x11)

# mc_rf_start_time_3 
add x1 x1 x5
sw x1, 32(x11)

# mc_rf_start_time_4 
add x1 x1 x5
sw x1, 36(x11)

# mc_rf_start_time_5 
add x1 x1 x5
sw x1, 40(x11)

# mc_rf_start_time_6 
add x1 x1 x5
sw x1, 44(x11)

# mc_rf_start_time_7 
add x1 x1 x5
sw x1, 48(x11)

# mc_rf_addr_map 
addi x1 x0 0
sw x1, 52(x11)

# mc_rf_row_cfg 
addi x1 x0 4
sw x1, 56(x11)

# mc_en 
addi x1 x0 0xff
sw x1, 60(x11)

# mc_dm_en 
addi x1 x0 0xff
sw x1, 64(x11)

# mc_refresh_cfg 		
li x1, 0xb71b00
sw x1, 68(x11)
      li s11, 2 
      li s10, 0 
      li s9, 0
      li s8, 64
      li s7, 0
      li s6, 0
      li s5, 0
      li s4, 0
      li a7, 0




    li s4, 0
send_config_loop1:

li a0, 1
jal sendSingle2FPGA

#enable irq
      li x3, 0x7FFFFFF0			# 8'h7ffffff0
      #.word 0x0601e00b #enable irq
nop      #enable irq

#wait_irq()
      #.word 0x0800400B #wait irq
nop      #wait irq
init:
      li x3, 0xFFFFFFF0			# 8'hfffffff0      #.word 0x0601e00b #disable irq
nop      #disable irq
    mv a1, s4
    li s6, 0
CI_addr_add1:
    beqz a1, conti_send_node
    li a2, 0x0800000
    add s6, s6, a2
    addi a1, a1, -1
    j CI_addr_add1
conti_send_node:
li a0, 0x10000000
    mv a1, s4
ni_sel_add1:
    beqz a1, conti_send_config1
    addi a0, a0, 4
    addi a1, a1, -1
    j ni_sel_add1
conti_send_config1:
li a1, 1
sw a1, 0(a0)
    li a0, 0xdf8
    li a1, 0xe3c
    li a2, 0xE0000000
    add a2, a2, s6
    li a3, 9
    jal config_copy
    li a0, 0xdb0
    li a1, 0xdf4
    li a2, 0xE0000000
    add a2, a2, s6
    li a3, 9
    jal config_copy
    li a0, 0xd68
    li a1, 0xdac
    li a2, 0xE0000000
    add a2, a2, s6
    li a3, 9
    jal config_copy
    li a0, 0xd20
    li a1, 0xd64
    li a2, 0xE0000000
    add a2, a2, s6
    li a3, 9
    jal config_copy
    li a0, 0xcd8
    li a1, 0xd1c
    li a2, 0xE0000000
    add a2, a2, s6
    li a3, 9
    jal config_copy
    li a0, 0xc90
    li a1, 0xcd4
    li a2, 0xE0000000
    add a2, a2, s6
    li a3, 9
    jal config_copy
    li a0, 0xc48
    li a1, 0xc8c
    li a2, 0xE0000000
    add a2, a2, s6
    li a3, 9
    jal config_copy
    li a0, 0xc00
    li a1, 0xc44
    li a2, 0xE0000000
    add a2, a2, s6
    li a3, 9
    jal config_copy
    addi s7, s7, 1
    addi s4, s4, 1
    li a0, 1
    bne s4, a0, send_config_loop1
    li s4, 0
    li s6, 0
wait_result_loop1:
    mv a1, s4
    li s6, 0
CI_addr_add2:
    beqz a1, conti_wait_node1
    li a2, 0x0800000
    add s6, s6, a2
    addi a1, a1, -1
    j CI_addr_add2
conti_wait_node1:
# t0: 切换需要的地址
li t0, 0xe0000000
add t0, t0, s6
li a2, 0xffff
wait_exe0_1:
    lw t1, 0(t0) 
bne t1, a2, wait_exe0_1 
#---------------------------------------
# 切换mem_ctrl到riscv过程：
# t0: 切换需要的地址
li t2, 0xe0000080
add t2, t2, s6
li a3, 16
wait_st1:
    lw t1, 0(t2) 
    bne t1, a3, wait_st1 
    li a0, 0x10000000
    mv a1, s4
ni_sel_add11:
    beqz a1, conti_send_config11
    addi a0, a0, 4
    addi a1, a1, -1
    j ni_sel_add11
conti_send_config11:
    li a1, 0
    sw a1, 0(a0)


#---------------------------------
    li t1, 0xf0020428     # 当前写地址
    li a1, 0xf0020428    # 末地址
    li t3, 0x2000    # sram用于暂存向量地址
    li t4, 0x3000    # sram用于暂存向量地址
    li a3, 4
    li a4, 1
    bne a4, s5, jump_flag_0_0
    li a4, 1
    j jump_2_wait_0_0
jump_flag_0_0:
    li a4, 0
jump_2_wait_0_0:
    jal wait
    li t1, 0xf0060428     # 当前写地址
    li a1, 0xf0060428    # 末地址
    li t3, 0x2010    # sram用于暂存向量地址
    li t4, 0x3010    # sram用于暂存向量地址
    li a3, 4
    li a4, 1
    bne a4, s5, jump_flag_0_1
    li a4, 1
    j jump_2_wait_0_1
jump_flag_0_1:
    li a4, 0
jump_2_wait_0_1:
    jal wait
    li t1, 0xf00a0428     # 当前写地址
    li a1, 0xf00a0428    # 末地址
    li t3, 0x2020    # sram用于暂存向量地址
    li t4, 0x3020    # sram用于暂存向量地址
    li a3, 4
    li a4, 1
    bne a4, s5, jump_flag_0_2
    li a4, 1
    j jump_2_wait_0_2
jump_flag_0_2:
    li a4, 0
jump_2_wait_0_2:
    jal wait
    li t1, 0xf00e0428     # 当前写地址
    li a1, 0xf00e0428    # 末地址
    li t3, 0x2030    # sram用于暂存向量地址
    li t4, 0x3030    # sram用于暂存向量地址
    li a3, 4
    li a4, 1
    bne a4, s5, jump_flag_0_3
    li a4, 1
    j jump_2_wait_0_3
jump_flag_0_3:
    li a4, 0
jump_2_wait_0_3:
    jal wait
    addi s9, s9, 1
    addi s4, s4, 1
    addi a7, a7, 1
    li a0, 1
    bne s4, a0, wait_result_loop1
    li s4, 0
    li s6, 0
load_data: 
    li s4, 0
    li s6, 0
reload_loop1:
    mv a1, s4
    li s6, 0
CI_addr_add3:
    beqz a1, conti_reload_node1
    li a2, 0x0800000
    add s6, s6, a2
    addi a1, a1, -1
    j CI_addr_add3
conti_reload_node1:
li a0, 2
beq s7, a0, FPGA_n_try_stop

li a0, 1
FPGA_n_try_stop:
jal sendSingle2FPGA

#enable irq
      li x3, 0x7FFFFFF0			# 8'h7ffffff0
      #.word 0x0601e00b #enable irq
nop      #enable irq

#wait_irq()
      #.word 0x0800400B #wait irq
nop      #wait irq

    li a0, 2
    bne s9, a0, coni_row_tile1
    li s9, 0
    addi s5, s5, 1
coni_row_tile1:
    li a0, 4
    blt a7, a0, jump_reload
    li a0, 0x2000
    li a1, 0x201c
    li a2, 0xf0000400
    add a2, a2, s6
    jal datacopy
#---------------------------------
    li a0, 0x2020
    li a1, 0x203c
    li a2, 0xf0020400
    add a2, a2, s6
    jal datacopy
#---------------------------------
    li a0, 0x2000
    li a1, 0x201c
    li a2, 0xf0040400
    add a2, a2, s6
    jal datacopy
#---------------------------------
    li a0, 0x2020
    li a1, 0x203c
    li a2, 0xf0060400
    add a2, a2, s6
    jal datacopy
#---------------------------------
    li a0, 0x2000
    li a1, 0x201c
    li a2, 0xf0080400
    add a2, a2, s6
    jal datacopy
#---------------------------------
    li a0, 0x2020
    li a1, 0x203c
    li a2, 0xf00a0400
    add a2, a2, s6
    jal datacopy
#---------------------------------
    li a0, 0x2000
    li a1, 0x201c
    li a2, 0xf00c0400
    add a2, a2, s6
    jal datacopy
#---------------------------------
    li a0, 0x2020
    li a1, 0x203c
    li a2, 0xf00e0400
    add a2, a2, s6
    jal datacopy
#---------------------------------
jump_reload:
li a0, 0xE000007C 
add a0, a0, s6
li a1, 1 
sw a1, 0(a0) 
li a1, 0 
sw a1, 0(a0)
li a0, 0x10000000
    mv a1, s4
ni_sel_add2:
    beqz a1, conti_send_config2
    addi a0, a0, 4
    addi a1, a1, -1
    j ni_sel_add2
conti_send_config2:
li a1, 1
sw a1, 0(a0)
    li a0, 0xdf8
    li a1, 0xe3c
    li a2, 0xE0000000
    add a2, a2, s6
    li a3, 9
    jal config_copy
    li a0, 0xdb0
    li a1, 0xdf4
    li a2, 0xE0000000
    add a2, a2, s6
    li a3, 9
    jal config_copy
    li a0, 0xd68
    li a1, 0xdac
    li a2, 0xE0000000
    add a2, a2, s6
    li a3, 9
    jal config_copy
    li a0, 0xd20
    li a1, 0xd64
    li a2, 0xE0000000
    add a2, a2, s6
    li a3, 9
    jal config_copy
    li a0, 0xcd8
    li a1, 0xd1c
    li a2, 0xE0000000
    add a2, a2, s6
    li a3, 9
    jal config_copy
    li a0, 0xc90
    li a1, 0xcd4
    li a2, 0xE0000000
    add a2, a2, s6
    li a3, 9
    jal config_copy
    li a0, 0xc48
    li a1, 0xc8c
    li a2, 0xE0000000
    add a2, a2, s6
    li a3, 9
    jal config_copy
    li a0, 0xc00
    li a1, 0xc44
    li a2, 0xE0000000
    add a2, a2, s6
    li a3, 9
    jal config_copy
    addi s7, s7, 1
    addi s4, s4, 1
    li a0, 1
    bne s4, a0, reload_loop1
    li s4, 0
    li s6, 0
wait_result_loop2:
    mv a1, s4
    li s6, 0
CI_addr_add4:
    beqz a1, conti_wait_node2
    li a2, 0x0800000
    add s6, s6, a2
    addi a1, a1, -1
    j CI_addr_add4
conti_wait_node2:
# t0: 切换需要的地址
li t0, 0xe0000000
add t0, t0, s6
li a2, 0xffff
wait_exe0_2:
    lw t1, 0(t0) 
bne t1, a2, wait_exe0_2 
#---------------------------------------
# 切换mem_ctrl到riscv过程：
# t0: 切换需要的地址
li t2, 0xe0000080
add t2, t2, s6
li a3, 16
wait_st2:
    lw t1, 0(t2) 
    bne t1, a3, wait_st2 
    li a0, 0x10000000
    mv a1, s4
ni_sel_add12:
    beqz a1, conti_send_config12
    addi a0, a0, 4
    addi a1, a1, -1
    j ni_sel_add12
conti_send_config12:
    li a1, 0
    sw a1, 0(a0)


#---------------------------------
    li t1, 0xf0020428     # 当前写地址
    li a1, 0xf0020428    # 末地址
    li t3, 0x2000    # sram用于暂存向量地址
    li t4, 0x3000    # sram用于暂存向量地址
    li a3, 4
    li a4, 1
    bne a4, s5, jump_flag_1_0
    li a4, 1
    j jump_2_wait_1_0
jump_flag_1_0:
    li a4, 0
jump_2_wait_1_0:
    jal wait
    li t1, 0xf0060428     # 当前写地址
    li a1, 0xf0060428    # 末地址
    li t3, 0x2010    # sram用于暂存向量地址
    li t4, 0x3010    # sram用于暂存向量地址
    li a3, 4
    li a4, 1
    bne a4, s5, jump_flag_1_1
    li a4, 1
    j jump_2_wait_1_1
jump_flag_1_1:
    li a4, 0
jump_2_wait_1_1:
    jal wait
    li t1, 0xf00a0428     # 当前写地址
    li a1, 0xf00a0428    # 末地址
    li t3, 0x2020    # sram用于暂存向量地址
    li t4, 0x3020    # sram用于暂存向量地址
    li a3, 4
    li a4, 1
    bne a4, s5, jump_flag_1_2
    li a4, 1
    j jump_2_wait_1_2
jump_flag_1_2:
    li a4, 0
jump_2_wait_1_2:
    jal wait
    li t1, 0xf00e0428     # 当前写地址
    li a1, 0xf00e0428    # 末地址
    li t3, 0x2030    # sram用于暂存向量地址
    li t4, 0x3030    # sram用于暂存向量地址
    li a3, 4
    li a4, 1
    bne a4, s5, jump_flag_1_3
    li a4, 1
    j jump_2_wait_1_3
jump_flag_1_3:
    li a4, 0
jump_2_wait_1_3:
    jal wait
    addi s9, s9, 1
    addi s4, s4, 1
    addi a7, a7, 1
    li a0, 1
    bne s4, a0, wait_result_loop2
    li s4, 0
    li s6, 0
#---------------------------------------
# 等待结束过程：
# s10: 结束标志，为0表示结束
wait_end2:
    li a0, 4
    bne s7, a0, load_data
    beqz s10, quit 
    li a1, 0x1300
    lw a0, 0(a1)
    addi a0, a0, -1
    beqz a0, quit 
    sw a0, 0(a1)
    li s10, 0 
    addi s11, s11, 1
    li s7, 0
    li s5, 0
    li s9, 0
    j load_data 


#---------------------------------
quit: 
li a0, 0xf
jal sendSingle2FPGA

#wait_irq()
      #.word 0x0800400B #wait irq
nop      #wait irq

li a0, 0xf
li a1, 0
sw a1, 0(a0)


#---------------------------------------
# 等待结果：
# t1: ST_addr_start
# a1: ST_addr_end
# t3: vector_buffer_addr
# t4: level_addr
# a3: width
# a4: 为标志寄存器，若为0，则不是最后一行，不存
wait:
    li a2, -1 
    add t1, t1, s6
    add a1, a1, s6
    addi s0, s9, 0
addr_add1:
    beqz s0, wait_loop
    add t3, t3, s8
    add t4, t4, s8
    addi s0, s0, -1
    j addr_add1
wait_loop:
    lw s0, 0(t1)
    lw s1, 0(t1)
    lw s2, 0(t1)
    lw s3, 0(t1)
    addi a3, a3, -1
    beqz a3, buffer0    
    addi a3, a3, 1
    addi a3, a3, -2
    beqz a3, buffer1   
    addi a3, a3, 2
    addi a3, a3, -3
    beqz a3, buffer2   
    addi a3, a3, 3
    addi a3, a3, -4
    beqz a3, buffer3   
buffer3:    
    lw t5, 0xc(t4) 
    snez t5, t5 
    xori t5, t5, 1
    and s3, s3, t5
    lw a0, 0xc(t3)
    or a0, a0, s3
    beqz a4, jump_st_3
    lw t5, 0xc(t4) 
    snez t5, t5 
    or a0, a0, t5
    sw a0, 0xc(t3)
jump_st_3:
    beq s3, x0, buffer2 
    sw s11, 0xc(t4)    #s11存放当前level
    li s10, 1
buffer2:    
    lw t5, 8(t4) 
    snez t5, t5 
    xori t5, t5, 1
    and s2, s2, t5
    lw a0, 8(t3)
    or a0, a0, s2
    beqz a4, jump_st_2
    lw t5, 8(t4) 
    snez t5, t5 
    or a0, a0, t5
    sw a0, 8(t3)
jump_st_2:
    beq s2, x0, buffer1 
    sw s11, 8(t4)    #s11存放当前level
    li s10, 1
buffer1:    
    lw t5, 4(t4) 
    snez t5, t5 
    xori t5, t5, 1
    and s1, s1, t5
    lw a0, 4(t3)
    or a0, a0, s1
    beqz a4, jump_st_1
    lw t5, 4(t4) 
    snez t5, t5 
    or a0, a0, t5
    sw a0, 4(t3)
jump_st_1:
    beq s1, x0, buffer0 
    sw s11, 4(t4)    #s11存放当前level
    li s10, 1
buffer0:   
    lw t5, 0(t4) 
    snez t5, t5 
    xori t5, t5, 1
    and s0, s0, t5
    lw a0, 0(t3)
    or a0, a0, s0
    beqz a4, jump_st_0
    lw t5, 0(t4) 
    snez t5, t5 
    or a0, a0, t5
    sw a0, 0(t3)
jump_st_0:
    beq s0, x0, next 
    sw s11, 0(t4)    #s11存放当前level
    li s10, 1
next:    
    blt a1, t1, wait_return   # 若读地址越界，跳转
    beqz a3, wait_return   # 若读取数量超出范围，跳转
    addi t1, t1, 4
    addi t3, t3, 16 
    addi t4, t4, 16 
    j wait_loop
wait_return:
    ret
#---------------------------------------
# 搬运函数，调用参数：
# a0: 源首地址
# a1: 源末地址
# a2: 目首地址
copy:
	mv t0, a0     # 当前读地址
    mv t1, a2     # 当前写地址
copyloop:
    blt a1, t0, copyreturn   # 若读地址越界，跳转
    lw t2, 0(t0)
    sw t2, 0(t1)
    addi t0, t0, 4
    addi t1, t1, 4
    j copyloop
copyreturn:
	ret

#---------------------------------
#---------------------------------------
# data数据专用搬运函数，调用参数：
# a0: 源首地址
# a1: 源末地址
# a2: 目首地址
datacopy:
	mv t0, a0     # 当前读地址
    mv t1, a2     # 当前写地址
   li t3, 0
    addi s0, s5, 0
addr_add2_:
    beqz s0, sram_addr_add
    add t3, t3, s8
    addi s0, s0, -1
    j addr_add2_
sram_addr_add:
    add t0, t0, t3
    add a1, a1, t3
datacopyloop:
    blt a1, t0, datacopyreturn   # 若读地址越界，跳转
    lw t2, 0(t0)
    sw t2, 0(t1)
    lw t2, 0x4(t0)
    sw t2, 0(t1)
    lw t2, 0x8(t0)
    sw t2, 0(t1)
    lw t2, 0xC(t0)
    sw t2, 0(t1)
    addi t0, t0, 16
    addi t1, t1, 4
    j datacopyloop
datacopyreturn:
	ret

#---------------------------------
#-------------------------------------------------------
#send单数据到FPGA
#a0: 源数据

sendSingle2FPGA:
  li  t2, 0x00001308  #buffer地址R2H
  sw a0, 0(t2)  #写入数据
  ret
#---------------------------------------
# 配置信息专用搬运函数，调用参数：
# a0: 源首地址
# a1: 源末地址
# a2: 目首地址
config_copy:
	mv t0, a0     # 当前读地址
    mv t1, a2     # 当前写地址
    mv t3, a3
config_copyloop:
    blt a1, t0, config_copyreturn   # 若读地址越界，跳转
    lw t2, 0(t0)
    sw t2, 0(t1)
    addi t0, t0, 4
    addi t1, t1, 4
    addi t3, t3, -1
    bnez t3, n_next
    mv t1, a2
    mv t3, a3
n_next:
    j config_copyloop
config_copyreturn:
	ret

#---------------------------------
