import streamlit as st

st.title("Text-to-Speech with Fairseq")

import torch

st.write(f"Torch version: `{torch.__version__}`")

import fairseq
from fairseq.checkpoint_utils import load_model_ensemble_and_task_from_hf_hub
from fairseq.models.text_to_speech.hub_interface import TTSHubInterface

st.write(f"Fairseq version: `{fairseq.__version__}`")

import nltk
import soundfile


@st.cache_resource
def load_task_model_generator():
    """Load the model and return the task, model, and generator."""
    model_name = "facebook/fastspeech2-en-ljspeech"
    models, cfg, task = load_model_ensemble_and_task_from_hf_hub(
        model_name, arg_overrides={"vocoder": "hifigan", "fp16": False}
    )
    TTSHubInterface.update_cfg_with_data_cfg(cfg, task.data_cfg)  # type: ignore
    generator = task.build_generator(models, cfg)  # type: ignore
    return task, models[0], generator


# Step 1: Load the model
task, model, generator = load_task_model_generator()

with st.expander("model"):
    st.write(model)


@st.cache_resource
def download_averaged_perceptron_tagger():
    nltk.download("averaged_perceptron_tagger_eng")


@st.cache_data
def get_wav(_task, _model, _generator, input_text):
    """Generate the speech waveform."""
    # Requirement for this to work
    download_averaged_perceptron_tagger()

    # Now run inference
    sample = TTSHubInterface.get_model_input(_task, input_text)
    wav, sample_rate = TTSHubInterface.get_prediction(_task, _model, _generator, sample)
    return wav, sample_rate


# Step 2: Define the input text
input_text = st.text_input(
    "Enter text to convert to speech:",
    "Hello, this is a test of FastSpeech 2 with Fairseq.",
)
wav, sample_rate = get_wav(task, model, generator, input_text)
st.write(f"Sample rate: `{sample_rate}`")

st.audio(wav.numpy(), sample_rate=sample_rate)

# # Step 4: Save the waveform to a .wav file
if st.button("Save to .wav"):
    output_file = "output.wav"
    soundfile.write(output_file, wav.numpy(), sample_rate)
    st.success(f"Generated speech saved to {output_file}")
