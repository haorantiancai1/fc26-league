
/* === 自动更新检测（独立模块，不影响任何现有功能） === */
(function(){
  var _cv = '50'; // 当前版本号，每次发版时更新
  try {
    fetch('version.txt?t=' + Date.now())
      .then(function(r){ return r.text(); })
      .then(function(v){
        var _nv = (v && v.trim()) || '';
        // 从URL中提取v参数，如果与远端版本一致，说明刚刷新完，不提示
        var _urlV = location.search.match(/[?&]v=(\d+)/);
        if(_urlV && _urlV[1] === _nv) return;
        // URL中的v参数等于当前页面内嵌版本号，说明已经是最新的，不提示
        if(_urlV && _urlV[1] === _cv) return;
        // 版本不一致，显示提示条
        if(_nv !== _cv && !document.getElementById('_verBar')){
          var _b = document.createElement('div');
          _b.id = '_verBar';
          _b.style.cssText = 'position:fixed;top:0;left:0;right:0;z-index:999999;background:#00e676;color:#000;text-align:center;padding:10px 16px;font-size:15px;font-weight:600;cursor:pointer;font-family:Inter,sans-serif;';
          _b.innerHTML = '📦 发现新版本（v' + _nv + '）！<u style="margin-left:8px;">点击此处刷新页面</u>';
          _b.onclick = function(){
            _b.style.display = 'none';
            // 跳转到带最新版本号的干净URL
            var _base = location.pathname + location.search.replace(/[&?][_tv]=\d+/g, '').replace(/^\?$/, '');
            var _sep = _base.indexOf('?') >= 0 ? '&' : '?';
            location.replace(_base + _sep + 'v=' + _nv);
          };
          document.body.appendChild(_b);
        }
      })
      .catch(function(){});
  } catch(e){}
})();
