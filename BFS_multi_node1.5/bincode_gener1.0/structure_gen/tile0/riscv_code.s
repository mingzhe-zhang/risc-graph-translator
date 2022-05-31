.globl __start
.text
__start:
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
      li s11, 2 
      li s10, 0 
      li s9, 0
      li s8, 144
      li s7, 0
      li s6, 0
      li s5, 0
      li s4, 0



#---------------------------------------
# level���̣�
# t1: ���sram�׵�ַ
select:
    li t1, 0x1990     # ��ǰд��ַ
    li t3, 0x1310    # ��ǰд��ַ
    li a1, 72     # ĩ��ַ
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
    li a0, 0x1080
    li a1, 0x110c
    li a2, 0xE0000000
    add a2, a2, s6
    li a3, 9
    jal config_copy
    li a0, 0xff0
    li a1, 0x107c
    li a2, 0xE0000000
    add a2, a2, s6
    li a3, 9
    jal config_copy
    li a0, 0xf60
    li a1, 0xfec
    li a2, 0xE0000000
    add a2, a2, s6
    li a3, 9
    jal config_copy
    li a0, 0xed0
    li a1, 0xf5c
    li a2, 0xE0000000
    add a2, a2, s6
    li a3, 9
    jal config_copy
    li a0, 0xe40
    li a1, 0xecc
    li a2, 0xE0000000
    add a2, a2, s6
    li a3, 9
    jal config_copy
    li a0, 0xdb0
    li a1, 0xe3c
    li a2, 0xE0000000
    add a2, a2, s6
    li a3, 9
    jal config_copy
    li a0, 0xd20
    li a1, 0xdac
    li a2, 0xE0000000
    add a2, a2, s6
    li a3, 9
    jal config_copy
    li a0, 0xc90
    li a1, 0xd1c
    li a2, 0xE0000000
    add a2, a2, s6
    li a3, 9
    jal config_copy
    li a0, 0xc00
    li a1, 0xc8c
    li a2, 0xE0000000
    add a2, a2, s6
    li a3, 9
    jal config_copy
    addi s7, s7, 1
    addi s4, s4, 1
    addi s9, s9, 1
    li a0, 2
    bne s4, a0, send_config_loop1
    li s4, 0
    li s6, 0
    li s9, 0
wait_result_loop1:
    mv a1, s4
CI_addr_add2:
    beqz a1, conti_wait_node1
    li a2, 0x0800000
    add s6, s6, a2
    addi a1, a1, -1
    j CI_addr_add2
conti_wait_node1:
# t0: �л���Ҫ�ĵ�ַ
li t0, 0xe0000000
add t0, t0, s6
li a2, 0xffffffff
wait_exe0_1:
    lw t1, 0(t0) 
bne t1, a2, wait_exe0_1 
# t0: �л���Ҫ�ĵ�ַ
li t0, 0xe0000004
add t0, t0, s6
li a2, 0xf
wait_exe1_1:
    lw t1, 0(t0) 
bne t1, a2, wait_exe1_1 
#---------------------------------------
# �л�mem_ctrl��riscv���̣�
# t0: �л���Ҫ�ĵ�ַ
li t2, 0xe0000084
add t2, t2, s6
li a3, 36
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
    li t1, 0xf01c7664     # ��ǰд��ַ
    li a1, 0xf01c766c    # ĩ��ַ
    li t3, 0x1310    # sram�����ݴ�������ַ
    li t4, 0x1990    # sram�����ݴ�������ַ
    li a3, 12
    jal wait
    li t1, 0xf0472110     # ��ǰд��ַ
    li a1, 0xf0472118    # ĩ��ַ
    li t3, 0x1340    # sram�����ݴ�������ַ
    li t4, 0x19c0    # sram�����ݴ�������ַ
    li a3, 12
    jal wait
    li t1, 0xf071cbb8     # ��ǰд��ַ
    li a1, 0xf071cbc0    # ĩ��ַ
    li t3, 0x1370    # sram�����ݴ�������ַ
    li t4, 0x19f0    # sram�����ݴ�������ַ
    li a3, 12
    jal wait
    addi s9, s9, 1
    addi s4, s4, 1
    li a0, 2
    bne s4, a0, wait_result_loop1
    li s4, 0
    li s6, 0
load_data: 
    li s4, 0
    li s6, 0
