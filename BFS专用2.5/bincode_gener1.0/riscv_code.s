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
    li t1, 0xE800     # 当前写地址
    li t3, 0xe600    # 当前写地址
    li a1, 36     # 末地址
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

    li a0, 0x1500
    li a1, 0x1814
    li a2, 0xf0000004
    jal datacopy
    li a0, 0x1818
    li a1, 0x1b2c
    li a2, 0xf0038e3c
    jal datacopy
    li a0, 0x1b30
    li a1, 0x1e44
    li a2, 0xf0071c74
    jal datacopy
    li a0, 0x1e48
    li a1, 0x22dc
    li a2, 0xf00aaaac
    jal datacopy
    li a0, 0x22e0
    li a1, 0x25f4
    li a2, 0xf00e38e4
    jal datacopy
    li a0, 0x25f8
    li a1, 0x290c
    li a2, 0xf011c720
    jal datacopy
    li a0, 0x2910
    li a1, 0x2c24
    li a2, 0xf0155558
    jal datacopy
    li a0, 0x2c28
    li a1, 0x311c
    li a2, 0xf018e390
    jal datacopy
    li a0, 0x3120
    li a1, 0x3434
    li a2, 0xf01c71c8
    jal datacopy
    li a0, 0x3438
    li a1, 0x374c
    li a2, 0xf0200004
    jal datacopy
    li a0, 0x3750
    li a1, 0x3a64
    li a2, 0xf0238e3c
    jal datacopy
    li a0, 0x3a68
    li a1, 0x3fbc
    li a2, 0xf0271c74
    jal datacopy
    li a0, 0x3fc0
    li a1, 0x42d4
    li a2, 0xf02aaaac
    jal datacopy
    li a0, 0x42d8
    li a1, 0x45ec
    li a2, 0xf02e38e4
    jal datacopy
    li a0, 0x45f0
    li a1, 0x4904
    li a2, 0xf031c720
    jal datacopy
    li a0, 0x4908
    li a1, 0x4d9c
    li a2, 0xf0355558
    jal datacopy
    li a0, 0x4da0
    li a1, 0x50b4
    li a2, 0xf038e390
    jal datacopy
    li a0, 0x50b8
    li a1, 0x53cc
    li a2, 0xf03c71c8
    jal datacopy
    li a0, 0x53d0
    li a1, 0x56e4
    li a2, 0xf0400004
    jal datacopy
    li a0, 0x56e8
    li a1, 0x5c3c
    li a2, 0xf0438e3c
    jal datacopy
    li a0, 0x5c40
    li a1, 0x5f54
    li a2, 0xf0471c74
    jal datacopy
    li a0, 0x5f58
    li a1, 0x626c
    li a2, 0xf04aaaac
    jal datacopy
    li a0, 0x6270
    li a1, 0x6584
    li a2, 0xf04e38e4
    jal datacopy
    li a0, 0x6588
    li a1, 0x6adc
    li a2, 0xf051c720
    jal datacopy
    li a0, 0x6ae0
    li a1, 0x6df4
    li a2, 0xf0555558
    jal datacopy
    li a0, 0x6df8
    li a1, 0x710c
    li a2, 0xf058e390
    jal datacopy
    li a0, 0x7110
    li a1, 0x7424
    li a2, 0xf05c71c8
    jal datacopy
    li a0, 0x7428
    li a1, 0x78bc
    li a2, 0xf0600004
    jal datacopy
    li a0, 0x78c0
    li a1, 0x7bd4
    li a2, 0xf0638e3c
    jal datacopy
    li a0, 0x7bd8
    li a1, 0x7eec
    li a2, 0xf0671c74
    jal datacopy
    li a0, 0x7ef0
    li a1, 0x8204
    li a2, 0xf06aaaac
    jal datacopy
    li a0, 0x8208
    li a1, 0x869c
    li a2, 0xf06e38e4
    jal datacopy
    li a0, 0x86a0
    li a1, 0x89b4
    li a2, 0xf071c720
    jal datacopy
    li a0, 0x89b8
    li a1, 0x8ccc
    li a2, 0xf0755558
    jal datacopy
    li a0, 0x8cd0
    li a1, 0x8fe4
    li a2, 0xf078e390
    jal datacopy
    li a0, 0x8fe8
    li a1, 0x953c
    li a2, 0xf07c71c8
    jal datacopy
    li a0, 0x9ae4
    li a1, 0x9d50
    li a2, 0xf0000400
    jal datacopy
    li a0, 0x9d54
    li a1, 0x9fc0
    li a2, 0xf00e3ce4
    jal datacopy
    li a0, 0x9fc4
    li a1, 0xa230
    li a2, 0xf01c75c8
    jal datacopy
    li a0, 0xa234
    li a1, 0xa4a0
    li a2, 0xf02aaeac
    jal datacopy
    li a0, 0xa4a4
    li a1, 0xa710
    li a2, 0xf038e790
    jal datacopy
    li a0, 0xa714
    li a1, 0xa980
    li a2, 0xf0472074
    jal datacopy
    li a0, 0xa984
    li a1, 0xabf0
    li a2, 0xf0555958
    jal datacopy
    li a0, 0xabf4
    li a1, 0xae60
    li a2, 0xf0639238
    jal datacopy
    li a0, 0xae64
    li a1, 0xb0d0
    li a2, 0xf071cb1c
    jal datacopy
