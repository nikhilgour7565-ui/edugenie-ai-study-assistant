"""
Sleek Modern SaaS Theme Engine for EduGenie.
Implements refined dark slate backdrops, subtle glass cards, compact file dropzones,
glowing active nav states, and balanced typography.
"""

import streamlit as st


def apply_custom_styles():
    """Injects the refined modern SaaS design system into the Streamlit app."""
    st.markdown("""
    <style>
        /* 1. Google Fonts Import */
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Outfit:wght@500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

        /* 2. Global CSS Variables & Tokens */
        :root {
            --bg-canvas: #0b0f19;
            --bg-card: rgba(18, 24, 38, 0.7);
            --bg-card-hover: rgba(28, 38, 58, 0.85);
            --border-subtle: rgba(255, 255, 255, 0.08);
            --border-focus: rgba(99, 102, 241, 0.45);
            --border-cyan: rgba(56, 189, 248, 0.5);
            --text-primary: #f8fafc;
            --text-secondary: #94a3b8;
            --text-muted: #64748b;
            --grad-primary: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
            --grad-accent: linear-gradient(135deg, #818cf8 0%, #38bdf8 100%);
            --radius-sm: 8px;
            --radius-md: 12px;
            --radius-lg: 16px;
        }

        /* 3. Global Typography & Background */
        html, body, [class*="css"], .stApp {
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
            background-color: var(--bg-canvas) !important;
            color: var(--text-primary) !important;
        }

        h1, h2, h3, h4, .hero-title, .brand-title {
            font-family: 'Outfit', sans-serif !important;
            letter-spacing: -0.02em !important;
        }

        /* 4. Streamlit Default Spacing Refinement */
        .block-container {
            padding-top: 1.8rem !important;
            padding-bottom: 2rem !important;
            max-width: 1280px !important;
        }

        /* 5. Refined Subtle Glass Hero Header */
        .hero-banner {
            background: rgba(255, 255, 255, 0.025);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: var(--radius-lg);
            padding: 18px 24px;
            margin-bottom: 22px;
            backdrop-filter: blur(12px);
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.18);
            display: flex;
            flex-direction: column;
            gap: 6px;
        }

        .hero-top-row {
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 10px;
        }

        .hero-title {
            font-size: 1.65rem;
            font-weight: 800;
            background: linear-gradient(135deg, #ffffff 0%, #c7d2fe 45%, #38bdf8 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin: 0;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .hero-subtitle {
            color: #94a3b8;
            font-size: 0.92rem;
            font-weight: 400;
            line-height: 1.5;
            margin: 0;
            max-width: 900px;
        }

        /* Sleek Chip Pills */
        .pill-container {
            display: flex;
            flex-wrap: wrap;
            gap: 6px;
            margin-top: 6px;
        }

        .feature-pill {
            display: inline-flex;
            align-items: center;
            gap: 5px;
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid rgba(255, 255, 255, 0.08);
            color: #cbd5e1;
            padding: 3px 10px;
            border-radius: 20px;
            font-size: 0.76rem;
            font-weight: 500;
            transition: all 0.2s ease;
        }

        .feature-pill:hover {
            background: rgba(99, 102, 241, 0.18);
            border-color: rgba(129, 140, 248, 0.4);
            color: #ffffff;
            transform: translateY(-1px);
        }

        /* 6. Sidebar Reorganization & Custom Nav */
        .sidebar-brand-card {
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid rgba(255, 255, 255, 0.06);
            border-radius: var(--radius-md);
            padding: 14px;
            margin-bottom: 14px;
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .brand-icon {
            font-size: 1.6rem;
            display: flex;
            align-items: center;
            justify-content: center;
            width: 38px;
            height: 38px;
            background: linear-gradient(135deg, rgba(99, 102, 241, 0.3), rgba(56, 189, 248, 0.2));
            border: 1px solid rgba(99, 102, 241, 0.4);
            border-radius: 10px;
        }

        .brand-title {
            font-size: 1.2rem;
            font-weight: 800;
            color: #f8fafc;
            line-height: 1.2;
            margin: 0;
        }

        .brand-subtitle {
            font-size: 0.74rem;
            color: #64748b;
            font-weight: 500;
        }

        /* Sidebar Navigation Active Pill Style */
        [data-testid="stSidebar"] .stRadio [role="radiogroup"] {
            gap: 6px;
        }

        [data-testid="stSidebar"] .stRadio [role="radiogroup"] label {
            background: rgba(255, 255, 255, 0.025);
            border: 1px solid rgba(255, 255, 255, 0.06);
            border-radius: 10px;
            padding: 8px 12px;
            transition: all 0.2s ease;
            margin: 0;
        }

        [data-testid="stSidebar"] .stRadio [role="radiogroup"] label:hover {
            background: rgba(99, 102, 241, 0.12);
            border-color: rgba(99, 102, 241, 0.3);
            transform: translateX(2px);
        }

        [data-testid="stSidebar"] .stRadio [role="radiogroup"] label[data-checked="true"] {
            background: linear-gradient(90deg, rgba(99, 102, 241, 0.22) 0%, rgba(56, 189, 248, 0.1) 100%) !important;
            border-color: rgba(129, 140, 248, 0.5) !important;
            box-shadow: 0 2px 8px rgba(99, 102, 241, 0.15);
        }

        /* 7. Streamlit File Uploader Compact Styling */
        [data-testid="stFileUploader"] {
            padding: 0 !important;
        }

        [data-testid="stFileUploader"] section {
            padding: 10px 14px !important;
            background: rgba(15, 23, 42, 0.5) !important;
            border: 1px dashed rgba(255, 255, 255, 0.15) !important;
            border-radius: 10px !important;
            min-height: auto !important;
        }

        [data-testid="stFileUploader"] section:hover {
            border-color: rgba(99, 102, 241, 0.4) !important;
        }

        [data-testid="stFileUploader"] section button {
            padding: 4px 12px !important;
            font-size: 0.8rem !important;
            border-radius: 6px !important;
        }

        [data-testid="stFileUploader"] small {
            font-size: 0.74rem !important;
            color: #64748b !important;
        }

        /* 8. Glassmorphism Card Containers */
        .glass-card {
            background: rgba(18, 24, 38, 0.65);
            border: 1px solid rgba(255, 255, 255, 0.07);
            border-radius: var(--radius-md);
            padding: 18px 22px;
            margin-bottom: 16px;
            backdrop-filter: blur(12px);
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
            transition: all 0.2s ease;
        }

        .glass-card:hover {
            border-color: rgba(255, 255, 255, 0.12);
        }

        /* 9. Flashcard Styling */
        .flashcard-box {
            background: linear-gradient(145deg, #161f33 0%, #0d1424 100%);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-left: 4px solid #6366f1;
            border-radius: var(--radius-md);
            padding: 18px 22px;
            margin-bottom: 12px;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.25);
            transition: all 0.2s ease;
        }

        .flashcard-box:hover {
            transform: translateY(-2px);
            border-left-color: #38bdf8;
            box-shadow: 0 6px 20px rgba(56, 189, 248, 0.15);
        }

        /* 10. Status Badges */
        .badge-tag {
            display: inline-flex;
            align-items: center;
            gap: 4px;
            padding: 3px 10px;
            border-radius: 8px;
            font-size: 0.74rem;
            font-weight: 600;
        }
        .badge-blue { background: rgba(56, 189, 248, 0.12); color: #7dd3fc; border: 1px solid rgba(56, 189, 248, 0.3); }
        .badge-purple { background: rgba(129, 140, 248, 0.12); color: #c7d2fe; border: 1px solid rgba(129, 140, 248, 0.3); }
        .badge-green { background: rgba(34, 197, 94, 0.12); color: #86efac; border: 1px solid rgba(34, 197, 94, 0.3); }
        .badge-amber { background: rgba(245, 158, 11, 0.12); color: #fde68a; border: 1px solid rgba(245, 158, 11, 0.3); }

        /* 11. Buttons Overhaul */
        .stButton>button {
            border-radius: 10px !important;
            font-weight: 600 !important;
            font-size: 0.9rem !important;
            padding: 0.5rem 1.2rem !important;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
        }
        .stButton>button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 4px 14px rgba(99, 102, 241, 0.25) !important;
            border-color: #818cf8 !important;
        }

        /* Primary Button Gradient */
        .stButton>button[kind="primary"] {
            background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%) !important;
            border: none !important;
            color: #ffffff !important;
            box-shadow: 0 4px 14px rgba(99, 102, 241, 0.35) !important;
        }
        .stButton>button[kind="primary"]:hover {
            box-shadow: 0 6px 20px rgba(99, 102, 241, 0.5) !important;
            transform: translateY(-2px) !important;
        }

        /* 12. Styled Tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 4px;
            background: rgba(15, 23, 42, 0.5);
            padding: 4px;
            border-radius: 10px;
            border: 1px solid rgba(255, 255, 255, 0.06);
        }
        .stTabs [data-baseweb="tab"] {
            border-radius: 8px !important;
            padding: 6px 14px !important;
            font-weight: 600 !important;
            font-size: 0.85rem !important;
            color: #94a3b8 !important;
        }
        .stTabs [aria-selected="true"] {
            background: rgba(99, 102, 241, 0.2) !important;
            color: #ffffff !important;
            border: 1px solid rgba(99, 102, 241, 0.35) !important;
        }

        /* 13. Input Focus Rings */
        .stTextInput input, .stTextArea textarea, .stSelectbox select {
            border-radius: 8px !important;
            background: rgba(15, 23, 42, 0.6) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            color: #f8fafc !important;
            font-size: 0.92rem !important;
        }
        .stTextInput input:focus, .stTextArea textarea:focus {
            border-color: #38bdf8 !important;
            box-shadow: 0 0 0 2px rgba(56, 189, 248, 0.2) !important;
        }
    </style>
    """, unsafe_allow_html=True)
