"""
Core educational business logic and generation services for EduGenie.
"""

import io
import json
import re
from typing import List, Dict, Any, Optional
from gtts import gTTS
from backend.gemini_client import get_gemini_model, handle_gemini_error
from backend.parsers import clean_json_output, extract_text_from_pdf, process_image


def generate_explanation(
    api_key: str,
    model_name: str = "gemini-3.8-flash",
    topic: str = "",
    audience_level: str = "Beginner / High School",
    output_style: str = "Balanced & Structured",
    uploaded_file_bytes: Optional[bytes] = None,
    file_type: Optional[str] = None
) -> Dict[str, Any]:
    """Generates structured concept explanation with optional multimodal document/diagram intake."""
    try:
        model = get_gemini_model(api_key, model_name or "gemini-3.8-flash", temperature=0.6)
        if not model:
            return {"success": False, "error": "Model initialization failed."}

        prompt_text = f"""
        You are an elite academic tutor and master explainer. Provide a deeply intuitive and comprehensive explanation.
        
        Topic/Subject: {topic if topic else 'Uploaded Study Document/Diagram'}
        Target Level: {audience_level}
        Focus Style: {output_style}

        Break your response down into the following structured sections:
        [SECTION: Core Intuition]
        A simple, jargon-free overview of the fundamental idea.

        [SECTION: Deep Breakdown]
        Step-by-step breakdown of how it works, mechanisms, and key components.

        [SECTION: Real-World Analogy]
        A vivid, relatable metaphor that connects abstract theory to everyday experience.

        [SECTION: Industry Applications]
        How this is actually used in research, engineering, biology, or modern industry.

        [SECTION: Self-Check Quiz]
        3 quick questions with answers to test understanding.
        """

        content_payload: List[Any] = [prompt_text]

        if uploaded_file_bytes and file_type:
            if "image" in file_type:
                img = process_image(uploaded_file_bytes)
                if img:
                    content_payload.append(img)
                    content_payload.append("Note: Analyze the uploaded visual image/diagram and incorporate its content into your explanation.")
            elif "pdf" in file_type:
                extracted_pdf = extract_text_from_pdf(uploaded_file_bytes)
                content_payload.append(f"\nEXTRACTED PDF CONTEXT:\n{extracted_pdf[:5000]}")
            elif "text" in file_type:
                text_str = uploaded_file_bytes.decode("utf-8", errors="ignore")
                content_payload.append(f"\nEXTRACTED TEXT CONTEXT:\n{text_str[:5000]}")

        response = model.generate_content(content_payload)
        return {"success": True, "content": response.text}
    except Exception as e:
        return {"success": False, "error": handle_gemini_error(e)}


def generate_quiz(
    api_key: str,
    model_name: str = "gemini-3.8-flash",
    topic: str = "",
    num_questions: int = 5,
    difficulty: str = "Medium"
) -> Dict[str, Any]:
    """Generates dynamic multiple-choice questions."""
    try:
        model = get_gemini_model(api_key, model_name or "gemini-3.8-flash", temperature=0.3)
        if not model:
            return {"success": False, "error": "Model initialization failed."}

        quiz_prompt = f"""
        You are an expert academic examiner. Generate a {num_questions}-question multiple choice quiz on '{topic}' with difficulty '{difficulty}'.
        
        You MUST respond ONLY with a valid JSON array of objects. Do not include markdown preamble or text outside JSON.
        Format:
        [
          {{
            "id": 1,
            "question": "Question text here?",
            "options": ["Option A", "Option B", "Option C", "Option D"],
            "correct_answer": "Option A",
            "explanation": "Why this answer is correct."
          }}
        ]
        """
        response = model.generate_content(quiz_prompt)
        cleaned_json = clean_json_output(response.text)
        parsed_quiz = json.loads(cleaned_json)
        return {"success": True, "data": parsed_quiz}
    except Exception as e:
        return {"success": False, "error": handle_gemini_error(e)}


def generate_flashcards(
    api_key: str,
    model_name: str = "gemini-3.8-flash",
    topic: str = "",
    count: int = 5
) -> Dict[str, Any]:
    """Generates active-recall study flashcards."""
    try:
        model = get_gemini_model(api_key, model_name or "gemini-3.8-flash", temperature=0.4)
        if not model:
            return {"success": False, "error": "Model initialization failed."}

        fc_prompt = f"""
        Create {count} high-yield study flashcards for '{topic}'.
        Return ONLY a valid JSON array of objects with keys 'front' (question or concept) and 'back' (concise, clear answer/definition).
        Format:
        [
          {{"front": "What is overfitting?", "back": "When a model learns training data noise too closely and fails to generalize to unseen data."}}
        ]
        """
        response = model.generate_content(fc_prompt)
        cleaned_json = clean_json_output(response.text)
        parsed_fc = json.loads(cleaned_json)
        return {"success": True, "data": parsed_fc}
    except Exception as e:
        return {"success": False, "error": handle_gemini_error(e)}


def generate_summary(
    api_key: str,
    model_name: str = "gemini-3.8-flash",
    text_content: str = "",
    summary_depth: str = "In-Depth Structured Notes"
) -> Dict[str, Any]:
    """Summarizes study notes and extracts cheat-sheets."""
    try:
        model = get_gemini_model(api_key, model_name or "gemini-3.8-flash", temperature=0.3)
        if not model:
            return {"success": False, "error": "Model initialization failed."}

        prompt = f"""
        You are an expert academic summarizer. Process the provided study notes at detail level: '{summary_depth}'.

        STUDY NOTES:
        \"\"\"{text_content[:12000]}\"\"\"

        Organize your response with these exact delimiters:
        [SECTION: Overview]
        3-4 sentences giving the high-level executive summary.

        [SECTION: Key Glossary]
        Table or bullet list of core terms, formulas, and crisp definitions.

        [SECTION: Structured Notes]
        In-depth categorised bullet points covering all critical mechanisms.

        [SECTION: One-Page Cheat-Sheet]
        Formulas, laws, rules of thumb, and must-know exam takeaways.
        """
        response = model.generate_content(prompt)
        return {"success": True, "content": response.text}
    except Exception as e:
        return {"success": False, "error": handle_gemini_error(e)}


def chat_doubt_solver(
    api_key: str,
    model_name: str = "gemini-3.8-flash",
    conversation_history: List[Dict[str, Any]] = None,
    user_query: str = ""
) -> Dict[str, Any]:
    """Processes interactive Socratic doubt clarification with conversational history."""
    try:
        model = get_gemini_model(api_key, model_name or "gemini-3.8-flash", temperature=0.5)
        if not model:
            return {"success": False, "error": "Model initialization failed."}

        if conversation_history is None:
            conversation_history = []

        chat = model.start_chat(history=gemini_history)
        system_prefix = "You are EduGenie, a supportive, patient, and world-class AI tutor. Answer questions clearly, provide step-by-step guidance, and format formulas or code cleanly with markdown.\n\n"
        
        response = chat.send_message(system_prefix + user_query)
        return {"success": True, "reply": response.text}
    except Exception as e:
        return {"success": False, "error": handle_gemini_error(e)}


def generate_tts_audio(text_content: str) -> io.BytesIO:
    """Generates MP3 audio stream using gTTS for auditory revision."""
    cleaned = re.sub(r"[#*_`>\-\[\]\(\)]", " ", text_content)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()[:2000]
    
    fp = io.BytesIO()
    tts = gTTS(text=cleaned, lang='en', slow=False)
    tts.write_to_fp(fp)
    fp.seek(0)
    return fp