li a0, 0x10000000
li a1, 1
sw a1, 0(a0)
    li a0, 0x9a40
    li a1, 0x9a60
    li a2, 0xE0000000
    jal copy
    li a0, 0x9a68
    li a1, 0x9a88
    li a2, 0xE0000000
    jal copy
    li a0, 0x9a90
    li a1, 0x9ab0
    li a2, 0xE0000000
    jal copy
    li a0, 0x9ab8
    li a1, 0x9ad8
    li a2, 0xE0000000
    jal copy
    li a0, 0x99a0
    li a1, 0x99c0
    li a2, 0xE0000000
    jal copy
    li a0, 0x99c8
    li a1, 0x99e8
    li a2, 0xE0000000
    jal copy
    li a0, 0x99f0
    li a1, 0x9a10
    li a2, 0xE0000000
    jal copy
    li a0, 0x9a18
    li a1, 0x9a38
    li a2, 0xE0000000
    jal copy
    li a0, 0x9900
    li a1, 0x9920
    li a2, 0xE0000000
    jal copy
    li a0, 0x9928
    li a1, 0x9948
    li a2, 0xE0000000
    jal copy
    li a0, 0x9950
    li a1, 0x9970
    li a2, 0xE0000000
    jal copy
    li a0, 0x9978
    li a1, 0x9998
    li a2, 0xE0000000
    jal copy
    li a0, 0x9860
    li a1, 0x9880
    li a2, 0xE0000000
    jal copy
    li a0, 0x9888
    li a1, 0x98a8
    li a2, 0xE0000000
    jal copy
    li a0, 0x98b0
    li a1, 0x98d0
    li a2, 0xE0000000
    jal copy
    li a0, 0x98d8
    li a1, 0x98f8
    li a2, 0xE0000000
    jal copy
    li a0, 0x97c0
    li a1, 0x97e0
    li a2, 0xE0000000
    jal copy
    li a0, 0x97e8
    li a1, 0x9808
    li a2, 0xE0000000
    jal copy
    li a0, 0x9810
    li a1, 0x9830
    li a2, 0xE0000000
    jal copy
    li a0, 0x9838
    li a1, 0x9858
    li a2, 0xE0000000
    jal copy
    li a0, 0x9720
    li a1, 0x9740
    li a2, 0xE0000000
    jal copy
    li a0, 0x9748
    li a1, 0x9768
    li a2, 0xE0000000
    jal copy
    li a0, 0x9770
    li a1, 0x9790
    li a2, 0xE0000000
    jal copy
    li a0, 0x9798
    li a1, 0x97b8
    li a2, 0xE0000000
    jal copy
    li a0, 0x9680
    li a1, 0x96a0
    li a2, 0xE0000000
    jal copy
    li a0, 0x96a8
    li a1, 0x96c8
    li a2, 0xE0000000
    jal copy
    li a0, 0x96d0
    li a1, 0x96f0
    li a2, 0xE0000000
    jal copy
    li a0, 0x96f8
    li a1, 0x9718
    li a2, 0xE0000000
    jal copy
    li a0, 0x95e0
    li a1, 0x9600
    li a2, 0xE0000000
    jal copy
    li a0, 0x9608
    li a1, 0x9628
    li a2, 0xE0000000
    jal copy
    li a0, 0x9630
    li a1, 0x9650
    li a2, 0xE0000000
    jal copy
    li a0, 0x9658
    li a1, 0x9678
    li a2, 0xE0000000
    jal copy
    li a0, 0x9540
    li a1, 0x9560
    li a2, 0xE0000000
    jal copy
    li a0, 0x9568
    li a1, 0x9588
    li a2, 0xE0000000
    jal copy
    li a0, 0x9590
    li a1, 0x95b0
    li a2, 0xE0000000
    jal copy
    li a0, 0x95b8
    li a1, 0x95d8
    li a2, 0xE0000000
    jal copy
