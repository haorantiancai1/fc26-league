"""
Binary search: find the first commit with syntax error
"""
import subprocess, sys, re

sys.stdout.reconfigure(encoding='utf-8')

deploy_dir = r'E:\FC26传奇联赛\deploy'
node_exe = r'C:\Program Files\nodejs\node.exe'

# All commits from v35 to v50
commits = [
    ('0292771', 'v35'),
    ('fba8750', 'pre-v35'),
    ('0970058', 'archive'),
    ('c205ef0', 'settlement'),
    ('becf1f0', 'v41'),
    ('c3ebb56', 'v40'),
    ('e0f3913', 'v39'),
    ('25a896b', 'v38'),
    ('801df53', 'v37'),
    ('28791e0', 'v36'),
    ('a36bec8', 'v42-2'),
    ('144a202', 'v42-1'),
    ('cabc09f', 'v43'),
    ('cfdec13', 'v44'),
    ('8a7df20', 'v45'),
    ('c01cc70', 'v46'),
    ('41ac5b3', 'v47'),
    ('0c7116c', 'v48'),
    ('edb679b', 'v49'),
    ('ff29109', 'v50'),
]

for commit_hash, version in commits:
    result = subprocess.run(
        ['git', '-C', deploy_dir, 'show', commit_hash + ':index.html'],
        capture_output=True, text=True, encoding='utf-8'
    )
    if result.returncode != 0:
        print(version + ': EXTRACT FAILED')
        continue
    
    html = result.stdout
    scripts = re.findall(r'<script[^>]*>(.*?)</script>', html, re.DOTALL)
    main_js = max(scripts, key=len)
    
    with open(deploy_dir + '\\_tmp_code.js', 'w', encoding='utf-8') as f:
        f.write(main_js)
    
    r = subprocess.run(
        [node_exe, deploy_dir + '\\_node_eval_test.js'],
        capture_output=True, timeout=15
    )
    
    stdout = r.stdout.decode('utf-8', errors='replace').strip()[:100]
    
    if 'EVAL_OK' in stdout:
        print(version + ' (' + commit_hash + '): OK')
    elif 'EVAL_ERROR' in stdout:
        print(version + ' (' + commit_hash + '): BROKEN')
    else:
        print(version + ' (' + commit_hash + '): ? (stdout=' + stdout + ')')
