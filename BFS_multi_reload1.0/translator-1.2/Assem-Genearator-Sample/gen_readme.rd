程序默认输出文件为assem_inst.txt
默认输出文件b_exeblock*__#为每个exeblock提供的二进制配置信息，*表示PE号，#表示第几个exeblock
默认输出文件inf_exeblock*_#为每个exeblock提供的配置信息说明，*表示PE号，#表示第几个exeblock
默认输出文件data为所需数据，result为计算结果
由于不确定输入配置文件的接口，目前需要在程序代码中手动修改PE大小、PE内exeblock数量以及每个PE处理的两个矩阵的shape
本版本仅为demo
目前没有复用功能，相关位均为0
生成的二进制配置信息完全按照配置信息格式设置