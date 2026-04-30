"""
Run node without --check, just execute the script
"""
import subprocess, sys, re

sys.stdout.reconfigure(encoding='utf-8')

deploy_dir = r'E:\FC26传奇联赛\deploy'
node_exe = r'C:\Program Files\nodejs\node.exe'

test_commits = [
    ('0292771', 'v35'),
    ('ff29109', 'v50'),
]

for commit_hash, version in test_commits:
    result = subprocess.run(
        ['git', '-C', deploy_dir, 'show', commit_hash + ':index.html'],
        capture_output=True, text=True, encoding='utf-8'
    )
    html = result.stdout
    scripts = re.findall(r'<script[^>]*>(.*?)</script>', html, re.DOTALL)
    main_js = max(scripts, key=len)
    
    with open(deploy_dir + '\\_tmp_code.js', 'w', encoding='utf-8') as f:
        f.write(main_js)
    
    r = subprocess.run(
        [node_exe, deploy_dir + '\\_node_eval_test.js'],
        capture_output=True, timeout=15
    )
    
    stdout = r.stdout.decode('utf-8', errors='replace').strip()[:300]
    stderr = r.stderr.decode('utf-8', errors='replace').strip()[:500] if r.stderr else ''
    print(version + ' (' + commit_hash + '): rc=' + str(r.returncode))
    if stdout:
        print('  stdout: ' + stdout)
    if stderr:
        print('  stderr: ' + stderr[:500])
    print()
