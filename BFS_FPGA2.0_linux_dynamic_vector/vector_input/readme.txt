使用方法：在运行上一级目录的Runthis.py后，修改iter_limit_example.txt文件与vec_ind_example.txt文件成需要的内容，运行vector_loader.py代码即可。

这两个文件的含义如下：
1. 	iter_limit_example.txt文件：
	用于限制迭代次数
	示例：“2”，表示最多迭代两次，此时BFS算法最大的level值为3

2. 	vec_ind_example.txt文件
	用于初始化向量值，每一行表示非零值向量的位置
	示例：
	”
	0
	3
	5
	7
	8
	15
	20
	29
	“
	表示第0，3，5，7，8，15，20，29号节点的初始level设定为1

注1：使用本工具必须在vec_ind_example.txt文件中显式指定初始值，本工具不提供默认值。
注2：本工具暂不支持修改以上两个文件的文件名，如有需要，请自行修改vector_loader.py文件中的第6行和第29行。
注3：如需验证硬件结果正确性，请参考以往方法，上一级目录的验证程序已经过修改，支持这两项自定义功能。