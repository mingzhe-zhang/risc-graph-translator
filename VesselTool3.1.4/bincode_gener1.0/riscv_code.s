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
    li a1, 0x13a0
    li a2, 0xf0000004
    jal datacopy
    li a0, 0x13a0
    li a1, 0x1740
    li a2, 0xf00aaaac
    jal datacopy
    li a0, 0x1740
    li a1, 0x1ae0
    li a2, 0xf0155558
    jal datacopy
    li a0, 0x1ae0
    li a1, 0x2040
    li a2, 0xf0200004
    jal datacopy
    li a0, 0x2040
    li a1, 0x23e0
    li a2, 0xf02aaaac
    jal datacopy
    li a0, 0x23e0
    li a1, 0x2780
    li a2, 0xf0355558
    jal datacopy
    li a0, 0x2780
    li a1, 0x2b20
    li a2, 0xf0400004
    jal datacopy
    li a0, 0x2b20
    li a1, 0x3080
    li a2, 0xf04aaaac
    jal datacopy
    li a0, 0x3080
    li a1, 0x3420
    li a2, 0xf0555558
    jal datacopy
    li a0, 0x3420
    li a1, 0x37c0
    li a2, 0xf0600004
    jal datacopy
    li a0, 0x37c0
    li a1, 0x3b60
    li a2, 0xf06aaaac
    jal datacopy
    li a0, 0x3b60
    li a1, 0x4140
    li a2, 0xf0755558
    jal datacopy
    li a0, 0x4324
    li a1, 0x4564
    li a2, 0xf0000404
    jal datacopy
    li a0, 0x4564
    li a1, 0x47a4
    li a2, 0xf02aaeac
    jal datacopy
    li a0, 0x47a4
    li a1, 0x49e4
    li a2, 0xf0555958
    jal datacopy
li a0, 0x10000000
li a1, 1
sw a1, 0(a0)
    li a0, 0x4280
    li a1, 0x42a0
    li a2, 0xE0000000
    jal copy
    li a0, 0x42a8
    li a1, 0x42c8
    li a2, 0xE0000000
    jal copy
    li a0, 0x42d0
    li a1, 0x42f0
    li a2, 0xE0000000
    jal copy
    li a0, 0x42f8
    li a1, 0x4318
    li a2, 0xE0000000
    jal copy
    li a0, 0x41e0
    li a1, 0x4200
    li a2, 0xE0000000
    jal copy
    li a0, 0x4208
    li a1, 0x4228
    li a2, 0xE0000000
    jal copy
    li a0, 0x4230
    li a1, 0x4250
    li a2, 0xE0000000
    jal copy
    li a0, 0x4258
    li a1, 0x4278
    li a2, 0xE0000000
    jal copy
    li a0, 0x4140
    li a1, 0x4160
    li a2, 0xE0000000
    jal copy
    li a0, 0x4168
    li a1, 0x4188
    li a2, 0xE0000000
    jal copy
    li a0, 0x4190
    li a1, 0x41b0
    li a2, 0xE0000000
    jal copy
    li a0, 0x41b8
    li a1, 0x41d8
    li a2, 0xE0000000
    jal copy
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
