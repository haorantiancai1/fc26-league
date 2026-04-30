import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'E:\FC26传奇联赛\deploy\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Find TEAMS_DATA section
idx = html.find('TEAMS_DATA = [')
if idx < 0:
    print('TEAMS_DATA assignment not found!')
    sys.exit(1)

# Find the end of the array
arr_start = html.find('[', idx)
depth = 0
arr_end = -1
for i in range(arr_start, min(arr_start + 500000, len(html))):
    if html[i] == '[': depth += 1
    elif html[i] == ']':
        depth -= 1
        if depth == 0:
            arr_end = i
            break

teams_json = html[arr_start:arr_end+1]

# Check for single quotes in the JSON
import re
singles = re.findall(r"'", teams_json)
print(f'Single quotes in TEAMS_DATA JSON: {len(singles)}')

# Check for template literals
templates = re.findall(r'`', teams_json)
print(f'Template literals in TEAMS_DATA JSON: {len(templates)}')

# Check for </script>
scripts = re.findall(r'</script>', teams_json, re.IGNORECASE)
print(f'</script> in TEAMS_DATA JSON: {len(scripts)}')

# Check for newlines inside strings
print(f'Total lines in JSON: {teams_json.count(chr(10))}')

# Check if json.dumps used indent=2 - that changes the format
# The original was compact JSON on one line, now it's multi-line with indent=2
# This shouldn't matter for JS parsing

# Let's check if there are any issues with the try-catch around TEAMS_DATA
tc_start = html.find('try {', max(0, idx - 200))
tc_context = html[tc_start:tc_start+100] if tc_start > 0 else 'NOT FOUND'
print(f'\nTry-catch around TEAMS_DATA:')
print(tc_context)

# Check the TEAMS_DATA assignment line
assign_line = html[idx:idx+50]
print(f'\nTEAMS_DATA assignment:')
print(assign_line)
