"""A set of utility functions used across all pages in the app."""

import streamlit as st
import pandas as pd
from fairseq.checkpoint_utils import load_model_ensemble_and_task_from_hf_hub
from fairseq.models.text_to_speech.hub_interface import TTSHubInterface
import nltk


@st.cache_resource
def load_task_model_generator():
    """Load the model and return the task, model, and generator."""
    model_name = "facebook/fastspeech2-en-ljspeech"
    models, cfg, task = load_model_ensemble_and_task_from_hf_hub(
        # model_name, arg_overrides={"vocoder": "hifigan", "fp16": False}
        model_name,
        arg_overrides={"fp16": False},
    )
    TTSHubInterface.update_cfg_with_data_cfg(cfg, task.data_cfg)  # type: ignore
    generator = task.build_generator(models, cfg)  # type: ignore
    model = models[0]
    model.eval()
    return task, model, generator


def display_task(task):
    st.write("**`task.args`**")
    # Convert `task.args` to a dictionary for easier handling
    args_dict = vars(task.args)  # Convert Namespace to a dictionary

    # Convert the dictionary into a DataFrame for better tabular display
    args_df = pd.DataFrame(list(args_dict.items()), columns=["Parameter", "Value"])  # type: ignore

    # Display the DataFrame as a table
    st.dataframe(args_df, use_container_width=True)


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
