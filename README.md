# sabda

Playground repo to explore AI + realtime sound generation

### Tuesday Demo M2 (looping and effects)

- Loop the synthesis on a beat
- Add some effects to make it sound cool

#### Examples that I can use

- `Buffr Glitch` - uses incoming midi signal
- `examples/sine` - just create a sine wave
- Also look at[Transport](https://github.com/robbert-vdh/nih-plug/blob/master/src/context/process.rs#L104)

## Todo

### Steps

- Background studying (**Goal: Understand how I can put samples into the buffer**)
    - Ask AI how do to his
        - Add in all the code files as context. Then ask it to answer this question.
        - Quetions
            1. How would I implement a plugin that reads in a large .wav file
            2. At what point during the plug-in's lifecycle does it make sense to read
               in suhc such a file (and allocate a whole bunch of memory)
            3. How do I store state such as which sample I'm on from the perspective of
               of playing back the sample
            3. How can I read the clock signal from midi and then play the sample only
               every four beats.
        - Ask of
            - [ ] OpenAI
            - [ ] Claude
- Rust side (**Goal: Get a fixed set of samples looping on the beat.**)
    - First, create my own sinusoidal (or something else?) plug-in (outside `nih-plug`)
    - Clean up git
- Can I plug in the ONNX runtime into the plugin
- Combining Rust + Python
    - See if I can get some vectors in there
- See if I can get Kokoro-82M to play properly
    - Anything more to add here?
- Go through the risks below .. **which have I resolved??**
- Sort and clean up the following...
    - See if I can inject a fixed set of samples (wav) into the vst3 plugin architecture
    - Can I compile the onnx code as a plugin for Ableton
    - Add effects to it? <- Fun!

## Vision

### Tuesday Demo M2 (playing a sample + effects)

- See if I can play a sample on the beat
- Add some effects to make it sound cool

### Tuesday Demo M3 (showing off the NN in realtime)

- Loop the synthesis on a beat
- Save to a text file which is read by the plug-in
- It resynthesizes based on what it sees in that file

### Larger vision

- See if we can get a neural net running in Ableton which lets you generate audio
- We want to trigger the plugin to play the audio every n midi steps if we can

## Observations

- It's really easy to get these models running in Python
    - But it's hard to get them to compile to Rust
    - All the computation to encode / decode inputs and outputs will need to be ported.

## Risks (unordered)

- **TBH** There's a lot of plumbing (and exploring!) "risk" here..
    - what about **artistic risk?**
    - would that affect greatly what I'm working on right now
    - *In principle, wouldn't it better shape my tehcnical explorations to have
      a clearer sense of what I might want to expolore technically?* (Short guess:
      yes)
- Can I run a neural net in Rust?
- I can't play a sample using nih-plug
- I don't know if I can run a neural net in Rust
- I don't know how to read the midi clock in nih-plug
- I don't unerstand how nih-plug works
    - There is no good documentation for nih-plug
- I don't have a way of debugging nih-plug

## Building the project

To build the project with cargo build run

To build the project:

```bash
# Debug mode for M1/M2 Macs (Apple Silicon)
cargo build --target aarch64-apple-darwin

# Release mode for M1/M2 Macs (Apple Silicon)
cargo build --release --target aarch64-apple-darwin
```

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

