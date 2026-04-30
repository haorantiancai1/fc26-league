"""
Check each git commit's index.html for JS syntax errors using Node.js
"""
import subprocess, sys, os, re, json

sys.stdout.reconfigure(encoding='utf-8')

# Commits to check (newest first)
commits = [
    'ff29109', 'edb679b', '0c7116c', '41ac5b3', 'c01cc70',
    '8a7df20', 'cfdec13', 'cabc09f', 'a36bec8', '144a202',
    'becf1f0', 'c3ebb56', 'e0f3913', '25a896b', '801df53',
    '28791e0', '0292771', 'fba8750', '0970058', 'c205ef0',
]

deploy_dir = r'E:\FC26传奇联赛\deploy'
tmp_file = os.path.join(deploy_dir, '_tmp_syntax_check.js')

FIREBASE_STUB = """
var firebase = {
  apps: [],
  initializeApp: function() { this.apps.push({}); return {database: function(){return {ref:function(){return {set:function(){},get:function(){return Promise.resolve({val:function(){return null}})},on:function(){},off:function(){},remove:function(){return Promise.resolve()},update:function(){return Promise.resolve()},push:function(){return {key:'x',set:function(){return Promise.resolve()}}}}};}};} },
  database: function() {
    return {
      ref: function(path) {
        return {
          set: function(d) { return Promise.resolve(); },
          get: function() { return Promise.resolve({val: function() { return null; }}); },
          on: function() {},
          off: function() {},
          remove: function() { return Promise.resolve(); },
          update: function(d) { return Promise.resolve(); },
          push: function() { return {key:'x', set:function(){return Promise.resolve()}}; }
        };
      }
    };
  }
};
var window = {};
var document = {createElement:function(){return{textContent:'',innerHTML:'',style:{},appendChild:function(){},addEventListener:function(){},classList:{add:function(){},remove:function(){},toggle:function(){},contains:function(){return false}}}},getElementById:function(){return{textContent:'',innerHTML:'',style:{},value:'',checked:false,addEventListener:function(){},removeEventListener:function(){},classList:{add:function(){},remove:function(){},toggle:function(){},contains:function(){return false}},querySelector:function(){return null},querySelectorAll:function(){return[]}}},querySelector:function(){return null},querySelectorAll:function(){return[]},body:{appendChild:function(){},removeChild:function(){}},head:{appendChild:function(){},removeChild:function(){}},addEventListener:function(){},removeEventListener:function(){},readyState:'complete'},createTextNode:function(t){return{textContent:t}},cookie:'',location:{href:'',search:'',hash:''},title:''};
var localStorage = {getItem:function(){return null;},setItem:function(){},removeItem:function(){}};
var console = {log:function(){},warn:function(){},error:function(){},info:function(){},debug:function(){}};
var setTimeout = function(f,t){return 0;};
var setInterval = function(f,t){return 0;};
var clearTimeout = function(){};
var clearInterval = function(){};
var AudioContext = function(){return{};};
var fetch = function(){return Promise.resolve({json:function(){return Promise.resolve({})},text:function(){return Promise.resolve('')}});};
var alert = function(){};
var confirm = function(){return false;};
var navigator = {userAgent:''};
var atob = function(s){return s;};
var btoa = function(s){return s;};
var URL = {createObjectURL:function(){return''}};
var Blob = function(){};
var XMLHttpRequest = function(){return{open:function(){},send:function(){},setRequestHeader:function(){},onload:null,onerror:null,responseText:'',status:200}};
var History = function(){return{pushState:function(){},replaceState:function(){}}};
var performance = {now:function(){return 0}};
var crypto = {randomUUID:function(){return'xxxx-xxxx'}};
var MutationObserver = function(){return{observe:function(){},disconnect:function(){}}};
var ResizeObserver = function(){return{observe:function(){},disconnect:function(){}}};
var IntersectionObserver = function(){return{observe:function(){},disconnect:function(){}}};
var HTMLAudioElement = function(){};
var requestAnimationFrame = function(f){return 0;};
var cancelAnimationFrame = function(){};
"""

for commit in commits:
    # Get the index.html content for this commit
    result = subprocess.run(
        ['git', '-C', deploy_dir, 'show', f'{commit}:index.html'],
        capture_output=True, text=True, encoding='utf-8'
    )
    if result.returncode != 0:
        print(f'{commit}: FAILED to checkout')
        continue
    
    html = result.stdout
    
    # Extract main script (the one without src=)
    scripts = re.findall(r'<script[^>]*>(.*?)</script>', html, re.DOTALL)
    if not scripts:
        print(f'{commit}: NO SCRIPTS FOUND')
        continue
    
    main_js = max(scripts, key=len)
    
    # Write stub + main_js to temp file
    with open(tmp_file, 'w', encoding='utf-8') as f:
        f.write(FIREBASE_STUB)
        f.write(main_js)
    
    # Check syntax with Node.js
    result = subprocess.run(
        [r'C:\Program Files\nodejs\node.exe', '--check', tmp_file],
        capture_output=True, text=True, encoding='utf-8', errors='replace'
    )
    
    if result.returncode == 0:
        print(f'{commit}: OK')
    else:
        err = result.stderr.strip()
        # Extract line number if present
        import re as re2
        line_match = re2.search(r':(\d+)', err)
        line_info = f' (line {line_match.group(1)})' if line_match else ''
        print(f'{commit}: SYNTAX ERROR{line_info}: {err[:120]}')
