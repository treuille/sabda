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
    wav, sample_rate = model_util.get_wav(task, model, generator, input_text)
    st.write(f"Sample rate: `{sample_rate}`")

    st.audio(wav.numpy(), sample_rate=sample_rate)

    # Step 4: Save the waveform to a .wav file
    if st.button("Save to .wav"):
        output_file = "output.wav"
        soundfile.write(output_file, wav.numpy(), sample_rate)
        st.success(f"Generated speech saved to {output_file}")


def export_models():
    """This is the page where we can save the models to ONNX."""
    # Load the model
    task, model, generator = model_util.load_task_model_generator()

    with st.expander("model"):
        st.write(model)

    with st.expander("task"):
        model_util.display_task(task)

    with st.expander("generator"):
        st.write(generator)

    def export_model_to_onnx(model, task, filename):
        # TODO: Move this to model_util.py
        import torch
        from fairseq.models.text_to_speech.hub_interface import TTSHubInterface

        # Set model to evaluation mode
        model.eval()

        # Debug model configuration
        with st.expander("Model Configuration"):
            st.write("Encoder Configuration:")

            # Get all attributes of the encoder
            encoder_attrs = dir(model.encoder)
            st.write("All encoder attributes:", encoder_attrs)

            # Get all non-private attributes and their values
            encoder_public_attrs = {
                attr: getattr(model.encoder, attr)
                for attr in encoder_attrs
                if not attr.startswith("_")
            }
            st.write("Public encoder attributes and values:", encoder_public_attrs)

            # Original configuration info
            st.write(
                "Original Configuration:",
                {
                    "embed_dim": model.encoder.embed_tokens.embedding_dim,
                    "padding_idx": model.encoder.embed_tokens.padding_idx,
                    "pos_embed_dim": (
                        model.encoder.embed_positions.embedding_dim
                        if hasattr(model.encoder, "embed_positions")
                        else None
                    ),
                    "num_embeddings": model.encoder.embed_tokens.num_embeddings,
                },
            )

        # Dummy input for export
        sample_text = "Hello, this is a test."
        st.write(f"Sample text len: {len(sample_text)}")
        sample = TTSHubInterface.get_model_input(task, sample_text)

        with st.expander("Sample Details"):
            st.write(
                {
                    "Raw sample": sample,
                    "Net input keys": sample["net_input"].keys(),
                    "Token shape": (
                        sample["net_input"]["src_tokens"].shape
                        if isinstance(sample["net_input"]["src_tokens"], torch.Tensor)
                        else None
                    ),
                    "Length shape": (
                        sample["net_input"]["src_lengths"].shape
                        if isinstance(sample["net_input"]["src_lengths"], torch.Tensor)
                        else None
                    ),
                }
            )

        # Get both required inputs
        tokens = sample["net_input"]["src_tokens"]
        lengths = sample["net_input"]["src_lengths"]

        # Add batch dimension to both inputs and ensure they're on the same device as model
        dummy_tokens = (
            torch.tensor(tokens).unsqueeze(0).to(next(model.parameters()).device)
        )
        dummy_lengths = (
            torch.tensor(lengths).unsqueeze(0).to(next(model.parameters()).device)
        )

        with st.expander("Tensor Dimensions"):
            st.write(
                {
                    "tokens_shape": dummy_tokens.shape,
                    "lengths_shape": dummy_lengths.shape,
                    "device": str(dummy_tokens.device),
                    "tokens_dtype": str(dummy_tokens.dtype),
                    "lengths_dtype": str(dummy_lengths.dtype),
                    "tokens_min_max": (
                        dummy_tokens.min().item(),
                        dummy_tokens.max().item(),
                    ),
                }
            )

        # Try a test forward pass
        with st.expander("Test Forward Pass"):
            try:
                with torch.no_grad():
                    # Get encoder embedding dimensions
                    token_embedding = model.encoder.embed_tokens(dummy_tokens)
                    st.write(
                        {
                            "token_embedding_shape": token_embedding.shape,
                            "expected_pos_embed_shape": (
                                dummy_tokens.size(0),
                                dummy_tokens.size(1),
                                model.encoder.embed_tokens.embedding_dim,
                            ),
                        }
                    )

                    # Try to get positional embedding shape
                    if hasattr(model.encoder, "embed_positions"):
                        enc_padding_mask = dummy_tokens.eq(model.encoder.padding_idx)
                        pos_embed = model.encoder.embed_positions(enc_padding_mask)

                        # Reshape positional embedding to match token embedding
                        pos_embed = pos_embed.view(1, 1, 16, 256)

                        st.write(
                            {
                                "original_pos_embedding_shape": (1, 1, 16 * 256),
                                "reshaped_pos_embedding_shape": pos_embed.shape,
                                "padding_mask_shape": enc_padding_mask.shape,
                            }
                        )

                        # Test the addition
                        combined = token_embedding + pos_embed
                        st.write({"combined_shape": combined.shape})
            except Exception as e:
                st.error(f"Forward pass error: {str(e)}")

        # Create a wrapper class to handle the reshaping
        class ModelWrapper(torch.nn.Module):
            def __init__(self, model):
                super().__init__()
                self.model = model

            def forward(self, src_tokens, src_lengths):
                # Override the encoder's forward method temporarily
                original_forward = self.model.encoder.forward

                def new_forward(self, src_tokens, src_lengths, **kwargs):
                    x = self.embed_tokens(src_tokens)
                    enc_padding_mask = src_tokens.eq(self.padding_idx)

                    # Get positional embeddings and reshape them
                    pos_embed = self.embed_positions(enc_padding_mask)
                    pos_embed = pos_embed.view(*x.size())  # Reshape to match x

                    x += self.pos_emb_alpha * pos_embed

                    # Apply dropout
                    x = self.dropout_module(x)

                    # Transpose for attention layers
                    x = x.transpose(0, 1)  # [B, T, D] -> [T, B, D]

                    # Transformer layers
                    for layer in self.encoder_fft_layers:
                        x = layer(x, enc_padding_mask)

                    # Transpose back
                    x = x.transpose(0, 1)  # [T, B, D] -> [B, T, D]

                    # Apply layer norm if it exists
                    if self.layer_norm is not None:
                        x = self.layer_norm(x)
                    return {
                        "encoder_out": x,  # B x T x C
                        "encoder_padding_mask": enc_padding_mask,  # B x T
                        "encoder_embedding": None,
                        "encoder_states": None,
                        "src_tokens": None,
                        "src_lengths": None,
                    }

                # Replace the forward method
                self.model.encoder.forward = new_forward.__get__(self.model.encoder)

                try:
                    # Get the output
                    encoder_out = self.model.encoder(src_tokens, src_lengths)
                finally:
                    # Restore the original forward method
                    self.model.encoder.forward = original_forward

                return encoder_out

        # Wrap the model
        wrapped_model = ModelWrapper(model)

        # Export to ONNX with both required inputs
        if st.button("Export to ONNX"):
            with torch.no_grad():
                torch.onnx.export(
                    wrapped_model,
                    (dummy_tokens, dummy_lengths),  # Pass both inputs as a tuple
                    filename,
                    export_params=True,
                    opset_version=12,
                    input_names=["src_tokens", "src_lengths"],
                    output_names=["encoder_out", "encoder_padding_mask"],
                    dynamic_axes={
                        "src_tokens": {0: "batch_size", 1: "sequence_length"},
                        "src_lengths": {0: "batch_size"},
                        "encoder_out": {0: "batch_size", 1: "sequence_length"},
                        "encoder_padding_mask": {0: "batch_size", 1: "sequence_length"},
                    },
                    do_constant_folding=True,
                )
            st.success(f"FastSpeech2 exported to ONNX: {filename}")

    filename = "fastspeech2.onnx"
    export_model_to_onnx(model, task, filename)
    st.warning(f"This is where it's going to be saved: `{filename}`")


