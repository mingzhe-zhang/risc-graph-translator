bincode_gener1.0为最终放入HOST的SRAM中的code.txt生成器
translator-1.2为pe指令生成器和汇编器，其中assem-gen-sample1.2为pe指令生成器，ISA-sample1.1为汇编器
内有详细说明readme.txt

本脚本需要先打开pe_module_input.json文件，修改配置参数，之后执行data_load.py，然后再执行Runthis.py

2.0版本更新：
修改pe_module.json文件，运行Runthis.py，该文件目录下会生成code.txt以及result.txt用于比对。
无需考虑运行目录问题。

3.0版本更新：
修复了部分bug，最终结果ST地址可在ST_ADDR.txt中查看

3.1版本更新：
ST地址默认为从0开始，删除了ST_ADDR.txt文件

3.1.1版本更新：
添加数据范围选项，修改pe_module.json中的min_data以及max_data调整随机数生成范围，
目前不支持浮点数

3.1.2版本更新：
由于目前riscv上挂载的sram大小有限，所以修改了pe指令存储的起始地址，另外添加了超出
sram地址空间报错的功能。

3.1.3版本更新：
修复了ST存储顺序的问题

3.1.4版本更新：
加入了cfg配置信息，修改当前目录下的cfg_config.fig即可修改。

BFS专用1.5：
使用延时方式等待数据写入dram

BFS专用2.0：
增加列tiling，将可运算顶点数扩大

BFS专用2.5：
稳定版本，一次最多36个顶点

BFS_multi_reload1.0：
FPGA模拟单node多次装载指令、数据、配置信息方式

BFS_multi_node1.0：
FPGA模拟多个node多次装载指令、数据、配置信息方式