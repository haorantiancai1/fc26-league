"""
For each commit, create a test HTML, serve it, and check if doLogin is defined
"""
import subprocess, sys, re, time, os

sys.stdout.reconfigure(encoding='utf-8')

deploy_dir = r'E:\FC26传奇联赛\deploy'

# Test these commits
commits = [
    ('ff29109', 'v50'),
    ('edb679b', 'v49'),
    ('0c7116c', 'v48'),
    ('41ac5b3', 'v47'),
    ('c01cc70', 'v46'),
    ('8a7df20', 'v45'),
    ('cfdec13', 'v44'),
    ('cabc09f', 'v43'),
    ('a36bec8', 'v42-2'),
    ('becf1f0', 'v41'),
    ('c3ebb56', 'v40'),
    ('e0f3913', 'v39'),
    ('25a896b', 'v38'),
    ('801df53', 'v37'),
    ('28791e0', 'v36'),
    ('0292771', 'v35'),
    ('fba8750', 'pre-v35'),
    ('0970058', 'archive'),
    ('c205ef0', 'settlement'),
]

for commit_hash, version in commits:
    # Extract index.html for this commit
    result = subprocess.run(
        ['git', '-C', deploy_dir, 'show', f'{commit_hash}:index.html'],
        capture_output=True, text=True, encoding='utf-8'
    )
    if result.returncode != 0:
        print(f'{version} ({commit_hash}): EXTRACT FAILED')
        continue
    
    html = result.stdout
    test_file = deploy_dir + f'\\_test_{commit_hash}.html'
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f'{version} ({commit_hash}): OK - wrote {len(html)} chars')
