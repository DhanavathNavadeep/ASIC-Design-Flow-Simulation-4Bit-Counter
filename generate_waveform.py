import sys

def generate_waveform_svg():
    # Setup coordinates
    x_offset = 120
    scale_x = 5.5  # 1 ns = 5.5 pixels
    
    svg_content = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 820 480" width="100%" height="100%">
        <!-- Background -->
        <rect width="820" height="480" fill="#0f172a" rx="10"/>
        
        <!-- Title -->
        <text x="410" y="35" fill="#f8fafc" font-family="Segoe UI, sans-serif" font-size="20" font-weight="bold" text-anchor="middle">
            Simulation Timing Diagram (Waveform)
        </text>
        
        <!-- Definitions for styling -->
        <style>
            .grid { stroke: #334155; stroke-width: 1; stroke-dasharray: 2,2; }
            .grid-label { fill: #64748b; font-family: Segoe UI, sans-serif; font-size: 10px; text-anchor: middle; }
            .sig-label { fill: #94a3b8; font-family: Segoe UI, sans-serif; font-size: 13px; font-weight: bold; }
            .sig-value { fill: #e2e8f0; font-family: monospace; font-size: 11px; text-anchor: middle; }
        </style>
    """
    
    # Draw time grid lines and labels (every 10 ns from 0 to 110)
    for t in range(0, 120, 10):
        x = x_offset + t * scale_x
        # Grid line
        svg_content += f'        <line x1="{x}" y1="60" x2="{x}" y2="380" class="grid" />\n'
        # Grid label
        svg_content += f'        <text x="{x}" y="395" class="grid-label">{t} ns</text>\n'
        
    # Time label header
    svg_content += f'        <text x="{x_offset - 15}" y="395" fill="#94a3b8" font-family="Segoe UI, sans-serif" font-size="11px" font-weight="bold" text-anchor="end">Time:</text>\n'

    # --- CLOCK SIGNAL (clk) ---
    svg_content += f'        <text x="20" y="110" class="sig-label">clk</text>\n'
    clk_path = f"M {x_offset} 120"
    clk_val = 0
    for t in range(5, 115, 5):
        x = x_offset + t * scale_x
        # horizontal line
        y = 120 if clk_val == 0 else 80
        clk_path += f" H {x}"
        # vertical transition
        clk_val = 1 - clk_val
        y_next = 120 if clk_val == 0 else 80
        clk_path += f" V {y_next}"
    # complete last segment to 110 ns
    x_end = x_offset + 110 * scale_x
    clk_path += f" H {x_end}"
    svg_content += f'        <path d="{clk_path}" fill="none" stroke="#38bdf8" stroke-width="2.5" />\n'

    # --- RESET SIGNAL (rst) ---
    svg_content += f'        <text x="20" y="190" class="sig-label">rst</text>\n'
    # High from 0 to 10ns, then drops to Low
    x_rst_fall = x_offset + 10 * scale_x
    rst_path = f"M {x_offset} 160 H {x_rst_fall} V 200 H {x_end}"
    svg_content += f'        <path d="{rst_path}" fill="none" stroke="#f43f5e" stroke-width="2.5" />\n'

    # --- COUNT SIGNAL (count [3:0]) ---
    svg_content += f'        <text x="20" y="270" class="sig-label">count [3:0]</text>\n'
    
    # Transition points for count:
    # 0 to 15ns: 0
    # 15 to 25ns: 1
    # 25 to 35ns: 2
    # 35 to 45ns: 3
    # 45 to 55ns: 4
    # 55 to 65ns: 5
    # 65 to 75ns: 6
    # 75 to 85ns: 7
    # 85 to 95ns: 8
    # 95 to 105ns: 9
    # 105 to 110ns: 10
    transitions = [0, 15, 25, 35, 45, 55, 65, 75, 85, 95, 105, 110]
    values = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    
    for i in range(len(transitions) - 1):
        t_start = transitions[i]
        t_end = transitions[i+1]
        val = values[i]
        
        x1 = x_offset + t_start * scale_x
        x2 = x_offset + t_end * scale_x
        
        # Draw bus lines
        y_top = 250
        y_bot = 280
        
        # Horizontal segments
        if i == 0:
            svg_content += f'        <line x1="{x1}" y1="{y_top}" x2="{x2 - 3}" y2="{y_top}" stroke="#10b981" stroke-width="2" />\n'
            svg_content += f'        <line x1="{x1}" y1="{y_bot}" x2="{x2 - 3}" y2="{y_bot}" stroke="#10b981" stroke-width="2" />\n'
        elif i == len(transitions) - 2:
            svg_content += f'        <line x1="{x1 + 3}" y1="{y_top}" x2="{x2}" y2="{y_top}" stroke="#10b981" stroke-width="2" />\n'
            svg_content += f'        <line x1="{x1 + 3}" y1="{y_bot}" x2="{x2}" y2="{y_bot}" stroke="#10b981" stroke-width="2" />\n'
        else:
            svg_content += f'        <line x1="{x1 + 3}" y1="{y_top}" x2="{x2 - 3}" y2="{y_top}" stroke="#10b981" stroke-width="2" />\n'
            svg_content += f'        <line x1="{x1 + 3}" y1="{y_bot}" x2="{x2 - 3}" y2="{y_bot}" stroke="#10b981" stroke-width="2" />\n'
            
        # Draw crossovers (except at start/end boundary)
        if i > 0:
            svg_content += f'        <!-- crossover at {t_start}ns -->\n'
            svg_content += f'        <line x1="{x1 - 3}" y1="{y_top}" x2="{x1 + 3}" y2="{y_bot}" stroke="#10b981" stroke-width="2" />\n'
            svg_content += f'        <line x1="{x1 - 3}" y1="{y_bot}" x2="{x1 + 3}" y2="{y_top}" stroke="#10b981" stroke-width="2" />\n'
            
        # Draw value label centered in the bus segment
        x_mid = (x1 + x2) / 2
        y_text = 269
        svg_content += f'        <text x="{x_mid}" y="{y_text}" class="sig-value">{val}</text>\n'
        
    # --- LEGEND & LOGS ---
    svg_content += """
        <!-- Legend border -->
        <rect x="50" y="325" width="720" height="45" fill="#1e293b" stroke="#334155" stroke-width="1" rx="5" />
        
        <!-- Legend items -->
        <circle cx="70" cy="347" r="6" fill="#38bdf8" />
        <text x="85" y="351" fill="#cbd5e1" font-family="Segoe UI, sans-serif" font-size="11px">clk (Clock Pulse)</text>
        
        <circle cx="230" cy="347" r="6" fill="#f43f5e" />
        <text x="245" y="351" fill="#cbd5e1" font-family="Segoe UI, sans-serif" font-size="11px">rst (Asynchronous Reset)</text>
        
        <rect x="425" y="341" width="30" height="12" fill="#10b981" rx="2" />
        <text x="465" y="351" fill="#cbd5e1" font-family="Segoe UI, sans-serif" font-size="11px">count [3:0] (Bus value)</text>
        
        <text x="640" y="351" fill="#94a3b8" font-family="Segoe UI, sans-serif" font-size="11px" font-weight="bold">Timescale: 1ns/1ps</text>
    </svg>
    """
    
    with open("counter_waveform.svg", "w") as f:
        f.write(svg_content)
    print("Waveform diagram SVG written to counter_waveform.svg successfully!")

if __name__ == "__main__":
    generate_waveform_svg()
