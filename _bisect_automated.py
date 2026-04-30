"""
Test each commit version in Playwright to see if doLogin is defined.
Run each version, wait 2s, check typeof doLogin.
"""
import subprocess, sys, os, time, json

sys.stdout.reconfigure(encoding='utf-8')

deploy_dir = r'E:\FC26传奇联赛\deploy'
pw_cmd = r'C:\Users\17087\AppData\Roaming\npm\playwright-cli.cmd'
pw_env = r'C:\Program Files\nodejs;C:\Users\17087\AppData\Roaming\npm;'

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

# Set up env for subprocess
env = os.environ.copy()
env['Path'] = pw_env + env.get('Path', '')

results = []

for commit_hash, version in commits:
    test_url = f'http://localhost:8099/_test_{commit_hash}.html'
    
    try:
        # Open page
        result = subprocess.run(
            ['powershell', '-Command', 
             f'$env:Path = "{pw_env}" + $env:Path; & "{pw_cmd}" open {test_url}'],
            capture_output=True, text=True, encoding='utf-8', errors='replace',
            timeout=15
        )
        
        time.sleep(2)
        
        # Check doLogin
        result2 = subprocess.run(
            ['powershell', '-Command',
             f'$env:Path = "{pw_env}" + $env:Path; & "{pw_cmd}" eval "typeof doLogin"'],
            capture_output=True, text=True, encoding='utf-8', errors='replace',
            timeout=10
        )
        
        # Parse result
        output = result2.stdout + result2.stderr
        if '"function"' in output or 'function' in output.split('Result')[1][:50] if 'Result' in output else '':
            status = 'OK (doLogin defined)'
        elif 'undefined' in output.lower():
            status = 'FAIL (doLogin undefined)'
        else:
            status = f'? ({output.strip()[:80]})'
        
        results.append((version, commit_hash, status))
        print(f'{version}: {status}')
        
    except Exception as e:
        results.append((version, commit_hash, f'ERROR: {str(e)[:60]}'))
        print(f'{version}: ERROR - {str(e)[:60]}')
    
    # Close browser between tests
    try:
        subprocess.run(
            ['powershell', '-Command',
             f'$env:Path = "{pw_env}" + $env:Path; & "{pw_cmd}" close-all'],
            capture_output=True, text=True, timeout=10
        )
    except:
        pass
    time.sleep(1)

print('\n=== SUMMARY ===')
for version, commit_hash, status in results:
    marker = 'OK' if 'OK' in status else 'FAIL'
    print(f'{marker} {version} ({commit_hash}): {status}')
