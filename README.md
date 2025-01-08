# sabda

Playground repo to explore AI + realtime sound generation

## Todo

- Write the vision statement
    - Write down the risks
    - Categorize the risks
    - Rank order the risks
- Start to create todo list based on burning down the single biggest risk

## Vision

- See if we can get a neural net running in Ableton which lets you generate audio
- We want to trigger the plugin to play the audio every n midi steps if we can

### Risks (unordered)

- I don't know how to see if there are any voice generation neural nets in hugging face
    - Or should I look for something commerical
- I don't know if I can run a neural net in Rust
- I can't play a sample using nih-plug
- I don't know how to read the midi clock in nih-plug
- I don't unerstand how nih-plug works
    - There is no good documentation for nih-plug
- I don't have a way of debugging nih-plug

### Later

- See if I can make this setup reproducible (that is: work in a new container)

## Building the project

To build the project with cargo build run

To build the project:

```bash
# Debug mode for M1/M2 Macs (Apple Silicon)
cargo build --target aarch64-apple-darwin

# Release mode for M1/M2 Macs (Apple Silicon)
cargo build --release --target aarch64-apple-darwin
``catppuccin`

The executable will be in:

- `target/aarch64-apple-darwin/release/hello` (for M1/M2)

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

