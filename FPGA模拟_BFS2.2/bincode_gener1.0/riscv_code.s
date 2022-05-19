.globl __start
.text
__start:
init:
      li s11, 2 
      li s10, 0 



#---------------------------------------
# level���̣�
# t1: ���sram�׵�ַ
select:
    li t1, 0x1800     # ��ǰд��ַ
    li t3, 0x1600    # ��ǰд��ַ
    li a1, 8     # ĩ��ַ
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

li a0, 0x10000000
li a1, 1
sw a1, 0(a0)
    li a0, 0x770
    li a1, 0x790
    li a2, 0xE0000000
    jal copy
    li a0, 0x798
    li a1, 0x7b8
    li a2, 0xE0000000
    jal copy
    li a0, 0x720
    li a1, 0x740
    li a2, 0xE0000000
    jal copy
    li a0, 0x748
    li a1, 0x768
    li a2, 0xE0000000
    jal copy
    li a0, 0x6d0
    li a1, 0x6f0
    li a2, 0xE0000000
    jal copy
    li a0, 0x6f8
    li a1, 0x718
    li a2, 0xE0000000
    jal copy
    li a0, 0x680
    li a1, 0x6a0
    li a2, 0xE0000000
    jal copy
    li a0, 0x6a8
    li a1, 0x6c8
    li a2, 0xE0000000
    jal copy
#---------------------------------------
# �л�mem_ctrl��riscv���̣�
# t0: �л���Ҫ�ĵ�ַ
li t0, 0xe0000000
li t2, 0xe0000080
li a2, 255
li a3, 8
wait_exe1:
    lw t1, 0(t0) 
    bne t1, a2, wait_exe1 
wait_st1:
    lw t1, 0(t2) 
    bne t1, a3, wait_st1 
    li a0, 0x10000000
    li a1, 0
    sw a1, 0(a0)


#---------------------------------
#---------------------------------------
# �ȴ������
# t1: ���dram�׵�ַ
# t3: ���sram�׵�ַ
wait1:
    li t1, 0xf0300414     # ��ǰд��ַ
    li a1, 0xf0300418    # ĩ��ַ
    li a2, -1 
    li t3, 0x1600 
    li t4, 0x1800 
    li a3, 8
wait_loop1:
    lw s0, 0(t1)
    lw s1, 0(t1)
    lw s2, 0(t1)
    lw s3, 0(t1)
    addi a3, a3, -1
    beqz a3, buffer0_1    
    addi a3, a3, 1
    addi a3, a3, -2
    beqz a3, buffer1_1    
    addi a3, a3, 2
    addi a3, a3, -3
    beqz a3, buffer2_1    
    addi a3, a3, 3
    addi a3, a3, -4
    beqz a3, buffer3_1    
buffer3_1:    
    lw t5, 0xc(t4) 
    snez t5, t5 
    xori t5, t5, 1
    and s3, s3, t5
    sw s3, 0xc(t3)
    beq s3, x0, buffer2_1 
    sw s11, 0xc(t4)    #s11��ŵ�ǰlevel
    li s10, 1
buffer2_1:    
    lw t5, 8(t4) 
    snez t5, t5 
    xori t5, t5, 1
    and s2, s2, t5
    sw s2, 8(t3)
    beq s2, x0, buffer1_1 
    sw s11, 8(t4)    #s11��ŵ�ǰlevel
    li s10, 1
buffer1_1:    
    lw t5, 4(t4) 
    snez t5, t5 
    xori t5, t5, 1
    and s1, s1, t5
    sw s1, 4(t3)
    beq s1, x0, buffer0_1 
    sw s11, 4(t4)    #s11��ŵ�ǰlevel
    li s10, 1
buffer0_1:    
    lw t5, 0(t4) 
    snez t5, t5 
    xori t5, t5, 1
    and s0, s0, t5
    sw s0, 0(t3)
    beq s0, x0, next1 
    sw s11, 0(t4)    #s11��ŵ�ǰlevel
    li s10, 1
next1:    
    blt a1, t1, wait_return1   # ������ַԽ�磬��ת
    beqz a3, wait_return1   # ����ȡ����������Χ����ת
    addi t1, t1, 4
    addi t3, t3, 16 
    addi t4, t4, 16 
    j wait_loop1
wait_return1:

    li a0, 0x1600
    li a1, 0x1604
    li a2, 0x7c4
    jal copy
#---------------------------------
    li a0, 0x1608
    li a1, 0x160c
    li a2, 0x814
    jal copy
#---------------------------------
    li a0, 0x1610
    li a1, 0x1614
    li a2, 0x864
    jal copy
#---------------------------------
    li a0, 0x1618
    li a1, 0x161c
    li a2, 0x8b4
    jal copy
#---------------------------------
#---------------------------------------
# �ȴ��������̣�
# s10: ������־��Ϊ0��ʾ����
wait_end1:
    beqz s10, quit 
    li s10, 0 
    addi s11, s11, 1
    j load_data 