# t0: 切换需要的地址
li t0, 0xe0000000
li a2, 0xffffffff
wait_exe0_1:
    lw t1, 0(t0) 
bne t1, a2, wait_exe0_1 
# t0: 切换需要的地址
li t0, 0xe0000004
li a2, 0xf
wait_exe1_1:
    lw t1, 0(t0) 
bne t1, a2, wait_exe1_1 
#---------------------------------------
# 切换mem_ctrl到riscv过程：
# t0: 切换需要的地址
li t2, 0xe0000084
li a3, 36
wait_st1:
    lw t1, 0(t2) 
    bne t1, a3, wait_st1 
    li a0, 0x10000000
    li a1, 0
    sw a1, 0(a0)


#---------------------------------
    li t1, 0xf01c7664     # 当前写地址
    li a1, 0xf01c766c    # 末地址
    li t3, 0xe600    # sram用于暂存向量地址
    li t4, 0xe800    # sram用于暂存向量地址
    li a3, 12
    jal wait
    li t1, 0xf0472110     # 当前写地址
    li a1, 0xf0472118    # 末地址
    li t3, 0xe630    # sram用于暂存向量地址
    li t4, 0xe830    # sram用于暂存向量地址
    li a3, 12
    jal wait
    li t1, 0xf071cbb8     # 当前写地址
    li a1, 0xf071cbc0    # 末地址
    li t3, 0xe660    # sram用于暂存向量地址
    li t4, 0xe860    # sram用于暂存向量地址
    li a3, 12
    jal wait
    li a0, 0xe600
    li a1, 0xe62c
    li a2, 0x9ae4
    jal copy
#---------------------------------
    li a0, 0xe630
    li a1, 0xe65c
    li a2, 0x9d54
    jal copy
#---------------------------------
    li a0, 0xe660
    li a1, 0xe68c
    li a2, 0x9fc4
    jal copy
#---------------------------------
    li a0, 0xe600
    li a1, 0xe62c
    li a2, 0xa234
    jal copy
#---------------------------------
    li a0, 0xe630
    li a1, 0xe65c
    li a2, 0xa4a4
    jal copy
#---------------------------------
    li a0, 0xe660
    li a1, 0xe68c
    li a2, 0xa714
    jal copy
#---------------------------------
    li a0, 0xe600
    li a1, 0xe62c
    li a2, 0xa984
    jal copy
#---------------------------------
    li a0, 0xe630
    li a1, 0xe65c
    li a2, 0xabf4
    jal copy
#---------------------------------
    li a0, 0xe660
    li a1, 0xe68c
    li a2, 0xae64
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
    li a0, 0x9ae4
    li a1, 0x9b10
    li a2, 0xf0000400
    jal datacopy
    li a0, 0x9d54
    li a1, 0x9d80
    li a2, 0xf00e3ce4
    jal datacopy
    li a0, 0x9fc4
    li a1, 0x9ff0
    li a2, 0xf01c75c8
    jal datacopy
    li a0, 0xa234
    li a1, 0xa260
    li a2, 0xf02aaeac
    jal datacopy
    li a0, 0xa4a4
    li a1, 0xa4d0
    li a2, 0xf038e790
    jal datacopy
    li a0, 0xa714
    li a1, 0xa740
    li a2, 0xf0472074
    jal datacopy
    li a0, 0xa984
    li a1, 0xa9b0
    li a2, 0xf0555958
    jal datacopy
    li a0, 0xabf4
    li a1, 0xac20
    li a2, 0xf0639238
    jal datacopy
    li a0, 0xae64
    li a1, 0xae90
    li a2, 0xf071cb1c
    jal datacopy
