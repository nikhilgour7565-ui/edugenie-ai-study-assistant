"""
Ultra-Modern Fintech/AI SaaS Design System for EduGenie.
Featuring layered glass containers, micro-interactions, gradient glow borders,
custom scrollbars, floating action bars, and refined typography.
"""

import streamlit as st


def apply_custom_styles():
    """Injects the flagship modern design system into the Streamlit app."""
    st.markdown("""
    <style>
        /* 1. Fonts Import */
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Outfit:wght@500;600;700;800;900&family=JetBrains+Mono:wght@400;500&display=swap');

        /* 2. Design System Variables */
        :root {
            --bg-canvas: #080c14;
            --bg-surface: rgba(15, 23, 42, 0.65);
            --bg-card: rgba(20, 29, 51, 0.55);
            --bg-card-hover: rgba(30, 43, 77, 0.7);
            --border-glass: rgba(255, 255, 255, 0.08);
            --border-hover: rgba(99, 102, 241, 0.35);
            --border-active: rgba(56, 189, 248, 0.6);
            --primary: #6366f1;
            --accent-cyan: #38bdf8;
            --accent-violet: #a855f7;
            --text-main: #f8fafc;
            --text-sub: #94a3b8;
            --text-dim: #64748b;
            --grad-brand: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #38bdf8 100%);
            --grad-btn: linear-gradient(135deg, #4f46e5 0%, #6366f1 50%, #06b6d4 100%);
            --radius-sm: 8px;
            --radius-md: 14px;
            --radius-lg: 18px;
        }

        /* 3. Global Reset & Canvas Background with Subtle Mesh Gradient */
        html, body, [class*="css"], .stApp {
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
            background: #080c14 !important;
            background-image: 
                radial-gradient(at 0% 0%, rgba(99, 102, 241, 0.08) 0px, transparent 50%),
                radial-gradient(at 100% 100%, rgba(56, 189, 248, 0.06) 0px, transparent 50%) !important;
            color: var(--text-main) !important;
        }

        h1, h2, h3, h4, .brand-title, .hero-title {
            font-family: 'Outfit', sans-serif !important;
            letter-spacing: -0.025em !important;
        }

        /* 4. Canvas Container Polish */
        .block-container {
            padding-top: 1.5rem !important;
            padding-bottom: 2.5rem !important;
            max-width: 1300px !important;
        }

        /* 5. Sleek Floating Top Banner */
        .hero-banner {
            background: rgba(18, 25, 45, 0.45);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: var(--radius-lg);
            padding: 20px 26px;
            margin-bottom: 24px;
            backdrop-filter: blur(16px);
            box-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5), inset 0 1px 1px rgba(255, 255, 255, 0.1);
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 14px;
            transition: all 0.3s ease;
        }

        .hero-banner:hover {
            border-color: rgba(99, 102, 241, 0.25);
            box-shadow: 0 14px 36px -10px rgba(99, 102, 241, 0.2);
        }

        .hero-left {
            display: flex;
            align-items: center;
            gap: 14px;
        }

        .hero-icon-box {
            width: 44px;
            height: 44px;
            border-radius: 12px;
            background: linear-gradient(135deg, rgba(99, 102, 241, 0.25), rgba(56, 189, 248, 0.25));
            border: 1px solid rgba(99, 102, 241, 0.4);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5rem;
            box-shadow: 0 4px 12px rgba(99, 102, 241, 0.25);
        }

        .hero-title {
            font-size: 1.5rem;
            font-weight: 800;
            background: linear-gradient(90deg, #ffffff 0%, #cbd5e1 50%, #38bdf8 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin: 0;
            line-height: 1.2;
        }

        .hero-desc {
            color: #94a3b8;
            font-size: 0.88rem;
            margin: 2px 0 0 0;
        }

        .pill-container {
            display: flex;
            flex-wrap: wrap;
            gap: 6px;
        }

        .feature-pill {
            display: inline-flex;
            align-items: center;
            gap: 5px;
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid rgba(255, 255, 255, 0.08);
            color: #cbd5e1;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.76rem;
            font-weight: 600;
            transition: all 0.2s ease;
        }

        .feature-pill:hover {
            background: rgba(99, 102, 241, 0.2);
            border-color: rgba(99, 102, 241, 0.4);
            color: #ffffff;
            transform: translateY(-1px);
        }

        /* 6. Sidebar Brand & Nav Styling */
        [data-testid="stSidebar"] {
            background: #0b0f19 !important;
            border-right: 1px solid rgba(255, 255, 255, 0.06) !important;
        }

        .sidebar-brand-card {
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid rgba(255, 255, 255, 0.06);
            border-radius: var(--radius-md);
            padding: 14px 16px;
            margin-bottom: 16px;
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .brand-icon {
            font-size: 1.5rem;
            display: flex;
            align-items: center;
            justify-content: center;
            width: 38px;
            height: 38px;
            background: linear-gradient(135deg, rgba(99, 102, 241, 0.35), rgba(56, 189, 248, 0.25));
            border: 1px solid rgba(99, 102, 241, 0.4);
            border-radius: 10px;
        }

        .brand-title {
            font-size: 1.25rem;
            font-weight: 800;
            color: #f8fafc;
            margin: 0;
            line-height: 1.1;
        }

        .brand-subtitle {
            font-size: 0.74rem;
            color: #64748b;
            font-weight: 500;
            margin-top: 2px;
        }

        /* Custom Sidebar Nav Items */
        [data-testid="stSidebar"] .stRadio [role="radiogroup"] {
            gap: 8px;
        }

        [data-testid="stSidebar"] .stRadio [role="radiogroup"] label {
            background: rgba(255, 255, 255, 0.025);
            border: 1px solid rgba(255, 255, 255, 0.06);
            border-radius: 10px;
            padding: 10px 14px;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
            margin: 0;
            cursor: pointer;
        }

        [data-testid="stSidebar"] .stRadio [role="radiogroup"] label:hover {
            background: rgba(99, 102, 241, 0.12);
            border-color: rgba(99, 102, 241, 0.3);
            transform: translateX(3px);
        }

        [data-testid="stSidebar"] .stRadio [role="radiogroup"] label[data-checked="true"] {
            background: linear-gradient(90deg, rgba(99, 102, 241, 0.25) 0%, rgba(56, 189, 248, 0.12) 100%) !important;
            border-color: rgba(129, 140, 248, 0.55) !important;
            box-shadow: 0 4px 12px rgba(99, 102, 241, 0.2);
        }

        /* 7. Glass Card Containers */
        .glass-card {
            background: var(--bg-card);
            border: 1px solid var(--border-glass);
            border-radius: var(--radius-md);
            padding: 20px 24px;
            margin-bottom: 16px;
            backdrop-filter: blur(14px);
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.25);
            transition: all 0.2s ease;
        }

        .glass-card:hover {
            border-color: rgba(255, 255, 255, 0.14);
            transform: translateY(-1px);
        }

        /* 8. Modern Buttons with Smooth Gradients & Shadows */
        .stButton>button {
            border-radius: 10px !important;
            font-weight: 600 !important;
            font-size: 0.92rem !important;
            padding: 0.55rem 1.3rem !important;
            transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
        }

        .stButton>button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 18px rgba(99, 102, 241, 0.3) !important;
            border-color: #818cf8 !important;
        }

        .stButton>button[kind="primary"] {
            background: var(--grad-btn) !important;
            border: none !important;
            color: #ffffff !important;
            box-shadow: 0 4px 16px rgba(79, 70, 229, 0.4) !important;
        }

        .stButton>button[kind="primary"]:hover {
            box-shadow: 0 8px 24px rgba(79, 70, 229, 0.6) !important;
            transform: translateY(-2px) !important;
        }

        /* 9. Styled Modern Tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 6px;
            background: rgba(15, 23, 42, 0.55);
            padding: 6px;
            border-radius: 12px;
            border: 1px solid rgba(255, 255, 255, 0.06);
        }

        .stTabs [data-baseweb="tab"] {
            border-radius: 8px !important;
            padding: 7px 16px !important;
            font-weight: 600 !important;
            font-size: 0.88rem !important;
            color: #94a3b8 !important;
            transition: all 0.2s ease !important;
        }

        .stTabs [aria-selected="true"] {
            background: rgba(99, 102, 241, 0.25) !important;
            color: #ffffff !important;
            border: 1px solid rgba(99, 102, 241, 0.4) !important;
            box-shadow: 0 2px 8px rgba(99, 102, 241, 0.15) !important;
        }

        /* 10. Flashcard Box Polish */
        .flashcard-box {
            background: linear-gradient(145deg, #131b2e 0%, #0b1120 100%);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-left: 4px solid #6366f1;
            border-radius: var(--radius-md);
            padding: 20px 24px;
            margin-bottom: 14px;
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
            transition: all 0.2s ease;
        }

        .flashcard-box:hover {
            transform: translateY(-2px);
            border-left-color: #38bdf8;
            box-shadow: 0 8px 24px rgba(56, 189, 248, 0.2);
        }

        /* 11. Compact Dropzone Styling */
        [data-testid="stFileUploader"] section {
            padding: 10px 14px !important;
            background: rgba(15, 23, 42, 0.5) !important;
            border: 1px dashed rgba(255, 255, 255, 0.14) !important;
            border-radius: 10px !important;
        }

        [data-testid="stFileUploader"] section:hover {
            border-color: rgba(99, 102, 241, 0.45) !important;
        }

        /* 12. Inputs & Glowing Focus Rings */
        .stTextInput input, .stTextArea textarea, .stSelectbox select {
            border-radius: 10px !important;
            background: rgba(15, 23, 42, 0.65) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            color: #f8fafc !important;
            font-size: 0.92rem !important;
        }

        .stTextInput input:focus, .stTextArea textarea:focus {
            border-color: #38bdf8 !important;
            box-shadow: 0 0 0 2px rgba(56, 189, 248, 0.25) !important;
        }

        /* 13. Badges */
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
    </style>
    """, unsafe_allow_html=True)
