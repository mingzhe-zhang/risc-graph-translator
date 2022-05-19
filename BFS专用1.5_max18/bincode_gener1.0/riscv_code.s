.globl __start
.text
__start:
init:
      li s11, 2 
      li s10, 0 
li x10, 0x20000000
li x11, 0x30000000

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


#---------------------------------------
# level过程：
# t1: 结果sram首地址
select:
    li t1, 0x7800     # 当前写地址
    li t3, 0x7600    # 当前写地址
    li a1, 18     # 末地址
    li t2, 1 
select_loop:
    sw t2, 0(t1)
    sw t2, 0(t3)
    addi t1, t1, 4
    addi t3, t3, 4
    addi a1, a1, -1
    li t2, 0 
    bnez a1, select_loop

#---------------------------------
#---------------------------------------
# 结果初始化：
# a1: 结果dram末地址
# t1: 结果dram首地址
result_init:
    li t1, 0xf038e7b8     # 当前写地址
    li a1, 0xf038e7cc     # 末地址
result_init_loop:
    blt a1, t1, result_init_return   # 若读地址越界，跳转
    li t2, -1
    sw t2, 0(t1)
    sw t2, 0(t1)
    sw t2, 0(t1)
    sw t2, 0(t1)
    addi t1, t1, 4
    j result_init_loop
result_init_return:

#---------------------------------

    li a0, 0x2000
    li a1, 0x2124
    li a2, 0xf0000004
    jal datacopy
    li a0, 0x2128
    li a1, 0x23fc
    li a2, 0xf0038e3c
    jal datacopy
    li a0, 0x2400
    li a1, 0x2524
    li a2, 0xf0071c74
    jal datacopy
    li a0, 0x2528
    li a1, 0x27fc
    li a2, 0xf00aaaac
    jal datacopy
    li a0, 0x2800
    li a1, 0x2924
    li a2, 0xf00e38e4
    jal datacopy
    li a0, 0x2928
    li a1, 0x2bfc
    li a2, 0xf011c720
    jal datacopy
    li a0, 0x2c00
    li a1, 0x2d24
    li a2, 0xf0155558
    jal datacopy
    li a0, 0x2d28
    li a1, 0x2ffc
    li a2, 0xf018e390
    jal datacopy
    li a0, 0x3000
    li a1, 0x3124
    li a2, 0xf01c71c8
    jal datacopy
    li a0, 0x3128
    li a1, 0x33fc
    li a2, 0xf0200004
    jal datacopy
    li a0, 0x3400
    li a1, 0x3524
    li a2, 0xf0238e3c
    jal datacopy
    li a0, 0x3528
    li a1, 0x37fc
    li a2, 0xf0271c74
    jal datacopy
    li a0, 0x3800
    li a1, 0x3924
    li a2, 0xf02aaaac
    jal datacopy
    li a0, 0x3928
    li a1, 0x3bfc
    li a2, 0xf02e38e4
    jal datacopy
    li a0, 0x3c00
    li a1, 0x3d24
    li a2, 0xf031c720
    jal datacopy
    li a0, 0x3d28
    li a1, 0x3ffc
    li a2, 0xf0355558
    jal datacopy
    li a0, 0x4000
    li a1, 0x4124
    li a2, 0xf038e390
    jal datacopy
    li a0, 0x4128
    li a1, 0x487c
    li a2, 0xf03c71c8
    jal datacopy
    li a0, 0x4b54
    li a1, 0x4bf0
    li a2, 0xf0000400
    jal datacopy
    li a0, 0x4bf4
    li a1, 0x4c90
    li a2, 0xf0072074
    jal datacopy
    li a0, 0x4c94
    li a1, 0x4d30
    li a2, 0xf00e3ce4
    jal datacopy
    li a0, 0x4d34
    li a1, 0x4dd0
    li a2, 0xf0155958
    jal datacopy
    li a0, 0x4dd4
    li a1, 0x4e70
    li a2, 0xf01c75c8
    jal datacopy
    li a0, 0x4e74
    li a1, 0x4f10
    li a2, 0xf0239238
    jal datacopy
    li a0, 0x4f14
    li a1, 0x4fb0
    li a2, 0xf02aaeac
    jal datacopy
    li a0, 0x4fb4
    li a1, 0x5050
    li a2, 0xf031cb1c
    jal datacopy
    li a0, 0x5054
    li a1, 0x50f0
    li a2, 0xf038e790
    jal datacopy