reload_loop1:
    mv a1, s4
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
    li a0, 0x1310
    li a1, 0x133c
    li a2, 0xf0000400
    add a2, a2, s6
    jal datacopy
#---------------------------------
    li a0, 0x1340
    li a1, 0x136c
    li a2, 0xf00e3ce4
    add a2, a2, s6
    jal datacopy
#---------------------------------
    li a0, 0x1370
    li a1, 0x139c
    li a2, 0xf01c75c8
    add a2, a2, s6
    jal datacopy
#---------------------------------
    li a0, 0x1310
    li a1, 0x133c
    li a2, 0xf02aaeac
    add a2, a2, s6
    jal datacopy
#---------------------------------
    li a0, 0x1340
    li a1, 0x136c
    li a2, 0xf038e790
    add a2, a2, s6
    jal datacopy
#---------------------------------
    li a0, 0x1370
    li a1, 0x139c
    li a2, 0xf0472074
    add a2, a2, s6
    jal datacopy
#---------------------------------
    li a0, 0x1310
    li a1, 0x133c
    li a2, 0xf0555958
    add a2, a2, s6
    jal datacopy
#---------------------------------
    li a0, 0x1340
    li a1, 0x136c
    li a2, 0xf0639238
    add a2, a2, s6
    jal datacopy
#---------------------------------
    li a0, 0x1370
    li a1, 0x139c
    li a2, 0xf071cb1c
    add a2, a2, s6
    jal datacopy
#---------------------------------
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
    li a0, 0x1080
    li a1, 0x110c
    li a2, 0xE0000000
    add a2, a2, s6
    li a3, 9
    jal config_copy
    li a0, 0xff0
    li a1, 0x107c
    li a2, 0xE0000000
    add a2, a2, s6
    li a3, 9
    jal config_copy
    li a0, 0xf60
    li a1, 0xfec
    li a2, 0xE0000000
    add a2, a2, s6
    li a3, 9
    jal config_copy
    li a0, 0xed0
    li a1, 0xf5c
    li a2, 0xE0000000
    add a2, a2, s6
    li a3, 9
    jal config_copy
    li a0, 0xe40
    li a1, 0xecc
    li a2, 0xE0000000
    add a2, a2, s6
    li a3, 9
    jal config_copy
    li a0, 0xdb0
    li a1, 0xe3c
    li a2, 0xE0000000
    add a2, a2, s6
    li a3, 9
    jal config_copy
    li a0, 0xd20
    li a1, 0xdac
    li a2, 0xE0000000
    add a2, a2, s6
    li a3, 9
    jal config_copy
    li a0, 0xc90
    li a1, 0xd1c
    li a2, 0xE0000000
    add a2, a2, s6
    li a3, 9
    jal config_copy
    li a0, 0xc00
    li a1, 0xc8c
    li a2, 0xE0000000
    add a2, a2, s6
    li a3, 9
    jal config_copy
    addi s7, s7, 1
    addi s4, s4, 1
    addi s9, s9, 1
    li a0, 2
    bne s4, a0, reload_loop1
    li s4, 0
    li s6, 0
    li s9, 0
wait_result_loop2:
    mv a1, s4
CI_addr_add4:
    beqz a1, conti_wait_node2
    li a2, 0x0800000
    add s6, s6, a2
    addi a1, a1, -1
    j CI_addr_add4
conti_wait_node2:
# t0: �л���Ҫ�ĵ�ַ
li t0, 0xe0000000
add t0, t0, s6
li a2, 0xffffffff
wait_exe0_2:
    lw t1, 0(t0) 
bne t1, a2, wait_exe0_2 
# t0: �л���Ҫ�ĵ�ַ
li t0, 0xe0000004
add t0, t0, s6
li a2, 0xf
wait_exe1_2:
    lw t1, 0(t0) 