li a0, 0xE000005C 
li a1, 1 
sw a1, 0(a0) 
li a1, 0 
sw a1, 0(a0)
li a0, 0x10000000
li a1, 1
sw a1, 0(a0)
    li a0, 0x9a40
    li a1, 0x9a60
    li a2, 0xE0000000
    jal copy
    li a0, 0x9a68
    li a1, 0x9a88
    li a2, 0xE0000000
    jal copy
    li a0, 0x9a90
    li a1, 0x9ab0
    li a2, 0xE0000000
    jal copy
    li a0, 0x9ab8
    li a1, 0x9ad8
    li a2, 0xE0000000
    jal copy
    li a0, 0x99a0
    li a1, 0x99c0
    li a2, 0xE0000000
    jal copy
    li a0, 0x99c8
    li a1, 0x99e8
    li a2, 0xE0000000
    jal copy
    li a0, 0x99f0
    li a1, 0x9a10
    li a2, 0xE0000000
    jal copy
    li a0, 0x9a18
    li a1, 0x9a38
    li a2, 0xE0000000
    jal copy
    li a0, 0x9900
    li a1, 0x9920
    li a2, 0xE0000000
    jal copy
    li a0, 0x9928
    li a1, 0x9948
    li a2, 0xE0000000
    jal copy
    li a0, 0x9950
    li a1, 0x9970
    li a2, 0xE0000000
    jal copy
    li a0, 0x9978
    li a1, 0x9998
    li a2, 0xE0000000
    jal copy
    li a0, 0x9860
    li a1, 0x9880
    li a2, 0xE0000000
    jal copy
    li a0, 0x9888
    li a1, 0x98a8
    li a2, 0xE0000000
    jal copy
    li a0, 0x98b0
    li a1, 0x98d0
    li a2, 0xE0000000
    jal copy
    li a0, 0x98d8
    li a1, 0x98f8
    li a2, 0xE0000000
    jal copy
    li a0, 0x97c0
    li a1, 0x97e0
    li a2, 0xE0000000
    jal copy
    li a0, 0x97e8
    li a1, 0x9808
    li a2, 0xE0000000
    jal copy
    li a0, 0x9810
    li a1, 0x9830
    li a2, 0xE0000000
    jal copy
    li a0, 0x9838
    li a1, 0x9858
    li a2, 0xE0000000
    jal copy
    li a0, 0x9720
    li a1, 0x9740
    li a2, 0xE0000000
    jal copy
    li a0, 0x9748
    li a1, 0x9768
    li a2, 0xE0000000
    jal copy
    li a0, 0x9770
    li a1, 0x9790
    li a2, 0xE0000000
    jal copy
    li a0, 0x9798
    li a1, 0x97b8
    li a2, 0xE0000000
    jal copy
    li a0, 0x9680
    li a1, 0x96a0
    li a2, 0xE0000000
    jal copy
    li a0, 0x96a8
    li a1, 0x96c8
    li a2, 0xE0000000
    jal copy
    li a0, 0x96d0
    li a1, 0x96f0
    li a2, 0xE0000000
    jal copy
    li a0, 0x96f8
    li a1, 0x9718
    li a2, 0xE0000000
    jal copy
    li a0, 0x95e0
    li a1, 0x9600
    li a2, 0xE0000000
    jal copy
    li a0, 0x9608
    li a1, 0x9628
    li a2, 0xE0000000
    jal copy
    li a0, 0x9630
    li a1, 0x9650
    li a2, 0xE0000000
    jal copy
    li a0, 0x9658
    li a1, 0x9678
    li a2, 0xE0000000
    jal copy
    li a0, 0x9540
    li a1, 0x9560
    li a2, 0xE0000000
    jal copy
    li a0, 0x9568
    li a1, 0x9588
    li a2, 0xE0000000
    jal copy
    li a0, 0x9590
    li a1, 0x95b0
    li a2, 0xE0000000
    jal copy
    li a0, 0x95b8
    li a1, 0x95d8
    li a2, 0xE0000000
    jal copy