li a0, 0x10000000
li a1, 1
sw a1, 0(a0)
    li a0, 0x4b00
    li a1, 0x4b20
    li a2, 0xE0000000
    jal copy
    li a0, 0x4b28
    li a1, 0x4b48
    li a2, 0xE0000000
    jal copy
    li a0, 0x4ab0
    li a1, 0x4ad0
    li a2, 0xE0000000
    jal copy
    li a0, 0x4ad8
    li a1, 0x4af8
    li a2, 0xE0000000
    jal copy
    li a0, 0x4a60
    li a1, 0x4a80
    li a2, 0xE0000000
    jal copy
    li a0, 0x4a88
    li a1, 0x4aa8
    li a2, 0xE0000000
    jal copy
    li a0, 0x4a10
    li a1, 0x4a30
    li a2, 0xE0000000
    jal copy
    li a0, 0x4a38
    li a1, 0x4a58
    li a2, 0xE0000000
    jal copy
    li a0, 0x49c0
    li a1, 0x49e0
    li a2, 0xE0000000
    jal copy
    li a0, 0x49e8
    li a1, 0x4a08
    li a2, 0xE0000000
    jal copy
    li a0, 0x4970
    li a1, 0x4990
    li a2, 0xE0000000
    jal copy
    li a0, 0x4998
    li a1, 0x49b8
    li a2, 0xE0000000
    jal copy
    li a0, 0x4920
    li a1, 0x4940
    li a2, 0xE0000000
    jal copy
    li a0, 0x4948
    li a1, 0x4968
    li a2, 0xE0000000
    jal copy
    li a0, 0x48d0
    li a1, 0x48f0
    li a2, 0xE0000000
    jal copy
    li a0, 0x48f8
    li a1, 0x4918
    li a2, 0xE0000000
    jal copy
    li a0, 0x4880
    li a1, 0x48a0
    li a2, 0xE0000000
    jal copy
    li a0, 0x48a8
    li a1, 0x48c8
    li a2, 0xE0000000
    jal copy
#---------------------------------------
# 切换mem_ctrl到riscv过程：
# t0: 切换需要的地址
li t0, 0xe0000000
li a2, 262143
wait_st1:
    lw t1, 0(t0) 
    bne t1, a2, wait_st1 
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    li a0, 0x10000000
    li a1, 0
    sw a1, 0(a0)


#---------------------------------
#---------------------------------------
# 等待结果：
# t1: 结果dram首地址
# t3: 结果sram首地址
wait1:
    li t1, 0xf038e7b8     # 当前写地址
    li a1, 0xf038e7c8    # 末地址
    li a2, -1 
    li t3, 0x7600 
    li t4, 0x7800 
    li a3, 18
wait_loop1:
    lw s0, 0(t1)
    lw s1, 0(t1)
    lw s2, 0(t1)
    lw s3, 0(t1)
    beq s0, a2, wait_loop1 
    addi a3, a3, -1
    beqz a3, buffer0_1    
    addi a3, a3, 1
    beq s1, a2, wait_loop1 
    addi a3, a3, -2
    beqz a3, buffer1_1    
    addi a3, a3, 2
    beq s2, a2, wait_loop1 
    addi a3, a3, -3
    beqz a3, buffer2_1    
    addi a3, a3, 3
    beq s3, a2, wait_loop1 
    addi a3, a3, -4
    beqz a3, buffer3_1    
buffer3_1:    
    lw t5, 0xc(t4) 
    snez t5, t5 
    xori t5, t5, 1
    and s3, s3, t5
    sw s3, 0xc(t3)
    beq s3, x0, buffer2_1 
    sw s11, 0xc(t4)    #s11存放当前level
    li s10, 1
buffer2_1:    
    lw t5, 8(t4) 
    snez t5, t5 
    xori t5, t5, 1
    and s2, s2, t5
    sw s2, 8(t3)
    beq s2, x0, buffer1_1 
    sw s11, 8(t4)    #s11存放当前level
    li s10, 1
buffer1_1:    
    lw t5, 4(t4) 
    snez t5, t5 
    xori t5, t5, 1
    and s1, s1, t5
    sw s1, 4(t3)
    beq s1, x0, buffer0_1 
    sw s11, 4(t4)    #s11存放当前level
    li s10, 1
buffer0_1:    
    lw t5, 0(t4) 
    snez t5, t5 
    xori t5, t5, 1
    and s0, s0, t5
    sw s0, 0(t3)
    beq s0, x0, next1 
    sw s11, 0(t4)    #s11存放当前level
    li s10, 1
