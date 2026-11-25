# Project Overview & Step-by-Step Process

## Brief Introduction
The **Multilingual Motor Claims Intake Agent** is a Python and Streamlit prototype for First Notice of Loss (FNOL) insurance claims. It captures spoken accident reports in any native language, translates and normalizes them into clear English, and extracts structured claim fields for downstream processing and handler triage.

## Agents / Workflow Steps Used
Rather than a single autonomous agent picking actions at random, the project uses a **2-step deterministic prompt chain** (an agentic workflow) powered by a Gemini multimodal model:

1. **Multilingual Translation & Normalization Step:** Processes caller audio directly across languages and accents, detects the source language, and produces a clear English transcript while preserving incident context.
2. **Structured Extraction & Triage Step:** Reads the English transcript and maps key details (such as vehicle details, incident summary, damage, and injury or urgency flags) into a strict JSON schema.

*(Planned v2 additions introduce tool-calling functions—such as policy lookup, recovery dispatch, or human escalation—so the model can trigger specific actions when conditions match.)*

## Tech Stack Used
* **Language:** Python 3.11+
* **Frontend & Audio Capture:** Streamlit and `streamlit-mic-recorder`
* **LLM & Multimodal SDK:** Google GenAI SDK (`google-genai`)
* **Schema & Data Validation:** Pydantic for structured JSON outputs
* **Development & Version Control:** VS Code, Git, and GitHub

## Advantages of This Workflow
* **Reduces Language Friction:** Handles spoken reports in multiple languages without requiring a manual interpreter step first.
* **Turns Speech into Structured Fields:** Converts free-form voice notes into consistent fields that align with claims schemas and triage checks.
* **Predictable & Auditable:** A fixed sequence (`Audio` -> `English Transcript` -> `Structured Claim Fields`) makes each stage easier to inspect, validate, and keep under human review.
* **Clear Path to Tool Use:** Keeps v1 reliable while leaving room to add function calling and enterprise governance controls later.

## Step-by-Step Process (What Happens at Runtime)
1. **Launch the App:** Run `streamlit run app.py` with `GEMINI_API_KEY` set in your environment to open the local web UI.
2. **Record Caller Audio:** Speak a test accident report in any language using the microphone recorder in Streamlit.
3. **Step 1 — Translate to English:** Send the audio to Gemini to detect the spoken language and generate a clear English transcript.
4. **Step 2 — Extract Structured Fields:** Pass the English transcript to Gemini with a Pydantic schema to produce structured claim fields and triage flags.
5. **Review in the UI:** Inspect the transcript and structured output on screen (`st.session_state` keeps data in local memory during the session).