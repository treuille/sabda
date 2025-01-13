import streamlit as st
import torch
import numpy as np


@st.cache_resource
def load_pth_model(model_path, device):
    """Wrapping this function so that we don't rebuild models over and over."""
    from models import build_model as _build_model

    return _build_model(model_path, device)


@st.cache_data(hash_funcs={torch.Tensor: lambda x: x.cpu().numpy().tobytes()})
def generate(_model, text, voice_name, voice_pack):
    from kokoro import generate as _generate

    # Language is determined by the first letter of the VOICE_NAME:
    # [US] 'a' => American English => en-us
    # [UK] 'b' => British English => en-gb
    return _generate(_model, text, voice_pack, lang=voice_name[0])


@st.cache_resource
def load_voice_pack(voice_name, device):
    return torch.load(f"voices/{voice_name}.pt", weights_only=True).to(device)


@st.cache_resource
def load_inference_session(model_path):
    from onnxruntime import InferenceSession

    return InferenceSession(model_path)


@st.cache_data
def get_tokens(text, voice_name):
    from kokoro import phonemize, tokenize

    # Language is determined by the first letter of the VOICE_NAME:
    # [US] 'a' => American English => en-us
    # [UK] 'b' => British English => en-gb
    lang = voice_name[0]
    ps = phonemize(text, lang)
    tokens = tokenize(ps)
    return tokens


def get_voice_name():
    """Gives the user the option to select a voice."""
    voice_options = [
        "af",  # Default voice is a 50-50 mix of Bella & Sarah
        "af_bella",
        "af_sarah",
        "am_adam",
        "am_michael",
        "bf_emma",
        "bf_isabella",
        "bm_george",
        "bm_lewis",
        "af_nicole",
        "af_sky",
    ]
    voice_name = st.selectbox(
        "Select voice",
        options=voice_options,
        help="af = American Female (Bella & Sarah mix), am = American Male, bf = British Female, bm = British Male",
    )
    return voice_name


def run_pth_model():

    device = "cuda" if torch.cuda.is_available() else "cpu"
    st.write("cuda is available:", torch.cuda.is_available())
    st.write("device:", device)

    # TODO: Rename to `model` and `voicepack`
    model_path = "kokoro-v0_19.pth"
    model = load_pth_model(model_path, device)
    st.success(f"Model loaded successfully `{model_path}`")
    with st.expander("Model details"):
        st.write(model)

    voice_name = get_voice_name()
    voice_pack = load_voice_pack(voice_name, device)
    st.success(f"Voice pack loaded successfully `{voice_name}`")
    with st.expander("Voice pack details"):
        st.write(voice_pack)

    # [Step 3] Call generate, which returns 24khz audio and the phonemes used
    default_text = "How could I know? It's an unanswerable question. Like asking an unborn child if they'll lead a good life. They haven't even been born."
    text = st.text_input("Enter text", default_text)
    audio, out_ps = generate(model, text, voice_name, voice_pack)  # type: ignore

    # [Step 4] Display the 24khz audio and print the output phonemes
    st.audio(audio, sample_rate=24000)
    st.write("Output phonemes:", out_ps)


def run_onnx_model():
    """Run the model, this time using onnx."""
    # !pip install onnxruntime

    # Tokens produced by phonemize() and tokenize() in kokoro.py
    voice_name = get_voice_name()
    default_text = "How could I know? It's an unanswerable question. Like asking an unborn child if they'll lead a good life. They haven't even been born."
    text = st.text_input("Enter text", default_text)
    tokens = get_tokens(text, voice_name)
    st.write(f"There are `{len(tokens)}` tokens")

    # Context length is 512, but leave room for the pad token 0 at the start & end
    assert len(tokens) <= 510, len(tokens)

    # Style vector based on len(tokens), ref_s has shape (1, 256)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    voice_pack = load_voice_pack(voice_name, device)
    ref_s = voice_pack[len(tokens)].numpy()

    # Add the pad ids, and reshape tokens, should now have shape (1, <=512)
    tokens = [[0, *tokens, 0]]

    sess = load_inference_session("kokoro-v0_19.onnx")
    model_input = {
        "tokens": tokens,
        "style": ref_s,
        "speed": np.ones(1, dtype=np.float32),
    }
    with st.expander("The model input"):
        for key, value in model_input.items():
            st.subheader(key)
            value = np.array(value)
            st.write(value)
            st.caption(
                f"type: `{type(value)}` shape: `{value.shape}` dtype: `{value.dtype}`"
            )
        if st.button("Construct this ndarray in rust"):
            st.code(
                f"""
                let tokens = vec![{', '.join(str(t) for t in tokens[0])}];
                let style = vec![{', '.join(str(s) for s in ref_s[0])}];
                let speed = vec![1.0];
                """
            )

    audio = sess.run(None, model_input)[0]

    st.audio(audio, sample_rate=24000)

    with st.expander("Audio statistics"):
        # Min, max, amd mean of the audio
        st.write("Min:", audio.min())
        st.write("Max:", audio.max())
        st.write("Mean:", audio.mean())

    st.success("Audio successfully generated!!")


def main():
    """Execution starts here."""
    st.title("Kokoro")
    st.navigation(
        [
            st.Page(run_pth_model, title="Run PTH Model", icon=":material/volume_up:"),
            st.Page(run_onnx_model, title="Run ONNX Model", icon=":material/save:"),
        ]
    ).run()


if __name__ == "__main__":
    main()