next1:    
    blt a1, t1, wait_return1   # 若读地址越界，跳转
    beqz a3, wait_return1   # 若读取数量超出范围，跳转
    addi t1, t1, 4
    addi t3, t3, 16 
    addi t4, t4, 16 
    j wait_loop1
wait_return1:

    li a0, 0x7600
    li a1, 0x7604
    li a2, 0x4b54
    jal copy
#---------------------------------
    li a0, 0x7608
    li a1, 0x760c
    li a2, 0x4bf4
    jal copy
#---------------------------------
    li a0, 0x7610
    li a1, 0x7614
    li a2, 0x4c94
    jal copy
#---------------------------------
    li a0, 0x7618
    li a1, 0x761c
    li a2, 0x4d34
    jal copy
#---------------------------------
    li a0, 0x7620
    li a1, 0x7624
    li a2, 0x4dd4
    jal copy
#---------------------------------
    li a0, 0x7628
    li a1, 0x762c
    li a2, 0x4e74
    jal copy
#---------------------------------
    li a0, 0x7630
    li a1, 0x7634
    li a2, 0x4f14
    jal copy
#---------------------------------
    li a0, 0x7638
    li a1, 0x763c
    li a2, 0x4fb4
    jal copy
#---------------------------------
    li a0, 0x7640
    li a1, 0x7644
    li a2, 0x5054
    jal copy
#---------------------------------
#---------------------------------------
# 等待结束过程：
# s10: 结束标志，为0表示结束
wait_end1:
    beqz s10, quit 
    li s10, 0 
    addi s11, s11, 1
    j load_data 


#---------------------------------
load_data: 
    li a0, 0x4b54
    li a1, 0x4b58
    li a2, 0xf0000400
    jal datacopy
    li a0, 0x4bf4
    li a1, 0x4bf8
    li a2, 0xf0072074
    jal datacopy
    li a0, 0x4c94
    li a1, 0x4c98
    li a2, 0xf00e3ce4
    jal datacopy
    li a0, 0x4d34
    li a1, 0x4d38
    li a2, 0xf0155958
    jal datacopy
    li a0, 0x4dd4
    li a1, 0x4dd8
    li a2, 0xf01c75c8
    jal datacopy
    li a0, 0x4e74
    li a1, 0x4e78
    li a2, 0xf0239238
    jal datacopy
    li a0, 0x4f14
    li a1, 0x4f18
    li a2, 0xf02aaeac
    jal datacopy
    li a0, 0x4fb4
    li a1, 0x4fb8
    li a2, 0xf031cb1c
    jal datacopy
    li a0, 0x5054
    li a1, 0x5058
    li a2, 0xf038e790
    jal datacopy
li a0, 0xE000005C 
li a1, 1 
sw a1, 0(a0) 
li a1, 0 
sw a1, 0(a0)
li a0, 0x10000000
li a1, 1
sw a1, 0(a0)
    li a0, 0x4b00
    li a1, 0x4b20
    li a2, 0xE0000000
    jal copy
    li a0, 0x4b28
    li a1, 0x4b48
    li a2, 0xE0000000
    jal copy
    li a0, 0x4ab0
    li a1, 0x4ad0
    li a2, 0xE0000000
    jal copy
    li a0, 0x4ad8
    li a1, 0x4af8
    li a2, 0xE0000000
    jal copy
    li a0, 0x4a60
    li a1, 0x4a80
    li a2, 0xE0000000
    jal copy
    li a0, 0x4a88
    li a1, 0x4aa8
    li a2, 0xE0000000
    jal copy
    li a0, 0x4a10
    li a1, 0x4a30
    li a2, 0xE0000000
    jal copy
    li a0, 0x4a38
    li a1, 0x4a58
    li a2, 0xE0000000
    jal copy
    li a0, 0x49c0
    li a1, 0x49e0
    li a2, 0xE0000000
    jal copy
    li a0, 0x49e8
    li a1, 0x4a08
    li a2, 0xE0000000
    jal copy
    li a0, 0x4970
    li a1, 0x4990
    li a2, 0xE0000000
    jal copy
    li a0, 0x4998
    li a1, 0x49b8
    li a2, 0xE0000000
    jal copy
    li a0, 0x4920
    li a1, 0x4940
    li a2, 0xE0000000
    jal copy
    li a0, 0x4948
    li a1, 0x4968
    li a2, 0xE0000000
    jal copy
    li a0, 0x48d0
    li a1, 0x48f0
    li a2, 0xE0000000
    jal copy
    li a0, 0x48f8
    li a1, 0x4918
    li a2, 0xE0000000
    jal copy
    li a0, 0x4880
    li a1, 0x48a0
    li a2, 0xE0000000
    jal copy
    li a0, 0x48a8
    li a1, 0x48c8
    li a2, 0xE0000000
    jal copy
