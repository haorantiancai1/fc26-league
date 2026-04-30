import sys, re, subprocess, json
sys.stdout.reconfigure(encoding='utf-8')

with open(r'E:\FC26传奇联赛\deploy\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

blocks = list(re.finditer(r'<script>(.*?)</script>', html, re.DOTALL))
main_script = max(blocks, key=lambda m: len(m.group(1))).group(1)
lines = main_script.split('\n')

# Find TEAMS_DATA start
start_line = None
for i, line in enumerate(lines):
    if 'TEAMS_DATA = [' in line:
        start_line = i
        break

print(f'TEAMS_DATA starts at line {start_line}: {lines[start_line][:100]}')

# Count brackets properly - ignore brackets in strings
depth = 0
in_string = False
string_char = None
end_line = None
for i in range(start_line, len(lines)):
    line = lines[i]
    j = 0
    while j < len(line):
        ch = line[j]
        if in_string:
            if ch == '\\':
                j += 2  # Skip escaped char
                continue
            if ch == string_char:
                in_string = False
        else:
            if ch in ('"', "'"):
                in_string = True
                string_char = ch
            elif ch == '[':
                depth += 1
            elif ch == ']':
                depth -= 1
                if depth == 0:
                    end_line = i
                    break
        j += 1
    if end_line:
        break

print(f'TEAMS_DATA ends at line {end_line}: {lines[end_line][:100]}')
print(f'Total lines: {end_line - start_line + 1}')

# Extract and validate JSON
data_lines = lines[start_line:end_line+1]
data_text = '\n'.join(data_lines)
data_text = re.sub(r'TEAMS_DATA\s*=\s*\[', '[', data_text, count=1)
data_text = data_text.rstrip()
if data_text.endswith('];'):
    data_text = data_text[:-2] + ']'

print(f'JSON text length: {len(data_text)}')
try:
    parsed = json.loads(data_text)
    print(f'JSON valid! {len(parsed)} teams')
except json.JSONDecodeError as e:
    print(f'JSON INVALID: {e}')
    err_pos = e.pos
    start_ctx = max(0, err_pos - 150)
    end_ctx = min(len(data_text), err_pos + 150)
    print(f'Context around error (pos {err_pos}):')
    print(data_text[start_ctx:end_ctx])
