import sys
sys.stdout.reconfigure(encoding='utf-8')

# Quick check: read the playerMoves from Firebase via the page
# Just print what we need
print("Checking playerMoves data...")
print("From console logs we saw:")
print("  21 playerMoves, but 19 had 'player not found' warnings")
print("  This means those 19 moves couldn't find the source player")
print()
print("Wait - the replay 'player not found' was in _fbPullOnLogin")
print("But in initFirebaseSync the incremental replay also ran OK for 21 moves")
print("This is contradictory - need to check the actual move data")