def visualize_weights():
    """Visualize the weights of different layers in the model."""
    task, model, generator = model_util.load_task_model_generator()

    # Helper function to normalize weights for visualization
    def normalize_weights(weights):
        weights = weights.detach().cpu().numpy()
        min_val = weights.min()
        max_val = weights.max()
        normalized = (weights - min_val) * 255 / (max_val - min_val)
        return normalized.astype("uint8")

    # Get all named parameters
    named_params = [
        (name, param) for name, param in model.named_parameters() if param.dim() >= 2
    ]
    layer_names = [name for name, _ in named_params]

    # Create selectbox for layer selection
    selected_layer = st.selectbox("Select layer to visualize:", layer_names)

    # Get the selected weights
    selected_weights = dict(named_params)[selected_layer]

    # Display layer info
    st.write(f"Layer shape: {selected_weights.shape}")

    # Normalize and visualize the weights
    weights_norm = normalize_weights(selected_weights)

    # Handle different dimensional tensors
    if len(weights_norm.shape) == 2:
        # For 2D tensors, show directly
        st.image(
            weights_norm,
            caption=f"Weights visualization for {selected_layer}",
            use_container_width=True,
        )

    elif len(weights_norm.shape) == 3:
        # For 3D tensors, show slices
        dim_to_slice = st.selectbox(
            "Select dimension to slice:", range(weights_norm.shape[0])
        )
        st.image(
            weights_norm[dim_to_slice],
            caption=f"Slice {dim_to_slice} of {selected_layer}",
            use_container_width=True,
        )

    elif len(weights_norm.shape) == 4:
        # For 4D tensors (like conv layers), show multiple slices
        dim1_to_slice = st.selectbox(
            "Select first dimension to slice:", range(weights_norm.shape[0])
        )
        dim2_to_slice = st.selectbox(
            "Select second dimension to slice:", range(weights_norm.shape[1])
        )
        st.image(
            weights_norm[dim1_to_slice, dim2_to_slice],
            caption=f"Slice [{dim1_to_slice}, {dim2_to_slice}] of {selected_layer}",
            use_container_width=True,
        )

    import altair as alt
    import pandas as pd
    import numpy as np

    # Convert weights to pandas DataFrame
    hist_data = selected_weights.detach().cpu().numpy().flatten()
    df = pd.DataFrame({"weights": hist_data})

    # Create histogram using Altair
    chart = (
        alt.Chart(df)
        .mark_bar()
        .encode(
            alt.X("weights", bin=alt.Bin(maxbins=50), title="Weight Value"),
            alt.Y("count()", title="Count"),
            tooltip=["count()"],
        )
        .properties(title="Weight Distribution", width=600, height=400)
    )

    # Add a line for the mean
    mean_line = (
        alt.Chart(df)
        .mark_rule(color="red")
        .encode(x="mean(weights)", size=alt.value(2), tooltip=["mean(weights)"])
    )

    # Combine histogram and mean line
    st.altair_chart(chart + mean_line, use_container_width=True)


def main():
    # Create a bunch of pages and the first one of which is to generate text
    generate_audio_page = st.Page(
        generate_audio, title="Generate audio", icon=":material/volume_up:"
    )
    generate_audio_page_2 = st.Page(
        export_models, title="Export models", icon=":material/save:"
    )
    visualize_weights_page = st.Page(
        visualize_weights, title="Visualize Weights", icon=":material/visibility:"
    )
    # delete_page = st.Page("delete.py", title="Delete entry", icon=":material/delete:")

    pg = st.navigation(
        [generate_audio_page, generate_audio_page_2, visualize_weights_page]
    )
    pg.run()


if __name__ == "__main__":
    main()
