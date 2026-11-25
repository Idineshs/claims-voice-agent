# 🎙️ Multilingual Motor Claims Intake Agent

A Python and Streamlit prototype demonstrating an **Agentic Workflow (Prompt Chaining)** designed to eliminate language barriers in First Notice of Loss (FNOL) insurance claims intake.

The system ingests spoken accident reports in any native language, translates and normalizes the narrative into clear English, and extracts structured, schema-validated claim data ready for downstream insurance systems and handler triage.

> **Builder Note & Privacy Disclaimer:** Built by **Dinesh**—a Data Engineer who started out in System Administration and learns new technologies hands-on out of genuine curiosity, experimenting with agentic workflows alongside **Claude** and **Gemini**. This repository is a local Proof of Concept (PoC) intended strictly for testing with **synthetic/fictional data**. Never record real customer Personally Identifiable Information (PII), policy numbers, or confidential company details using public API endpoints.

---

## 🎯 Project Objective & Business Problem
In motor insurance claims, non-native English speakers often struggle to report urgent incidents clearly under stress, leading to delayed FNOL logging, miscommunication, and costly third-party interpreter bottlenecks.

**Ultimate Aim:**
1. **Multilingual Voice Ingestion:** Capture spoken incident reports in any native language or regional accent.
2. **Accurate English Normalization:** Translate the caller's statement into clear, domain-accurate English while preserving critical context.
3. **Structured Field Extraction:** Automatically map unstructured spoken narratives into standardized database fields (vehicle details, incident timeline, damage description, and injury/urgency triage flags).

---

## 🧠 Architecture: Deterministic Agentic Workflow vs. Autonomous Agent
In regulated financial services and insurance environments, **deterministic workflows** are preferred over unconstrained autonomous agents for core data capture because every step must be predictable, repeatable, and auditable.

This prototype implements a **2-Stage Prompt Chaining Workflow**:

```text
[ Caller Audio (Any Language) ]
               │
               ▼
┌─────────────────────────────────────────┐
│  Step 1: Multimodal Ingestion &         │
│  Native-to-English Translation          │  ◀── Gemini Multimodal LLM
└─────────────────────────────────────────┘
               │
               ▼  (Normalized English Transcript)
┌─────────────────────────────────────────┐
│  Step 2: Structured Entity Extraction   │
│  & Triage Flagging                      │  ◀── Gemini + Pydantic Schema
└─────────────────────────────────────────┘
               │
               ▼
[ Validated JSON Claim Record + UI Review ]