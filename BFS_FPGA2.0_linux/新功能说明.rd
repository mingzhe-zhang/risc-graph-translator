当pe_module_input.json文件中：
	sparse=1，表示启用稀疏功能
	sparse=0，表示关闭稀疏功能
	is_random=1，表示随机产生数据
	is_random=0，表示按需生成数据，修改data_load.py可改变数据生成方式
	0 < sparse_degree <= sparse_degree_max，表示稀疏度，稀疏度越大数据越稀疏，可能会产生多个连通分量
	sparse_degree_max，表示稀疏度最大值，建议为100
	请查看column_tiling_constraints项，注意约束条件

注意：新增GM.py文件，当使用data_laod.py后如果还想查看运行结果，只能执行这个文件，不可再重新执行data_load.py，
否则会损失原始数据！！！

运行结果验证程序包括推理出的硬件结果与纯软件运行的真是结果，请仔细对比。
验证程序中一个round表示一次完整的迭代，并非某一个tile