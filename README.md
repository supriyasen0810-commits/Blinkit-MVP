# Blinkit · Try-Small-First MVP (Streamlit version)

Same prototype as the React version, rebuilt natively in Streamlit so it can
be deployed on Streamlit Community Cloud alongside your Part 1 discovery
engine.

## Run locally

```bash
pip install -r requirements.txt
mkdir -p .streamlit
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# edit secrets.toml and paste your real Anthropic API key
streamlit run app.py
```

## Deploy to Streamlit Community Cloud (free)

1. Push this folder to a GitHub repo (must include `app.py` and
   `requirements.txt` at minimum).
2. Go to **share.streamlit.io** -> sign in with GitHub -> **New app**.
3. Pick the repo, branch, and `app.py` as the entry point -> **Deploy**.
4. Once deployed: app **Settings -> Secrets** -> paste:
   ```toml
   ANTHROPIC_API_KEY = "sk-ant-your-real-key"
   ```
   Save -- the app restarts automatically with the key available.
5. You'll get a public URL like `https://blinkit-try-small-first.streamlit.app`.
   That's the link to submit.

## Notes

- The Claude call happens directly in `app.py` (function `call_claude`),
  server-side, using `st.secrets` -- there's no separate backend/serverless
  step needed like the Vercel version, since Streamlit apps are just a
  live Python process already.
- Without a real key set, screen 6 (the AI recommendation) falls back to a
  static but honest default message instead of erroring out -- the rest of
  the flow works regardless.
