1.0：
可通过命令行运行python程序，指令格式为python translator_sample -i 汇编文件名 -o 二进制指令文件名
程序默认的输入文件名为"insts.txt"
程序默认输出文件为"binary_inst.txt"

1.1更新：
修正了ISA-def中ctrl域不可更改的问题，且提供了最新的ISA-def名为risc-graph-isa-def1.1.xml
增加了指令格式前4个定义必须是操作符、F0、F1、F2的限制
取消了ctrl域可合并为一个汇编指令操作数的功能，现在如果不为ctrl域中的某一个域填写操作数将默认为0

1.2更新：
生成的二进制指令分为两行，第一行为47-32位，第二行为31-0位