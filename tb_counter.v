`timescale 1ns/1ps

module tb_counter;

reg clk;
reg rst;
wire [3:0] count;

counter uut(
    .clk(clk),
    .rst(rst),
    .count(count)
);

always #5 clk = ~clk;

initial begin
    clk = 0;
    rst = 1;

    #10 rst = 0;

    #100;

    $finish;
end

initial begin
    $dumpfile("counter.vcd");
    $dumpvars(0,tb_counter);
end

endmodule
