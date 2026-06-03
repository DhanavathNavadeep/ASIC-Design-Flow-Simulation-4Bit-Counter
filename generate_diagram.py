import sys

def generate_svg():
    svg_content = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 500" width="100%" height="100%">
        <!-- Background -->
        <rect width="800" height="500" fill="#0f172a" rx="10"/>
        
        <!-- Title -->
        <text x="400" y="45" fill="#f8fafc" font-family="Segoe UI, sans-serif" font-size="24" font-weight="bold" text-anchor="middle">
            ASIC 4-Bit Counter Architecture
        </text>
        
        <!-- Definitions for Arrowheads -->
        <defs>
            <marker id="arrow" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                <path d="M 0 1 L 10 5 L 0 9 z" fill="#64748b" />
            </marker>
            <marker id="arrow-blue" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                <path d="M 0 1 L 10 5 L 0 9 z" fill="#38bdf8" />
            </marker>
        </defs>

        <!-- 4-Bit Register Block -->
        <rect x="350" y="200" width="120" height="120" fill="#1e293b" stroke="#38bdf8" stroke-width="3" rx="8"/>
        <text x="410" y="250" fill="#f8fafc" font-family="Segoe UI, sans-serif" font-size="16" font-weight="bold" text-anchor="middle">
            4-Bit Reg
        </text>
        <text x="410" y="280" fill="#94a3b8" font-family="Segoe UI, sans-serif" font-size="12" text-anchor="middle">
            (Flip-Flops)
        </text>
        
        <!-- Clock Input Port -->
        <path d="M 350 290 L 365 295 L 350 300" fill="none" stroke="#38bdf8" stroke-width="2"/>
        <text x="340" y="295" fill="#38bdf8" font-family="Segoe UI, sans-serif" font-size="12" text-anchor="end" font-weight="bold">clk</text>
        <line x1="300" y1="295" x2="350" y2="295" stroke="#38bdf8" stroke-width="2" marker-end="url(#arrow-blue)"/>
        
        <!-- Reset Input Port (Asynchronous Reset Arrow) -->
        <text x="410" y="185" fill="#f43f5e" font-family="Segoe UI, sans-serif" font-size="12" text-anchor="middle" font-weight="bold">rst</text>
        <line x1="410" y1="140" x2="410" y2="200" stroke="#f43f5e" stroke-width="2" stroke-dasharray="3,3" marker-end="url(#arrow)"/>

        <!-- Feedback Loop & Adder Block -->
        <!-- Adder (Incrementer) -->
        <rect x="550" y="210" width="100" height="100" fill="#1e293b" stroke="#10b981" stroke-width="3" rx="8"/>
        <text x="600" y="255" fill="#f8fafc" font-family="Segoe UI, sans-serif" font-size="20" font-weight="bold" text-anchor="middle">
            +1
        </text>
        <text x="600" y="285" fill="#94a3b8" font-family="Segoe UI, sans-serif" font-size="12" text-anchor="middle">
            Incrementer
        </text>

        <!-- Multiplexer Block (Selects between reset value and incremented value) -->
        <polygon points="220,180 260,200 260,320 220,340" fill="#1e293b" stroke="#fbbf24" stroke-width="3" />
        <text x="240" y="265" fill="#f8fafc" font-family="Segoe UI, sans-serif" font-size="16" font-weight="bold" text-anchor="middle" transform="rotate(-90 240 265)">
            MUX
        </text>
        
        <!-- MUX Inputs -->
        <!-- Input 0 (Reset value 4'b0000) -->
        <line x1="150" y1="210" x2="220" y2="210" stroke="#64748b" stroke-width="2" marker-end="url(#arrow)"/>
        <text x="140" y="215" fill="#94a3b8" font-family="Segoe UI, sans-serif" font-size="12" text-anchor="end">4'b0000</text>
        
        <!-- Connection from MUX to Reg -->
        <line x1="260" y1="260" x2="350" y2="260" stroke="#f8fafc" stroke-width="2" marker-end="url(#arrow)"/>
        <text x="305" y="250" fill="#94a3b8" font-family="Segoe UI, sans-serif" font-size="12" text-anchor="middle">D [3:0]</text>
        
        <!-- Output Port -->
        <line x1="470" y1="260" x2="520" y2="260" stroke="#38bdf8" stroke-width="3"/>
        <!-- Branch to output count -->
        <line x1="520" y1="260" x2="720" y2="260" stroke="#38bdf8" stroke-width="3" marker-end="url(#arrow-blue)"/>
        <text x="730" y="265" fill="#38bdf8" font-family="Segoe UI, sans-serif" font-size="14" font-weight="bold">count [3:0]</text>
        
        <!-- Branch to Adder input -->
        <line x1="520" y1="260" x2="520" y2="380" stroke="#64748b" stroke-width="2"/>
        <line x1="520" y1="380" x2="680" y2="380" stroke="#64748b" stroke-width="2"/>
        <line x1="680" y1="380" x2="680" y2="260" stroke="#64748b" stroke-width="2"/>
        <line x1="680" y1="260" x2="650" y2="260" stroke="#64748b" stroke-width="2" marker-end="url(#arrow)"/>
        
        <!-- Adder Output to MUX input 1 -->
        <line x1="600" y1="210" x2="600" y2="120" stroke="#64748b" stroke-width="2"/>
        <line x1="600" y1="120" x2="180" y2="120" stroke="#64748b" stroke-width="2"/>
        <line x1="180" y1="120" x2="180" y2="310" stroke="#64748b" stroke-width="2"/>
        <line x1="180" y1="310" x2="220" y2="310" stroke="#64748b" stroke-width="2" marker-end="url(#arrow)"/>
        
        <!-- MUX Select Line (rst) -->
        <line x1="410" y1="140" x2="240" y2="140" stroke="#f43f5e" stroke-width="2"/>
        <line x1="240" y1="140" x2="240" y2="180" stroke="#f43f5e" stroke-width="2" marker-end="url(#arrow)"/>
        <text x="250" y="160" fill="#f43f5e" font-family="Segoe UI, sans-serif" font-size="12" font-weight="bold">sel (rst)</text>
        
        <!-- Annotations / Legends -->
        <rect x="50" y="410" width="700" height="70" fill="#1e293b" stroke="#334155" stroke-width="1" rx="5"/>
        <text x="60" y="435" fill="#94a3b8" font-family="Segoe UI, sans-serif" font-size="12" font-weight="bold">Function Summary:</text>
        <text x="60" y="455" fill="#cbd5e1" font-family="Segoe UI, sans-serif" font-size="12">
            - On clk posedge or rst posedge, the state updates.
        </text>
        <text x="400" y="455" fill="#cbd5e1" font-family="Segoe UI, sans-serif" font-size="12">
            - If rst is active (1), count resets to 0000. Else, it increments by 1.
        </text>
    </svg>
    """
    with open("counter_architecture.svg", "w") as f:
        f.write(svg_content)
    print("Architecture diagram SVG written to counter_architecture.svg successfully!")

if __name__ == "__main__":
    generate_svg()
