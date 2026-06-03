# ASIC 4-Bit Counter Project

A comprehensive development, simulation, and visualization environment for a Verilog-based 4-bit synchronous counter with an asynchronous active-high reset.

---

## 📁 Project Directory Structure

All files in this project are organized in a flat structure at the root directory:

```text
ASIC_Counter_Project/
├── .vscode/
│   ├── launch.json              # VS Code Launch/Debug configurations
│   └── tasks.json               # VS Code automated task configurations
├── counter.v                    # Verilog HDL design module
├── tb_counter.v                 # Verilog simulation testbench
├── simulate.py                  # Python-based logic simulator
├── generate_diagram.py          # Architectural block diagram generator
├── generate_waveform.py         # Timing waveform SVG generator
├── counter_architecture.svg     # SVG Block Diagram of the counter hardware
├── counter_waveform.svg         # SVG Timing Diagram of the simulation waves
├── counter.vcd                  # Value Change Dump waveform data
├── diagram.md                   # Core architecture documentation
└── README.md                    # This project documentation manual
```

---

## ⚙️ 1. HDL Design Details

### Module Interface (`counter.v`)

| Port Name | Direction | Data Type | Width | Description |
|:---|:---|:---|:---|:---|
| `clk` | Input | Wire | 1 bit | System clock signal |
| `rst` | Input | Wire | 1 bit | Active-high asynchronous reset signal |
| `count` | Output | Reg | 4 bits | Current counter value (0 to 15) |

### Verilog Code

```verilog
module counter(
    input clk,
    input rst,
    output reg [3:0] count
);

always @(posedge clk or posedge rst)
begin
    if(rst)
        count <= 4'b0000;
    else
        count <= count + 1;
end

endmodule
```

### Working Principle
* **Asynchronous Reset**: The register resets immediately when `rst` transitions to high (`posedge rst`), regardless of the state of `clk`.
* **Synchronous Increment**: When `rst` is low, the counter increments on the rising edge of `clk` (`posedge clk`). The counter rolls over automatically from `15` (`4'b1111`) to `0` (`4'b0000`) on the next clock pulse due to its 4-bit width limit.

---

## 🧪 2. Verification & Testbench

### Verilog Testbench (`tb_counter.v`)
The testbench validates the logic of the counter under controlled input stimuli.

```verilog
`timescale 1ns/1ps

module tb_counter;

reg clk;
reg rst;
wire [3:0] count;

// Instantiate Unit Under Test (UUT)
counter uut(
    .clk(clk),
    .rst(rst),
    .count(count)
);

// Clock Generation (10ns Period -> 100MHz)
always #5 clk = ~clk;

initial begin
    clk = 0;
    rst = 1;      // Initialize with reset active

    #10 rst = 0;  // Release reset at 10ns

    #100;         // Run simulation for 100ns

    $finish;      // End simulation
end

initial begin
    $dumpfile("counter.vcd");
    $dumpvars(0, tb_counter);
end

endmodule
```

---

## 🐍 3. Python Simulation Tool

Because hardware simulators can sometimes be difficult to set up, this workspace includes a custom Python simulator (`simulate.py`) that models the Verilog behavior and testbench logic exactly.

### Execution
Run the simulation in the terminal:
```bash
python simulate.py
```

### Simulation Log Output
```text
====================================================
           ASIC 4-Bit Counter Simulator             
====================================================
Simulating Verilog Design: counter.v
Timescale: 1ns / 1ps
Output Waveform: counter.vcd

Time (ns)  Clock  Reset  Count (Dec)  Count (Bin)  Waveform Monitor
---------------------------------------------------------------------------
0          0      1      0            0000         [RESET ACTIVE]
5          1      1      0            0000         [RESET ACTIVE]
10         0      0      0            0000         [---------------]
15         1      0      1            0001         [#--------------]
20         0      0      1            0001         [#--------------]
25         1      0      2            0010         [##-------------]
...
105        1      0      10           1010         [##########-----]
110        0      0      10           1010         [##########-----]
---------------------------------------------------------------------------
Simulation completed successfully!
Waveform data updated in counter.vcd
```

---

## 📊 4. Design & Simulation Diagrams

To aid in documentation and understanding, the project includes scripts to programmatically generate beautiful SVG vector diagrams of both the hardware and simulation timing.

### Hardware Block Diagram (`counter_architecture.svg`)
* **Generator**: `generate_diagram.py`
* Shows the connection between the Clock, Reset, Multiplexer, 4-Bit Register (Flip-Flops), and the +1 Combinational Incrementer.

### Timing Diagram (`counter_waveform.svg`)
* **Generator**: `generate_waveform.py`
* Shows waveforms for `clk`, `rst`, and the bus-line transitions of `count [3:0]` from time `0` to `110 ns`.

---

## 💻 5. VS Code IDE Integration

The project comes pre-configured with VS Code integration. You can run all development steps with hotkeys or clicks:

### ⚙️ VS Code Run Configurations (`F5`)
Go to the **Run & Debug** panel (or press `F5`) and select one of the following configurations:
1. **Run Verilog Counter Simulation (Python)**: Runs `simulate.py` in the terminal to execute the simulation and generate `counter.vcd`.
2. **Generate Architecture Diagram**: Runs `generate_diagram.py` to regenerate the hardware diagram SVG file.
3. **Generate Waveform Diagram**: Runs `generate_waveform.py` to regenerate the timing wave SVG file.

### 🛠️ VS Code Build/Run Tasks
Access via **Terminal** -> **Run Task...** (or `Ctrl` + `Shift` + `B` / task menu):
* `Run Counter Simulation`
* `Generate Architecture Diagram`
* `Generate Waveform Diagram`

---

## 📈 6. Viewing Simulation Waveforms (VCD)

The simulation generates a standard Value Change Dump (`.vcd`) file: **`counter.vcd`**.
To view the hardware signals dynamically in a graphical waveform viewer:
1. Open **GTKWave**.
2. Click **File -> Open New Tab** and select `counter.vcd`.
3. In the tree on the left, select `tb_counter` -> click on `uut`.
4. Highlight `clk`, `rst`, and `count [3:0]`, then click **Append** to insert the waves.
