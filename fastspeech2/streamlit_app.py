import streamlit as st
import model_util
import soundfile

st.title("Text-to-Speech with Fairseq")


def generate_audio():
    """This is the default page which loads the model and generates speech."""
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

    # Step 4: Save the waveform to a .wav file
    if st.button("Save to .wav"):
        output_file = "output.wav"
        soundfile.write(output_file, wav.numpy(), sample_rate)
        st.success(f"Generated speech saved to {output_file}")


def generate_audio_2():
    generate_audio()


def main():
    # Create a bunch of pages and the first one of which is to generate text
    generate_audio_page = st.Page(
        generate_audio, title="Generate audio", icon=":material/add_circle:"
    )
    generate_audio_page_2 = st.Page(
        generate_audio_2, title="Generate audio 2", icon=":material/add_circle:"
    )
    # delete_page = st.Page("delete.py", title="Delete entry", icon=":material/delete:")

    pg = st.navigation([generate_audio_page, generate_audio_page_2])
    pg.run()


if __name__ == "__main__":
    main()
