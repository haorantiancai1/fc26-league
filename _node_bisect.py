"""
Test with Node.js - print both stdout and stderr
"""
import subprocess, sys, re, os, json

sys.stdout.reconfigure(encoding='utf-8')

deploy_dir = r'E:\FC26传奇联赛\deploy'
node_exe = r'C:\Program Files\nodejs\node.exe'

# Test just v35 (earliest) and v50 (latest) to save time
test_commits = [('0292771', 'v35'), ('ff29109', 'v50')]

stub = """var firebase={apps:[],initializeApp:function(){this.apps.push({});return this;},database:function(){return{ref:function(){return{set:function(){return Promise.resolve();},get:function(){return Promise.resolve({val:function(){return null;}});},on:function(){},off:function(){},remove:function(){return Promise.resolve();},update:function(){return Promise.resolve();},push:function(){return{key:'x',set:function(){return Promise.resolve();}}}}}}}}};
var window=global;
var document={createElement:function(){return{textContent:'',innerHTML:'',style:{},appendChild:function(){},addEventListener:function(){},classList:{add:function(){},remove:function(){},toggle:function(){},contains:function(){return false}}}},getElementById:function(){return{textContent:'',innerHTML:'',style:{},value:'',checked:false,addEventListener:function(){},removeEventListener:function(){},classList:{add:function(){},remove:function(){},toggle:function(){},contains:function(){return false}},querySelector:function(){return null},querySelectorAll:function(){return[]}},querySelector:function(){return null},querySelectorAll:function(){return[]},body:{appendChild:function(){},removeChild:function(){}},head:{appendChild:function(){},removeChild:function(){}},addEventListener:function(){},removeEventListener:function(){},readyState:'complete',createTextNode:function(t){return{textContent:t}},cookie:'',location:{href:'',search:'',hash:''},title:''};
var localStorage={getItem:function(){return null;},setItem:function(){},removeItem:function(){}};
var console={log:function(){},warn:function(){},error:function(){},info:function(){},debug:function(){}};
var setTimeout=function(f,t){return 0;};
var setInterval=function(f,t){return 0;};
var clearTimeout=function(){};
var clearInterval=function(){};
var alert=function(){};
var confirm=function(){return false;};
var navigator={userAgent:''};
var atob=function(s){return s;};
var btoa=function(s){return s;};
var fetch=function(){return Promise.resolve({json:function(){return Promise.resolve({})},text:function(){return Promise.resolve('')}});};
var AudioContext=function(){return{};};
var XMLHttpRequest=function(){return{open:function(){},send:function(){},setRequestHeader:function(){},onload:null,onerror:null,responseText:'',status:200}};
var performance={now:function(){return 0;}};
var crypto={randomUUID:function(){return'xxxx-xxxx';}};
var MutationObserver=function(){return{observe:function(){},disconnect:function(){}};};
var ResizeObserver=function(){return{observe:function(){},disconnect:function(){}};};
var IntersectionObserver=function(){return{observe:function(){},disconnect:function(){}};};
var requestAnimationFrame=function(f){return 0;};
var cancelAnimationFrame=function(){};
var History=function(){return{pushState:function(){},replaceState:function(){}};};
var URL={createObjectURL:function(){return'';}};
var Blob=function(){};
var HTMLAudioElement=function(){};
"""

test_file = deploy_dir + '\\_tmp_node_test.js'

for commit_hash, version in test_commits:
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
    print(version + ': main_js is ' + str(len(main_js)) + ' chars')
    
    # Method 1: Write main_js to file, then eval it with stub
    js_file = deploy_dir + '\\_tmp_main.js'
    with open(js_file, 'w', encoding='utf-8') as f:
        f.write(stub)
        f.write('\ntry { eval(require("fs").readFileSync(require("path").join(__dirname, "_tmp_code.js"), "utf8")); console.log("EVAL_OK"); } catch(e) { console.log("EVAL_ERROR: " + e.message); }\n')
    
    with open(deploy_dir + '\\_tmp_code.js', 'w', encoding='utf-8') as f:
        f.write(main_js)
    
    r = subprocess.run(
        [node_exe, js_file],
        capture_output=True, text=True, encoding='utf-8', errors='replace',
        timeout=15
    )
    
    stdout = r.stdout.strip()[:200]
    stderr = r.stderr.strip()[:200] if r.stderr else ''
    rc = r.returncode
    print(version + ': rc=' + str(rc) + ' stdout=[' + stdout + '] stderr=[' + stderr + ']')