#---------------------------------------
# 切换mem_ctrl到riscv过程：
# t0: 切换需要的地址
li t0, 0xe0000000
li a2, 262143
wait_st2:
    lw t1, 0(t0) 
    bne t1, a2, wait_st2 
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    li a0, 0x10000000
    li a1, 0
    sw a1, 0(a0)


#---------------------------------
#---------------------------------------
# 等待结果：
# t1: 结果dram首地址
# t3: 结果sram首地址
wait2:
    li t1, 0xf038e7b8     # 当前写地址
    li a1, 0xf038e7c8    # 末地址
    li a2, -1 
    li t3, 0x7600 
    li t4, 0x7800 
    li a3, 18
wait_loop2:
    lw s0, 0(t1)
    lw s1, 0(t1)
    lw s2, 0(t1)
    lw s3, 0(t1)
    beq s0, a2, wait_loop2 
    addi a3, a3, -1
    beqz a3, buffer0_2    
    addi a3, a3, 1
    beq s1, a2, wait_loop2 
    addi a3, a3, -2
    beqz a3, buffer1_2    
    addi a3, a3, 2
    beq s2, a2, wait_loop2 
    addi a3, a3, -3
    beqz a3, buffer2_2    
    addi a3, a3, 3
    beq s3, a2, wait_loop2 
    addi a3, a3, -4
    beqz a3, buffer3_2    
buffer3_2:    
    lw t5, 0xc(t4) 
    snez t5, t5 
    xori t5, t5, 1
    and s3, s3, t5
    sw s3, 0xc(t3)
    beq s3, x0, buffer2_2 
    sw s11, 0xc(t4)    #s11存放当前level
    li s10, 1
buffer2_2:    
    lw t5, 8(t4) 
    snez t5, t5 
    xori t5, t5, 1
    and s2, s2, t5
    sw s2, 8(t3)
    beq s2, x0, buffer1_2 
    sw s11, 8(t4)    #s11存放当前level
    li s10, 1
buffer1_2:    
    lw t5, 4(t4) 
    snez t5, t5 
    xori t5, t5, 1
    and s1, s1, t5
    sw s1, 4(t3)
    beq s1, x0, buffer0_2 
    sw s11, 4(t4)    #s11存放当前level
    li s10, 1
buffer0_2:    
    lw t5, 0(t4) 
    snez t5, t5 
    xori t5, t5, 1
    and s0, s0, t5
    sw s0, 0(t3)
    beq s0, x0, next2 
    sw s11, 0(t4)    #s11存放当前level
    li s10, 1
next2:    
    blt a1, t1, wait_return2   # 若读地址越界，跳转
    beqz a3, wait_return2   # 若读取数量超出范围，跳转
    addi t1, t1, 4
    addi t3, t3, 16 
    addi t4, t4, 16 
    j wait_loop2
wait_return2:

    li a0, 0x7600
    li a1, 0x7604
    li a2, 0x4b54
    jal copy
#---------------------------------
    li a0, 0x7608
    li a1, 0x760c
    li a2, 0x4bf4
    jal copy
#---------------------------------
    li a0, 0x7610
    li a1, 0x7614
    li a2, 0x4c94
    jal copy
#---------------------------------
    li a0, 0x7618
    li a1, 0x761c
    li a2, 0x4d34
    jal copy
#---------------------------------
    li a0, 0x7620
    li a1, 0x7624
    li a2, 0x4dd4
    jal copy
#---------------------------------
    li a0, 0x7628
    li a1, 0x762c
    li a2, 0x4e74
    jal copy
#---------------------------------
    li a0, 0x7630
    li a1, 0x7634
    li a2, 0x4f14
    jal copy
#---------------------------------
    li a0, 0x7638
    li a1, 0x763c
    li a2, 0x4fb4
    jal copy
#---------------------------------
    li a0, 0x7640
    li a1, 0x7644
    li a2, 0x5054
    jal copy
#---------------------------------
#---------------------------------------
# 等待结束过程：
# s10: 结束标志，为0表示结束
wait_end2:
    beqz s10, quit 
    li s10, 0 
    addi s11, s11, 1
    j load_data 


#---------------------------------
quit: 
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
