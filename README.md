# Text-to-Image AI Generator

A simple web app that turns a text description into an AI-generated image, built as a
beginner learning project.

## Description

Type a sentence like "a small cabin in a snowy forest," click a button, and an AI
model generates a matching image — all in your browser, with no AI running on your
own computer.

## Features

- Simple, single-page web interface
- Text prompt input and a Generate Image button
- Loading indicator while the image is generated
- Friendly error messages for empty prompts, bad tokens, network issues, and API errors
- No API keys stored in the code

## Technologies Used

- **Python** — the programming language
- **Hugging Face Inference API** — runs the text-to-image model in the cloud
- **`black-forest-labs/FLUX.1-schnell`** — the text-to-image model used
- **Google Colab** — used to prototype and test the AI logic first
- **Streamlit** — turns the Python script into a web app
- **GitHub** — stores the project's code
- **Streamlit Community Cloud** — hosts the deployed app for free

## How the Application Works

```
User enters prompt
        ↓
Streamlit receives prompt
        ↓
Python sends request
        ↓
Hugging Face API
        ↓
Text-to-Image Model
        ↓
Generated Image
        ↓
Streamlit displays image
```

## Installation (Run Locally)

1. Clone this repository:
   ```bash
   git clone https://github.com/<your-username>/text-to-image-app.git
   cd text-to-image-app
   ```
2. (Recommended) create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate      # Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## API Configuration

This app needs a Hugging Face API token.

1. Create a free account at [huggingface.co](https://huggingface.co).
2. Go to **Settings → Access Tokens** and create a new token (a "Read" token is enough).
3. Create a local secrets file at `.streamlit/secrets.toml` (this file is git-ignored
   and will never be uploaded):
   ```toml
   HF_TOKEN = "hf_your_token_here"
   ```

## Run the Application Locally

```bash
streamlit run app.py
```

Then open the URL Streamlit prints in your terminal (usually `http://localhost:8501`).

## Deploy to Streamlit Community Cloud

1. Push this project to a GitHub repository (make sure `.streamlit/secrets.toml` is
   **not** included — check `.gitignore`).
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.
3. Click **New app**, select this repository and branch, and set the main file to `app.py`.
4. Under **Advanced settings → Secrets**, paste:
   ```toml
   HF_TOKEN = "hf_your_token_here"
   ```
5. Click **Deploy** and wait for the build to finish.
6. Open the generated public URL and test image generation.

## Example Prompts

- "A small cabin in a snowy forest"
- "A red vintage car parked on a cobblestone street, golden hour"
- "A futuristic city skyline at night, neon lights, cyberpunk style"
- "A cup of coffee on a wooden table, soft morning light"

## Troubleshooting

| Problem | Likely Cause | Fix |
|---|---|---|
| "No Hugging Face API token found" | `HF_TOKEN` missing from secrets | Add it to `.streamlit/secrets.toml` (local) or Streamlit Cloud Secrets (deployed) |
| Authentication failed / 401 error | Token is invalid, expired, or mistyped | Generate a new token on Hugging Face and update your secrets |
| "Model not found" / 404 error | Model name changed or is temporarily unavailable | Wait and retry, or check the model page on Hugging Face |
| "Too many requests" / 429 error | Hit the free-tier rate limit | Wait a minute before generating again |
| Network / connection error | No internet, or Hugging Face servers unreachable | Check your internet connection and retry |
| App works locally but not when deployed | Secrets not set on Streamlit Community Cloud | Re-check the Secrets section in the app's settings |

## Project Structure

```
text-to-image-app/
│
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```