# t0: 切换需要的地址
li t0, 0xe0000000
li a2, 0xffffffff
wait_exe0_2:
    lw t1, 0(t0) 
bne t1, a2, wait_exe0_2 
# t0: 切换需要的地址
li t0, 0xe0000004
li a2, 0xf
wait_exe1_2:
    lw t1, 0(t0) 
bne t1, a2, wait_exe1_2 
#---------------------------------------
# 切换mem_ctrl到riscv过程：
# t0: 切换需要的地址
li t2, 0xe0000084
li a3, 36
wait_st2:
    lw t1, 0(t2) 
    bne t1, a3, wait_st2 
    li a0, 0x10000000
    li a1, 0
    sw a1, 0(a0)


#---------------------------------
    li t1, 0xf01c7664     # 当前写地址
    li a1, 0xf01c766c    # 末地址
    li t3, 0xe600    # sram用于暂存向量地址
    li t4, 0xe800    # sram用于暂存向量地址
    li a3, 12
    jal wait
    li t1, 0xf0472110     # 当前写地址
    li a1, 0xf0472118    # 末地址
    li t3, 0xe630    # sram用于暂存向量地址
    li t4, 0xe830    # sram用于暂存向量地址
    li a3, 12
    jal wait
    li t1, 0xf071cbb8     # 当前写地址
    li a1, 0xf071cbc0    # 末地址
    li t3, 0xe660    # sram用于暂存向量地址
    li t4, 0xe860    # sram用于暂存向量地址
    li a3, 12
    jal wait
    li a0, 0xe600
    li a1, 0xe62c
    li a2, 0x9ae4
    jal copy
#---------------------------------
    li a0, 0xe630
    li a1, 0xe65c
    li a2, 0x9d54
    jal copy
#---------------------------------
    li a0, 0xe660
    li a1, 0xe68c
    li a2, 0x9fc4
    jal copy
#---------------------------------
    li a0, 0xe600
    li a1, 0xe62c
    li a2, 0xa234
    jal copy
#---------------------------------
    li a0, 0xe630
    li a1, 0xe65c
    li a2, 0xa4a4
    jal copy
#---------------------------------
    li a0, 0xe660
    li a1, 0xe68c
    li a2, 0xa714
    jal copy
#---------------------------------
    li a0, 0xe600
    li a1, 0xe62c
    li a2, 0xa984
    jal copy
#---------------------------------
    li a0, 0xe630
    li a1, 0xe65c
    li a2, 0xabf4
    jal copy
#---------------------------------
    li a0, 0xe660
    li a1, 0xe68c
    li a2, 0xae64
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
# 等待结果：
# t1: ST_addr_start
# a1: ST_addr_end
# t3: vector_buffer_addr
# t4: level_addr
# a3: width
wait:
    li a2, -1 
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
    sw s3, 0xc(t3)
    beq s3, x0, buffer2 
    sw s11, 0xc(t4)    #s11存放当前level
    li s10, 1
buffer2:    
    lw t5, 8(t4) 
    snez t5, t5 
    xori t5, t5, 1
    and s2, s2, t5
    sw s2, 8(t3)
    beq s2, x0, buffer1 
    sw s11, 8(t4)    #s11存放当前level
    li s10, 1
buffer1:    
    lw t5, 4(t4) 
    snez t5, t5 
    xori t5, t5, 1
    and s1, s1, t5
    sw s1, 4(t3)
    beq s1, x0, buffer0 
    sw s11, 4(t4)    #s11存放当前level
    li s10, 1
buffer0:   
    lw t5, 0(t4) 
    snez t5, t5 
    xori t5, t5, 1
    and s0, s0, t5
    sw s0, 0(t3)
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