bne t1, a2, wait_exe1_2 
#---------------------------------------
# �л�mem_ctrl��riscv���̣�
# t0: �л���Ҫ�ĵ�ַ
li t2, 0xe0000084
add t2, t2, s6
li a3, 36
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
    li t1, 0xf01c7664     # ��ǰд��ַ
    li a1, 0xf01c766c    # ĩ��ַ
    li t3, 0x1310    # sram�����ݴ�������ַ
    li t4, 0x1990    # sram�����ݴ�������ַ
    li a3, 12
    jal wait
    li t1, 0xf0472110     # ��ǰд��ַ
    li a1, 0xf0472118    # ĩ��ַ
    li t3, 0x1340    # sram�����ݴ�������ַ
    li t4, 0x19c0    # sram�����ݴ�������ַ
    li a3, 12
    jal wait
    li t1, 0xf071cbb8     # ��ǰд��ַ
    li a1, 0xf071cbc0    # ĩ��ַ
    li t3, 0x1370    # sram�����ݴ�������ַ
    li t4, 0x19f0    # sram�����ݴ�������ַ
    li a3, 12
    jal wait
    addi s9, s9, 1
    addi s4, s4, 1
    li a0, 2
    bne s4, a0, wait_result_loop2
    li s4, 0
    li s6, 0
#---------------------------------------
# �ȴ��������̣�
# s10: ������־��Ϊ0��ʾ����
wait_end2:
    li a0, 4
    bne s7, a0, load_data
    beqz s10, quit 
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
li a0, 0xf
li a1, 0
sw a1, 0(a0)


#---------------------------------------
# �ȴ������
# t1: ST_addr_start
# a1: ST_addr_end
# t3: vector_buffer_addr
# t4: level_addr
# a3: width
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
    sw a0, 0xc(t3)
    beq s3, x0, buffer2 
    sw s11, 0xc(t4)    #s11��ŵ�ǰlevel
    li s10, 1
buffer2:    
    lw t5, 8(t4) 
    snez t5, t5 
    xori t5, t5, 1
    and s2, s2, t5
    lw a0, 8(t3)
    or a0, a0, s2
    sw a0, 8(t3)
    beq s2, x0, buffer1 
    sw s11, 8(t4)    #s11��ŵ�ǰlevel
    li s10, 1
buffer1:    
    lw t5, 4(t4) 
    snez t5, t5 
    xori t5, t5, 1
    and s1, s1, t5
    lw a0, 4(t3)
    or a0, a0, s1
    sw a0, 4(t3)
    beq s1, x0, buffer0 
    sw s11, 4(t4)    #s11��ŵ�ǰlevel
    li s10, 1
buffer0:   
    lw t5, 0(t4) 
    snez t5, t5 
    xori t5, t5, 1
    and s0, s0, t5
    lw a0, 0(t3)
    or a0, a0, s0
    sw a0, 0(t3)
    beq s0, x0, next 
    sw s11, 0(t4)    #s11��ŵ�ǰlevel
    li s10, 1
next:    
    blt a1, t1, wait_return   # ������ַԽ�磬��ת
    beqz a3, wait_return   # ����ȡ����������Χ����ת
    addi t1, t1, 4
    addi t3, t3, 16 
    addi t4, t4, 16 
    j wait_loop
wait_return:
    ret
#---------------------------------------
# ���˺��������ò�����
# a0: Դ�׵�ַ
# a1: Դĩ��ַ
# a2: Ŀ�׵�ַ
copy:
	mv t0, a0     # ��ǰ����ַ
    mv t1, a2     # ��ǰд��ַ
copyloop:
    blt a1, t0, copyreturn   # ������ַԽ�磬��ת
    lw t2, 0(t0)
    sw t2, 0(t1)
    addi t0, t0, 4
    addi t1, t1, 4
    j copyloop
copyreturn:
	ret

#---------------------------------
#---------------------------------------
# data����ר�ð��˺��������ò�����
# a0: Դ�׵�ַ
# a1: Դĩ��ַ
# a2: Ŀ�׵�ַ
datacopy:
	mv t0, a0     # ��ǰ����ַ
    mv t1, a2     # ��ǰд��ַ
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
    blt a1, t0, datacopyreturn   # ������ַԽ�磬��ת
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
#send�����ݵ�FPGA
#a0: Դ����

sendSingle2FPGA:
  li  t2, 0x00001308  #buffer��ַR2H
  sw a0, 0(t2)  #д������
  ret
#---------------------------------------
# ������Ϣר�ð��˺��������ò�����
# a0: Դ�׵�ַ
# a1: Դĩ��ַ
# a2: Ŀ�׵�ַ
config_copy:
	mv t0, a0     # ��ǰ����ַ
    mv t1, a2     # ��ǰд��ַ
    mv t3, a3
config_copyloop:
    blt a1, t0, config_copyreturn   # ������ַԽ�磬��ת
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
