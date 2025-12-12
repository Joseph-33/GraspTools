import numpy as np
import re
import sys
filename = sys.argv[1] if len(sys.argv) > 1 else None
combine = '--combine' in sys.argv

if not filename:
    print("Usage: python script.py <filename.sum> [--combine]")
    sys.exit(1)

# filename = "even_sci_n1_layer0.sum"
csf_filename = filename.split(".")[0] + ".c"

# Read entire file once into memory
with open(csf_filename) as fh:
    csf_lines = fh.readlines()

def combine_orbitals(line):
    """Combine + and - orbitals in CSF notation."""
    orbitals = re.findall(r'(\d+[a-z][+-]?)\s*\(\s*(\d+)\)', line)
    
    combined = {}
    for orb, count in orbitals:
        base = orb.rstrip('+-')
        combined[base] = combined.get(base, 0) + int(count)
    
    return ' '.join(f"{orb}({count})" for orb, count in combined.items())

def line_get(x):
    index = x * 3 + 3 - 1
    if index >= len(csf_lines):
        return ""
    
    line = csf_lines[index].strip()
    return combine_orbitals(line) if combine else line
        


start_phrase = "Weights of major contributors to ASF"
found_start = False
useful_lines = []

def extract_from_phrase(file_path, start_phrase="Weights of major contributors to ASF"):
    """Extract lines starting from phrase (includes phrase line)."""
    useful = []
    found = False
    try:
        with open(file_path) as f:
            for line in f:
                if not found and start_phrase in line:
                    found = True
                if found:
                    useful.append(line.strip())
        return useful
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return []


def parse_asf_contributions(lines):
    """Parse ASF weight/CSF pairs from extracted lines."""
    parsed = []
    i = 3  # Skip header lines
    
    while i < len(lines) - 1:
        if lines[i].strip() and ' +' in lines[i]:
            # Parse weights line
            parts = lines[i].split()
            block, level, j_parity = parts[0], parts[1], ' '.join(parts[2:4])
            weights = [float(w) for w in parts[4:]]
            
            # Parse CSF numbers line
            if i + 1 < len(lines):
                csfs = [int(c) for c in lines[i+1].split()]
                
                # Pair weights with CSFs
                pairs = list(zip(weights, csfs))
                parsed.append({
                    'block': int(block),
                    'level': int(level),
                    'j_parity': j_parity,
                    'contributions': pairs
                })
            
            i += 2  # Skip to next pair
        else:
            i += 1
    
    return parsed

# Or even more compact if you don't need dict structure:
def parse_asf_pairs(lines):
    """Return list of (weight, csf) pairs grouped by level."""
    pairs_list = []
    i = 3  # Skip headers
    
    while i < len(lines) - 1:
        if lines[i].strip() and ' +' in lines[i]:
            weights = [float(w) for w in lines[i].split()[4:]]
            csfs = [int(c) for c in lines[i+1].split()]
            pairs_list.append(list(zip(weights, csfs[:len(weights)])))
            i += 2
        else:
            i += 1
    
    return pairs_list

lines = extract_from_phrase(filename)
parsed = parse_asf_contributions(lines)

# for i in range(len(parsed)):
#     print(f"\nBlock: {parsed[i]['block']}, Level: {parsed[i]['level']}, J Parity: {parsed[i]['j_parity']}")
#     
#     # Create formatted string for contributions
#     contrib_strs = []
#     for weight, csf in parsed[i]['contributions']:
#         # Format: cont1: CSF1, cont2: CSF2, etc.
#         csfline = line_get(int(csf))
#         # Using absolute weight index
#         contrib_strs.append(f"{weight:7.4f}: {csfline}")
#     
#     # Print all contributions on one line
#     print("   " + ", ".join(contrib_strs))

print("Block info")
print("-" * 40)

for level_data in parsed:
    print(f"\nBlock: {level_data['block']}, Level: {level_data['level']}, J Parity: {level_data['j_parity']}")
    
    for weight, csf in level_data['contributions']:
        csfline = line_get(int(csf))
        print(f"{weight:7.4f}: {csfline}")
