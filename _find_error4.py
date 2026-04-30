import sys, re, subprocess, json
sys.stdout.reconfigure(encoding='utf-8')

with open(r'E:\FC26传奇联赛\deploy\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

blocks = list(re.finditer(r'<script>(.*?)</script>', html, re.DOTALL))
main_script = max(blocks, key=lambda m: len(m.group(1))).group(1)

# Find TEAMS_DATA assignment
idx = main_script.find('TEAMS_DATA = [')
# Find the matching closing ]; — try parsing from idx
# Look for the line after TEAMS_DATA = [ until we find ]; at start of line
lines = main_script.split('\n')

# Find where TEAMS_DATA starts
start_line = None
for i, line in enumerate(lines):
    if 'TEAMS_DATA = [' in line:
        start_line = i
        break

print(f'TEAMS_DATA starts at line {start_line}')

# Try to find where it ends by finding ]; at column 0 or close to it
# Count brackets
depth = 0
end_line = None
for i in range(start_line, len(lines)):
    for ch in lines[i]:
        if ch == '[': depth += 1
        elif ch == ']': depth -= 1
        if depth == 0:
            end_line = i
            break
    if end_line:
        break

print(f'TEAMS_DATA ends at line {end_line}')
print(f'Lines: {end_line - start_line + 1}')

# Try to extract the JSON array and validate
data_lines = lines[start_line:end_line+1]
# Replace TEAMS_DATA = [ with just [
data_text = '\n'.join(data_lines)
data_text = re.sub(r'TEAMS_DATA\s*=\s*\[', '[', data_text, count=1)
# Replace ]; with just ]
data_text = data_text.rstrip()
if data_text.endswith('];'):
    data_text = data_text[:-2] + ']'

print(f'JSON text length: {len(data_text)}')
try:
    parsed = json.loads(data_text)
    print(f'JSON valid! {len(parsed)} teams')
except json.JSONDecodeError as e:
    print(f'JSON INVALID: {e}')
    # Show context around error
    err_pos = e.pos
    start_ctx = max(0, err_pos - 100)
    end_ctx = min(len(data_text), err_pos + 100)
    print(f'Context around error (pos {err_pos}):')
    print(repr(data_text[start_ctx:end_ctx]))
