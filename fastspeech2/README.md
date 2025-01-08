# Testing neural networ

Testing neural network sound generation in Python

## Todo

## Installation instructions

Make sure the Python develpment headers are installed.

```bash
sudo apt-get update
sudo apt-get install python3.12-dev
```

### Optional

Let's also update your requirements.txt to be more specific about versions and add some build dependencies:

Filepath: requirements.txt
Replace lines: 1-10
```requirements
# Streamlit
streamlit
watchdog

# Build dependencies
setuptools>=41.0.0
wheel>=0.35.0

# Neural net stuff
--find-links https://download.pytorch.org/whl/torch_stable.html
torch>=1.9.0
fairseq>=0.12.0

# Sound output
soundfile>=0.10.3
```

After installing python3.12-dev, try these steps:
1. Remove your virtual environment and create a new one
2. Upgrade pip: `pip install --upgrade pip`
3. Install the requirements again: `pip install -r requirements.txt`

If you're still having issues, you might need to install additional system dependencies:
```bash
sudo apt-get install build-essential
sudo apt-get install libsndfile1
```


