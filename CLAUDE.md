# CLAUDE.md: CS4106 Session 5 Class Activity (Sentiment Analyzer)

## Goal
Build, test, deploy and document a Streamlit + Hugging Face sentiment analyzer. End with a 2-page PDF submission (`submission.pdf`) in this folder.

## Student
- Name: **Muhammad Jibran Narejo**, B04-0923-000020, BSCS, Sec A
- Partner: none unless the user says otherwise (ask once at the start)
- Course: Foundations of Generative AI · CS4106 · Dr. Azhar Dilshad
- Date: use today's date

## Rules
- The OS is Windows + VS Code terminal (PowerShell). Use `python`, `.\venv\Scripts\Activate.ps1`, and forward-slash-safe paths.
- Stop and ask the user **only** for: HF / GitHub login, a browser click you can't do, and the partner question. Do everything else yourself.
- Never invent outputs. Every test result and screenshot comes from actually running the app.
- Do NOT copy the sample submission's test sentences, wording or personalization. The structure matches; the content must be original.
- Never commit tokens, `.env` or `venv/`.

## Step 1: Environment
```
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install streamlit transformers torch playwright reportlab
python -m playwright install chromium
```
Create `.gitignore` containing: `venv/`, `__pycache__/`, `.env`, `screenshots/*.tmp`.

## Step 2: app.py
Base it on the handout's starter code, with these fixes and personalization:
- Pin the model: `distilbert/distilbert-base-uncased-finetuned-sst-2-english`
- `@st.cache_resource` for model loading
- Don't reuse the same quote type inside an f-string (e.g. `f"{r["score"]}"`). It's a SyntaxError on Python < 3.12.
- Call with `truncation=True`, because inputs over 512 tokens crash otherwise
- Empty input → `st.warning`; wrap inference in try/except → `st.error`
- `st.spinner` while analyzing; green for POSITIVE / red for NEGATIVE; show confidence as `%` + `st.progress`
- A low-confidence note when score < 0.75
- **Personalization (distinct from the sample):** a header with Jibran's name and roll no; a sidebar "Try an example" button that fills in sample sentences; a session history table (`st.session_state`) of the last 5 analyses; a footer listing model limits (binary only, sarcasm, 512-token truncation)

`requirements.txt`: exactly `streamlit`, `transformers`, `torch`. **Never** use `pip freeze`.

## Step 3: Run locally and test
- `streamlit run app.py` → http://localhost:8501
- Write `test_model.py`. It runs the pipeline on the inputs below and prints label + score. Run it and save the output to `test_results.txt`.
  - Happy positive, e.g. `The new library timings made exam week so much easier.`
  - Happy negative, e.g. `My laptop froze twice during the online quiz.`
  - Sarcasm, e.g. `Oh wonderful, the Wi-Fi died right before submission.`
  - Negation `I wouldn't say it was bad.`, neutral `The bus arrived at 9.`, emojis only `🔥🔥🔥`, empty string, and a ~700-word paragraph (tests truncation)
- Pick **3 cases for the submission**: 1 positive, 1 negative, and 1 that **fooled** the model. If sarcasm is classified correctly, try other fooling inputs until one fails and use that.

## Step 4: Deploy (check what actually works today, then pick a path)
First check at huggingface.co/new-space which SDKs are offered for free.
- **Path A, Streamlit SDK available:** create Space `<hf-user>/sentiment-analyzer` (Streamlit, CPU basic, Public), then `git push` app.py + requirements.txt to it.
- **Path B, only Docker/Gradio/Static offered free:** use a **Docker Space** on the free CPU basic tier. Add a `Dockerfile` (python:3.11-slim, install requirements, `EXPOSE 7860`, `CMD streamlit run app.py --server.port 7860 --server.address 0.0.0.0`) and set `sdk: docker` + `app_port: 7860` in the Space README.md YAML header.
- **Path C, Docker blocked by billing:** do what the sample did. Push the code to a GitHub repo (`gh repo create`), have the user deploy it on share.streamlit.io (they click through that UI; give them exact steps), then create a free **Static** HF Space whose `index.html` iframes the Streamlit Cloud URL with `?embed=true`.

Auth: run `hf auth login` (or `huggingface-cli login`) and let the user paste a **write** token. Wait for the build to show "Running" and open the URL to confirm it works.
Record: the live Space URL and the commit-history URL (`.../commits/main`).

## Step 5: Screenshots
Use Playwright against the **live** URL (for Path C, use the Streamlit Cloud URL directly, since the iframe makes selectors awkward). Take 3 PNGs in `screenshots/`: positive, negative, fooled. Title and name must be visible in each. Wait for the result text before capturing, and allow for cold start (~30–60 s).

## Step 6: submission.pdf (reportlab, about 2 pages, mirrors the sample's sections)
Header: `Class Activity — Session 5: Sentiment Analyzer` · name/roll · Program BSCS · Section A · date
1. Live App URL (+ "confirmed working")
2. Commit-History Link
3. Screenshots: 3 side by side with captions (Positive / Negative / Fools the model)
4. Our Personalization: 2–3 lines on what was added beyond the starter code
5. Final Code: app.py + requirements.txt (+ Dockerfile/index.html if used), monospace
6. Three Test Cases: an Input | Output table with real scores, and the fooled case annotated with why
7. Reflection: one real error hit during the build and how it was fixed; **industry fit**; **biggest risk** (1–2 lines each)

Render the PDF to PNG and look at it: no overflowing code, no clipped images, 2–3 pages.

## Done when
- [ ] The live URL opens and analyzes text
- [ ] Commit history is visible
- [ ] 3 real screenshots
- [ ] `submission.pdf` is complete, with no placeholders left