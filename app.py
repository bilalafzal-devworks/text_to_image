"""
Text-to-Image AI Web App
-------------------------
A beginner-friendly Streamlit app that turns a text prompt into an AI-generated
image using the Hugging Face Inference API.

How it works:
    User types a prompt -> Streamlit sends it to Hugging Face's API ->
    the text-to-image model generates a picture -> Streamlit displays it.
"""

import streamlit as st
from huggingface_hub import InferenceClient
from huggingface_hub.utils import HfHubHTTPError
import requests

# ---------------------------------------------------------------------------
# Basic page setup
# ---------------------------------------------------------------------------
st.set_page_config(page_title="Text-to-Image AI", page_icon="🖼️")

st.title("🖼️ Text-to-Image AI Generator")
st.write(
    "Type a description below and click **Generate Image**. "
    "An AI model will create a picture based on your text."
)

# Model used for generation. Kept in one place so it's easy to change later.
MODEL_NAME = "black-forest-labs/FLUX.1-schnell"


# ---------------------------------------------------------------------------
# Load the Hugging Face API token securely
# ---------------------------------------------------------------------------
# The token is NEVER written in this file. Locally, it comes from a file at
# .streamlit/secrets.toml (which is excluded from GitHub by .gitignore).
# On Streamlit Community Cloud, it comes from the app's "Secrets" settings.
def get_hf_token():
    try:
        return st.secrets["HF_TOKEN"]
    except Exception:
        return None


hf_token = get_hf_token()

if not hf_token:
    st.error(
        "No Hugging Face API token found. Add HF_TOKEN to your Streamlit "
        "secrets before using this app (see the README for instructions)."
    )
    st.stop()

client = InferenceClient(api_key=hf_token)


# ---------------------------------------------------------------------------
# App UI: prompt input and generate button
# ---------------------------------------------------------------------------
prompt = st.text_area(
    "Describe the image you want:",
    placeholder="e.g. A small cabin in a snowy forest",
    height=100,
)

generate_clicked = st.button("Generate Image", type="primary")


# ---------------------------------------------------------------------------
# Handle the button click
# ---------------------------------------------------------------------------
if generate_clicked:
    # 1. Empty prompt check
    if not prompt or not prompt.strip():
        st.warning("Please type a description before generating an image.")
        st.stop()

    # 2. Try to generate the image, handling the most common failure cases
    with st.spinner("Generating your image... this can take up to a minute."):
        try:
            image = client.text_to_image(prompt.strip(), model=MODEL_NAME)

        except HfHubHTTPError as e:
            # Covers invalid/expired token (401), rate limits, and model errors
            status = getattr(e.response, "status_code", None)
            if status == 401:
                st.error(
                    "Authentication failed. Your Hugging Face token is missing, "
                    "invalid, or expired. Check your Streamlit secrets."
                )
            elif status == 404:
                st.error(
                    f"Model '{MODEL_NAME}' was not found or isn't available "
                    "right now. Try again in a moment."
                )
            elif status == 429:
                st.error(
                    "Too many requests right now (rate limit reached). "
                    "Please wait a bit and try again."
                )
            else:
                st.error(f"Hugging Face API returned an error: {e}")

        except requests.exceptions.ConnectionError:
            st.error(
                "Network problem: couldn't reach Hugging Face's servers. "
                "Check your internet connection and try again."
            )

        except requests.exceptions.Timeout:
            st.error("The request timed out. The model may be busy — try again.")

        except Exception as e:
            # Catch-all so the app never crashes with a raw traceback
            st.error(f"Something unexpected went wrong: {e}")

        else:
            # This only runs if no exception was raised
            st.image(image, caption=prompt, use_container_width=True)
            st.success("Image generated successfully!")


st.divider()
st.caption(
    "Powered by the Hugging Face Inference API "
    f"(model: {MODEL_NAME}) and Streamlit."
)
