# AI Recipe Idea Generator

A beginner-friendly AI internship project built with Python, Streamlit, and the Google Gemini API.

## 1. Get a Gemini API key
Create an API key in Google AI Studio: https://aistudio.google.com/app/apikey

## 2. Install dependencies
```bash
python -m venv .venv
```

Windows:
```bash
.venv\Scripts\activate
```

macOS/Linux:
```bash
source .venv/bin/activate
```

Then run:
```bash
pip install -r requirements.txt
```

## 3. Add your API key
Create a folder named `.streamlit` in the project directory. Inside it, create `secrets.toml`:

```toml
GEMINI_API_KEY = "paste-your-api-key-here"
```

Do not commit `secrets.toml` to GitHub or share your API key.

## 4. Run the app
```bash
streamlit run app.py
```

## Deploying to Streamlit Community Cloud
1. Upload `app.py` and `requirements.txt` to a GitHub repository.
2. Create a new app at https://share.streamlit.io/
3. In the app's settings, open Secrets and add:
   ```toml
   GEMINI_API_KEY = "your-api-key"
   ```
4. Deploy.

The app uses the Google Gen AI Python SDK and the `gemini-3.8-flash` model name. If that model is not enabled for your API key, replace it in `app.py` with a Gemini model available in your Google AI Studio account.
