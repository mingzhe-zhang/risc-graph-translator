SCALE = 5;
edgefactor = 15;

rand ("seed", 2020);

ijw = edgelist_generator (SCALE, edgefactor);
ijw = adjust_and_output (ijw);
