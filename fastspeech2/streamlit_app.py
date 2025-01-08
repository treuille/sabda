import torch
from fairseq.checkpoint_utils import load_model_ensemble_and_task_from_hf_hub
from fairseq.models.text_to_speech.hub_interface import TTSHubInterface
import soundfile as sf

st.title("Text-to-Speech with Fairseq")

# # Step 1: Load the model
# model_name = "facebook/fastspeech2-en-ljspeech"
# models, cfg, task = load_model_ensemble_and_task_from_hf_hub(
#     model_name, arg_overrides={"vocoder": "hifigan", "fp16": False}
# )
# model = models[0]
# TTSHubInterface.update_cfg_with_data_cfg(cfg, task.data_cfg)
# generator = task.build_generator(model, cfg)
#
# # Step 2: Define the input text
# input_text = "Hello, this is a test of FastSpeech 2 with Fairseq."
#
# # Step 3: Generate the speech
# sample = TTSHubInterface.get_model_input(task, input_text)
# wav, sample_rate = TTSHubInterface.get_prediction(task, model, generator, sample)
#
# # Step 4: Save the waveform to a .wav file
# output_file = "output.wav"
# sf.write(output_file, wav.numpy(), sample_rate)
#
# print(f"Generated speech saved to {output_file}")
