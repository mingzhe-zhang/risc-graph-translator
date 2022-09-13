   integer file_src, file_dst;
    initial begin
        file_src = $fopen("./simdumpdat/<replace>/<replace>_SRC.dat","w");
        file_dst = $fopen("./simdumpdat/<replace>/<replace>_DST.dat","w");
        $fwrite(file_src,"====SIM START====\n\n");
        $fwrite(file_dst,"====SIM START====\n\n");
    end
//-------------------------------------------------------------
//--------------------- clks & reset signals ------------------
//-------------------------------------------------------------
    initial 
    begin
        PLL_CKREF_p <= 0;
        forever
        begin
            PLL_CKREF_p = ~PLL_CKREF_p;
            # (50000/4); // 40MHz -> 25ns
        end
    end
	initial begin
		s_reset_n_p <= 0;
		PLL_PD_p    <= 1;
		# (50000*3);
		PLL_PD_p    <= 0;
	end

	initial 
    begin
		clk_FPGA <= 0;
		# (`CLK_PERIORD/4); // No clock edge at T=0
		forever
    	begin
    	    clk_FPGA = ~clk_FPGA;
    	    # (`CLK_PERIORD*2); // 400MHz -> 2.5ns
    	end
	end

	logic riscv_start_0;
	logic riscv_start_1;

	logic cfg_end;
	logic task_end_0;
	logic task_end_1;
	logic task_end_1_to_1;

	logic reading_end;
	logic R_ok;
	logic [20:0] results_addr;


    initial begin
        asyn_rst_n      <= 1'b0;
        bridge_rst_n    <= 1'b0;
		wait(top.uut_CHIP_DRAM_8G.uut_Host_Nodes_withIO.uut_Host_Nodes.uut_PLL_SPI.PLL_LOCK);
    	# (`CLK_PERIORD*5);
        # (`CLK_PERIORD/4);
        asyn_rst_n      <= 1'b1;
		wait(cfg_end);
		# (`CLK_PERIORD*20);
        bridge_rst_n    <= 1'b1;
    end

    initial begin
        pico_rst_n <= 1'b0;
		irq <= 1'b0;
    	wait(riscv_start_0);		// 1st starting pico
        # (`CLK_PERIORD*20);
        pico_rst_n <= 1'b1;

		forever begin
			wait(riscv_start_1);
			# (`CLK_PERIORD*20);
			irq <= 1'b1;
			# (`CLK_PERIORD*4);
			irq <= 1'b0;
		end
	end
//-------------------------------------------------------------
//--------------------- FPGA writes & SRAM writes -------------
//-------------------------------------------------------------
	logic [31:0] dram_data_num_1;
	logic [31:0] sram_data_num_1;

	logic [31:0] cfg_data_num;

	integer file_inform;
	initial begin
		file_inform = $fopen("./case/<replace>/inform.txt","r");
		$fscanf(file_inform," %d %d %d",dram_data_num_1,sram_data_num_1,cfg_data_num);
	end
	logic [31:0] dram_write_num_1;
	logic [31:0] sram_write_num_1;

	logic [31:0] cfg_write_num;

	reg [32-1:0] dram_data_file_1 [20000-1:0];
	reg [32-1:0] dram_addr_file_1 [20000-1:0];
	reg [32-1:0] sram_data_file_1 [4096-1:0];
	reg [32-1:0] sram_addr_file_1 [4096-1:0];

	reg [32-1:0] cfg_data_file [2048-1:0];
	reg [32-1:0] cfg_addr_file [2048-1:0];
	initial begin
		$readmemh("./case/<replace>/TILE/tile0/dram_data.txt", dram_data_file_1);
		$readmemh("./case/<replace>/TILE/tile0/dram_data_addr.txt", dram_addr_file_1);
		$readmemh("./case/<replace>/TILE/tile0/sram_code.txt", sram_data_file_1);
		$readmemh("./case/<replace>/TILE/tile0/sram_code_addr.txt", sram_addr_file_1);

		$readmemh("./case/<replace>/riscv_code.txt", cfg_data_file);
		$readmemh("./case/<replace>/riscv_code_addr.txt", cfg_addr_file);
	end
