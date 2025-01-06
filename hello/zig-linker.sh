#!/bin/sh
/home/adrien/.local/zig-linux-aarch64-0.13.0/zig cc -target aarch64-macos --sysroot=/home/adrien/.local/zig-linux-aarch64-0.13.0/lib/libc/macos/MacOSX15.1.sdk "$@"
