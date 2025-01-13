#!/bin/sh

# Filter out the -exported_symbols_list argument and its following file
filtered_args=""
skip_next=0
for arg in "$@"; do
    if [ $skip_next -eq 1 ]; then
        skip_next=0
        continue
    fi

    if [ "$arg" = "-Wl,-exported_symbols_list" ]; then
        skip_next=1
        continue
    fi

    filtered_args="$filtered_args $arg"
done

SDK_PATH="/home/adrien/.local/zig-linux-aarch64-0.13.0/lib/libc/macos/MacOSX15.1.sdk"

/home/adrien/.local/zig-linux-aarch64-0.13.0/zig cc -target aarch64-macos \
  --sysroot="$SDK_PATH" \
  -L"$SDK_PATH/usr/lib" \
  -F"$SDK_PATH/System/Library/Frameworks" \
  -undefined dynamic_lookup \
  -dynamiclib \
  -fvisibility=default \
  $filtered_args


# #!/bin/sh
# /home/adrien/.local/zig-linux-aarch64-0.13.0/zig cc -target aarch64-macos --sysroot=/home/adrien/.local/zig-linux-aarch64-0.13.0/lib/libc/macos/MacOSX15.1.sdk "$@"
