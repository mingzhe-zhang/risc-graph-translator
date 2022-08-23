string = ''
string += '    //Dump Wave\n'
string +=         'initial begin\n'
string +=         '    $fsdbDumpfile("./simwave/<replace>/<replace>.fsdb");\n'
for i in range(16):
    for j in range(9):
        string +=         '    $fsdbDumpvars(0,top.uut_CHIP_DRAM_8G.uut_Host_Nodes_withIO.uut_Host_Nodes.Node_group_'+str(int(i/4))+'['+str(i)+'].uut_Node.PE_NI['+str(j)+'].uut_PE_NI,"+mda");\n'
string +=         'end\n'

print(string)