#---------------------------------
load_data: 
    li a0, 0x7c4
    li a1, 0x7c8
    li a2, 0xf0000400
    jal datacopy
    li a0, 0x814
    li a1, 0x818
    li a2, 0xf0100400
    jal datacopy
    li a0, 0x864
    li a1, 0x868
    li a2, 0xf0200400
    jal datacopy
    li a0, 0x8b4
    li a1, 0x8b8
    li a2, 0xf0300400
    jal datacopy
li a0, 0xE000005C 
li a1, 1 
sw a1, 0(a0) 
li a1, 0 
sw a1, 0(a0)
li a0, 0x10000000
li a1, 1
sw a1, 0(a0)
    li a0, 0x770
    li a1, 0x790
    li a2, 0xE0000000
    jal copy
    li a0, 0x798
    li a1, 0x7b8
    li a2, 0xE0000000
    jal copy
    li a0, 0x720
    li a1, 0x740
    li a2, 0xE0000000
    jal copy
    li a0, 0x748
    li a1, 0x768
    li a2, 0xE0000000
    jal copy
    li a0, 0x6d0
    li a1, 0x6f0
    li a2, 0xE0000000
    jal copy
    li a0, 0x6f8
    li a1, 0x718
    li a2, 0xE0000000
    jal copy
    li a0, 0x680
    li a1, 0x6a0
    li a2, 0xE0000000
    jal copy
    li a0, 0x6a8
    li a1, 0x6c8
    li a2, 0xE0000000
    jal copy
#---------------------------------------
# �л�mem_ctrl��riscv���̣�
# t0: �л���Ҫ�ĵ�ַ
li t0, 0xe0000000
li t2, 0xe0000080
li a2, 255
li a3, 8
wait_exe2:
    lw t1, 0(t0) 
    bne t1, a2, wait_exe2 
wait_st2:
    lw t1, 0(t2) 
    bne t1, a3, wait_st2 
    li a0, 0x10000000
    li a1, 0
    sw a1, 0(a0)


#---------------------------------
#---------------------------------------
# �ȴ������
# t1: ���dram�׵�ַ
# t3: ���sram�׵�ַ
wait2:
    li t1, 0xf0300414     # ��ǰд��ַ
    li a1, 0xf0300418    # ĩ��ַ
    li a2, -1 
    li t3, 0x1600 
    li t4, 0x1800 
    li a3, 8
wait_loop2:
    lw s0, 0(t1)
    lw s1, 0(t1)
    lw s2, 0(t1)
    lw s3, 0(t1)
    addi a3, a3, -1
    beqz a3, buffer0_2    
    addi a3, a3, 1
    addi a3, a3, -2
    beqz a3, buffer1_2    
    addi a3, a3, 2
    addi a3, a3, -3
    beqz a3, buffer2_2    
    addi a3, a3, 3
    addi a3, a3, -4
    beqz a3, buffer3_2    
buffer3_2:    
    lw t5, 0xc(t4) 
    snez t5, t5 
    xori t5, t5, 1
    and s3, s3, t5
    sw s3, 0xc(t3)
    beq s3, x0, buffer2_2 
    sw s11, 0xc(t4)    #s11��ŵ�ǰlevel
    li s10, 1
buffer2_2:    
    lw t5, 8(t4) 
    snez t5, t5 
    xori t5, t5, 1
    and s2, s2, t5
    sw s2, 8(t3)
    beq s2, x0, buffer1_2 
    sw s11, 8(t4)    #s11��ŵ�ǰlevel
    li s10, 1
buffer1_2:    
    lw t5, 4(t4) 
    snez t5, t5 
    xori t5, t5, 1
    and s1, s1, t5
    sw s1, 4(t3)
    beq s1, x0, buffer0_2 
    sw s11, 4(t4)    #s11��ŵ�ǰlevel
    li s10, 1
buffer0_2:    
    lw t5, 0(t4) 
    snez t5, t5 
    xori t5, t5, 1
    and s0, s0, t5
    sw s0, 0(t3)
    beq s0, x0, next2 
    sw s11, 0(t4)    #s11��ŵ�ǰlevel
    li s10, 1
next2:    
    blt a1, t1, wait_return2   # ������ַԽ�磬��ת
    beqz a3, wait_return2   # ����ȡ����������Χ����ת
    addi t1, t1, 4
    addi t3, t3, 16 
    addi t4, t4, 16 
    j wait_loop2
wait_return2:

    li a0, 0x1600
    li a1, 0x1604
    li a2, 0x7c4
    jal copy
#---------------------------------
    li a0, 0x1608
    li a1, 0x160c
    li a2, 0x814
    jal copy
#---------------------------------
    li a0, 0x1610
    li a1, 0x1614
    li a2, 0x864
    jal copy
#---------------------------------
    li a0, 0x1618
    li a1, 0x161c
    li a2, 0x8b4
    jal copy
#---------------------------------
#---------------------------------------
# �ȴ��������̣�
# s10: ������־��Ϊ0��ʾ����
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
