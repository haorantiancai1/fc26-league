import re, subprocess, sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r'E:\FC26传奇联赛\deploy\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

scripts = re.findall(r'<script[^>]*>(.*?)</script>', html, re.DOTALL)
main_js = max(scripts, key=len)
lines = main_js.split('\n')
total = len(lines)

prefix = "var firebase = {initializeApp: function(){}, database: function(){return {ref: function(){return {set:function(){},on:function(){}};}};}};\n"

# Check chunks - but use a wrapper function approach
# Put the code inside a function so unclosed brackets don't matter
chunk = 500
start_line = 1
while start_line <= total:
    end_line = min(start_line + chunk - 1, total)
    test_code = prefix + 'function _test(){\n' + '\n'.join(lines[:end_line]) + '\n}\n'
    with open(r'E:\FC26传奇联赛\deploy\_tmp_test.js', 'w', encoding='utf-8') as f:
        f.write(test_code)
    result = subprocess.run(
        ['C:\\Program Files\\nodejs\\node.exe', '--check', r'E:\FC26传奇联赛\deploy\_tmp_test.js'],
        capture_output=True, text=True, encoding='utf-8', errors='replace'
    )
    if result.returncode != 0:
        # Error in this chunk
        clo, chi = start_line, end_line
        while clo < chi:
            cmid = (clo + chi) // 2
            test_code2 = prefix + 'function _test(){\n' + '\n'.join(lines[:cmid]) + '\n}\n'
            with open(r'E:\FC26传奇联赛\deploy\_tmp_test2.js', 'w', encoding='utf-8') as f:
                f.write(test_code2)
            result2 = subprocess.run(
                ['C:\\Program Files\\nodejs\\node.exe', '--check', r'E:\FC26传奇联赛\deploy\_tmp_test2.js'],
                capture_output=True, text=True, encoding='utf-8', errors='replace'
            )
            if result2.returncode == 0:
                clo = cmid + 1
            else:
                chi = cmid
        print(f'First error at line {clo} (in extracted JS, 1-indexed)')
        for i in range(max(0, clo-5), min(total, clo+10)):
            marker = '>>>' if i+1 == clo else '   '
            print(f'{marker} {i+1:5d}: {lines[i].rstrip()[:150]}')
        break
    else:
        start_line = end_line + 1
        print(f'Lines 1-{end_line}: OK')

if start_line > total:
    print('No syntax error found!')
