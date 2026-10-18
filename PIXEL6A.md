# Pixel 6a SukiSU 4.2.1 build candidate

This manual GitHub Actions workflow compiles one Android 14 / Linux 6.1.162 GKI kernel and packages it with AnyKernel3 for Pixel 6a (`bluejay`). Target firmware: `CP3A.261005.002.A1`.

The common-kernel revision matches a previously booted kernel. SukiSU and SUSFS are updated together for the 4.2.1 manager's UAPI 5. The newer builtin source already implements scoped su-session file descriptors and EVENT_SERVICES start/skip results; its stale interface declaration is synchronized after source checks. The bundled-driver flag is defined but remains unset, since this is a standalone builtin kernel. This is a custom build, not an official SukiSU release.

SUSFS is enabled. KPM, BBG, ReKernel and additional ZRAM changes are disabled. No custom seccomp-cache patch is included. Sources are listed in `config/pixel6a-sources.json`. The reusable builder derives from zzh20188/GKI_KernelSU_SUSFS v2.3.0-r4; upstream licenses are preserved.

Run only `Pixel 6a SukiSU 4.2.1 candidate` manually. It uploads the AnyKernel3 package and a build provenance artifact. The workflow does not publish a release or flash a device. Other upstream workflows are archived with `.disabled` extensions. Any patch rejection stops the build before compilation.

Successful compilation does not establish boot compatibility. Inspect the binary's UAPI, configuration, and module symbol CRCs against the firmware before considering a controlled boot test. Preserve the known-working and stock boot images.
