code.txt文件生成器（缝合器）1.0版本
功能：将pe指令，配置信息，数据，riscv汇编的二进制信息全部缝合在一起
可自动生成riscv汇编搬运指令（1.0版）

使用说明：
请将所有需要的文件放入test文件夹中
在Windows环境下，运行suture文件
如需linux环境版本，请联系本人
其中，数据文件名需要有data关键字；配置信息文件名需要有exe关键字且以x_y.txt结尾，
表示第x个pe的第y个exeblock的配置信息；pe指令文件需要有pe关键字

内置jupiter汇编器

code.txt为最终生成文件
half_code.txt为未缝合riscv汇编之前文件
hex_riscv_code.txt为十六进制riscv汇编文件
riscv_code.s为自动生成的riscv汇编文件