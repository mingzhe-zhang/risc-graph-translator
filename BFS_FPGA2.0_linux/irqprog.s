.globl __start
.text
__start:
# Interrupt handler
irq_vec:
    # disable irq	
    li x3, 0xFFFFFFF0			# 32'hFFFFFFF0
    
    
  #.word 0x0601e00b		# picorv32_maskirq_insn(zero, x3)
  nop

  #.word 0x0400000B    	# picorv32_retirq_insn() (ret)
  nop   
