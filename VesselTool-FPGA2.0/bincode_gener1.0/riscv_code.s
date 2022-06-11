.globl __start
.text
__start:
li x10, 0x20000000
li x11, 0x30000000

################## PHY cfg ##################

# cfg_dly_cc_bnksel_n
sw x0, 0(x10)

# cfg_dly_gcas_wr
sw x0, 4(x10)

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
sw x1, 24(x11)

# mc_rf_start_time_2 
sw x1, 28(x11)

# mc_rf_start_time_3 
sw x1, 32(x11)

# mc_rf_start_time_4 
sw x1, 36(x11)

# mc_rf_start_time_5 
sw x1, 40(x11)

# mc_rf_start_time_6 
sw x1, 44(x11)

# mc_rf_start_time_7 
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


    li a0, 0x1000
    li a1, 0x11dc
    li a2, 0xf0000004
    jal datacopy
    li a0, 0x11e0
    li a1, 0x13bc
    li a2, 0xf0040004
    jal datacopy
    li a0, 0x13c0
    li a1, 0x159c
    li a2, 0xf0080004
    jal datacopy
    li a0, 0x15a0
    li a1, 0x185c
    li a2, 0xf00c0004
    jal datacopy
    li a0, 0x1860
    li a1, 0x1a3c
    li a2, 0xf0100004
    jal datacopy
    li a0, 0x1a40
    li a1, 0x1c1c
    li a2, 0xf0140004
    jal datacopy
    li a0, 0x1c20
    li a1, 0x1dfc
    li a2, 0xf0180004
    jal datacopy
    li a0, 0x1e00
    li a1, 0x20dc
    li a2, 0xf01c0004
    jal datacopy
    li a0, 0x2224
    li a1, 0x2360
    li a2, 0xf0000404
    jal datacopy
    li a0, 0x2364
    li a1, 0x24a0
    li a2, 0xf0100404
    jal datacopy
li a0, 0x10000000
li a1, 1
sw a1, 0(a0)
    li a0, 0x2180
    li a1, 0x21a0
    li a2, 0xE0000000
    jal copy
    li a0, 0x21a8
    li a1, 0x21c8
    li a2, 0xE0000000
    jal copy
    li a0, 0x21d0
    li a1, 0x21f0
    li a2, 0xE0000000
    jal copy
    li a0, 0x21f8
    li a1, 0x2218
    li a2, 0xE0000000
    jal copy
    li a0, 0x20e0
    li a1, 0x2100
    li a2, 0xE0000000
    jal copy
    li a0, 0x2108
    li a1, 0x2128
    li a2, 0xE0000000
    jal copy
    li a0, 0x2130
    li a1, 0x2150
    li a2, 0xE0000000
    jal copy
    li a0, 0x2158
    li a1, 0x2178
    li a2, 0xE0000000
    jal copy
# t0: 切换需要的地址
li t0, 0xe0000000
li a2, 0xff
wait_exe0_1:
    lw t1, 0(t0) 
bne t1, a2, wait_exe0_1 
#---------------------------------------
    li a0, 20
nop_loop:
    nop
    addi a0, a0, -1
    bnez a0, nop_loop
    li a0, 0x10000000
    li a1, 0
    sw a1, 0(a0)


#---------------------------------
    li t1, 0xf0000000     # 当前写地址
    li a1, 0xf0000004    # 末地址
    li t3, 0x7900    # sram用于暂存向量地址
    li a3, 4
    jal wait
li a0, 0xf
li a1, 0
sw a1, 0(a0)


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
#---------------------------------------
# 等待结果：
# t1: ST_addr_start
# a1: ST_addr_end
# t3: vector_buffer_addr
# a3: width
wait:
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
    sw s3, 0xc(t3)
buffer2:    
    sw s2, 8(t3)
buffer1:    
    sw s1, 4(t3)
buffer0:   
    sw s0, 0(t3)
next:    
    blt a1, t1, wait_return   # 若读地址越界，跳转
    beqz a3, wait_return   # 若读取数量超出范围，跳转
    addi t1, t1, 4
    addi t3, t3, 16 
    j wait_loop
wait_return:
    ret
