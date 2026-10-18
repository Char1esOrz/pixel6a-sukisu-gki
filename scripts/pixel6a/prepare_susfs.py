"""Match the SUSFS call sites to the pinned SukiSU driver's bool switch."""
from pathlib import Path
import sys

root = Path(sys.argv[1])
driver = (root / 'KernelSU/kernel/feature/sucompat.c').read_text()
assert 'bool ksu_su_compat_enabled __read_mostly = true;' in driver
assert 'ksu_su_compat_enabled = enable;' in driver
for name in ('fs/exec.c', 'fs/open.c', 'fs/stat.c'):
    p = root / 'common' / name
    s = p.read_text()
    declaration = 'extern struct static_key_true ksu_su_compat_enabled;'
    condition = 'static_branch_likely(&ksu_su_compat_enabled)'
    assert s.count(declaration) == 1, name
    assert s.count(condition) == 1, name
    s = s.replace(declaration, 'extern bool ksu_su_compat_enabled;')
    s = s.replace(condition, 'READ_ONCE(ksu_su_compat_enabled)')
    p.write_text(s, encoding='utf-8', newline='\n')
print('Matched all three SUSFS sucompat call sites to the actual bool definition.')
