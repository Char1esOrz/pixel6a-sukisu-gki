from pathlib import Path
import re
import sys

p = Path(sys.argv[1])
s = p.read_text()
assert re.search(r'^do\.devicecheck=\d+', s, flags=re.M)
assert re.search(r'^device\.name1=.*$', s, flags=re.M)
s = re.sub(r'^do\.devicecheck=\d+', 'do.devicecheck=1', s, flags=re.M)
s = re.sub(r'^device\.name1=.*$', 'device.name1=bluejay', s, flags=re.M)
s = re.sub(r'^device\.name[2-9]=.*$', '', s, flags=re.M)
s = re.sub(r'^kernel\.string=.*$', 'kernel.string=Pixel 6a SukiSU 4.2.1 UAPI5 SUSFS candidate', s, flags=re.M)
p.write_text(s, encoding='utf-8', newline='\n')
print('Restricted AnyKernel3 device check to bluejay.')
