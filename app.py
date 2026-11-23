import streamlit as st
from pydantic import BaseModel, Field
from google import genai
from google.genai import types
from streamlit_mic_recorder import mic_recorder

# --- 1. DEFINE STRUCTURED OUTPUT SCHEMA (Pydantic) ---
class MotorClaimReport(BaseModel):
    detected_language: str = Field(description="Language or accent spoken by the caller")
    native_transcript: str = Field(description="Exact transcription in the caller's original language")
    english_translation: str = Field(description="Accurate English translation of what the caller said")
    policyholder_name: str = Field(description="Full name of caller, or 'Not provided'")
    vehicle_registration: str = Field(description="License plate / reg number, or 'Not provided'")
    incident_location: str = Field(description="Street, city, or landmark where the accident happened")
    incident_summary_en: str = Field(description="Clear, concise English summary of the accident for the claims handler")
    injuries_reported: bool = Field(description="True if anyone was injured, otherwise False")
    urgency_level: str = Field(description="'HIGH' if injuries or undrivable vehicle, else 'STANDARD'")

# --- 2. INITIALIZE CLIENT & STREAMLIT UI ---
st.set_page_config(page_title="Multilingual Claims Intake Agent", layout="wide")
st.title("🎙️ Multilingual Motor Claims Intake Demo")
st.caption("Speak in any language (Chinese, Malayalam, Arabic, accented English). The chain translates and structures the claim in English.")

client = genai.Client()

# Initialize session state to store processed claims like a live call-center queue
if "claims_queue" not in st.session_state:
    st.session_state.claims_queue = []

col1, col2 = st.columns([1, 1.5])

# --- LEFT PANEL: CALLER VOICE INPUT ---
with col1:
    st.subheader("1. Caller Voice Input")
    st.write("Record a mock accident report in your native language:")
    
    audio = mic_recorder(
        start_prompt="🔴 Start Recording Claim",
        stop_prompt="⏹️ Stop & Submit Call",
        just_once=True,
        key="caller_mic"
    )

    if audio:
        st.audio(audio["bytes"], format="audio/wav")
        
        with st.spinner("Running Prompt Chain: Transcribing, Translating & Structuring..."):
            # STEP 1: Audio -> Native Transcript + English Translation
            step1_prompt = (
                "Listen to this insurance caller recording. "
                "1) Identify the language/accent. "
                "2) Transcribe accurately in the original language. "
                "3) Translate accurately into clear English."
            )
            
            step1_response = client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=[
                    step1_prompt,
                    types.Part.from_bytes(data=audio["bytes"], mime_type="audio/wav")
                ]
            )
            
            # STEP 2: English Translation -> Structured Claims JSON (Chained Output)
            step2_prompt = f"""
            You are a motor insurance claims triage agent. Extract structured claim details 
            in clean English from the following call transcript and translation:
            
            {step1_response.text}
            """
            
            step2_response = client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=step2_prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=MotorClaimReport,
                )
            )
            
            # Parse validated Pydantic JSON and add to dashboard queue
            claim_data = MotorClaimReport.model_validate_json(step2_response.text)
            st.session_state.claims_queue.insert(0, claim_data.model_dump())
            st.success("Call processed and routed to English Claims Queue!")

# --- RIGHT PANEL: CALL CENTER ENGLISH DASHBOARD ---
with col2:
    st.subheader("2. Call Center English Dashboard (Live Queue)")
    
    if not st.session_state.claims_queue:
        st.info("No calls recorded yet. Click 'Start Recording Claim' on the left to test.")
    else:
        # Show latest structured claim card
        latest = st.session_state.claims_queue[0]
        badge = "🚨 HIGH URGENCY" if latest["urgency_level"] == "HIGH" else "🟢 STANDARD"
        
        st.markdown(f"### Latest Claim ({badge} | Spoken: `{latest['detected_language']}`)")
        st.json(latest)
        
        st.markdown("### All Logged Claims (English Table)")
        st.dataframe(st.session_state.claims_queue, use_container_width=True)