// Check if potential_bump is present and what buildTeamCard produces
var team = TEAMS_DATA.find(function(t) { return t.team === '切尔西'; });
var p = team.players.find(function(p) { return p.name === '迪迪'; });
console.log('potential_bump:', p.potential_bump);
console.log('is_player:', p.is_player);

// Check what buildTeamCard generates
var result = buildTeamCard('切尔西');
// Find the 迪迪 row
var idx = result.indexOf('迪迪');
if (idx >= 0) {
    console.log('迪迪 row in buildTeamCard output:', result.substring(idx, idx + 200));
} else {
    console.log('迪迪 not found in buildTeamCard output');
}
