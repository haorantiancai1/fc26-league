import subprocess, sys, os, re

sys.stdout.reconfigure(encoding='utf-8')

# Check firebase-app-compat.js for syntax errors
result = subprocess.run(
    ['C:\\Program Files\\nodejs\\node.exe', '--check', r'E:\FC26传奇联赛\deploy\firebase-sdk\firebase-app-compat.js'],
    capture_output=True, text=True, encoding='utf-8', errors='replace'
)
print(f'app-compat: return={result.returncode}, stderr={result.stderr[:200] if result.stderr else "none"}')

result = subprocess.run(
    ['C:\\Program Files\\nodejs\\node.exe', '--check', r'E:\FC26传奇联赛\deploy\firebase-sdk\firebase-database-compat.js'],
    capture_output=True, text=True, encoding='utf-8', errors='replace'
)
print(f'db-compat: return={result.returncode}, stderr={result.stderr[:200] if result.stderr else "none"}')
