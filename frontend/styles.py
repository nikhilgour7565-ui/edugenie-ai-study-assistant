"""
Design tokens, Glassmorphism styles, glowing gradients, animations, and typography for EduGenie.
"""

import streamlit as st


def apply_custom_styles():
    """Injects modern Glassmorphism styling, animated glowing accents, and premium typography."""
    st.markdown("""
    <style>
        /* Import Premium Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Outfit:wght@400;500;600;700;800;900&display=swap');
        
        :root {
            --primary-gradient: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #d946ef 100%);
            --secondary-gradient: linear-gradient(135deg, #0ea5e9 0%, #3b82f6 50%, #6366f1 100%);
            --glass-bg: rgba(15, 23, 42, 0.75);
            --glass-border: rgba(255, 255, 255, 0.1);
            --glow-color: rgba(99, 102, 241, 0.25);
        }

        html, body, [class*="css"] {
            font-family: 'Plus Jakarta Sans', sans-serif;
            color: #f8fafc;
        }

        h1, h2, h3, .hero-title {
            font-family: 'Outfit', sans-serif !important;
            letter-spacing: -0.02em;
        }

        /* Animated Glowing Hero Banner */
        .hero-banner {
            position: relative;
            background: linear-gradient(135deg, rgba(30, 27, 75, 0.85) 0%, rgba(49, 46, 129, 0.7) 40%, rgba(88, 28, 135, 0.6) 100%);
            border: 1px solid rgba(167, 139, 250, 0.25);
            border-radius: 20px;
            padding: 32px 36px;
            margin-bottom: 28px;
            backdrop-filter: blur(16px);
            box-shadow: 0 12px 40px -10px rgba(99, 102, 241, 0.35), inset 0 1px 1px rgba(255, 255, 255, 0.2);
            overflow: hidden;
            transition: all 0.3s ease;
        }

        .hero-banner::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle at center, rgba(168, 85, 247, 0.12) 0%, transparent 60%);
            pointer-events: none;
        }
        
        .hero-title {
            font-size: 2.4rem;
            font-weight: 800;
            background: linear-gradient(90deg, #ffffff 0%, #c4b5fd 40%, #93c5fd 80%, #f472b6 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            gap: 12px;
        }
        
        .hero-subtitle {
            color: #cbd5e1;
            font-size: 1.05rem;
            font-weight: 400;
            line-height: 1.6;
            margin-bottom: 18px;
            max-width: 900px;
        }

        .pill-container {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
        }

        .feature-pill {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: rgba(255, 255, 255, 0.06);
            border: 1px solid rgba(255, 255, 255, 0.15);
            color: #e2e8f0;
            padding: 6px 14px;
            border-radius: 30px;
            font-size: 0.84rem;
            font-weight: 600;
            backdrop-filter: blur(8px);
            transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
        }

        .feature-pill:hover {
            background: rgba(99, 102, 241, 0.3);
            border-color: #a78bfa;
            color: #ffffff;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(139, 92, 246, 0.3);
        }

        /* Glassmorphism Cards */
        .glass-card {
            background: linear-gradient(135deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0.8) 100%);
            border: 1px solid rgba(255, 255, 255, 0.09);
            border-radius: 16px;
            padding: 22px 26px;
            margin-bottom: 20px;
            backdrop-filter: blur(14px);
            box-shadow: 0 6px 24px rgba(0, 0, 0, 0.25);
            transition: transform 0.2s ease, border-color 0.2s ease;
        }

        .glass-card:hover {
            border-color: rgba(167, 139, 250, 0.3);
        }

        .glass-card-header {
            font-size: 1.18rem;
            font-weight: 700;
            color: #f8fafc;
            margin-bottom: 12px;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        /* Flashcard Premium Deck Styling */
        .flashcard-box {
            background: linear-gradient(145deg, #1e293b 0%, #0f172a 100%);
            border: 1px solid #334155;
            border-left: 6px solid #6366f1;
            border-radius: 14px;
            padding: 22px 26px;
            margin-bottom: 16px;
            box-shadow: 0 8px 24px rgba(0,0,0,0.3);
            transition: all 0.25s ease;
        }

        .flashcard-box:hover {
            transform: translateY(-3px);
            border-left-color: #ec4899;
            box-shadow: 0 12px 28px rgba(99, 102, 241, 0.25);
        }

        .flashcard-front {
            font-family: 'Outfit', sans-serif;
            font-weight: 700;
            font-size: 1.15rem;
            color: #f1f5f9;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        .flashcard-back {
            color: #cbd5e1;
            font-size: 1rem;
            line-height: 1.65;
            padding-top: 12px;
            border-top: 1px dashed rgba(255, 255, 255, 0.12);
        }

        /* Badge Tags */
        .badge-tag {
            display: inline-flex;
            align-items: center;
            gap: 4px;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 0.78rem;
            font-weight: 700;
            letter-spacing: 0.3px;
        }
        .badge-blue { background: rgba(59, 130, 246, 0.18); color: #93c5fd; border: 1px solid rgba(59, 130, 246, 0.4); }
        .badge-purple { background: rgba(168, 85, 247, 0.18); color: #d8b4fe; border: 1px solid rgba(168, 85, 247, 0.4); }
        .badge-green { background: rgba(34, 197, 94, 0.18); color: #86efac; border: 1px solid rgba(34, 197, 94, 0.4); }
        .badge-amber { background: rgba(245, 158, 11, 0.18); color: #fde68a; border: 1px solid rgba(245, 158, 11, 0.4); }

        /* Quick Suggestion Chips */
        .chip-btn {
            display: inline-block;
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.12);
            color: #cbd5e1;
            padding: 5px 12px;
            border-radius: 18px;
            font-size: 0.82rem;
            font-weight: 500;
            margin-right: 8px;
            margin-bottom: 8px;
            transition: all 0.2s ease;
        }
        .chip-btn:hover {
            background: rgba(99, 102, 241, 0.2);
            border-color: #818cf8;
            color: #ffffff;
        }

        /* Stats Indicator */
        .stat-pill {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            font-size: 0.88rem;
            color: #94a3b8;
            background: rgba(15, 23, 42, 0.7);
            padding: 5px 14px;
            border-radius: 10px;
            border: 1px solid rgba(255,255,255,0.08);
        }

        /* Streamlit Button Custom Hover */
        .stButton>button {
            border-radius: 10px !important;
            font-weight: 600 !important;
            transition: all 0.2s ease !important;
        }
        .stButton>button:hover {
            transform: translateY(-1px) !important;
            box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3) !important;
        }

        /* Custom Tabs Styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
        }
        .stTabs [data-baseweb="tab"] {
            border-radius: 8px !important;
            padding: 8px 16px !important;
            font-weight: 600 !important;
        }
    </style>
    """, unsafe_allow_html=True)
