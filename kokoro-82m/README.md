# kokoro-82m

Trying to get this model to work inside of Python / Streamlit for the purpose\
of the Ableton exploration project

## Installation

**Todo:** Write this up properly

```sh
# [Step 1] Install dependencies silently
# !git lfs install
# !git clone https://`huggingface.co/hexgrad/Kokoro-82M
# %cd Kokoro-82M
# !apt-get -qq -y install espeak-ng > /dev/null 2>&1
# !pip install -q
```

Then copy the big files over

```sh
cp Kokoro-82M/kokoro-v0_19.pth .
cp -r Kokoro-82M/voices .
```

## License stuff

Some of the files were copied from `huggingface.co/hexgrad/Kokoro-82M`, which seems to
have an Apache-2 license.
