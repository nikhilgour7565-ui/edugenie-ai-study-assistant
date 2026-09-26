"""
Complete CSS Design System & Theme Engine for EduGenie.
Implements Deep Slate / Indigo theme with Violet-to-Cyan gradients,
polished glassmorphism, responsive cards, glowing focus rings, and custom tabs.
"""

import streamlit as st


def apply_custom_styles():
    """Injects the complete EduGenie design system into the Streamlit app."""
    st.markdown("""
    <style>
        /* 1. Google Fonts Import */
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;1,400&family=Outfit:wght@500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600&display=swap');

        /* 2. Global CSS Variables & Tokens */
        :root {
            --bg-canvas: #090d16;
            --bg-card: rgba(19, 27, 46, 0.7);
            --bg-card-hover: rgba(30, 41, 69, 0.85);
            --border-subtle: rgba(255, 255, 255, 0.08);
            --border-accent: rgba(99, 102, 241, 0.35);
            --border-active: rgba(6, 182, 212, 0.6);
            --text-primary: #f8fafc;
            --text-secondary: #94a3b8;
            --text-muted: #64748b;
            --grad-primary: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #06b6d4 100%);
            --grad-card: linear-gradient(145deg, rgba(23, 32, 54, 0.75) 0%, rgba(13, 20, 36, 0.85) 100%);
            --grad-hero: linear-gradient(135deg, rgba(30, 27, 75, 0.85) 0%, rgba(49, 46, 129, 0.75) 45%, rgba(14, 116, 144, 0.65) 100%);
            --glow-indigo: 0 0 25px rgba(99, 102, 241, 0.25);
            --glow-cyan: 0 0 25px rgba(6, 182, 212, 0.25);
            --radius-sm: 8px;
            --radius-md: 14px;
            --radius-lg: 20px;
        }

        /* 3. Global Typography */
        html, body, [class*="css"], .stApp {
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
            background-color: var(--bg-canvas) !important;
            color: var(--text-primary) !important;
        }

        h1, h2, h3, h4, h5, .hero-title, .brand-title {
            font-family: 'Outfit', sans-serif !important;
            letter-spacing: -0.025em !important;
            font-weight: 700 !important;
        }

        code, pre, .mono-text {
            font-family: 'JetBrains Mono', monospace !important;
        }

        /* 4. Top Hero Banner */
        .hero-banner {
            position: relative;
            background: var(--grad-hero);
            border: 1px solid rgba(167, 139, 250, 0.25);
            border-radius: var(--radius-lg);
            padding: 28px 32px;
            margin-bottom: 24px;
            backdrop-filter: blur(16px);
            box-shadow: 0 12px 36px -10px rgba(99, 102, 241, 0.35), inset 0 1px 1px rgba(255, 255, 255, 0.15);
            overflow: hidden;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }

        .hero-banner::after {
            content: '';
            position: absolute;
            top: -50%;
            right: -20%;
            width: 300px;
            height: 300px;
            background: radial-gradient(circle, rgba(6, 182, 212, 0.18) 0%, transparent 70%);
            pointer-events: none;
        }

        .hero-title {
            font-size: 2.25rem;
            font-weight: 800;
            background: linear-gradient(90deg, #ffffff 0%, #c4b5fd 40%, #a5f3fc 85%, #f472b6 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 6px;
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .hero-subtitle {
            color: #cbd5e1;
            font-size: 1.02rem;
            font-weight: 400;
            line-height: 1.55;
            margin-bottom: 16px;
            max-width: 850px;
        }

        .pill-container {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
        }

        .feature-pill {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: rgba(255, 255, 255, 0.07);
            border: 1px solid rgba(255, 255, 255, 0.14);
            color: #e2e8f0;
            padding: 5px 12px;
            border-radius: 24px;
            font-size: 0.8rem;
            font-weight: 600;
            backdrop-filter: blur(8px);
            transition: all 0.25s ease;
        }

        .feature-pill:hover {
            background: rgba(99, 102, 241, 0.3);
            border-color: #a78bfa;
            color: #ffffff;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(139, 92, 246, 0.35);
        }

        /* 5. Sidebar Identity & App Header */
        .sidebar-brand-card {
            background: linear-gradient(135deg, rgba(30, 41, 69, 0.9) 0%, rgba(15, 23, 42, 0.95) 100%);
            border: 1px solid rgba(99, 102, 241, 0.28);
            border-radius: var(--radius-md);
            padding: 16px 18px;
            margin-bottom: 18px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
            text-align: center;
        }

        .brand-icon-wrapper {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 46px;
            height: 46px;
            border-radius: 12px;
            background: linear-gradient(135deg, #6366f1, #06b6d4);
            box-shadow: 0 4px 14px rgba(99, 102, 241, 0.45);
            font-size: 1.5rem;
            margin-bottom: 8px;
        }

        .brand-title {
            font-size: 1.35rem;
            font-weight: 800;
            color: #ffffff;
            margin: 0;
            letter-spacing: -0.02em;
        }

        .brand-subtitle {
            font-size: 0.78rem;
            color: #94a3b8;
            font-weight: 500;
            margin-top: 2px;
        }

        /* 6. Glassmorphism Card Containers */
        .glass-card {
            background: var(--grad-card);
            border: 1px solid var(--border-subtle);
            border-radius: var(--radius-md);
            padding: 20px 24px;
            margin-bottom: 18px;
            backdrop-filter: blur(14px);
            box-shadow: 0 8px 30px rgba(0, 0, 0, 0.28);
            transition: transform 0.2s ease, border-color 0.2s ease;
        }

        .glass-card:hover {
            border-color: var(--border-accent);
        }

        .glass-card-header {
            font-size: 1.15rem;
            font-weight: 700;
            color: #f8fafc;
            margin-bottom: 12px;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        /* 7. Flashcards & Interactive Decks */
        .flashcard-box {
            background: linear-gradient(145deg, #1e293b 0%, #0b1329 100%);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-left: 6px solid #6366f1;
            border-radius: var(--radius-md);
            padding: 20px 24px;
            margin-bottom: 14px;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
            transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
        }

        .flashcard-box:hover {
            transform: translateY(-3px);
            border-left-color: #06b6d4;
            box-shadow: 0 12px 28px rgba(6, 182, 212, 0.25);
        }

        .flashcard-front {
            font-family: 'Outfit', sans-serif;
            font-weight: 700;
            font-size: 1.12rem;
            color: #f1f5f9;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .flashcard-back {
            color: #cbd5e1;
            font-size: 0.98rem;
            line-height: 1.6;
            padding-top: 12px;
            border-top: 1px dashed rgba(255, 255, 255, 0.12);
        }

        /* 8. Badge Tags & Status Indicators */
        .badge-tag {
            display: inline-flex;
            align-items: center;
            gap: 5px;
            padding: 4px 11px;
            border-radius: 12px;
            font-size: 0.76rem;
            font-weight: 700;
            letter-spacing: 0.3px;
        }
        .badge-blue { background: rgba(59, 130, 246, 0.16); color: #93c5fd; border: 1px solid rgba(59, 130, 246, 0.38); }
        .badge-purple { background: rgba(168, 85, 247, 0.16); color: #d8b4fe; border: 1px solid rgba(168, 85, 247, 0.38); }
        .badge-green { background: rgba(34, 197, 94, 0.16); color: #86efac; border: 1px solid rgba(34, 197, 94, 0.38); }
        .badge-amber { background: rgba(245, 158, 11, 0.16); color: #fde68a; border: 1px solid rgba(245, 158, 11, 0.38); }
        .badge-cyan { background: rgba(6, 182, 212, 0.16); color: #67e8f9; border: 1px solid rgba(6, 182, 212, 0.38); }

        /* 9. Quick Action Prompt Chips */
        .chip-btn {
            display: inline-block;
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.12);
            color: #cbd5e1;
            padding: 5px 12px;
            border-radius: 18px;
            font-size: 0.82rem;
            font-weight: 500;
            margin-right: 6px;
            margin-bottom: 8px;
            cursor: pointer;
            transition: all 0.2s ease;
        }
        .chip-btn:hover {
            background: rgba(99, 102, 241, 0.22);
            border-color: #818cf8;
            color: #ffffff;
            transform: translateY(-1px);
        }

        /* 10. Sidebar Stats & Metadata Pill */
        .stat-pill {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            font-size: 0.84rem;
            color: #94a3b8;
            background: rgba(15, 23, 42, 0.7);
            padding: 4px 12px;
            border-radius: 10px;
            border: 1px solid rgba(255, 255, 255, 0.08);
        }

        /* 11. Streamlit Buttons Overhaul */
        .stButton>button {
            border-radius: 10px !important;
            font-weight: 600 !important;
            font-size: 0.95rem !important;
            padding: 0.55rem 1.25rem !important;
            transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
            border: 1px solid rgba(255, 255, 255, 0.12) !important;
        }
        .stButton>button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 18px rgba(99, 102, 241, 0.35) !important;
            border-color: #818cf8 !important;
        }

        /* Primary Button Gradient */
        .stButton>button[kind="primary"] {
            background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #06b6d4 100%) !important;
            border: none !important;
            color: #ffffff !important;
            box-shadow: 0 4px 14px rgba(99, 102, 241, 0.4) !important;
        }

        /* 12. Styled Tabs System */
        .stTabs [data-baseweb="tab-list"] {
            gap: 6px;
            background: rgba(15, 23, 42, 0.6);
            padding: 6px;
            border-radius: 12px;
            border: 1px solid rgba(255, 255, 255, 0.07);
        }
        .stTabs [data-baseweb="tab"] {
            border-radius: 8px !important;
            padding: 8px 16px !important;
            font-weight: 600 !important;
            font-size: 0.9rem !important;
            color: #94a3b8 !important;
            transition: all 0.2s ease !important;
        }
        .stTabs [aria-selected="true"] {
            background: rgba(99, 102, 241, 0.25) !important;
            color: #ffffff !important;
            border: 1px solid rgba(99, 102, 241, 0.4) !important;
        }

        /* 13. Expanders Styling */
        .streamlit-expanderHeader {
            background: rgba(30, 41, 59, 0.5) !important;
            border-radius: 10px !important;
            font-weight: 600 !important;
        }

        /* 14. Inputs & Focus Glow */
        .stTextInput input, .stTextArea textarea, .stSelectbox select {
            border-radius: 10px !important;
            background: rgba(15, 23, 42, 0.65) !important;
            border: 1px solid rgba(255, 255, 255, 0.12) !important;
            color: #f8fafc !important;
            transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
        }
        .stTextInput input:focus, .stTextArea textarea:focus {
            border-color: #06b6d4 !important;
            box-shadow: 0 0 0 2px rgba(6, 182, 212, 0.25) !important;
        }
    </style>
    """, unsafe_allow_html=True)
