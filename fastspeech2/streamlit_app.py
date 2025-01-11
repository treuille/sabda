import streamlit as st
import model_util
import soundfile

st.title("Text-to-Speech with Fairseq")


def generate_audio():
    """This is the default page which loads the model and generates speech."""
    # Load the model
    task, model, generator = model_util.load_task_model_generator()

    # Step 2: Define the input text
    input_text = st.text_input(
        "Enter text to convert to speech:",
        "Hello, this is a test of FastSpeech 2 with Fairseq.",
    )
    if not st.checkbox("Use `get_wav_new()`"):
        wav, sample_rate = model_util.get_wav(task, model, generator, input_text)
    else:
        wav, sample_rate = model_util.get_wav_new(task, model, generator, input_text)

    st.write(f"Sample rate: `{sample_rate}`")

    st.audio(wav.numpy(), sample_rate=sample_rate)

    # Step 4: Save the waveform to a .wav file
    if st.button("Save to .wav"):
        output_file = "output.wav"
        soundfile.write(output_file, wav.numpy(), sample_rate)
        st.success(f"Generated speech saved to {output_file}")


def export_models():
    """This is the page where we can save the models to ONNX."""
    import torch

    # Load the model
    task, model, _generator = model_util.load_task_model_generator()
    source_dictionary = task.source_dictionary  # type: ignore

    if st.button("Export to ONNX"):
        # Set model to evaluation mode
        model.eval()

        # Get the vocabulary size from the model
        vocab_size = len(source_dictionary)

        # Create dummy inputs with valid token IDs (batch_size=1, sequence_length=128)
        dummy_tokens = torch.randint(0, vocab_size - 1, (1, 128), dtype=torch.long)
        # Add padding token at the end
        pad_idx = source_dictionary.pad()
        dummy_tokens[0, -10:] = pad_idx  # Add some padding at the end
        dummy_lengths = torch.LongTensor([118])  # Actual length without padding

        # Export the model
        output_path = "tts_model.onnx"
        torch.onnx.export(
            model,
            (dummy_tokens, dummy_lengths),  # Tuple of inputs
            output_path,
            input_names=["tokens", "lengths"],
            output_names=["output"],
            dynamic_axes={
                "tokens": {0: "batch_size", 1: "sequence_length"},
                "lengths": {0: "batch_size"},
                "output": {0: "batch_size", 1: "sequence_length"},
            },
            opset_version=14,
        )
        st.success(f"Model exported to {output_path}")


def main():
    # Create a bunch of pages and the first one of which is to generate text
    generate_audio_page = st.Page(
        generate_audio, title="Generate audio", icon=":material/volume_up:"
    )
    generate_audio_page_2 = st.Page(
        export_models, title="Export models", icon=":material/save:"
    )

    pg = st.navigation([generate_audio_page, generate_audio_page_2])
    pg.run()


if __name__ == "__main__":
    main()
