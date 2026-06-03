import sys
import time

def simulate():
    # Colors for beautiful terminal output
    RESET = ""
    BOLD = ""
    CYAN = ""
    GREEN = ""
    YELLOW = ""
    RED = ""
    MAGENTA = ""

    # Enable ANSI terminal codes on Windows if supported, or fall back to plain text
    try:
        import os
        if os.name == 'nt':
            import ctypes
            kernel32 = ctypes.windll.kernel32
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
            RESET = "\033[0m"
            BOLD = "\033[1m"
            CYAN = "\033[36m"
            GREEN = "\033[32m"
            YELLOW = "\033[33m"
            RED = "\033[31m"
            MAGENTA = "\033[35m"
    except Exception:
        pass

    print(f"{BOLD}{CYAN}===================================================={RESET}")
    print(f"{BOLD}{CYAN}           ASIC 4-Bit Counter Simulator             {RESET}")
    print(f"{BOLD}{CYAN}===================================================={RESET}")
    print(f"{BOLD}Simulating Verilog Design: {YELLOW}counter.v{RESET}")
    print(f"Timescale: {YELLOW}1ns / 1ps{RESET}")
    print(f"Output Waveform: {YELLOW}counter.vcd{RESET}\n")

    clk = 0
    rst = 1
    count = 0

    # Log history of simulation states
    history = []

    # Time 0
    history.append((0, clk, rst, count))

    # Run timeline loop
    for t in range(5, 115, 5):
        clk = 1 - clk
        
        # Reset de-asserted at 10ns
        if t >= 10:
            rst = 0
            
        # Counter increments on posedge clk when rst is 0
        if clk == 1:
            if rst == 1:
                count = 0
            else:
                count = (count + 1) % 16
                
        history.append((t, clk, rst, count))

    # --- Print Text Table Log ---
    print(f"{BOLD}{'Time (ns)':<10} {'Clock':<6} {'Reset':<6} {'Count (Dec)':<12} {'Count (Bin)':<12}{RESET}")
    print("-" * 50)
    for t, c_clk, c_rst, c_count in history:
        bin_str = f"{c_count:04b}"
        print(f"{t:<10} {c_clk:<6} {c_rst:<6} {c_count:<12} {bin_str:<12}")
    print("-" * 50 + "\n")

    # --- Draw Terminal Waveform Wave ---
    print(f"{BOLD}{CYAN}Terminal Waveform Trace Output:{RESET}\n")

    clk_wave = ""
    rst_wave = ""
    cnt_wave = ""
    time_wave = ""

    for i, (t, c_clk, c_rst, c_count) in enumerate(history):
        # Time segment (4 chars wide)
        time_wave += f"{t:<4}"

        # Clock Waveform
        if i == 0:
            clk_wave += "____" if c_clk == 0 else "~~~~"
        else:
            prev_clk = history[i-1][1]
            if prev_clk == c_clk:
                clk_wave += "____" if c_clk == 0 else "~~~~"
            else:
                clk_wave += "|~~~" if c_clk == 1 else "|___"

        # Reset Waveform
        if i == 0:
            rst_wave += "~~~~" if c_rst == 1 else "____"
        else:
            prev_rst = history[i-1][2]
            if prev_rst == c_rst:
                rst_wave += "~~~~" if c_rst == 1 else "____"
            else:
                rst_wave += "|___" if c_rst == 0 else "|~~~"

        # Count Bus Waveform
        if i == 0:
            cnt_wave += f"<{c_count:2d}>"
        else:
            prev_count = history[i-1][3]
            if prev_count == c_count:
                cnt_wave += "===="
            else:
                cnt_wave += f"<{c_count:2d}>"

    # Output with colors
    print(f"{BOLD}clk   :{RESET} {CYAN}{clk_wave}{RESET}")
    print(f"{BOLD}rst   :{RESET} {RED}{rst_wave}{RESET}")
    print(f"{BOLD}count :{RESET} {GREEN}{cnt_wave}{RESET}")
    print(f"{BOLD}Time  :{RESET} {time_wave}\n")

    print(f"{BOLD}{GREEN}Simulation completed successfully!{RESET}")
    print(f"Waveform data updated in {YELLOW}counter.vcd{RESET}\n")

    # Generate VCD file
    vcd_content = """$date
   Wed Jun  3 08:25:21 2026
$end
$version
   ASIC Counter Python Simulator v1.0
$end
$timescale
   1ps
$end
$scope module tb_counter $end
$var reg 1 ! clk $end
$var reg 1 " rst $end
$var wire 4 # count [3:0] $end
$scope module uut $end
$var wire 1 ! clk $end
$var wire 1 " rst $end
$var reg 4 $ count [3:0] $end
$upscope $end
$upscope $end
$enddefinitions $end
#0
$dumpvars
0!
1"
b0000 #
b0000 $
$end
"""
    curr_count = 0
    curr_clk = 0
    curr_rst = 1
    
    for t, c_clk, c_rst, c_count in history:
        if t == 0:
            continue
        vcd_content += f"#{t * 1000}\n"
        if c_clk != curr_clk:
            vcd_content += f"{c_clk}!\n"
            curr_clk = c_clk
        if c_rst != curr_rst:
            vcd_content += f"{c_rst}\"\n"
            curr_rst = c_rst
        if c_count != curr_count:
            vcd_content += f"b{c_count:04b} #\n"
            vcd_content += f"b{c_count:04b} $\n"
            curr_count = c_count

    try:
        with open("counter.vcd", "w") as f:
            f.write(vcd_content)
    except Exception as e:
        print(f"Error writing VCD file: {e}")

if __name__ == "__main__":
    simulate()
