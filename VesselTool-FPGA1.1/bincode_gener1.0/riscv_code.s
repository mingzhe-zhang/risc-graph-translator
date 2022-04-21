.globl __start
.text
__start:
    li a0, 0x1000
    li a1, 0x1170
    li a2, 0xf0000004
    jal datacopy
    li a0, 0x1170
    li a1, 0x12e0
    li a2, 0xf002aaac
    jal datacopy
    li a0, 0x12e0
    li a1, 0x1450
    li a2, 0xf0055558
    jal datacopy
    li a0, 0x1450
    li a1, 0x1668
    li a2, 0xf0080004
    jal datacopy
    li a0, 0x1668
    li a1, 0x17d8
    li a2, 0xf00aaaac
    jal datacopy
    li a0, 0x17d8
    li a1, 0x1948
    li a2, 0xf00d5558
    jal datacopy
    li a0, 0x1948
    li a1, 0x1ab8
    li a2, 0xf0100004
    jal datacopy
    li a0, 0x1ab8
    li a1, 0x1cd0
    li a2, 0xf012aaac
    jal datacopy
    li a0, 0x1cd0
    li a1, 0x1e40
    li a2, 0xf0155558
    jal datacopy
    li a0, 0x1e40
    li a1, 0x1fb0
    li a2, 0xf0180004
    jal datacopy
    li a0, 0x1fb0
    li a1, 0x2120
    li a2, 0xf01aaaac
    jal datacopy
    li a0, 0x2120
    li a1, 0x2368
    li a2, 0xf01d5558
    jal datacopy
    li a0, 0x254c
    li a1, 0x264c
    li a2, 0xf0000404
    jal datacopy
    li a0, 0x264c
    li a1, 0x274c
    li a2, 0xf00aaeac
    jal datacopy
    li a0, 0x274c
    li a1, 0x284c
    li a2, 0xf0155958
    jal datacopy
li a0, 0x10000000
li a1, 1
sw a1, 0(a0)
    li a0, 0x24a8
    li a1, 0x24c8
    li a2, 0xE0000000
    jal copy
    li a0, 0x24d0
    li a1, 0x24f0
    li a2, 0xE0000000
    jal copy
    li a0, 0x24f8
    li a1, 0x2518
    li a2, 0xE0000000
    jal copy
    li a0, 0x2520
    li a1, 0x2540
    li a2, 0xE0000000
    jal copy
    li a0, 0x2408
    li a1, 0x2428
    li a2, 0xE0000000
    jal copy
    li a0, 0x2430
    li a1, 0x2450
    li a2, 0xE0000000
    jal copy
    li a0, 0x2458
    li a1, 0x2478
    li a2, 0xE0000000
    jal copy
    li a0, 0x2480
    li a1, 0x24a0
    li a2, 0xE0000000
    jal copy
    li a0, 0x2368
    li a1, 0x2388
    li a2, 0xE0000000
    jal copy
    li a0, 0x2390
    li a1, 0x23b0
    li a2, 0xE0000000
    jal copy
    li a0, 0x23b8
    li a1, 0x23d8
    li a2, 0xE0000000
    jal copy
    li a0, 0x23e0
    li a1, 0x2400
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
    addi t0, t0, 4
    addi t1, t1, 4
    j datacopyloop
datacopyreturn:
	ret

#---------------------------------
