import re, sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'E:\FC26传奇联赛\deploy\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

scripts = re.findall(r'<script[^>]*>(.*?)</script>', html, re.DOTALL)
main_js = max(scripts, key=len)

# Look for patterns like: ) /something(  or  } /something(
# that could be confused as regex
# More specifically: look for / immediately followed by ( that's NOT in a string or comment
# This is hard to parse correctly, but let's look for suspicious patterns

lines = main_js.split('\n')
for i, line in enumerate(lines):
    stripped = line.strip()
    # Skip comments
    if stripped.startswith('//') or stripped.startswith('/*') or stripped.startswith('*'):
        continue

    # Look for patterns like: number/something(  or )/something(
    # that could be misinterpreted
    # Key: ) / ... ( where / is actually division but parser thinks it's regex
    if re.search(r'\)\s*/\s*\w', stripped):
        # Check if it looks like a division
        if not re.search(r'=.*/', stripped):  # Not an assignment with regex
            print(f'Line {i+1}: possible div/regex confusion: {stripped[:120]}')

    # Look for lines with /(  that could be regex start
    # but are actually division
    for m in re.finditer(r'/(\w)', stripped):
        pos = m.start()
        # Check what's before the /
        before = stripped[:pos].rstrip()
        if before and (before[-1] in '=<>!&|,;:{}()[]+-~^?%*' or before.endswith('return ') or before.endswith('else ')):
            # Likely a regex
            continue
        # If before is a number or closing bracket, it's division
        if before and (before[-1].isdigit() or before[-1] in ')]}'):
            # Check if what follows could be a regex
            after = stripped[pos+1:]
            if re.match(r'^\(', after):
                print(f'Line {i+1}: SUSPICIOUS / ( after {before[-1]}: {stripped[:120]}')
