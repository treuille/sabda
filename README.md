# sabda

Playground repo to explore AI + realtime sound generation

## Todo

- Clean out everything I can abou the current setup
    - Get rid of the JSON file?
    - Move the code at the bottom somewhere?
    - Look for any additional stray files I can get rid of
- Commit the current setup into git
    - At first do it in main
    - Then move it to its own branch.
    - Make main simply point to the branches
    - See if I can see it render properly inside of the Github site
- Start to follow the instructions to create an example plugin in Rust
    - See if I can build it first locally on my computer
    - Then see if I can build it for mac
    - See if I can open it in Ableton
- See if I can make this setup reproducible (that is: work in a new container)

## Building the project

To build the project with cargo build run

To build the project:

```bash
# For M1/M2 Macs (Apple Silicon)
cargo build --release --target aarch64-apple-darwin

# For Intel Macs
cargo build --release --target x86_64-apple-darwin
```

The executable will be in:

- `target/aarch64-apple-darwin/release/hello` (for M1/M2)
- `target/x86_64-apple-darwin/release/hello` (for Intel)

## Installation for MacOS

### Add the rustup targets

```bash
# First, add the macOS targets
rustup target add aarch64-apple-darwin  # For M1/M2 Macs (Apple Silicon)
```

### Install Zig (required for cross-compilation)

```sh
# Download and install Zig
wget https://ziglang.org/download/0.13.0/zig-linux-aarch64-0.13.0.tar.xz
tar -xvf zig-linux-aarch64-0.13.0.tar.xz -C ${HOME}/.local/
```

and add the following to `~/.zshrc`

```sh
export PATH=$PATH:${HOME}/.local/zig-linux-aarch64-0.11.0
```

You can verify the installation with:

```sh
zig version
```

#### Install Zig (required for cross-compilation)

Not sure if this is necessary but for the cross-compilation I did this:

```sh
sudo apt install -y autoconf automake libtool # necessary?
```

The next step was to get `MacOSX15.1.sdk` into the zig directory. First I had to:

```sh
mkdir -p /home/adrien/.local/zig-linux-aarch64-0.13.0/lib/libc/macos
```

Then I had so move `MacOSX15.1.sdk` into the container with this command 
**from outside the container**.

```sh
tar -cvf - /Library/Developer/CommandLineTools/SDKs/MacOSX15.1.sdk | ssh adrien@test-4 'tar -xvf - -C /home/adrien/.local/zig-linux-aarch64-0.13.0/lib/libc/macos'
```

## Branches

This project is organized into several branches.

| branch          | meaning                                   |
|-----------------|-------------------------------------------|
| `main`          | Right now, vst3                           |
| `solid_js`      | A test of creating sound using SolidJs    |

