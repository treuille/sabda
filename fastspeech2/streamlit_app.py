import streamlit as st
import model_util

import soundfile

st.title("Text-to-Speech with Fairseq")


# Step 1: Load the model
task, model, generator = model_util.load_task_model_generator()

with st.expander("model"):
    st.write(model)

with st.expander("task"):
    model_util.display_task(task)

# Step 2: Define the input text
input_text = st.text_input(
    "Enter text to convert to speech:",
    "Hello, this is a test of FastSpeech 2 with Fairseq.",
)
wav, sample_rate = model_util.get_wav(task, model, generator, input_text)
st.write(f"Sample rate: `{sample_rate}`")

st.audio(wav.numpy(), sample_rate=sample_rate)

# # Step 4: Save the waveform to a .wav file
if st.button("Save to .wav"):
    output_file = "output.wav"
    soundfile.write(output_file, wav.numpy(), sample_rate)
    st.success(f"Generated speech saved to {output_file}")
