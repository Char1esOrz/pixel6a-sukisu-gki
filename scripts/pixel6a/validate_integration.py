from pathlib import Path
import subprocess
import sys

root = Path(sys.argv[1])
assert subprocess.check_output(['git', '-C', str(root / 'common'), 'rev-parse', 'HEAD'], text=True).strip() == '1563b4144ef81c66cfbe02e85bb3570fd2167dfd'
rejects = list((root / 'common').rglob('*.rej')) + list((root / 'KernelSU').rglob('*.rej'))
assert not rejects, f'Unapplied patch hunks: {rejects}'
config = (root / 'common/arch/arm64/configs/gki_defconfig').read_text()
for option in ('CONFIG_KSU=y', 'CONFIG_KSU_SUSFS=y', 'CONFIG_KSU_SUSFS_SUS_PATH=y'):
    assert option in config, option
for option in ('CONFIG_KPM=y', 'CONFIG_BBG=y', 'CONFIG_REKERNEL=y'):
    assert option not in config, option
exec_c = (root / 'common/fs/exec.c').read_text()
assert 'is_su_session = !ksu_handle_execveat_sucompat' in exec_c
assert 'ksu_handle_post_execveat_sucompat(&fd' in exec_c
assert 'KERNEL_SU_UAPI_VERSION, 5' in (root / 'KernelSU/kernel/include/uapi/supercall.h').read_text()
for name in ('fs/exec.c', 'fs/open.c', 'fs/stat.c'):
    contents = (root / 'common' / name).read_text()
    assert 'extern bool ksu_su_compat_enabled;' in contents, name
    assert 'READ_ONCE(ksu_su_compat_enabled)' in contents, name
    assert 'static_branch_likely(&ksu_su_compat_enabled)' not in contents, name
print('Pinned common source, SUSFS hooks, UAPI and configuration checks passed.')
