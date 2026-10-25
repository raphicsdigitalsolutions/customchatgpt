# NEXORA AI — Think Beyond ✦

A polished Streamlit AI workspace with a dimensional animated identity, a reusable `nexora_3d.py` visual layer, day/night themes, chat history for the active session, model selection, and optional live web search with source links.

**Live app:** https://attanexora-ai.streamlit.app/
**Repository:** https://github.com/raphicsdigitalsolutions/customchatgpt

## Highlights

- Premium ocean-teal, champagne and porcelain visual system with responsive day/night layouts.
- Continuous CSS 3D depth across the workspace: a prominent animated creator signature, split hero with a rotating glass cube, top-right reactor, perspective grid, raised controls and dimensional chat messages.
- Day and Night appearance modes with contrast-aware controls.
- OpenAI API-key welcome dialog; API key is kept in the active Streamlit session when entered in the UI.
- Optional OpenAI Responses API web search for current information.
- Source links shown when returned by the search-enabled response.
- Recent conversation list and quick-start prompts during the current session.
- Assistant instructions and response-style settings.
- Streamlit Secrets and environment-variable support for deployments and local development.

## Run locally

Python 3.10+ is recommended.

```bash
python -m venv .venv
```

Activate the virtual environment:

**Windows PowerShell**
```powershell
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux**
```bash
source .venv/bin/activate
```

Install dependencies and run from the repository root. Keep both `chatgpt.py` and `nexora_3d.py` in the same folder:

```bash
pip install -r requirements.txt
streamlit run chatgpt.py
```

## Configure your OpenAI API key

### Option A — In the app

Open NEXORA AI and enter your API key in the welcome dialog. The UI-entered key is stored in the current Streamlit session, not committed to this repository. A new session may require entering it again.

### Option B — Streamlit Community Cloud

In the app's Streamlit Cloud settings, add a secret named `OPENAI_API_KEY`:

```toml
OPENAI_API_KEY = "your-api-key"
```

Never paste a real API key into source code, README files, screenshots, or Git commits.

### Option C — Local .env file

Create a local `.env` file (it is ignored by Git):

```env
OPENAI_API_KEY=your-api-key
# Optional: override the app's default model
OPENAI_MODEL=gpt-4.1-mini
```

The app supports choosing from the model options shown in the sidebar; availability depends on the API project and selected model.

## Web search notes

Turn on **Search the web for current answers** in the sidebar to allow the model to use the Responses API web-search tool. Search is most useful for recent events, software/API documentation, changing product details, and other time-sensitive topics. The model decides when search is useful. Source links appear when the API returns source annotations or search-source metadata.

API usage and web search may incur OpenAI API charges. A ChatGPT subscription does not automatically include API credits.

## Important scope notes

- This project is a Streamlit single-user/session-oriented app, **not a full account login system**. The welcome dialog connects an OpenAI API key; it does not create usernames or passwords.
- Chat history, theme selection, and UI settings live in Streamlit session state; they are not durable across all browser sessions or server restarts.
- Do not use this repository as a multi-user production service without adding server-side authentication, per-user data isolation, durable storage, rate limiting, and appropriate privacy controls.
- The animated scene uses lightweight CSS 3D transforms and continuous motion; it does not load a WebGL engine.

## Deployment

The configured Streamlit Community Cloud deployment can follow the `main` branch. After a commit, check the app's deployment status and logs in Streamlit Community Cloud if it does not refresh automatically.

## License

No license has been added. Please check with the repository owner before reusing or redistributing the project.
