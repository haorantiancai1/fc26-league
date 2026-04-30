import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'E:\FC26传奇联赛\deploy\index.html', 'rb') as f:
    content = f.read()

# Find the POSITION_COMPAT area
idx = content.find(b'POSITION_COMPAT')
if idx > -1:
    # Show bytes around this area
    chunk = content[idx-50:idx+100]
    print('Hex dump around POSITION_COMPAT:')
    for i in range(0, len(chunk), 16):
        hex_part = ' '.join(f'{b:02x}' for b in chunk[i:i+16])
        ascii_part = ''.join(chr(b) if 32 <= b < 127 else '.' for b in chunk[i:i+16])
        print(f'{i:04x}: {hex_part:<48} {ascii_part}')
