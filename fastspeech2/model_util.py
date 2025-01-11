"""A set of utility functions used across all pages in the app."""

import streamlit as st
import pandas as pd
from fairseq.checkpoint_utils import load_model_ensemble_and_task_from_hf_hub
from fairseq.models.text_to_speech.hub_interface import TTSHubInterface
import nltk

# import torch


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


def get_wav_new(task, model, _generator, _input_text):
    """Generate speech waveform step by step for better control and testing."""
    raise NotImplementedError("This function is not implemented yet.")
    # # Step 1: Prepare text input
    # # - Download required NLTK data
    # download_averaged_perceptron_tagger()
    #
    # # Step 2: Text to model input conversion
    # # - Convert text to tokens
    # # - Create input tensor with proper shape
    # # - Add any necessary padding
    # # Direct tokenization using the task's dictionary
    # tokens = task.source_dictionary.encode_line(
    #     input_text,
    #     append_eos=True,
    #     add_if_not_exist=False,
    # )
    #
    # # Add batch dimension and create lengths tensor
    # src_tokens = tokens.unsqueeze(0)  # Shape: [1, seq_len]
    # src_lengths = torch.LongTensor([tokens.size(0)])
    #
    # st.write(f"Tokens shape: {src_tokens.shape}")
    # st.write(f"First few tokens: {src_tokens[0][:10]}")  # Show first 10 tokens
    #
    # # Step 3: Run FastSpeech2 model (text -> mel spectrogram)
    # # Run model in eval mode and without gradients
    # model.eval()
    # with torch.no_grad():
    #     # Forward pass through the model
    #     model_output = model(
    #         src_tokens=src_tokens,
    #         src_lengths=src_lengths,
    #     )
    #     # model returns a tuple, first element is the mel spectrogram
    #     mel_spec = model_output[0]  # Shape should be [1, T, mel_bins]
    #
    # st.write(f"Mel spectrogram shape: {mel_spec.shape}")
    #
    # # Step 4: Run vocoder (mel spectrogram -> waveform)
    # # The generator expects a sample dictionary with net_input
    # sample = {
    #     "net_input": {
    #         "src_tokens": src_tokens,
    #         "src_lengths": src_lengths,
    #         "prev_output_tokens": torch.zeros_like(
    #             src_tokens
    #         ),  # For non-autoregressive model
    #     },
    #     "target": mel_spec,
    #     "target_lengths": torch.LongTensor([mel_spec.size(1)]),
    #     "speaker": torch.LongTensor([0]),  # Single speaker model uses index 0
    # }
    #
    # # Run the vocoder using generate method
    # wav = _generator.generate(model, sample, has_targ=True)[0]["waveform"]
    #
    # # Get sample rate from the task's config
    # sample_rate = task.data_cfg.config.get("features", {}).get("sample_rate", 22050)
    #
    # st.write(f"Generated waveform shape: {wav.shape}")
    #
    # return wav, sample_rate
    # # return (
    # #     wav,
    # #     sample_rate,
    # #     {
    # #         "input_sample": sample,
    # #         "model_output": model_output,
    # #     },
    # # )
