// Check if the potential_bump code line exists in buildTeamCard
var html = document.documentElement.outerHTML;
var idx = html.indexOf('potential_bump');
console.log('potential_bump found at index:', idx);
if (idx >= 0) {
    console.log('context:', html.substring(Math.max(0,idx-100), idx+100));
}

// Also check if the buildTeamCard function includes potential_bump
var btcStr = buildTeamCard.toString();
var btcIdx = btcStr.indexOf('potential_bump');
console.log('buildTeamCard potential_bump index:', btcIdx);
if (btcIdx >= 0) {
    console.log('buildTeamCard context:', btcStr.substring(Math.max(0,btcIdx-80), btcIdx+80));
}
