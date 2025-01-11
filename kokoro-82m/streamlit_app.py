import streamlit as st
import torch


@st.cache_resource
def build_model(model_path, device):
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


def script_1():

    device = "cuda" if torch.cuda.is_available() else "cpu"
    st.write("cuda is available:", torch.cuda.is_available())
    st.write("device:", device)

    # TODO: Rename to `model` and `voicepack`
    model_path = "kokoro-v0_19.pth"
    model = build_model(model_path, device)
    st.success(f"Model loaded successfully `{model_path}`")
    with st.expander("Model details"):
        st.write(model)

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


if __name__ == "__main__":
    st.title("Kokoro")
    script_1()
