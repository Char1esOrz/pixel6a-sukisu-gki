"""Synchronize builtin's stale UAPI declaration after verifying its implementations."""
from pathlib import Path
import subprocess
import sys

root = Path(sys.argv[1])
expected = 'ee35e65428054476c279eae59f7f2bba272040b9'
assert subprocess.check_output(['git', '-C', str(root), 'rev-parse', 'HEAD'], text=True).strip() == expected
checks = {
    'kernel/supercall/supercall.c': ['KSU_DRIVER_PERMISSION_SU_SESSION', 'int ksu_install_su_fd(void)', 'ksu_is_su_session_fd'],
    'kernel/supercall/dispatch.c': ['case EVENT_SERVICES:', 'services_started = false;', 'return 1;', 'cmd.uapi_version = KERNEL_SU_UAPI_VERSION;'],
    'kernel/feature/sucompat.c': ['ksu_handle_post_execveat_sucompat', 'ksu_install_su_fd();'],
    'kernel/include/uapi/supercall.h': ['EVENT_SERVICES, 4', 'KSU_IOCTL_MANAGER,'],
}
for name, tokens in checks.items():
    contents = (root / name).read_text(encoding='utf-8-sig')
    for token in tokens:
        assert token in contents, (name, token)

p = root / 'kernel/include/uapi/supercall.h'
s = p.read_text(encoding='utf-8-sig')
old = '// 2: allowlist v4 root profile flag\nDECLARE(__u32, KERNEL_SU_UAPI_VERSION, 2);'
new = '''// 2: allowlist v4 root profile flag
// 3: scoped su-session driver fd (implemented in this pinned builtin source)
// 4: bundled-driver flag (unset for this standalone builtin driver)
// 5: EVENT_SERVICES start/skip result (implemented in dispatch.c)
DECLARE(__u32, KERNEL_SU_UAPI_VERSION, 5);'''
assert s.count(old) == 1
s = s.replace(old, new)
anchor = 'DECLARE(__u32, KSU_GET_INFO_FLAG_PR_BUILD, (1U << 3));'
assert s.count(anchor) == 1
s = s.replace(anchor, anchor + '\nDECLARE(__u32, KSU_GET_INFO_FLAG_BUNDLED, (1U << 4));')
p.write_text(s, encoding='utf-8', newline='\n')

# Resolve version counts against an immutable revision, not a moving main branch.
p = root / 'kernel/Makefile'
s = p.read_text(encoding='utf-8')
assert 'REPO_BRANCH := main' in s
s = s.replace('REPO_BRANCH := main', 'REPO_BRANCH := ' + expected)
s = s.replace('VERSION_TAG     := $(or $(KSU_GITHUB_VER),$(git_latest_tag),4.2.1)', 'VERSION_TAG     := 4.2.1')
s = s.replace('KSU_GITHUB_VER   := $(shell $(CURL_BIN) -s "$(GITHUB_API_BASE)/releases/latest" 2>/dev/null | grep \'"tag_name":\' | sed -E \'s/.*"v?([^\"]+)".*/\\1/\')', 'KSU_GITHUB_VER   := 4.2.1')
s = s.replace('@$(call git_branch)', '@pixel6a-uapi5')
p.write_text(s, encoding='utf-8', newline='\n')
print('Verified scoped su-session and service-event implementations; synchronized UAPI 5 declaration.')