//-------------------------------------------------------------
//--------------------- states control ------------------------
//-------------------------------------------------------------
	localparam [20:0]
		S_IDLE 		        = 21'd0,
		S_cfg                  = 21'd1,
		S_cfg_polling          = 21'd2,
		S_transfer_1        =21'd3,
		S_polling_1         =21'd4,
		S_reading_results          = 21'd5,
		S_end                      = 21'd6;
	reg [20 : 0] S_state;

	always_ff@(posedge top.clk_FPGA, negedge top.asyn_rst_n) begin
		if ( top.asyn_rst_n == 1'b0 ) begin
	        S_state			<= S_IDLE;
	    end 
        else begin
			case(S_state) 
				S_IDLE : begin
														S_state	<= S_cfg;
				end
				S_cfg : begin
					if (cfg_write_num < cfg_data_num) 	S_state	<= S_cfg;
					else								S_state	<= S_cfg_polling;						
				end
				S_cfg_polling : begin
					if (cfg_end) 						S_state	<= S_transfer_1;
					else								S_state	<= S_cfg_polling;						
				end

				S_transfer_1 : begin
					if ( (sram_write_num_1 < sram_data_num_1) || (dram_write_num_1 < dram_data_num_1) ) begin
														S_state	<= S_transfer_1;
					end
					else								S_state	<= S_polling_1;
				end
				S_polling_1 : begin
					if (task_end_1) 					S_state	<= S_reading_results;
					else if (task_end_1_to_1) 			S_state	<= S_transfer_1;
					else  								S_state	<= S_polling_1;
				end

               S_reading_results : begin
					if (reading_end) 					S_state	<= S_end;
					else								S_state	<= S_reading_results;						
				end
				S_end : begin
					 									S_state	<= S_end;					
				end
				default: begin
														S_state	<= S_cfg;
				end
			endcase


		end
	end


    always_ff@(posedge top.clk_FPGA, negedge top.asyn_rst_n) begin
	    if ( top.asyn_rst_n == 1'b0 ) begin

				riscv_start_0 <= 0;
				riscv_start_1 <= 0;
		end

    	else begin
			if ( (S_state == S_cfg_polling) ) begin            
				riscv_start_0 <= 1;
            end
			else begin											
				riscv_start_0 <= 0;
			end

			if ( (S_state == S_polling_1) ) begin
				riscv_start_1 <= 1;
				end
			else begin
				riscv_start_1 <= 0;
			end
		end
	end

//-------------------------------------------------------------
//--------------------- dump files & end judging --------------
//-------------------------------------------------------------

	reg R_ok_1;
	always_ff@(posedge top.clk_FPGA) begin
		if ( S_state == S_reading_results ) begin
			if (R_ok_1) begin
				$fwrite(file_src,"SRAM Addr: %h,Results Data: %h\n",results_addr-2,QA);
        	    $fwrite(file_dst,"SRAM Addr: %h,Results Data: %h\n",results_addr-2,QA);
			end
		end
		else if ( S_state == S_end ) begin
	        $fwrite(file_src,"\n====SIM FINISH===");
        	$fwrite(file_dst,"\n====SIM FINISH===");
        	$fclose(file_src);
        	$fclose(file_dst);
        	$finish;
	    end 
	end

	/*initial begin
		# (`CLK_PERIORD*400);
		$fclose(file_src);
        $fclose(file_dst);
        $finish;
	end*/
//-------------------------------------------------------------
//--------------------- data transfer -------------------------
//-------------------------------------------------------------
//---------------------- FPGA to sram through port A-----------

	always_ff@(posedge top.clk_FPGA, negedge top.asyn_rst_n) begin
	    if ( top.asyn_rst_n == 1'b0 ) begin
	        CENA            	<= 1'b0;
		    WENA            	<= 0;
            cfg_write_num		<= 0;
			R_ok 				<= 0;
			R_ok_1 				<= 0;
			cfg_end				<= 0;
            results_addr		<= 0;
			reading_end			<= 0;

			sram_write_num_1   <= 0;
			task_end_1         <= 0;
			task_end_1_to_1    <= 0;
		end

        else begin
			if ( (S_state == S_cfg) && (cfg_write_num < cfg_data_num) ) begin
                CENA            <= 1'b1;
		        WENA            <= 1;
                AA              <= cfg_addr_file[cfg_write_num][11:0];
                DA              <= cfg_data_file[cfg_write_num];
                cfg_write_num   <= cfg_write_num + 1;
				R_ok 			<= 0;
				R_ok_1 			<= 0;
            end
			else if ( S_state == S_cfg_polling ) begin
            	if (R_ok_1 && QA != 0) begin
					CENA		<= 1'b0;
					cfg_end		<= 1;
				end
				else if (cfg_end == 1) begin
					CENA		<= 1'b0;
				end
				else begin
					CENA		<= 1'b1;
					AA			<= 11'h4c2;
					cfg_end		<= 0;
				end
				R_ok 			<= CENA;
				R_ok_1 			<= R_ok;
				cfg_write_num		<= 0;
            end

			else if ( (S_state == S_transfer_1) && (sram_write_num_1 < sram_data_num_1) ) begin
				task_end_1			<= 0;
				task_end_1_to_1		<= 0;
				CENA            	<= 1'b1;
				WENA            	<= 1;
				AA              	<= sram_addr_file_1[sram_write_num_1][11:0];
				DA              	<= sram_data_file_1[sram_write_num_1];
				sram_write_num_1  	<= sram_write_num_1 + 1;
				R_ok 				<= 0;
				R_ok_1				<= 0;
				end
			else if ( S_state == S_polling_1 ) begin
				if (R_ok_1 && QA == 32'hf) begin
					CENA			<= 1'b0;
					task_end_1		<= 1;
				end
				else if (R_ok_1 && QA != 0) begin
					CENA			<= 1'b0;
					task_end_1_to_1	<= 1;
				end
				else if ((task_end_1 == 1) || (task_end_1_to_1 == 1)) begin
					CENA			<= 1'b0;
				end
				else begin
					CENA			<= 1'b1;
					AA				<= 11'h4c2;
					task_end_1		<= 0;
					task_end_1_to_1	<= 0;
				end
				R_ok 				<= CENA;
				R_ok_1 			<= R_ok;
				sram_write_num_1  	<= 0;
			end
			else if ( S_state == S_reading_results ) begin
				if (results_addr == 33) begin
					CENA			<= 1'b0;
					reading_end		<= 1;
				end
				else if (reading_end == 1) begin
					CENA			<= 1'b0;
				end
				else begin
					CENA			<= 1'b1;
					AA				<= 3072 + results_addr;
					task_end_1		<= 0;
					results_addr	<= results_addr + 1;
				end
				R_ok 				<= CENA;
				R_ok_1 				<= R_ok;
            end

            else begin
            	CENA            <= 1'b0;
		    	WENA            <= 0;
				R_ok 			<= 0;
				R_ok_1 			<= 0;
            end

        end
    end
    //------------------------------ FPGA AXI master to logic slave AXI----------------------------------
	logic s_awv_awr_flag;
	logic s_arv_arr_flag;
	// Implement s_awready generation
	always_ff@(posedge top.clk_FPGA, negedge top.bridge_rst_n) begin
	  if ( top.bridge_rst_n == 1'b0 )
	    begin
	      m1_AWVALID <= 1'b0;
		  m1_AWADDR  <= 0;
	    end 
	  else
	    begin   
            if ( (S_state == S_transfer_1) ) begin
	      		if (~m1_AWVALID && ~s_awv_awr_flag && ~s_arv_arr_flag
		  				&& (dram_write_num_1 <dram_data_num_1) ) 
	      		  begin
	      		    m1_AWVALID <= 1'b1;
					  m1_AWADDR <= dram_addr_file_1[dram_write_num_1];
	      		  end

	      		else if(m1_AWVALID && m1_AWREADY)       
	      		  begin
	      		    m1_AWVALID <= 1'b0;
	      		  end
			end 


		end 
	end       
//---------------------------------------------------------------------------
	// Implement m1_AWADDR latching
	logic s_awv_awr_part;
	always_ff@(posedge top.clk_FPGA, negedge top.bridge_rst_n) begin
	  if ( top.bridge_rst_n == 1'b0 )
	    begin
		  s_awv_awr_part <= 1'b0;
	    end 
	  else
	    begin    
	      if (m1_AWVALID && ~s_awv_awr_part)
	        begin
			   	s_awv_awr_part <= 1'b1;   
	        end  
			else if (m1_BVALID && m1_BREADY) begin
	          	s_awv_awr_part  <= 1'b0;
	        end 
	    end 
	end    
	assign s_awv_awr_flag = m1_AWVALID || s_awv_awr_part;  
//----------------------------------------------------------------------------------
//**********************************************************************************
//--------------------------------W channel--------------------------------------
//**********************************************************************************
//----------------------------------------------------------------------------------
	// Implement m1_WVALID generation
	always_ff@(posedge top.clk_FPGA, negedge top.bridge_rst_n) begin
	  if ( top.bridge_rst_n == 1'b0 )
	    begin
	      m1_WVALID <= 1'b0;
		  m1_WDATA  <= 0;
		  //m1_WSTRB  <= 0;
	    end 
	  else
	    begin    
			if ( (S_state == S_transfer_1) ) begin
	      		if (~m1_WVALID && ~s_awv_awr_flag && ~s_arv_arr_flag
		  				&& (dram_write_num_1 < dram_data_num_1) ) // if command exists and is a write command
	      		  begin
	      		    m1_WVALID <= 1'b1;
					  m1_WDATA <= dram_data_file_1[dram_write_num_1]; 
					  //m1_WSTRB <= {(AXI_DATA_WIDTH/8){1'b1}}; 
	      		  end

	      		else if(m1_WVALID && m1_WREADY)       
	      		  begin
	      		    m1_WVALID <= 1'b0;
	      		  end
	    	end 


        end
	end   

// add W data process later

//----------------------------------------------------------------------------------
//**********************************************************************************
//-------------------------------B channel-------------------------------------  
//**********************************************************************************
//----------------------------------------------------------------------------------  
	// Implement write response logic generation
	always_ff@(posedge top.clk_FPGA, negedge top.bridge_rst_n) begin
	    if ( top.bridge_rst_n == 1'b0 ) begin
	        m1_BREADY <= 0;

			dram_write_num_1 <= 0;
		end
		else begin
			if (~m1_BREADY && m1_BVALID ) begin
				m1_BREADY <= 1'b1;
				if  ( (S_state == S_transfer_1) ) begin
					dram_write_num_1 <= dram_write_num_1 + 1;
				end
			end

            else begin           
	          m1_BREADY <= 1'b0;   
	        end
	    end
	 end   
//----------------------------------------------------------------------------------
//**********************************************************************************
//-------------------------------AR channel--------------------------------------
//**********************************************************************************
//----------------------------------------------------------------------------------
	// Implement s_arready generation
	always_ff@(posedge top.clk_FPGA, negedge top.bridge_rst_n) begin
	  if ( top.bridge_rst_n == 1'b0 )
	    begin
	      m1_ARVALID <= 1'b0;
		  m1_ARADDR  <= 0;
	    end 
	  else
	    begin    
	      if (~m1_ARVALID && ~s_awv_awr_flag && ~s_arv_arr_flag
		  	  )
	        begin
	          m1_ARVALID <= 1'b0;
			  m1_ARADDR  <= 0;  
	        end
	      else if(m1_ARVALID && m1_ARREADY)         
	        begin
	          m1_ARVALID <= 1'b0;
	        end
	    end 
	end   
//--------------------------------------------------------------------------
	// Implement m1_ARADDR latching. 
	logic s_arv_arr_part;
	always_ff@(posedge top.clk_FPGA, negedge top.bridge_rst_n) begin
	  if ( top.bridge_rst_n == 1'b0 )
	    begin
		  s_arv_arr_part <= 1'b0;
	    end 
	  else
	    begin    
	      if (m1_ARVALID && ~s_arv_arr_part)
	        begin
			   	s_arv_arr_part <= 1'b1;   
	        end  
		  else if (m1_RVALID && m1_RREADY) 
		    begin
	          	s_arv_arr_part  <= 1'b0;
	        end 
	    end 
	end   
	assign s_arv_arr_flag = m1_ARVALID || s_arv_arr_part;
	  
//----------------------------------------------------------------------------------
//**********************************************************************************
//--------------------------------R channel--------------------------------------
//**********************************************************************************
//----------------------------------------------------------------------------------
	// Implement m1_ARVALID generation
	always_ff@(posedge top.clk_FPGA, negedge top.bridge_rst_n) begin
	  if ( top.bridge_rst_n == 1'b0 )
	    begin
	      m1_RREADY <= 0;
	    end 
	  else
	    begin    
		  if (m1_RVALID && ~m1_RREADY)
	        begin
	          m1_RREADY <= 1'b1;
	        end   
	      else 
	        begin
	          m1_RREADY <= 1'b0;
	        end            
	    end
	end     
 
//----------------------------------------------------------------------------------
//**********************************************************************************
//**********************************************************************************
//----------------------------------------------------------------------------------


    //Dump Wave
    initial begin
        $fsdbDumpfile("./simwave/<replace>/<replace>.fsdb");
        $fsdbDumpvars(0,top,"+all");
    end

