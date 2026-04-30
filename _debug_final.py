import re, subprocess, sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r'E:\FC26传奇联赛\deploy\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Find the line number reported by browser: 12923
# But we added window.onerror script (1 line), so original was 12922
# Main script starts at HTML line 795 (with onerror at 760)
# Wait - we're now on v49 (checkout edb679b), which doesn't have onerror

# Let me re-read the file to check
line_12923 = html.split('\n')[12922]  # 0-indexed
print(f'HTML line 12923: {line_12923.strip()[:100]}')

# Check: does the HTML have a line 12923? 
total_lines = len(html.split('\n'))
print(f'Total HTML lines: {total_lines}')

# The error was from a version WITH window.onerror (1 extra script tag)
# Current v49 doesn't have it. So the line numbers might differ.

# Actually - the browser error said the SyntaxError was at line 12923
# in the PAGE. Let me check what's at that line in the current v49 version.

# Hmm - we checked out v49 but the onerror test added its own line.
# The browser test (_browser_test.html) fetches index.html and extracts the script.
# So the line number is within the extracted script, not the HTML.

# The original onerror capture said: "http://localhost:8099/:12923:5"
# That's the HTML file line 12923.

# Let's just try wrapping the ENTIRE main script in eval in the browser
# and see if it works or fails.

# Actually, the key insight: the browser said the error is at HTML line 12923.
# But we showed that line is just "}" which is fine.
# The real error must be BEFORE that line, and 12923 is where the parser gives up.

# Let me check: is there a </script> hidden somewhere in the JS?
count = html.lower().count('</script>')
print(f'</script> count in HTML: {count}')

# Find all positions
import re
for m in re.finditer(r'</script>', html, re.IGNORECASE):
    context = html[max(0,m.start()-30):m.end()+10]
    print(f'  at {m.start()}: ...{context}...')
