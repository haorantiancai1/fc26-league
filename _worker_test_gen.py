"""
Find the real JS syntax error using a proper AST-based approach.
Use esprima (JS parser) to parse the main script and get exact error location.
"""
import subprocess, sys, re, json

sys.stdout.reconfigure(encoding='utf-8')

deploy_dir = r'E:\FC26传奇联赛\deploy'

# Read current index.html
with open(deploy_dir + '\\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Extract main script
scripts = re.findall(r'<script[^>]*>(.*?)</script>', html, re.DOTALL)
main_js = max(scripts, key=len)
print(f'Main script: {len(main_js)} chars, {main_js.count(chr(10))} lines')

# Use Chromium (Playwright) to get the exact error via eval
# Write a minimal test HTML that uses a Worker
test_html = '''<!DOCTYPE html>
<html><head><meta charset="utf-8">
<script src="firebase-sdk/firebase-app-compat.js"></script>
<script src="firebase-sdk/firebase-database-compat.js"></script>
</head><body>
<pre id="r"></pre>
<script>
var mainScript = document.querySelector("#main-code").textContent;
var blob = new Blob([mainScript], {type: "text/javascript"});
var worker = new Worker(URL.createObjectURL(blob));
worker.onerror = function(e) {
  document.getElementById("r").textContent = 
    "ERROR: " + e.message + "\\n" + 
    "Line: " + e.lineno + " Col: " + e.colno + "\\n" +
    "File: " + e.filename;
  worker.terminate();
};
worker.onmessage = function(e) {
  document.getElementById("r").textContent = "WORKER OK: " + e.data;
  worker.terminate();
};
</script>
<script id="main-code" type="text/plain">''' + main_js + '''</script>
</body></html>'''

with open(deploy_dir + '\\_worker_test.html', 'w', encoding='utf-8') as f:
    f.write(test_html)

print("Wrote _worker_test.html")
print("Now test in browser...")
