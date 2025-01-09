# Testing neural networ

Testing neural network sound generation in Python

## Todo

## Installation instructions

**Important:** `fairseq` requires Python <= 3.10, as well as an older
version of `pip`, hence the following build steps:

```sh
sudo add-apt-repository -y ppa:deadsnakes/ppa
sudo apt update
sudo apt install -y python3.10 python3.10-dev
sudo apt install -y python3.10-venv python3.10-distutils

# Verify the Python installation
python3.10 --version
```

Install the virtual environment, and ensure an older version of pip

```sh
python3.10 -m venv .venv ; venv-activate
pip install -r dev_requirements.txt

# Verify the pip installation
pip --version
```

Now install everything else:

```sh
pip install -r requirements.txt
```

### TODO: I think the following instructions are unnecessary

If you're still having issues, you might need to install additional system dependencies:
```bash
sudo apt-get install build-essential
sudo apt-get install libsndfile1
```

