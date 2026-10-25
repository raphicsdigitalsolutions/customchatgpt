import os
import uuid
from datetime import datetime

import streamlit as st
from dotenv import load_dotenv, find_dotenv
from openai import OpenAI
from nexora_3d import apply_3d_premium_theme, hero_cube_html, header_reactor_html

# =========================================================
# NEXORA AI — Motion + Live Web Search
# Single-file Streamlit application
# =========================================================
load_dotenv(find_dotenv(), override=False)

APP_NAME = "NEXORA AI"
DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
DEFAULT_SYSTEM_PROMPT = (
    "You are NEXORA AI, a reliable, thoughtful, professional AI assistant. "
    "Answer the actual question directly, explain clearly, and adapt to the user. "
    "Never invent facts, sources, quotes, dates, statistics, or URLs. If unsure, say so. "
    "When web search is enabled, use it for current events, recent updates, changing facts, "
    "prices, product comparisons, software/API documentation, troubleshooting, and questions asking "
    "what is latest, today, or now. Prefer official documentation and primary sources, check publication "
    "dates, and cite sources supporting key claims. If search does not establish an answer, state the "
    "limitation instead of guessing. For stable general knowledge, answer directly without unnecessary searching."
)

st.set_page_config(
    page_title="NEXORA AI — Think beyond",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -------------------- DESIGN / MOTION --------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');
    :root{--ink:#211a32;--muted:#827990;--line:#ece5f2;--purple:#8057f5;--pink:#ed63bb;--paper:#fbf9f7;}
    @keyframes fadeUp{from{opacity:0;transform:translateY(16px)}to{opacity:1;transform:translateY(0)}}
    @keyframes orbFloat{0%,100%{transform:translateY(0) rotateX(10deg) rotateY(-12deg)}50%{transform:translateY(-8px) rotateX(14deg) rotateY(-4deg)}}
    @keyframes orbitSpin{from{transform:rotate(0)}to{transform:rotate(360deg)}}
    @keyframes glowPulse{0%,100%{opacity:.4;transform:scale(.94)}50%{opacity:.8;transform:scale(1.08)}}
    @keyframes gradientShift{0%,100%{background-position:0% 50%}50%{background-position:100% 50%}}
    html,body,[class*="css"]{font-family:'DM Sans',sans-serif}
    .stApp{color:var(--ink);background:radial-gradient(ellipse at 42% 1%,rgba(170,137,255,.24),transparent 34%),radial-gradient(ellipse at 92% 40%,rgba(255,177,216,.17),transparent 29%),radial-gradient(ellipse at 8% 84%,rgba(196,182,255,.13),transparent 31%),var(--paper);background-size:140% 140%;animation:gradientShift 18s ease-in-out infinite}
    [data-testid="stHeader"]{background:rgba(251,249,247,.72)}
    [data-testid="stMainBlockContainer"]{padding-bottom:7rem;animation:fadeUp .45s ease both}
    [data-testid="stSidebar"]{background:linear-gradient(180deg,rgba(255,253,252,.98),rgba(250,247,255,.98));border-right:1px solid rgba(230,220,241,.9)}
    [data-testid="stSidebar"]>div:first-child{padding:1.15rem .95rem}
    .brand-row{display:flex;align-items:center;gap:11px;margin:4px 0 5px}
    .brand-icon{width:44px;height:44px;border-radius:15px;display:flex;align-items:center;justify-content:center;color:white;font-size:23px;background:linear-gradient(145deg,#c7a8ff,#8057f5 45%,#ed63bb);background-size:160% 160%;animation:gradientShift 7s ease infinite;box-shadow:0 8px 20px rgba(128,87,245,.25),inset 0 1px 2px rgba(255,255,255,.7);transform:perspective(130px) rotateY(-8deg) rotateX(5deg);transition:transform .3s ease}
    .brand-icon:hover{transform:perspective(130px) rotateY(8deg) rotateX(-4deg) scale(1.08)}
    .brand-name{font:800 20px 'Manrope',sans-serif;letter-spacing:-.8px;color:#241d35}
    .brand-caption{margin:0 0 22px 55px;color:#92899e;font-size:10px;letter-spacing:.35px}
    .eyebrow{color:#988eaa;font-size:10px;font-weight:800;letter-spacing:1.55px;text-transform:uppercase;margin:22px 0 10px}
    .hero{max-width:920px;margin:2.2vh auto 16px;text-align:center;padding:10px 14px 5px;animation:fadeUp .7s cubic-bezier(.2,.8,.2,1) both}
    .orb-wrap{height:126px;display:flex;align-items:center;justify-content:center;margin:0 auto 12px;perspective:600px;position:relative}
    .orb-halo{position:absolute;width:112px;height:112px;border-radius:37px;background:radial-gradient(circle,rgba(159,112,255,.32),rgba(237,99,187,.08) 56%,transparent 72%);animation:glowPulse 4s ease-in-out infinite}
    .orb{position:relative;width:78px;height:78px;border-radius:27px;display:flex;align-items:center;justify-content:center;color:white;font-size:37px;background:linear-gradient(145deg,#d1b9ff,#9764ff 35%,#8057f5 55%,#ed69c1);box-shadow:0 20px 34px rgba(112,77,204,.24),inset 0 2px 4px rgba(255,255,255,.8),inset 0 -8px 14px rgba(73,35,147,.16);animation:orbFloat 5.2s ease-in-out infinite;transform-style:preserve-3d}
    .orb:before{content:"";position:absolute;inset:-10px;border-radius:33px;border:1px solid rgba(153,116,244,.24);transform:translateZ(-15px) rotateZ(12deg);box-shadow:0 0 28px rgba(169,128,255,.13)}
    .orb:after{content:"";position:absolute;left:13px;right:13px;top:5px;height:22px;border-radius:50%;background:linear-gradient(180deg,rgba(255,255,255,.52),transparent);filter:blur(2px)}
    .orbit{position:absolute;width:112px;height:112px;border-radius:38px;border:1px dashed rgba(143,105,238,.22);animation:orbitSpin 24s linear infinite}
    .orbit:after{content:"✦";position:absolute;top:5px;right:9px;font-size:13px;color:#a27bff;background:#fbf9f7;padding:0 2px}
    .hero-kicker{color:#887d9a;font-size:11px;font-weight:800;letter-spacing:1.4px;margin:0 0 10px}
    .hero h1{font:800 clamp(31px,4.2vw,53px)/1.13 'Manrope',sans-serif;letter-spacing:-2.2px;color:#211a32;margin:0 0 15px}
    .gradient-word{background:linear-gradient(100deg,#8057f5,#bd58e7,#ed63bb);background-size:200% auto;animation:gradientShift 5s ease infinite;-webkit-background-clip:text;background-clip:text;color:transparent;font-style:italic}
    .hero-subtitle{color:#898096;font-size:14px;line-height:1.8;max-width:570px;margin:0 auto}
    .section-heading{font:800 16px 'Manrope',sans-serif;color:#302741;margin:22px 0 13px;animation:fadeUp .8s .12s both}
    .stButton>button{border:1px solid rgba(234,225,244,.95);border-radius:16px;background:rgba(255,255,255,.79);color:#352b45;min-height:46px;font-weight:600;box-shadow:0 5px 15px rgba(47,30,75,.035),inset 0 1px 0 rgba(255,255,255,.92);transition:transform .22s ease,box-shadow .22s ease,border-color .22s ease}
    .stButton>button:hover{border-color:#c5afff;color:#7048e8;background:#fff;transform:translateY(-2px);box-shadow:0 11px 25px rgba(128,87,245,.12)}
    .stButton>button:active{transform:translateY(0) scale(.985)}
    .stButton>button[kind="primary"]{color:#fff;border:0;background:linear-gradient(105deg,#8057f5,#b65be8 55%,#ed63bb);background-size:180% 180%;animation:gradientShift 8s ease infinite;box-shadow:0 9px 22px rgba(128,87,245,.24),inset 0 1px 0 rgba(255,255,255,.25)}
    .stButton>button[kind="primary"]:hover{color:#fff;filter:brightness(1.05);box-shadow:0 12px 28px rgba(128,87,245,.3)}
    [data-testid="stChatInput"]{background:rgba(255,255,255,.96);border:1px solid #eae2f1;border-radius:20px;box-shadow:0 12px 30px rgba(49,31,75,.09)}
    [data-testid="stChatInput"]:focus-within{border-color:#c6b2ff;box-shadow:0 12px 32px rgba(128,87,245,.15)}
    [data-testid="stChatMessage"]{background:rgba(255,255,255,.82);border:1px solid #eee7f3;border-radius:18px;padding:16px 18px;margin-bottom:13px;box-shadow:0 5px 16px rgba(43,30,65,.025);animation:fadeUp .35s ease both}
    [data-testid="stTextInput"] input,[data-testid="stTextArea"] textarea,[data-testid="stSelectbox"] div[data-baseweb="select"]>div{border-radius:12px!important;border-color:#e9e1f0!important}
    .connection-pill{display:flex;align-items:center;gap:9px;padding:12px;border:1px solid #eee7f3;border-radius:15px;background:rgba(255,255,255,.9);margin:12px 0;color:#514860;font-size:12px;box-shadow:0 5px 14px rgba(40,24,60,.03)}
    .status-dot{width:8px;height:8px;border-radius:50%;background:#36bf7a;display:inline-block;box-shadow:0 0 0 4px rgba(54,191,122,.12)}
    .fine-print{text-align:center;color:#a098aa;font-size:11px;margin:16px auto 8px}
    [data-testid="stDialog"]>div{border-radius:25px}
    /* Compact, premium welcome dialog */
    [data-testid="stDialog"] [role="dialog"]{width:min(94vw,470px)!important;max-width:470px!important;border-radius:28px!important;border:1px solid rgba(255,255,255,.92)!important;background:rgba(255,255,255,.94)!important;box-shadow:0 28px 90px rgba(73,49,110,.18),0 2px 12px rgba(73,49,110,.05)!important;backdrop-filter:blur(22px)!important}
    [data-testid="stDialog"] [data-testid="stDialogHeader"]{background:transparent!important;border:0!important;min-height:12px!important;padding:8px 14px 0!important}
    [data-testid="stDialog"] [data-testid="stDialogHeader"] button{border-radius:50%!important}
    [data-testid="stDialog"] [data-testid="stVerticalBlock"]{gap:.6rem}
    .welcome-card{text-align:center;padding:0 5px 7px;animation:fadeUp .55s cubic-bezier(.2,.8,.2,1) both}
    .welcome-robot-wrap{width:100px;height:100px;margin:2px auto 13px;position:relative;display:flex;align-items:center;justify-content:center;border-radius:30px;background:linear-gradient(145deg,rgba(225,211,255,.8),rgba(255,224,241,.72));box-shadow:0 14px 35px rgba(143,103,218,.13),inset 0 1px 0 white}
    .welcome-robot{font-size:49px;filter:drop-shadow(0 7px 7px rgba(86,54,133,.16));animation:orbFloat 4.2s ease-in-out infinite}
    .robot-spark{position:absolute;color:#986bff;font-size:19px;animation:glowPulse 2.8s ease-in-out infinite}
    .spark-one{top:8px;right:8px}.spark-two{bottom:8px;left:9px;color:#ee76bd;animation-delay:.7s}
    .welcome-eyebrow{font-size:9px;font-weight:800;letter-spacing:1.8px;color:#9b8bab;margin:2px 0 9px}
    .welcome-title{font:800 29px/1.12 'Manrope',sans-serif;letter-spacing:-1.15px;color:#252035;margin:0 0 12px}
    .welcome-title span{background:linear-gradient(100deg,#8057f5,#c15fe4,#f27eb8);-webkit-background-clip:text;background-clip:text;color:transparent}
    .welcome-copy{font-size:12.5px;line-height:1.65;color:#877d98;max-width:300px;margin:0 auto 15px}
    .welcome-features{display:flex;justify-content:center;gap:6px;flex-wrap:wrap;margin:0 auto 12px}
    .welcome-features span{font-size:10px;font-weight:700;color:#5c4b71;padding:6px 9px;border-radius:30px;background:linear-gradient(120deg,#f5efff,#fff0f8);border:1px solid #eadcfb}
    .welcome-helper{text-align:center;color:#8c8398;font-size:10px;line-height:1.55;margin:0 5px}
    .welcome-link{text-align:center;color:#92869f;font-size:11px;margin:0 0 2px}
    .welcome-link a{color:#8057f5!important;font-weight:700;text-decoration:none!important}
    [data-testid="stDialog"] [data-testid="stCaptionContainer"]{text-align:center;color:#a39aaa;font-size:10px;line-height:1.5}
    [data-testid="stDialog"] [data-testid="stTextInput"] label{font-size:12px;font-weight:700;color:#514760}
    [data-testid="stDialog"] [data-testid="stTextInput"] input{background:#f4f2f8!important;border:1px solid #e9e1f2!important;border-radius:12px!important;min-height:43px}
    [data-testid="stDialog"] .stButton>button[kind="primary"]{min-height:45px;border-radius:13px!important}

    /* Premium, realistic workspace */
    [data-testid="stMainBlockContainer"]{max-width:1180px;padding-top:1.1rem}
    .workspace-topbar{display:flex;align-items:center;justify-content:space-between;gap:14px;margin:4px 0 18px;padding:12px 16px;border:1px solid rgba(232,223,242,.9);border-radius:18px;background:rgba(255,255,255,.68);box-shadow:0 8px 28px rgba(47,30,75,.035);backdrop-filter:blur(18px)}
    .workspace-brand{display:flex;align-items:center;gap:10px;font:800 14px 'Manrope',sans-serif;letter-spacing:-.3px;color:#2a223a}
    .workspace-mark{display:grid;place-items:center;width:34px;height:34px;border-radius:12px;color:#fff;font-size:18px;background:linear-gradient(145deg,#bca1ff,#8057f5 58%,#ed63bb);box-shadow:0 6px 15px rgba(128,87,245,.2),inset 0 1px 0 rgba(255,255,255,.7)}
    .workspace-status{display:flex;align-items:center;gap:7px;font-size:11px;font-weight:700;color:#7b718b;padding:7px 10px;border-radius:99px;border:1px solid #e9e1f1;background:rgba(255,255,255,.8)}
    .workspace-status-dot{width:7px;height:7px;border-radius:50%;background:#37bd83;box-shadow:0 0 0 4px rgba(55,189,131,.12)}
    .hero{max-width:850px;margin:4.2vh auto 22px;padding:10px 18px 8px}
    .orb-wrap{height:142px;margin-bottom:14px}
    .orb{width:84px;height:84px;border-radius:29px;font-size:40px}
    .hero-kicker{display:inline-flex;align-items:center;gap:7px;border:1px solid #e9dff9;background:rgba(255,255,255,.72);padding:7px 11px;border-radius:99px;margin-bottom:14px;font-size:10px}
    .hero h1{font-size:clamp(34px,4.5vw,54px);letter-spacing:-2.5px;margin-bottom:14px}
    .hero-subtitle{font-size:14px;max-width:590px}
    .section-heading{max-width:830px;margin:26px auto 13px;padding-left:3px;font-size:14px}
    [data-testid="stHorizontalBlock"]{gap:14px}
    .stButton>button{border-radius:16px;min-height:53px;text-align:left;padding:0 16px}
    .stButton>button[kind="primary"]{text-align:center}
    [data-testid="stChatInput"]{max-width:1000px;margin-left:auto;margin-right:auto;border-radius:22px}
    [data-testid="stChatMessage"]{max-width:1000px;margin-left:auto;margin-right:auto;border-radius:19px}
    [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"]{font-size:14px;line-height:1.75}
    .home-footnote{max-width:830px;margin:20px auto 0;padding:11px 14px;border-radius:14px;background:rgba(255,255,255,.5);border:1px solid rgba(235,227,243,.7);font-size:11px;color:#93899f;text-align:center}
    [data-testid="stSidebar"] [data-testid="stToggle"]{padding:10px;border-radius:14px;background:rgba(255,255,255,.65);border:1px solid #eee6f4}
    [data-testid="stExpander"]{border-color:#ece4f3!important;border-radius:14px!important;background:rgba(255,255,255,.65)!important}
    [data-testid="stAlert"]{border-radius:14px}
    @media(max-width:700px){[data-testid="stMainBlockContainer"]{padding:1rem .8rem 6rem}.workspace-topbar{padding:10px 12px}.hero{margin-top:2vh;padding-left:3px;padding-right:3px}.hero h1{font-size:34px;letter-spacing:-1.6px}.hero-subtitle{font-size:13px}.orb-wrap{height:112px}.stButton>button{min-height:48px;padding:0 10px;font-size:12px}}

        @media(prefers-reduced-motion:reduce){*,*::before,*::after{animation-duration:.01ms!important;animation-iteration-count:1!important;scroll-behavior:auto!important;transition-duration:.01ms!important}}
    @media(max-width:700px){.hero{margin-top:1vh;padding-left:2px;padding-right:2px}.hero h1{letter-spacing:-1.2px}.orb-wrap{height:100px}}
    </style>
    """,
    unsafe_allow_html=True,
)


st.markdown(
    """
<style>
.hero-trust-row{display:flex;justify-content:center;gap:8px;flex-wrap:wrap;margin:18px auto 0}
.hero-trust-row span{font:600 10px 'DM Sans',sans-serif;padding:7px 11px;border-radius:99px;color:#776786;background:rgba(255,255,255,.66);border:1px solid rgba(222,208,239,.88);box-shadow:0 5px 14px rgba(64,42,91,.035)}
.orb{box-shadow:0 24px 42px rgba(112,77,204,.28),inset 0 2px 4px rgba(255,255,255,.8),inset 0 -8px 14px rgba(73,35,147,.16)}
.welcome-card{padding-top:4px}
.welcome-robot-wrap{transform:perspective(360px) rotateX(4deg);border:1px solid rgba(255,255,255,.75)}
.welcome-robot{display:inline-block;animation:orbFloat 3.8s ease-in-out infinite}
@media(max-width:700px){.hero-trust-row span{font-size:9px;padding:6px 8px}}
@media(prefers-reduced-motion:reduce){.hero-trust-row span,.welcome-robot-wrap,.welcome-robot{animation:none!important;transition:none!important}}
</style>
    """,
    unsafe_allow_html=True,
)


# Final visual fixes requested after the first live preview:
# - remove the pulsing light blob behind the floating orb
# - stop animating the entire page background
# - prevent the headline and gradient word from clipping on narrower viewports
st.markdown(
    """
    <style>
    /* Calm, premium canvas: keep the 3D object moving, not the entire background. */
    .stApp {
        animation: none !important;
        background:
            radial-gradient(ellipse at 50% 0%, rgba(161,126,232,.10), transparent 38%),
            radial-gradient(ellipse at 95% 45%, rgba(230,154,197,.07), transparent 30%),
            var(--paper) !important;
        background-size: auto !important;
    }
    /* The halo was creating a large soft light patch that moved with the orb. */
    .orb-halo { display: none !important; animation: none !important; opacity: 0 !important; }
    .orb-wrap { isolation: isolate; overflow: visible !important; }
    .orb {
        z-index: 2;
        box-shadow:
            0 16px 28px rgba(95,63,171,.22),
            inset 0 2px 4px rgba(255,255,255,.82),
            inset 0 -8px 14px rgba(73,35,147,.17) !important;
    }
    .orb:before {
        box-shadow: none !important;
        border-color: rgba(153,116,244,.20) !important;
    }
    .orbit { z-index: 1; }
    .orbit:after { box-shadow: none !important; }

    /* Keep the headline centered and fully visible at desktop, tablet and mobile widths. */
    .hero {
        width: 100% !important;
        max-width: 980px !important;
        box-sizing: border-box !important;
        overflow: visible !important;
        padding-left: clamp(10px, 2.5vw, 28px) !important;
        padding-right: clamp(10px, 2.5vw, 28px) !important;
    }
    .hero h1 {
        display: block !important;
        width: 100% !important;
        max-width: 100% !important;
        box-sizing: border-box !important;
        margin-left: auto !important;
        margin-right: auto !important;
        padding: 0 .08em !important;
        font-size: clamp(27px, 4vw, 52px) !important;
        line-height: 1.18 !important;
        letter-spacing: clamp(-1.9px, -.11vw, -.45px) !important;
        white-space: normal !important;
        overflow: visible !important;
        overflow-wrap: normal !important;
        word-break: normal !important;
        text-wrap: balance;
    }
    .gradient-word {
        display: inline !important;
        white-space: normal !important;
        overflow-wrap: normal !important;
        word-break: normal !important;
        padding-right: .035em;
    }
    .hero-subtitle {
        width: 100% !important;
        max-width: 620px !important;
        box-sizing: border-box !important;
        padding-left: 8px !important;
        padding-right: 8px !important;
        margin-left: auto !important;
        margin-right: auto !important;
    }
    @media (max-width: 900px) {
        .hero { margin-top: 2.2vh !important; }
        .hero h1 {
            font-size: clamp(27px, 5.1vw, 42px) !important;
            letter-spacing: -.9px !important;
        }
        .orb-wrap { height: 124px !important; }
    }
    @media (max-width: 520px) {
        .hero { margin-top: 1vh !important; padding-left: 4px !important; padding-right: 4px !important; }
        .hero h1 { font-size: clamp(25px, 7vw, 34px) !important; letter-spacing: -.65px !important; line-height: 1.2 !important; }
        .hero-subtitle { font-size: 12.5px !important; line-height: 1.7 !important; }
        .orb-wrap { height: 108px !important; }
        .orbit { width: 100px !important; height: 100px !important; }
    }
    @media (prefers-reduced-motion: reduce) {
        .stApp, .orb, .orbit { animation: none !important; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# Apply the selected appearance without changing the app's functionality.
if st.session_state.get("dark_mode", False):
    st.markdown(
        """
        <style>
        :root{
          color-scheme:dark;
          --ink:#f3effb;--muted:#bdb2d0;--line:#3c314b;--paper:#15111c;
          --background-color:#15111c;--secondary-background-color:#211a2b;
          --text-color:#f3effb;--primary-color:#a88bff;
        }
        html,body,.stApp,[data-testid="stAppViewContainer"]{background:#15111c!important;color:#f3effb!important}
        .stApp{background:radial-gradient(ellipse at 42% 1%,rgba(119,82,195,.2),transparent 34%),radial-gradient(ellipse at 92% 40%,rgba(155,69,122,.12),transparent 29%),#15111c!important}
        [data-testid="stMain"],[data-testid="stMainBlockContainer"],[data-testid="stBottom"],[data-testid="stBottomBlockContainer"]{background:transparent!important;color:#f3effb!important}
        [data-testid="stHeader"]{background:rgba(21,17,28,.94)!important}
        [data-testid="stSidebar"],[data-testid="stSidebar"]>div:first-child{background:linear-gradient(180deg,#1b1623,#201829)!important;border-right:1px solid #393047!important}
        [data-testid="stSidebar"] *{color:#e9e1f5}
        [data-testid="stSidebar"] .eyebrow,[data-testid="stSidebar"] .brand-caption{color:#b9adca!important}
        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p{color:#c9bfd8!important}
        [data-testid="stSidebar"] [data-testid="stToggle"] label{color:#eee7fa!important}
        .brand-name,.hero h1,.section-heading,.workspace-brand{color:#f3effb!important}
        .brand-caption,.eyebrow,.hero-subtitle,.fine-print,.home-footnote{color:#bdb2d0!important}
        .hero-kicker{color:#d1c4e7!important;background:#251d31!important;border-color:#443653!important}
        .workspace-topbar,.home-footnote{background:rgba(34,28,45,.88)!important;border-color:#40344f!important;color:#eee7fa!important}
        .workspace-brand span,.workspace-status{color:#e8def5!important}
        .workspace-status{background:#292033!important;border-color:#4b3b5b!important}
        .workspace-status-dot{background:#50d6a0}
        .stApp [data-testid="stMarkdownContainer"],.stApp [data-testid="stMarkdownContainer"] p,.stApp [data-testid="stMarkdownContainer"] li,.stApp label,.stApp .stCaption{color:#e9e1f5}
        .stButton>button, [data-testid="stSidebar"] .stButton>button{background:#2a2235!important;color:#f3effb!important;border:1px solid #493957!important;box-shadow:0 5px 15px rgba(0,0,0,.2)!important}
        .stButton>button:hover,[data-testid="stSidebar"] .stButton>button:hover{background:#362943!important;color:#fff!important;border-color:#9878dd!important}
        .stButton>button[kind="primary"]{background:linear-gradient(105deg,#7650e8,#a64dd1 55%,#d855a7)!important;color:#fff!important;border:0!important}
        [data-testid="stMain"] .stButton>button:not([kind="primary"]){background:#2a2235!important;color:#f3effb!important;border:1px solid #493957!important}
        /* The fixed bottom chat area and its wrappers must stay transparent in dark mode. */
        [data-testid="stBottom"],[data-testid="stBottom"]>div,[data-testid="stBottomBlockContainer"],[data-testid="stChatInputContainer"],.stChatInputContainer{background:rgba(21,17,28,.97)!important;background-color:rgba(21,17,28,.97)!important}
        [data-testid="stChatInput"],[data-testid="stChatInput"]>div{background:#251e30!important;background-color:#251e30!important;border:1px solid #4a3b5c!important;border-radius:18px!important;box-shadow:0 10px 30px rgba(0,0,0,.3)!important}
        [data-testid="stChatInput"] textarea,[data-testid="stChatInput"] textarea::placeholder{color:#f3effb!important;-webkit-text-fill-color:#f3effb!important}
        [data-testid="stChatInput"] textarea::placeholder{color:#a99dbb!important;-webkit-text-fill-color:#a99dbb!important;opacity:1!important}
        [data-testid="stChatInput"] button{background:#3a3048!important;color:#f5efff!important;border:1px solid #51415f!important}
        [data-testid="stChatMessage"]{background:rgba(37,30,48,.96)!important;border:1px solid #40344f!important;border-radius:18px;color:#eee7fa!important;box-shadow:0 5px 16px rgba(0,0,0,.15)!important}
        [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"],[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] p,[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] li{color:#eee7fa!important}
        [data-testid="stTextInput"] input,[data-testid="stTextArea"] textarea,[data-testid="stNumberInput"] input{background:#251e30!important;color:#f3effb!important;-webkit-text-fill-color:#f3effb!important;border:1px solid #4a3b5c!important}
        [data-testid="stTextInput"] input::placeholder,[data-testid="stTextArea"] textarea::placeholder{color:#a99dbb!important;-webkit-text-fill-color:#a99dbb!important}
        [data-testid="stSelectbox"] div[data-baseweb="select"]>div{background:#251e30!important;color:#f3effb!important;border-color:#4a3b5c!important}
        [data-testid="stSelectbox"] [data-baseweb="select"] *{color:#f3effb!important}
        [data-baseweb="popover"],[data-baseweb="menu"],[role="listbox"]{background:#251e30!important;color:#f3effb!important}
        [role="option"]{background:#251e30!important;color:#f3effb!important}
        [data-testid="stExpander"]{background:#211b2b!important;border-color:#40354f!important}
        [data-testid="stExpander"] summary,[data-testid="stExpander"] p{color:#eee7fa!important}
        [data-testid="stAlert"]{background:#292033!important;color:#f3effb!important;border-color:#514060!important}
        [data-testid="stDialog"] [role="dialog"]{background:rgba(30,24,39,.99)!important;border-color:#40354f!important;color:#f3effb!important}
        [data-testid="stDialog"] [data-testid="stDialogHeader"]{background:transparent!important}
        [data-testid="stDialog"] [data-testid="stTextInput"] label{color:#e9e1f5!important}
        .welcome-title{color:#f2edf9!important}
        .welcome-copy,.welcome-helper,.welcome-link{color:#c2b6d2!important}
        .welcome-features span{color:#e9dffc!important;background:#30233d!important;border-color:#554067!important}
        .welcome-robot-wrap{background:linear-gradient(145deg,rgba(89,66,126,.7),rgba(89,47,76,.6))}
        [data-testid="stDialog"] [data-testid="stTextInput"] input{background:#211b2b!important;color:#f2edf9!important;border-color:#40354f!important}
        /* Keep code blocks and inline code readable against the dark surfaces. */
        .stApp pre,.stApp code{background:#211b2b!important;color:#e8dcff!important;border-color:#40354f!important}
        .stApp table th,.stApp table td{border-color:#40354f!important;color:#eee7fa!important}
        .stApp a{color:#c0a7ff!important}

        /* FINAL DARK-THEME OVERRIDES — stronger selectors for Streamlit/BaseWeb widgets */
        @keyframes nexoraOrbGlow{
          0%,100%{filter:drop-shadow(0 10px 18px rgba(128,87,245,.24));}
          50%{filter:drop-shadow(0 15px 30px rgba(189,88,231,.48));}
        }
        @keyframes nexoraHaloPulse{
          0%,100%{opacity:.38;transform:scale(.9)}
          50%{opacity:.9;transform:scale(1.13)}
        }
        @keyframes nexoraOrbitSpin{from{transform:rotate(0deg)}to{transform:rotate(360deg)}}
        .orb{animation:orbFloat 3.8s ease-in-out infinite,nexoraOrbGlow 3.4s ease-in-out infinite!important}
        .orb-halo{background:radial-gradient(circle,rgba(159,112,255,.46),rgba(237,99,187,.13) 56%,transparent 72%)!important;animation:nexoraHaloPulse 3.4s ease-in-out infinite!important}
        .orbit{border-color:rgba(174,143,255,.52)!important;animation:nexoraOrbitSpin 14s linear infinite!important}
        .orbit:after{background:#15111c!important;color:#d2baff!important}

        /* Fix the bright white theme-toggle button and ordinary buttons. */
        [data-testid="stButton"]>button,
        [data-testid="stButton"] button[kind="secondary"],
        .stApp button[kind="secondary"]{
          background:#2a2235!important;background-color:#2a2235!important;
          color:#f3effb!important;-webkit-text-fill-color:#f3effb!important;
          border:1px solid #51405f!important;
        }
        [data-testid="stButton"]>button:hover,
        [data-testid="stButton"] button[kind="secondary"]:hover,
        .stApp button[kind="secondary"]:hover{
          background:#3a2c49!important;background-color:#3a2c49!important;
          color:#fff!important;-webkit-text-fill-color:#fff!important;border-color:#a58aff!important;
        }
        [data-testid="stButton"] button[kind="primary"]{
          background:linear-gradient(105deg,#7650e8,#a64dd1 55%,#d855a7)!important;
          color:#fff!important;-webkit-text-fill-color:#fff!important;border:0!important;
        }

        /* Sidebar connection status card must not stay light in Night Mode. */
        .connection-pill{
          background:linear-gradient(135deg,#292033,#241c2f)!important;
          background-color:#292033!important;color:#eee7fa!important;
          border:1px solid #493957!important;box-shadow:0 8px 22px rgba(0,0,0,.18)!important;
        }
        .connection-pill *{color:#eee7fa!important}
        .connection-pill .status-dot{background:#50d6a0!important}

        /* Force model selector, selected value, dropdown menu and options into dark colors. */
        [data-testid="stSelectbox"] [data-baseweb="select"]>div,
        [data-testid="stSelectbox"] div[data-baseweb="select"]>div,
        [data-testid="stSelectbox"] [role="combobox"]{
          background:#251e30!important;background-color:#251e30!important;
          color:#f3effb!important;border:1px solid #51405f!important;box-shadow:none!important;
        }
        [data-testid="stSelectbox"] [data-baseweb="select"] *,
        [data-testid="stSelectbox"] [role="combobox"] *{
          color:#f3effb!important;fill:#c9b8e5!important;
        }
        [data-baseweb="popover"],[data-baseweb="menu"],[role="listbox"],ul[role="listbox"]{
          background:#251e30!important;background-color:#251e30!important;
          border:1px solid #51405f!important;color:#f3effb!important;
        }
        [data-baseweb="popover"] *,[data-baseweb="menu"] *,[role="listbox"] *,[role="option"]{
          background-color:transparent!important;color:#f3effb!important;
        }
        [role="option"]:hover,[aria-selected="true"]{background:#3a2c49!important;color:#fff!important}

        /* Ensure sidebar labels and helper copy remain readable. */
        [data-testid="stSidebar"] .connection-pill,
        [data-testid="stSidebar"] .connection-pill *,
        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
        [data-testid="stSidebar"] [data-testid="stCaptionContainer"]{color:#c9bfd8!important}
        [data-testid="stSidebar"] .connection-pill{color:#eee7fa!important}
        [data-testid="stSidebar"] [data-testid="stSelectbox"] label{color:#d8cde8!important}
        [data-testid="stSidebar"] [data-testid="stTextInput"] input{
          background:#251e30!important;color:#f3effb!important;-webkit-text-fill-color:#f3effb!important;border:1px solid #51405f!important;
        }
        [data-testid="stSidebar"] [data-testid="stTextInput"] input::placeholder{
          color:#b0a3c5!important;-webkit-text-fill-color:#b0a3c5!important;opacity:1!important;
        }
        [data-testid="stSidebar"] [data-testid="stToggle"] label,
        [data-testid="stSidebar"] [data-testid="stToggle"] label *{color:#e9e1f5!important}
        [data-testid="stSidebar"] [data-testid="stCaptionContainer"] p{color:#bdb2d0!important}

        @media(prefers-reduced-motion:reduce){.orb,.orb-halo,.orbit{animation:none!important}}
        </style>
        """,
        unsafe_allow_html=True,
    )

# Install theme-aware, high-contrast component styles once per render.
# These selectors intentionally target Streamlit's widget wrappers (not just nested HTML).
if st.session_state.get("dark_mode", False):
    st.markdown(
        """
        <style>
        :root { color-scheme: dark; }
        html, body, .stApp, [data-testid="stAppViewContainer"] {
            background: #14101b !important; color: #f4effb !important;
        }
        [data-testid="stMain"], [data-testid="stMainBlockContainer"],
        [data-testid="stBottom"], [data-testid="stBottomBlockContainer"] {
            background: transparent !important; color: #f4effb !important;
        }
        [data-testid="stHeader"] { background: rgba(20,16,27,.94) !important; }
        [data-testid="stSidebar"], [data-testid="stSidebar"] > div:first-child {
            background: linear-gradient(155deg,#1b1524 0%,#21172a 55%,#1a1422 100%) !important;
            border-right: 1px solid #40314f !important;
        }
        [data-testid="stSidebar"] .eyebrow { color:#c3b4d8 !important; }
        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
        [data-testid="stSidebar"] [data-testid="stCaptionContainer"] p { color:#bfb3ce !important; }
        .brand-name,.hero h1,.section-heading,.workspace-brand { color:#f7f1ff !important; }
        .hero-kicker { background:#281e35 !important; color:#d8c8ee !important; border:1px solid #4c3a60 !important; }
        .hero-subtitle,.brand-caption,.fine-print,.home-footnote { color:#c0b4cf !important; }
        .workspace-topbar,.home-footnote {
            background:rgba(36,27,47,.9) !important; border-color:#453650 !important; color:#f0e9fb !important;
        }
        .workspace-brand,.workspace-brand span,.workspace-status { color:#eee5fc !important; }
        .workspace-status { background:#2a2035 !important; border-color:#50405f !important; }
        .orbit { border-color:rgba(193,158,255,.66) !important; animation:orbitSpin 13s linear infinite !important; }
        .orb-halo { background:radial-gradient(circle,rgba(164,119,255,.53),rgba(236,99,187,.17) 56%,transparent 73%) !important; animation:glowPulse 3s ease-in-out infinite !important; }
        .orb { animation:orbFloat 3.8s ease-in-out infinite,glowPulse 3s ease-in-out infinite !important; filter:drop-shadow(0 12px 24px rgba(143,89,255,.23)); }
        .orbit:after { background:#14101b !important; color:#d9c4ff !important; }
        [data-testid="stButton"] > button,
        [data-testid="stSidebar"] [data-testid="stButton"] > button,
        .stApp button[kind="secondary"] {
            background:#2b2137 !important; background-color:#2b2137 !important;
            color:#f5eeff !important; -webkit-text-fill-color:#f5eeff !important;
            border:1px solid #574267 !important; box-shadow:0 7px 18px rgba(0,0,0,.17) !important;
        }
        [data-testid="stButton"] > button:hover {
            background:#3b2a4d !important; background-color:#3b2a4d !important;
            color:#fff !important; -webkit-text-fill-color:#fff !important;
            border-color:#a58aff !important; transform:translateY(-1px);
        }
        [data-testid="stButton"] > button[kind="primary"],
        [data-testid="stFormSubmitButton"] > button {
            background:linear-gradient(110deg,#7650ed,#a64dd5 55%,#e85fae) !important;
            background-color:#8c55e8 !important; color:#fff !important;
            -webkit-text-fill-color:#fff !important; border:0 !important;
        }
        [data-testid="stBottom"],[data-testid="stBottom"] > div,
        [data-testid="stBottomBlockContainer"],[data-testid="stChatInputContainer"] {
            background:rgba(20,16,27,.98) !important;
        }
        [data-testid="stChatInput"],[data-testid="stChatInput"] > div {
            background:#261d32 !important; background-color:#261d32 !important;
            border:1px solid #584269 !important; border-radius:19px !important;
            box-shadow:0 12px 32px rgba(0,0,0,.32) !important;
        }
        [data-testid="stChatInput"] textarea {
            color:#f7f1ff !important; -webkit-text-fill-color:#f7f1ff !important;
            caret-color:#d8c4ff !important;
        }
        [data-testid="stChatInput"] textarea::placeholder {
            color:#b8a9cb !important; -webkit-text-fill-color:#b8a9cb !important; opacity:1 !important;
        }
        [data-testid="stChatInput"] button {
            color:#fff !important; background:#463258 !important;
            border:1px solid #624778 !important;
        }
        [data-testid="stChatMessage"] {
            background:rgba(39,29,51,.96) !important; border:1px solid #493755 !important;
            border-radius:19px !important; color:#f1e9fc !important;
            box-shadow:0 8px 24px rgba(0,0,0,.15) !important;
        }
        [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"],
        [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] p,
        [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] li { color:#f1e9fc !important; }
        [data-testid="stTextInput"] input,[data-testid="stTextArea"] textarea,
        [data-testid="stNumberInput"] input {
            background:#261d32 !important; background-color:#261d32 !important;
            color:#f5eeff !important; -webkit-text-fill-color:#f5eeff !important;
            border:1px solid #574267 !important; border-radius:12px !important;
        }
        [data-testid="stTextInput"] input::placeholder,[data-testid="stTextArea"] textarea::placeholder {
            color:#b8a9cb !important; -webkit-text-fill-color:#b8a9cb !important; opacity:1 !important;
        }
        [data-testid="stSelectbox"] [data-baseweb="select"] > div,
        [data-testid="stSelectbox"] [role="combobox"] {
            background:#261d32 !important; background-color:#261d32 !important;
            color:#f5eeff !important; border-color:#574267 !important;
        }
        [data-testid="stSelectbox"] [data-baseweb="select"] * { color:#f5eeff !important; fill:#d5c3ed !important; }
        [data-baseweb="popover"],[data-baseweb="menu"],[role="listbox"] {
            background:#261d32 !important; background-color:#261d32 !important;
            color:#f5eeff !important; border:1px solid #574267 !important;
        }
        [role="option"] { color:#f5eeff !important; }
        [role="option"]:hover,[role="option"][aria-selected="true"] { background:#423052 !important; }
        [data-testid="stToggle"] label,[data-testid="stToggle"] label * { color:#eee5fc !important; }
        [data-testid="stExpander"] { background:#21192b !important; border-color:#493755 !important; border-radius:15px !important; }
        [data-testid="stExpander"] summary,[data-testid="stExpander"] p { color:#f0e8fb !important; }
        [data-testid="stAlert"] { background:#2b2036 !important; color:#f6edff !important; border-color:#574267 !important; }
        .connection-pill {
            background:linear-gradient(135deg,#2b2138,#241b30) !important;
            background-color:#2b2138 !important; border:1px solid #544064 !important;
            color:#f5efff !important; box-shadow:0 8px 23px rgba(0,0,0,.2) !important;
        }
        .connection-pill * { color:#f0e6ff !important; }
        .connection-pill .status-dot { background:#4cdda0 !important; }
        [data-testid="stDialog"] [role="dialog"] {
            background:rgba(29,22,39,.99) !important; border:1px solid #564169 !important;
            color:#f4edff !important; box-shadow:0 30px 100px rgba(0,0,0,.55) !important;
        }
        [data-testid="stDialog"] [data-testid="stDialogHeader"] { background:transparent !important; }
        [data-testid="stDialog"] [data-testid="stTextInput"] label { color:#eee5fc !important; }
        [data-testid="stDialog"] [data-testid="stTextInput"] input {
            background:#261d32 !important; color:#f7f1ff !important;
            -webkit-text-fill-color:#f7f1ff !important; border-color:#574267 !important;
        }
        .welcome-title { color:#f7f1ff !important; }
        .welcome-copy,.welcome-helper,.welcome-link { color:#c6b8d8 !important; }
        .welcome-features span { color:#eadcff !important; background:#332440 !important; border-color:#604670 !important; }
        .welcome-robot-wrap { background:linear-gradient(145deg,#3a2b50,#38233e) !important; box-shadow:0 15px 38px rgba(0,0,0,.28),inset 0 1px 0 rgba(255,255,255,.13) !important; }
        .stApp pre,.stApp code { background:#21182c !important; color:#e9d9ff !important; border-color:#4b385b !important; }
        .stApp table th,.stApp table td { border-color:#493755 !important; color:#f0e8fb !important; }
        .stApp a { color:#c7a8ff !important; }
        @media(prefers-reduced-motion:reduce){.orb,.orb-halo,.orbit,.welcome-robot{animation:none!important}}
        </style>
        """,
        unsafe_allow_html=True,
    )


# -------------------- SESSION STATE --------------------
defaults = {
    "chats": {},
    "active_chat": None,
    "system_prompt": DEFAULT_SYSTEM_PROMPT,
    "selected_model": DEFAULT_MODEL,
    "response_style": "Balanced",
    "api_key_session": "",
    "show_settings": False,
    "key_prompt_seen": False,
    "pending_prompt": "",
    "web_search_enabled": True,
    "dark_mode": False,
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value



# Final cohesive visual layer: centralized palette and responsive 3D treatment.
# Loaded after session defaults so the active theme is known on every Streamlit rerun.
_theme = "dark" if st.session_state.get("dark_mode", False) else "light"
_palette = {
    "light": {
        "bg": "#fbf9f7", "surface": "rgba(255,255,255,.88)", "surface_solid": "#ffffff",
        "ink": "#211a32", "muted": "#81778f", "line": "#e9e0f1",
        "control": "#ffffff", "control_text": "#30263f", "shadow": "rgba(55,35,79,.09)",
        "orb_edge": "rgba(255,255,255,.9)", "orb_floor": "rgba(82,57,123,.16)",
        "dialog": "rgba(255,255,255,.97)", "link": "#7650e8",
    },
    "dark": {
        "bg": "#14101b", "surface": "rgba(36,27,47,.94)", "surface_solid": "#241b30",
        "ink": "#f5efff", "muted": "#c0b4d0", "line": "#493755",
        "control": "#261d32", "control_text": "#f5efff", "shadow": "rgba(0,0,0,.25)",
        "orb_edge": "rgba(255,255,255,.34)", "orb_floor": "rgba(0,0,0,.34)",
        "dialog": "rgba(29,22,39,.99)", "link": "#c7a8ff",
    },
}[_theme]
_premium_css = """
<style>
:root {
  color-scheme: __SCHEME__;
  --nx-bg: __BG__;
  --nx-surface: __SURFACE__;
  --nx-surface-solid: __SURFACE_SOLID__;
  --nx-ink: __INK__;
  --nx-muted: __MUTED__;
  --nx-line: __LINE__;
  --nx-control: __CONTROL__;
  --nx-control-text: __CONTROL_TEXT__;
  --nx-shadow: __SHADOW__;
  --nx-dialog: __DIALOG__;
  --nx-link: __LINK__;
}
@keyframes nx-orb-float {
  0%,100% { transform: translateY(0) rotateX(9deg) rotateY(-10deg); }
  50% { transform: translateY(-7px) rotateX(12deg) rotateY(-3deg); }
}
@keyframes nx-orbit-turn { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
@keyframes nx-spark-twinkle { 0%,100% { opacity:.58; transform:scale(.92); } 50% { opacity:1; transform:scale(1.08); } }
.stApp {
  color:var(--nx-ink)!important;
  background:__BG__!important;
  animation:none!important;
}
[data-testid="stAppViewContainer"], [data-testid="stMain"], [data-testid="stMainBlockContainer"] {
  background:transparent!important; color:var(--nx-ink)!important;
}
[data-testid="stHeader"] { background:__HEADER__!important; }
[data-testid="stMainBlockContainer"] {
  width:100%!important; max-width:1280px!important;
  padding:1.25rem clamp(1rem,3vw,2.6rem) 7rem!important;
}
[data-testid="stSidebar"], [data-testid="stSidebar"]>div:first-child {
  background:__SIDEBAR__!important; border-right:1px solid var(--nx-line)!important;
}
.brand-name,.hero h1,.section-heading,.workspace-brand { color:var(--nx-ink)!important; }
.brand-caption,.eyebrow,.hero-subtitle,.fine-print,.home-footnote { color:var(--nx-muted)!important; }
.workspace-topbar {
  background:var(--nx-surface)!important; border:1px solid var(--nx-line)!important;
  box-shadow:0 12px 34px var(--nx-shadow),inset 0 1px 0 __TOP_HIGHLIGHT__!important;
  backdrop-filter:blur(20px); border-radius:20px!important;
}
.workspace-status { background:var(--nx-surface-solid)!important;color:var(--nx-muted)!important;border-color:var(--nx-line)!important; }
.hero {
  width:100%!important; max-width:1000px!important; margin:clamp(1.4rem,4vh,3.4rem) auto 1.3rem!important;
  padding:8px clamp(10px,2.8vw,32px) 10px!important; box-sizing:border-box!important;
  overflow:visible!important; text-align:center;
}
.orb-wrap {
  height:145px!important; width:180px!important; max-width:100%;
  margin:0 auto 10px!important; display:flex!important; align-items:center!important; justify-content:center!important;
  position:relative!important; isolation:isolate!important; overflow:visible!important; perspective:800px!important;
}
.orb-floor-shadow {
  position:absolute; z-index:0; left:50%; bottom:17px; width:54px; height:10px;
  transform:translateX(-50%) rotateX(65deg);
  border-radius:50%; background:__ORB_FLOOR__!important; filter:blur(5px);
}
.orb {
  position:relative!important; z-index:2!important; width:82px!important; height:82px!important;
  min-width:82px!important; border-radius:27px!important; display:flex!important; align-items:center!important; justify-content:center!important;
  font-size:39px!important; line-height:1!important; color:#fff!important;
  background:
    radial-gradient(ellipse at 27% 15%,rgba(255,255,255,.8),transparent 25%),
    linear-gradient(148deg,#d9c6ff 0%,#a17aff 23%,#8057f5 52%,#7044d7 72%,#e56bbf 100%)!important;
  border:1px solid __ORB_EDGE__!important;
  box-shadow:
    0 18px 28px rgba(91,58,158,.23),
    0 4px 8px rgba(53,31,95,.14),
    inset 0 2px 3px rgba(255,255,255,.85),
    inset 0 -9px 14px rgba(55,25,123,.24),
    inset 2px 0 5px rgba(255,255,255,.16)!important;
  transform-style:preserve-3d!important;
  animation:nx-orb-float 5.4s ease-in-out infinite!important;
}
.orb:before {
  content:""; position:absolute; inset:5px 7px auto; height:26px; border-radius:22px 22px 50% 50%;
  background:linear-gradient(180deg,rgba(255,255,255,.54),rgba(255,255,255,.04) 82%)!important;
  filter:blur(1.2px); pointer-events:none;
}
.orb:after {
  content:""; position:absolute; inset:0; border-radius:inherit; pointer-events:none;
  box-shadow:inset 0 0 0 1px rgba(255,255,255,.17),inset 0 -2px 3px rgba(38,18,84,.22);
}
.orbit {
  position:absolute!important; z-index:1!important; width:108px!important; height:108px!important;
  border:1px solid __ORBIT_LINE__!important; border-radius:34px!important;
  transform:rotate(18deg) rotateX(12deg)!important; animation:none!important;
  box-shadow:0 0 0 7px __ORBIT_OUTER__!important;
}
.orbit:after {
  content:"✦"; position:absolute; top:4px; right:5px; font-size:13px; line-height:1;
  color:#a77aff!important; background:var(--nx-bg)!important; padding:1px 3px;
  box-shadow:none!important;
}
.orb-spark { position:absolute; z-index:3; color:#bd9cff; font-size:13px; pointer-events:none; animation:nx-spark-twinkle 3.8s ease-in-out infinite; }
.orb-spark-a { top:30px; right:35px; }
.orb-spark-b { bottom:33px; left:37px; color:#ed8acb; animation-delay:1.2s; }
.hero-kicker {
  display:inline-flex!important; align-items:center; justify-content:center; gap:7px;
  color:var(--nx-muted)!important; background:var(--nx-surface)!important;
  border:1px solid var(--nx-line)!important; border-radius:999px!important;
  padding:7px 12px!important; margin:0 auto 17px!important; font-size:10px!important; letter-spacing:1.25px!important;
}
.hero h1 {
  display:block!important; width:100%!important; max-width:100%!important; box-sizing:border-box!important;
  margin:0 auto 16px!important; padding:0 .08em!important;
  color:var(--nx-ink)!important; font-family:'Manrope',sans-serif!important;
  font-size:clamp(30px,4.05vw,55px)!important; line-height:1.18!important;
  letter-spacing:clamp(-1.8px,-.1vw,-.45px)!important; font-weight:800!important;
  white-space:normal!important; overflow:visible!important; overflow-wrap:normal!important;
  word-break:normal!important; text-wrap:balance;
}
.gradient-word {
  display:inline!important; white-space:normal!important; padding-right:.04em!important;
  background:linear-gradient(100deg,#8057f5 0%,#bd58e7 52%,#ed63bb 100%)!important;
  -webkit-background-clip:text!important; background-clip:text!important; color:transparent!important;
  animation:none!important; font-style:italic!important;
}
.hero-subtitle { color:var(--nx-muted)!important; max-width:610px!important; padding:0 8px!important; margin:0 auto!important; font-size:14px!important; line-height:1.8!important; }
.hero-trust-row { display:flex!important; justify-content:center!important; flex-wrap:wrap!important; gap:8px!important; margin:18px auto 0!important; }
.hero-trust-row span {
  color:var(--nx-muted)!important; background:var(--nx-surface)!important;
  border:1px solid var(--nx-line)!important; border-radius:999px!important;
  padding:7px 11px!important; font:600 10px 'DM Sans',sans-serif!important;
  box-shadow:0 5px 16px var(--nx-shadow)!important;
}
.section-heading { max-width:860px!important; margin:25px auto 13px!important; font:800 15px 'Manrope',sans-serif!important; }
.stButton>button {
  color:var(--nx-control-text)!important; background:var(--nx-surface)!important;
  border:1px solid var(--nx-line)!important; border-radius:15px!important; min-height:49px!important;
  box-shadow:0 7px 20px var(--nx-shadow),inset 0 1px 0 __TOP_HIGHLIGHT__!important;
  transition:transform .2s ease,box-shadow .2s ease,border-color .2s ease!important;
}
.stButton>button:hover { transform:translateY(-2px)!important; border-color:#b7a0f6!important; box-shadow:0 12px 25px var(--nx-shadow)!important; }
.stButton>button[kind="primary"],[data-testid="stFormSubmitButton"]>button {
  color:#fff!important; -webkit-text-fill-color:#fff!important; border:0!important;
  background:linear-gradient(110deg,#7650ed,#a64dd5 56%,#e85fae)!important;
  box-shadow:0 10px 23px rgba(128,87,245,.24),inset 0 1px 0 rgba(255,255,255,.27)!important;
}
[data-testid="stChatInput"],[data-testid="stChatInput"]>div {
  background:var(--nx-control)!important; border:1px solid var(--nx-line)!important;
  border-radius:18px!important; box-shadow:0 12px 32px var(--nx-shadow)!important;
}
[data-testid="stChatInput"] textarea { color:var(--nx-control-text)!important;-webkit-text-fill-color:var(--nx-control-text)!important; }
[data-testid="stChatInput"] textarea::placeholder { color:var(--nx-muted)!important;-webkit-text-fill-color:var(--nx-muted)!important;opacity:1!important; }
[data-testid="stChatMessage"] {
  max-width:1000px!important; margin-left:auto!important; margin-right:auto!important;
  color:var(--nx-ink)!important; background:var(--nx-surface)!important;
  border:1px solid var(--nx-line)!important; border-radius:18px!important;
  box-shadow:0 8px 22px var(--nx-shadow)!important;
}
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"],
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] p,
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] li { color:var(--nx-ink)!important; line-height:1.75!important; }
[data-testid="stTextInput"] input,[data-testid="stTextArea"] textarea,
[data-testid="stSelectbox"] [data-baseweb="select"]>div {
  background:var(--nx-control)!important; color:var(--nx-control-text)!important;
  -webkit-text-fill-color:var(--nx-control-text)!important; border-color:var(--nx-line)!important; border-radius:12px!important;
}
[data-testid="stTextInput"] input::placeholder,[data-testid="stTextArea"] textarea::placeholder {
  color:var(--nx-muted)!important;-webkit-text-fill-color:var(--nx-muted)!important;opacity:1!important;
}
[data-baseweb="popover"],[data-baseweb="menu"],[role="listbox"] { background:var(--nx-control)!important;color:var(--nx-control-text)!important; }
[role="option"] { color:var(--nx-control-text)!important; }
[data-testid="stDialog"] [role="dialog"] {
  width:min(94vw,500px)!important; max-width:500px!important; max-height:92vh!important; overflow-y:auto!important;
  border-radius:28px!important; border:1px solid __DIALOG_EDGE__!important;
  background:var(--nx-dialog)!important; color:var(--nx-ink)!important;
  box-shadow:0 28px 90px var(--nx-shadow),inset 0 1px 0 __TOP_HIGHLIGHT__!important;
  backdrop-filter:blur(24px)!important;
}
[data-testid="stDialog"] [data-testid="stDialogHeader"] { background:transparent!important;border:0!important; }
.welcome-card { text-align:center!important; padding:4px 8px 9px!important; }
.welcome-robot-wrap {
  width:96px!important;height:96px!important;margin:4px auto 16px!important;position:relative!important;
  display:flex!important;align-items:center!important;justify-content:center!important;border-radius:29px!important;
  background:radial-gradient(circle at 28% 18%,rgba(255,255,255,.85),transparent 38%),linear-gradient(145deg,#e5d7ff,#c9aaff 48%,#f5c6e7)!important;
  border:1px solid __DIALOG_EDGE__!important;
  box-shadow:0 18px 38px rgba(128,87,245,.18),inset 0 2px 3px rgba(255,255,255,.85),inset 0 -7px 12px rgba(100,53,150,.09)!important;
  transform:perspective(420px) rotateX(5deg)!important;
}
.welcome-robot { display:inline-block!important; filter:drop-shadow(0 6px 7px rgba(86,54,133,.18))!important; animation:nx-orb-float 4.6s ease-in-out infinite!important; }
.welcome-title { color:var(--nx-ink)!important;font-size:clamp(25px,5vw,30px)!important;line-height:1.18!important; }
.welcome-copy,.welcome-helper,.welcome-link { color:var(--nx-muted)!important; }
.welcome-features span { color:var(--nx-control-text)!important;background:var(--nx-surface-solid)!important;border-color:var(--nx-line)!important; }
[data-testid="stDialog"] [data-testid="stTextInput"] label { color:var(--nx-ink)!important; }
[data-testid="stDialog"] [data-testid="stTextInput"] input { background:var(--nx-control)!important;color:var(--nx-control-text)!important;-webkit-text-fill-color:var(--nx-control-text)!important;border-color:var(--nx-line)!important; }
.connection-pill { background:var(--nx-surface)!important;color:var(--nx-ink)!important;border-color:var(--nx-line)!important;box-shadow:0 7px 20px var(--nx-shadow)!important; }
.connection-pill * { color:var(--nx-ink)!important; }
.home-footnote { color:var(--nx-muted)!important;background:var(--nx-surface)!important;border-color:var(--nx-line)!important; }
.stApp pre,.stApp code { background:__CODE_BG__!important;color:var(--nx-ink)!important;border-color:var(--nx-line)!important; }
.stApp table th,.stApp table td { border-color:var(--nx-line)!important;color:var(--nx-ink)!important; }
.stApp a { color:var(--nx-link)!important; }

/* Premium creator signature and dimensional onboarding icon. */
.welcome-robot-wrap {
  overflow:visible!important;
  transform:perspective(520px) rotateX(7deg) rotateY(-5deg)!important;
}
.welcome-robot {
  position:relative!important; width:62px!important;height:62px!important;
  display:flex!important;align-items:center!important;justify-content:center!important;
  border-radius:21px!important;color:#fff!important;font-size:34px!important;line-height:1!important;
  background:
    radial-gradient(ellipse at 28% 14%,rgba(255,255,255,.82),transparent 27%),
    linear-gradient(145deg,#d7c0ff 0%,#a27aff 28%,#8057f5 58%,#d85bb7 100%)!important;
  border:1px solid rgba(255,255,255,.72)!important;
  box-shadow:0 13px 24px rgba(103,66,183,.26),inset 0 2px 3px rgba(255,255,255,.8),inset 0 -7px 10px rgba(62,29,127,.2)!important;
  transform-style:preserve-3d!important;
}
.welcome-robot:before {
  content:"";position:absolute;inset:4px 6px auto;height:17px;border-radius:18px 18px 50% 50%;
  background:linear-gradient(180deg,rgba(255,255,255,.6),rgba(255,255,255,.04))!important;pointer-events:none;
}
.welcome-credit,.creator-credit-sidebar,.creator-credit-main {
  text-align:center!important;font-size:10px!important;line-height:1.6!important;
  color:var(--nx-muted)!important;letter-spacing:.1px;
}
.welcome-credit { margin:0 auto 10px!important; }
.welcome-credit strong,.creator-credit-sidebar strong,.creator-credit-main strong { color:var(--nx-link)!important;font-weight:800!important; }
.welcome-credit span,.creator-credit-main span { display:block!important;opacity:.86; }
.creator-credit-sidebar { margin:6px auto 12px!important;padding-top:9px!important;border-top:1px solid var(--nx-line)!important;font-size:9px!important; }
.creator-credit-main { margin:10px auto 20px!important;font-size:10px!important; }
@media(max-width:520px) {
  .welcome-credit { font-size:9.5px!important; }
  .creator-credit-main { margin-bottom:14px!important; }
}

@media(max-width:900px) {
  [data-testid="stMainBlockContainer"] { padding:1rem 1rem 6rem!important; }
  .hero { margin-top:1.5rem!important; }
  .hero h1 { font-size:clamp(28px,5.2vw,43px)!important; letter-spacing:-.9px!important; }
  .orb-wrap { height:130px!important; }
}
@media(max-width:520px) {
  [data-testid="stMainBlockContainer"] { padding:.8rem .65rem 6rem!important; }
  .workspace-topbar { padding:9px 10px!important; gap:8px!important; }
  .workspace-brand { font-size:12px!important; }
  .workspace-status { font-size:9px!important; padding:6px 8px!important; }
  .hero { margin-top:1rem!important; padding:4px 5px 8px!important; }
  .hero h1 { font-size:clamp(25px,7vw,34px)!important; line-height:1.22!important; letter-spacing:-.55px!important; }
  .hero-subtitle { font-size:12.5px!important; line-height:1.7!important; }
  .orb-wrap { width:150px!important;height:115px!important; }
  .orb { width:72px!important;height:72px!important;min-width:72px!important;border-radius:24px!important;font-size:34px!important; }
  .orbit { width:96px!important;height:96px!important;border-radius:30px!important; }
  .orb-spark-a { right:25px!important;top:22px!important; }
  .orb-spark-b { left:25px!important;bottom:25px!important; }
  .hero-trust-row { gap:6px!important; }
  .hero-trust-row span { font-size:9px!important;padding:6px 8px!important; }
  [data-testid="stDialog"] [role="dialog"] { width:calc(100vw - 20px)!important;max-width:calc(100vw - 20px)!important;max-height:90vh!important; }
}
@media(prefers-reduced-motion:reduce) {
  .orb,.orbit,.orb-spark,.welcome-robot { animation:none!important;transition:none!important; }
}




/* NEXORA signature: a layered, glassy 3D emblem with restrained cinematic motion. */
@keyframes nx-emblem-drift {
  0%,100% { transform:translateY(0) rotateX(8deg) rotateY(-8deg) rotateZ(-2deg); }
  50% { transform:translateY(-8px) rotateX(13deg) rotateY(7deg) rotateZ(2deg); }
}
@keyframes nx-emblem-glow {
  0%,100% { opacity:.52; filter:blur(13px); }
  50% { opacity:.9; filter:blur(19px); }
}
@keyframes nx-ring-turn { from { transform:rotate(0deg) rotateX(64deg); } to { transform:rotate(360deg) rotateX(64deg); } }
.orb-wrap { perspective:1000px!important; transform-style:preserve-3d!important; }
.orb {
  border-radius:25px!important;
  background:
    radial-gradient(ellipse at 23% 13%,rgba(255,255,255,.95),transparent 19%),
    radial-gradient(ellipse at 76% 85%,rgba(236,103,197,.7),transparent 32%),
    linear-gradient(140deg,#e7d9ff 0%,#b9a0ff 17%,#8a61f7 42%,#693fd0 66%,#db63bc 100%)!important;
  animation:nx-emblem-drift 6.2s cubic-bezier(.42,0,.58,1) infinite!important;
  box-shadow:
    0 24px 35px rgba(83,54,146,.26),
    0 7px 12px rgba(54,30,97,.16),
    inset 0 3px 4px rgba(255,255,255,.88),
    inset -5px -10px 18px rgba(45,20,100,.22),
    inset 4px 0 10px rgba(255,255,255,.18)!important;
}
.orb:before { height:32px!important; filter:blur(1.8px)!important; }
.orb:after { box-shadow:inset 0 0 0 1px rgba(255,255,255,.23),inset 0 -3px 5px rgba(38,18,84,.25)!important; }
.orbit {
  border:1px solid rgba(173,143,255,.48)!important;
  box-shadow:0 0 0 6px rgba(153,119,241,.035),inset 0 0 18px rgba(153,119,241,.035)!important;
  animation:nx-ring-turn 28s linear infinite!important;
}
.orb-floor-shadow { width:65px!important;height:11px!important;filter:blur(7px)!important; }
.welcome-robot-wrap {
  perspective:800px!important;transform-style:preserve-3d!important;
  animation:nx-emblem-drift 7s ease-in-out infinite!important;
  box-shadow:0 21px 38px rgba(103,66,183,.22),inset 0 2px 3px rgba(255,255,255,.85),inset 0 -8px 13px rgba(100,53,150,.12)!important;
}
.welcome-robot { animation:nx-emblem-glow 4s ease-in-out infinite,nx-orb-float 5s ease-in-out infinite!important; }
.stButton>button { transform-style:preserve-3d!important; }
.stButton>button[kind="primary"] { background-image:linear-gradient(115deg,#7650ed 0%,#9b51e0 55%,#e45eb6 100%)!important; }
@media(prefers-reduced-motion:reduce) {
  .orb,.orbit,.welcome-robot-wrap,.welcome-robot { animation:none!important; }
}

/* Tactile controls and subtle cinematic motion for the welcome screen. */
@keyframes nx-login-arrive { from { opacity:0; transform:translateY(16px) scale(.975); } to { opacity:1; transform:translateY(0) scale(1); } }
@keyframes nx-login-orbit { from { transform:rotate(18deg) rotateX(12deg) rotateY(0deg); } to { transform:rotate(378deg) rotateX(12deg) rotateY(0deg); } }
@keyframes nx-login-glint { 0%,100% { opacity:.35; transform:translateX(-4px) scale(.92); } 50% { opacity:.95; transform:translateX(4px) scale(1.08); } }
[data-testid="stDialog"] [role="dialog"] { animation:nx-login-arrive .42s cubic-bezier(.2,.8,.2,1) both!important; }
[data-testid="stDialog"] .welcome-robot-wrap { animation:nx-login-arrive .6s .06s both!important; }
[data-testid="stDialog"] .welcome-robot { animation:nx-orb-float 4.2s ease-in-out infinite!important; }
[data-testid="stDialog"] .welcome-robot-wrap:after {
  content:"✦"; position:absolute; top:-7px; right:-8px; color:#d77be8; font-size:17px;
  text-shadow:0 0 15px rgba(182,124,255,.5); animation:nx-login-glint 3s ease-in-out infinite; pointer-events:none;
}
.orbit { animation:nx-login-orbit 32s linear infinite!important; transform-style:preserve-3d!important; }
.stButton>button, [data-testid="stFormSubmitButton"]>button {
  position:relative!important; overflow:hidden!important; transform:translateZ(0);
  transition:transform .22s cubic-bezier(.2,.8,.2,1),box-shadow .22s ease,border-color .22s ease,filter .22s ease!important;
}
.stButton>button:before, [data-testid="stFormSubmitButton"]>button:before {
  content:""; position:absolute; inset:0; border-radius:inherit; pointer-events:none;
  background:linear-gradient(115deg,rgba(255,255,255,.18),transparent 38%,rgba(255,255,255,.06) 65%,transparent);
  opacity:.55; transition:opacity .2s ease;
}
.stButton>button:active, [data-testid="stFormSubmitButton"]>button:active {
  transform:translateY(1px) scale(.985)!important; box-shadow:0 3px 8px var(--nx-shadow)!important;
}
.stButton>button[kind="primary"],[data-testid="stFormSubmitButton"]>button[kind="primary"] {
  box-shadow:0 10px 0 rgba(74,42,145,.13),0 15px 28px rgba(128,87,245,.22),inset 0 1px 0 rgba(255,255,255,.4)!important;
}
.stButton>button[kind="primary"]:hover,[data-testid="stFormSubmitButton"]>button[kind="primary"]:hover {
  filter:saturate(1.12) brightness(1.04)!important; transform:translateY(-2px)!important;
  box-shadow:0 12px 0 rgba(74,42,145,.10),0 20px 35px rgba(128,87,245,.29),inset 0 1px 0 rgba(255,255,255,.45)!important;
}
.edit-message-heading { color:var(--nx-ink)!important;font:800 15px 'Manrope',sans-serif!important;margin:10px 0 8px!important; }
[data-testid="stForm"] { background:var(--nx-surface)!important;border:1px solid var(--nx-line)!important;border-radius:18px!important;padding:12px!important;box-shadow:0 10px 28px var(--nx-shadow)!important; }
[data-testid="stTextArea"] textarea { background:var(--nx-control)!important;color:var(--nx-control-text)!important;-webkit-text-fill-color:var(--nx-control-text)!important;border-color:var(--nx-line)!important;border-radius:13px!important; }
@media (prefers-reduced-motion:reduce) {
  [data-testid="stDialog"] [role="dialog"],[data-testid="stDialog"] .welcome-robot-wrap,.orbit,.stButton>button { animation:none!important;transition:none!important; }
}

/* Mobile-first finishing pass: touch targets, safe areas, stacked header, and compact chat. */
@media (max-width: 640px) {
  [data-testid="stAppViewContainer"] { overflow-x: clip!important; }
  [data-testid="stMainBlockContainer"] {
    width:100%!important; max-width:100%!important;
    padding: .75rem .7rem calc(6.5rem + env(safe-area-inset-bottom))!important;
  }
  [data-testid="stHorizontalBlock"] {
    flex-wrap:wrap!important; gap:.65rem!important;
  }
  [data-testid="stHorizontalBlock"] > [data-testid="stColumn"] {
    flex:1 1 100%!important; width:100%!important; min-width:0!important;
  }
  [data-testid="stHorizontalBlock"]:has(.workspace-topbar) > [data-testid="stColumn"] {
    flex:1 1 100%!important; width:100%!important;
  }
  .workspace-topbar {
    width:100%!important; box-sizing:border-box!important;
    min-height:60px!important; margin:0!important; padding:10px 12px!important;
    border-radius:17px!important; gap:8px!important;
  }
  .workspace-brand { font-size:12px!important; gap:8px!important; }
  .workspace-mark { width:34px!important; height:34px!important; min-width:34px!important; }
  .workspace-status { font-size:9px!important; padding:6px 8px!important; white-space:nowrap!important; }
  .hero {
    max-width:100%!important; margin:1.1rem auto .8rem!important;
    padding:4px 3px 6px!important;
  }
  .orb-wrap { width:145px!important; height:108px!important; margin-bottom:6px!important; }
  .orb { width:68px!important; height:68px!important; min-width:68px!important; border-radius:22px!important; font-size:31px!important; }
  .orbit { width:91px!important; height:91px!important; border-radius:27px!important; }
  .orb-floor-shadow { bottom:11px!important; }
  .orb-spark-a { top:17px!important; right:24px!important; }
  .orb-spark-b { bottom:19px!important; left:22px!important; }
  .hero-kicker { font-size:8px!important; letter-spacing:.9px!important; padding:6px 9px!important; margin-bottom:12px!important; }
  .hero h1 {
    font-size:clamp(25px,7.4vw,36px)!important; line-height:1.18!important;
    letter-spacing:-.75px!important; padding:0 .04em!important; margin-bottom:12px!important;
    text-wrap:balance!important;
  }
  .hero-subtitle { max-width:35rem!important; font-size:12.5px!important; line-height:1.7!important; padding:0 7px!important; }
  .hero-trust-row { gap:6px!important; margin-top:13px!important; }
  .hero-trust-row span { font-size:9px!important; padding:6px 8px!important; }
  .section-heading { margin:19px 0 10px!important; font-size:13px!important; }
  .stButton>button {
    min-height:46px!important; width:100%!important; padding:10px 12px!important;
    border-radius:14px!important; font-size:12px!important; white-space:normal!important;
  }
  [data-testid="stChatMessage"] {
    padding:10px 11px!important; border-radius:16px!important; margin-bottom:10px!important;
  }
  [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] p,
  [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] li {
    font-size:14px!important; line-height:1.7!important; overflow-wrap:anywhere!important;
  }
  [data-testid="stChatMessage"] pre { max-width:100%!important; overflow-x:auto!important; }
  [data-testid="stChatMessage"] table { display:block!important; max-width:100%!important; overflow-x:auto!important; }
  [data-testid="stChatInputContainer"],[data-testid="stBottomBlockContainer"] {
    padding-left:.55rem!important; padding-right:.55rem!important;
    padding-bottom:calc(.45rem + env(safe-area-inset-bottom))!important;
  }
  [data-testid="stChatInput"],[data-testid="stChatInput"]>div {
    min-height:52px!important; border-radius:17px!important;
  }
  [data-testid="stChatInput"] textarea { font-size:16px!important; line-height:1.45!important; }
  [data-testid="stChatInput"] button { min-width:40px!important; min-height:40px!important; border-radius:12px!important; }
  [data-testid="stDialog"] [role="dialog"] {
    width:calc(100vw - 18px)!important; max-width:calc(100vw - 18px)!important;
    max-height:calc(100dvh - 20px - env(safe-area-inset-bottom))!important;
    padding:12px!important; border-radius:23px!important;
  }
  .welcome-card { padding:2px 1px 8px!important; }
  .welcome-robot-wrap { width:78px!important; height:78px!important; border-radius:24px!important; margin-bottom:12px!important; }
  .welcome-robot { width:54px!important; height:54px!important; border-radius:18px!important; font-size:30px!important; }
  .welcome-title { font-size:25px!important; }
  .welcome-copy { font-size:12px!important; margin-bottom:12px!important; }
  .welcome-features { gap:5px!important; flex-wrap:wrap!important; }
  .welcome-features span { font-size:9px!important; padding:6px 8px!important; }
  .home-footnote { font-size:10px!important; line-height:1.6!important; padding:10px!important; }
  .creator-credit-main { font-size:10px!important; margin-bottom:12px!important; }
}
@media (max-width: 360px) {
  [data-testid="stMainBlockContainer"] { padding-left:.5rem!important; padding-right:.5rem!important; }
  .workspace-status { max-width:118px!important; overflow:hidden!important; text-overflow:ellipsis!important; }
  .hero h1 { font-size:clamp(23px,7.1vw,27px)!important; letter-spacing:-.55px!important; }
  .hero-trust-row span { font-size:8px!important; padding:5px 6px!important; }
  .welcome-title { font-size:23px!important; }
}
@media (hover:none) and (pointer:coarse) {
  .stButton>button:hover { transform:none!important; }
  .stButton>button, [data-testid="stChatInput"] button, input, textarea, [role="combobox"] { touch-action:manipulation; }
}




/* Inspiration-led art direction: liquid-chrome core, deep indigo glass, electric violet and cyan. */
@keyframes nx-liquid-orb {
  0%,100% { transform:translateY(0) rotateX(5deg) rotateY(-8deg) rotateZ(-2deg); }
  50% { transform:translateY(-10px) rotateX(11deg) rotateY(9deg) rotateZ(3deg); }
}
@keyframes nx-liquid-sheen { 0% { transform:translateX(-130%) rotate(20deg); } 100% { transform:translateX(130%) rotate(20deg); } }
@keyframes nx-nebula-breathe { 0%,100% { opacity:.5; transform:scale(.96); } 50% { opacity:.9; transform:scale(1.04); } }
@keyframes nx-particle-float { 0%,100% { transform:translateY(0) translateX(0); } 50% { transform:translateY(-9px) translateX(4px); } }

.stApp {
  background:
    radial-gradient(ellipse at 52% 4%,rgba(102,65,207,.20),transparent 39%),
    radial-gradient(ellipse at 8% 45%,rgba(23,157,188,.08),transparent 28%),
    radial-gradient(ellipse at 93% 63%,rgba(215,59,170,.09),transparent 30%),
    __BG__!important;
  background-attachment:fixed!important;
}
.workspace-topbar {
  background:linear-gradient(125deg,rgba(39,29,63,.88),rgba(24,25,49,.82))!important;
  border-color:rgba(169,133,255,.25)!important;
  box-shadow:0 18px 46px rgba(15,8,35,.12),inset 0 1px 0 rgba(255,255,255,.12)!important;
}
.hero {
  max-width:1120px!important;
  border-radius:30px!important;
  border:1px solid rgba(164,127,255,.26)!important;
  background:
    radial-gradient(ellipse at 50% 18%,rgba(115,78,230,.18),transparent 42%),
    radial-gradient(ellipse at 78% 54%,rgba(17,172,193,.09),transparent 32%),
    linear-gradient(135deg,rgba(19,16,38,.97),rgba(29,18,51,.94) 52%,rgba(14,23,40,.97))!important;
  box-shadow:0 2px 0 rgba(255,255,255,.10),0 28px 75px rgba(12,7,29,.20),inset 0 1px 0 rgba(255,255,255,.13)!important;
}
.hero:before { border-color:rgba(186,153,255,.12)!important; }
.hero:after {
  height:2px!important;left:12%!important;right:12%!important;
  background:linear-gradient(90deg,transparent,#8d6bff 30%,#55e1e7 55%,#e96ad0 75%,transparent)!important;
  filter:blur(.3px);
}
.hero h1 { color:#f8f4ff!important;text-shadow:0 4px 30px rgba(148,101,255,.15)!important; }
.hero-subtitle { color:#c7bfdc!important; }
.gradient-word {
  background:linear-gradient(100deg,#a68bff 0%,#d56bf2 45%,#68e6ef 100%)!important;
  -webkit-background-clip:text!important;background-clip:text!important;color:transparent!important;
}
.hero-kicker {
  color:#d6caff!important;background:rgba(96,64,161,.20)!important;
  border-color:rgba(172,139,255,.30)!important;
}
.hero-trust-row span {
  color:#d4cce7!important;background:rgba(255,255,255,.045)!important;
  border-color:rgba(181,150,255,.22)!important;
  box-shadow:0 8px 22px rgba(0,0,0,.12),inset 0 1px 0 rgba(255,255,255,.08)!important;
}
.orb-wrap { width:230px!important;height:190px!important;perspective:1200px!important; }
.orb {
  width:142px!important;height:142px!important;min-width:142px!important;border-radius:50%!important;
  font-size:54px!important;color:#fff!important;overflow:hidden!important;
  background:
    radial-gradient(ellipse at 29% 18%,rgba(255,255,255,.98) 0%,rgba(255,255,255,.50) 5%,transparent 18%),
    radial-gradient(ellipse at 34% 28%,rgba(89,242,255,.92) 0%,rgba(89,242,255,.20) 15%,transparent 31%),
    radial-gradient(ellipse at 72% 68%,rgba(233,76,225,.95) 0%,rgba(233,76,225,.24) 20%,transparent 38%),
    radial-gradient(ellipse at 45% 76%,rgba(89,70,255,.95) 0%,transparent 42%),
    radial-gradient(ellipse at 55% 42%,#20153e 0%,#100e27 43%,#050712 70%,#8d7cff 84%,#e7dfff 91%,#28203f 100%)!important;
  border:1px solid rgba(255,255,255,.7)!important;
  box-shadow:0 28px 45px rgba(3,2,14,.44),0 0 35px rgba(126,83,255,.36),0 0 76px rgba(80,211,255,.12),
    inset 0 3px 6px rgba(255,255,255,.75),inset -12px -15px 25px rgba(3,3,17,.82),inset 8px 4px 15px rgba(255,255,255,.14)!important;
  animation:nx-liquid-orb 7.5s ease-in-out infinite,nx-core-pulse 5.5s ease-in-out infinite!important;
}
.orb:before {
  content:"";position:absolute;inset:-20% auto -20% -45%;width:45%;height:140%;
  background:linear-gradient(90deg,transparent,rgba(255,255,255,.70),rgba(114,238,255,.20),transparent)!important;
  filter:blur(5px);transform:rotate(20deg);animation:nx-liquid-sheen 7s ease-in-out infinite!important;
}
.orb:after {
  content:"";position:absolute;inset:7%;border-radius:50%!important;
  border:1px solid rgba(255,255,255,.24)!important;
  box-shadow:inset 0 0 22px rgba(128,112,255,.25),inset 0 -10px 20px rgba(0,0,0,.42)!important;
}
.orb-floor-shadow { width:94px!important;height:17px!important;background:rgba(86,67,177,.28)!important;filter:blur(10px)!important; }
.orbit {
  width:177px!important;height:177px!important;border-radius:50%!important;
  border:1px solid rgba(112,221,255,.38)!important;
  box-shadow:0 0 0 8px rgba(126,93,255,.045),0 0 22px rgba(93,222,255,.12),inset 0 0 24px rgba(164,120,255,.08)!important;
  animation:nx-core-rotate 25s linear infinite!important;
}
.orbit:after { color:#7de8ff!important;background:#18142f!important; }
.orb-spark-a,.orb-spark-b { color:#8cefff!important;text-shadow:0 0 15px rgba(94,224,255,.85)!important;animation:nx-particle-float 4s ease-in-out infinite!important; }
.orb-spark-b { color:#ed8bff!important;animation-delay:1.1s!important; }
.stButton>button {
  background:linear-gradient(145deg,rgba(43,33,69,.98),rgba(26,24,47,.98))!important;
  border-color:rgba(165,130,255,.25)!important;color:#eee8ff!important;
  box-shadow:0 7px 0 rgba(4,3,15,.18),0 15px 28px rgba(10,6,27,.13),inset 0 1px 0 rgba(255,255,255,.10)!important;
}
.stButton>button[kind="primary"],[data-testid="stFormSubmitButton"]>button {
  background:linear-gradient(110deg,#6740ec 0%,#a444e0 53%,#e657bd 100%)!important;
  border:1px solid rgba(255,255,255,.28)!important;color:#fff!important;
  box-shadow:0 6px 0 rgba(48,22,106,.38),0 18px 35px rgba(111,62,219,.28),inset 0 1px 0 rgba(255,255,255,.45)!important;
}
[data-testid="stChatInput"],[data-testid="stChatInput"]>div {
  background:linear-gradient(135deg,rgba(35,28,57,.98),rgba(20,22,42,.98))!important;
  border-color:rgba(157,126,242,.32)!important;
  box-shadow:0 12px 36px rgba(8,4,22,.18),inset 0 1px 0 rgba(255,255,255,.10)!important;
}
[data-testid="stChatInput"] textarea { color:#f4efff!important;-webkit-text-fill-color:#f4efff!important; }
[data-testid="stChatInput"] textarea::placeholder { color:#b7accb!important;-webkit-text-fill-color:#b7accb!important; }
[data-testid="stChatMessage"] {
  background:linear-gradient(135deg,rgba(35,28,57,.95),rgba(20,22,42,.95))!important;
  border-color:rgba(157,126,242,.20)!important;
  box-shadow:0 12px 30px rgba(8,4,22,.13),inset 0 1px 0 rgba(255,255,255,.07)!important;
}
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"],
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] p,
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] li { color:#eee8ff!important; }
[data-testid="stDialog"] [role="dialog"] {
  border:1px solid rgba(174,142,255,.34)!important;
  background:
    radial-gradient(ellipse at 50% 0%,rgba(128,78,245,.25),transparent 52%),
    radial-gradient(ellipse at 100% 100%,rgba(22,182,201,.09),transparent 40%),
    linear-gradient(145deg,rgba(25,19,45,.99),rgba(12,15,31,.99))!important;
  box-shadow:0 38px 110px rgba(0,0,0,.48),0 0 0 1px rgba(255,255,255,.045),inset 0 1px 0 rgba(255,255,255,.15)!important;
}
[data-testid="stDialog"] [role="dialog"]:before { border-color:rgba(190,157,255,.17)!important; }
.welcome-robot-wrap {
  border-radius:50%!important;
  background:
    radial-gradient(circle at 28% 18%,rgba(255,255,255,.96),transparent 24%),
    radial-gradient(circle at 68% 78%,rgba(229,80,218,.82),transparent 35%),
    radial-gradient(circle at 40% 55%,#7756f2,#15112e 74%)!important;
  border:1px solid rgba(255,255,255,.55)!important;
  box-shadow:0 25px 48px rgba(0,0,0,.32),0 0 32px rgba(129,91,255,.24),inset 0 3px 5px rgba(255,255,255,.65),inset 0 -13px 18px rgba(3,3,15,.55)!important;
}
.welcome-robot-wrap:after {
  content:"";position:absolute;inset:-11px;border-radius:50%;border:1px solid rgba(102,224,255,.38);
  transform:rotateX(66deg);animation:nx-login-ring 21s linear infinite;pointer-events:none;
}
.welcome-robot {
  border-radius:50%!important;
  background:radial-gradient(circle at 30% 22%,#fff,rgba(141,109,255,.8) 15%,rgba(28,18,57,.95) 65%,rgba(220,89,211,.8))!important;
  box-shadow:0 9px 22px rgba(0,0,0,.35),inset 0 2px 5px rgba(255,255,255,.7),inset 0 -7px 14px rgba(0,0,0,.5)!important;
}
.welcome-title { color:#f8f4ff!important; }
.welcome-copy,.welcome-helper,.welcome-link { color:#c5badb!important; }
.welcome-features span {
  color:#e9e1ff!important;background:rgba(255,255,255,.055)!important;
  border-color:rgba(181,148,255,.25)!important;
  box-shadow:0 8px 19px rgba(0,0,0,.14),inset 0 1px 0 rgba(255,255,255,.09)!important;
}
[data-testid="stDialog"] [data-testid="stTextInput"] label { color:#eee8ff!important; }
[data-testid="stDialog"] [data-testid="stTextInput"] input {
  background:rgba(8,10,24,.88)!important;color:#fff!important;-webkit-text-fill-color:#fff!important;
  border-color:rgba(164,133,255,.32)!important;
}
[data-testid="stDialog"] [data-testid="stForm"] {
  background:rgba(255,255,255,.035)!important;border-color:rgba(174,142,255,.2)!important;
}
.connection-pill { background:rgba(255,255,255,.055)!important;color:#e9e1ff!important;border-color:rgba(174,142,255,.22)!important; }
.connection-pill * { color:#e9e1ff!important; }
.home-footnote { color:#bfb2d7!important;background:rgba(255,255,255,.04)!important;border-color:rgba(174,142,255,.18)!important; }
@media(max-width:640px) {
  .hero { border-radius:24px!important;padding:15px 8px 19px!important; }
  .orb-wrap { width:165px!important;height:135px!important; }
  .orb { width:100px!important;height:100px!important;min-width:100px!important;font-size:42px!important; }
  .orbit { width:124px!important;height:124px!important; }
}
@media(prefers-reduced-motion:reduce) {
  .orb,.orbit,.orb:before,.orb-spark-a,.orb-spark-b,.welcome-robot-wrap:before,.welcome-robot-wrap:after { animation:none!important; }
}

/* Full 3D art direction: sculpted surfaces, cinematic hero, and immersive onboarding. */
@keyframes nx-scene-drift { 0%,100% { transform:translate3d(0,0,0) rotateX(0deg); } 50% { transform:translate3d(0,-5px,0) rotateX(.5deg); } }
@keyframes nx-core-rotate { from { transform:rotate(0deg) rotateX(62deg) rotateY(-12deg); } to { transform:rotate(360deg) rotateX(62deg) rotateY(-12deg); } }
@keyframes nx-core-pulse { 0%,100% { box-shadow:0 0 28px rgba(145,101,255,.18),0 0 70px rgba(145,101,255,.08); } 50% { box-shadow:0 0 38px rgba(145,101,255,.28),0 0 90px rgba(145,101,255,.12); } }
@keyframes nx-login-entrance { 0% { opacity:0; transform:perspective(1200px) rotateX(8deg) translateY(24px) scale(.97); } 100% { opacity:1; transform:perspective(1200px) rotateX(0) translateY(0) scale(1); } }
@keyframes nx-login-ring { from { transform:rotate(0deg) rotateX(67deg) rotateY(-18deg); } to { transform:rotate(360deg) rotateX(67deg) rotateY(-18deg); } }
@keyframes nx-glass-shimmer { 0%,100% { opacity:.24; transform:translateX(-14%); } 50% { opacity:.55; transform:translateX(14%); } }

.stApp {
  background:
    radial-gradient(ellipse at 50% -12%,rgba(131,89,236,.16),transparent 42%),
    radial-gradient(ellipse at 0% 55%,rgba(88,62,155,.065),transparent 30%),
    radial-gradient(ellipse at 100% 75%,rgba(209,91,178,.055),transparent 30%),
    __BG__!important;
  background-attachment:fixed!important;
}
[data-testid="stMainBlockContainer"] { max-width:1380px!important; }
[data-testid="stSidebar"] { box-shadow:10px 0 38px rgba(0,0,0,.045)!important; }
.workspace-topbar {
  position:relative!important; overflow:hidden!important;
  border-radius:22px!important; padding:13px 17px!important;
  transform:perspective(1200px) rotateX(1deg)!important;
  box-shadow:0 15px 0 rgba(88,61,130,.025),0 24px 48px var(--nx-shadow),inset 0 1px 0 __TOP_HIGHLIGHT__!important;
}
.workspace-topbar:after {
  content:"";position:absolute;inset:0;pointer-events:none;border-radius:inherit;
  background:linear-gradient(110deg,transparent 15%,rgba(255,255,255,.07) 48%,transparent 76%);
  animation:nx-glass-shimmer 9s ease-in-out infinite;
}
.hero {
  position:relative!important; isolation:isolate!important;
  max-width:1080px!important; margin:clamp(1.4rem,4vh,3.5rem) auto 1.5rem!important;
  padding:clamp(20px,3vw,38px) clamp(12px,3vw,38px) 27px!important;
  border:1px solid __HERO_BORDER__!important; border-radius:34px!important;
  background:
    radial-gradient(ellipse at 50% 0%,rgba(143,106,245,.10),transparent 55%),
    linear-gradient(145deg,__HERO_SURFACE_A__,__HERO_SURFACE_B__)!important;
  box-shadow:0 2px 0 __TOP_HIGHLIGHT__,0 25px 60px var(--nx-shadow),inset 0 1px 0 __TOP_HIGHLIGHT__!important;
  transform:perspective(1400px) rotateX(.6deg)!important;
  backdrop-filter:blur(22px)!important;
}
.hero:before {
  content:"";position:absolute;z-index:-1;inset:9px;border-radius:26px;
  border:1px solid __HERO_INNER__!important;pointer-events:none;
}
.hero:after {
  content:"";position:absolute;z-index:-1;left:15%;right:15%;top:-1px;height:1px;
  background:linear-gradient(90deg,transparent,rgba(189,159,255,.72),transparent);
}
.orb-wrap { width:200px!important;height:168px!important;margin:0 auto 5px!important;perspective:1200px!important; }
.orb {
  width:94px!important;height:94px!important;min-width:94px!important;border-radius:30px!important;
  font-size:43px!important;
  background:
    radial-gradient(ellipse at 23% 12%,rgba(255,255,255,.98),transparent 18%),
    radial-gradient(ellipse at 78% 82%,rgba(244,123,215,.72),transparent 30%),
    linear-gradient(145deg,#eadfff 0%,#bda5ff 17%,#8e67f8 40%,#693bd2 68%,#d65fbc 100%)!important;
  box-shadow:0 30px 42px rgba(87,54,158,.24),0 9px 14px rgba(47,27,94,.18),
    inset 0 3px 4px rgba(255,255,255,.95),inset -7px -12px 18px rgba(47,20,101,.26),
    inset 4px 0 9px rgba(255,255,255,.22)!important;
  animation:nx-emblem-drift 6.5s ease-in-out infinite,nx-core-pulse 5s ease-in-out infinite!important;
}
.orbit {
  width:126px!important;height:126px!important;border-radius:38px!important;
  border:1px solid __ORBIT_LINE__!important;
  box-shadow:0 0 0 8px __ORBIT_OUTER__,inset 0 0 25px rgba(153,119,241,.06)!important;
  animation:nx-core-rotate 34s linear infinite!important;
}
.orb-spark { text-shadow:0 0 16px rgba(183,144,255,.7)!important; }
.hero-kicker {
  padding:8px 14px!important;letter-spacing:1.5px!important;font-size:10px!important;
  box-shadow:0 8px 22px var(--nx-shadow),inset 0 1px 0 __TOP_HIGHLIGHT__!important;
}
.hero h1 {
  font-size:clamp(34px,4.5vw,61px)!important;line-height:1.14!important;
  letter-spacing:clamp(-2.2px,-.11vw,-.6px)!important;
  text-shadow:0 1px 0 __TOP_HIGHLIGHT__!important;
}
.hero-subtitle { max-width:650px!important;font-size:15px!important;line-height:1.85!important; }
.hero-trust-row span {
  padding:8px 13px!important;border-radius:13px!important;
  box-shadow:0 7px 0 rgba(100,70,140,.025),0 12px 22px var(--nx-shadow),inset 0 1px 0 __TOP_HIGHLIGHT__!important;
}
.section-heading { font-size:16px!important;letter-spacing:-.2px!important;margin-top:28px!important; }
.stButton>button {
  min-height:52px!important;border-radius:17px!important;
  box-shadow:0 5px 0 rgba(75,52,110,.035),0 13px 26px var(--nx-shadow),inset 0 1px 0 __TOP_HIGHLIGHT__!important;
  transform:perspective(700px) translateZ(0)!important;
}
.stButton>button:hover {
  transform:perspective(700px) translateY(-3px) rotateX(2deg)!important;
  box-shadow:0 7px 0 rgba(75,52,110,.025),0 19px 32px var(--nx-shadow),inset 0 1px 0 __TOP_HIGHLIGHT__!important;
}
.stButton>button[kind="primary"],[data-testid="stFormSubmitButton"]>button[kind="primary"] {
  box-shadow:0 5px 0 rgba(71,40,139,.24),0 17px 30px rgba(128,87,245,.24),inset 0 1px 0 rgba(255,255,255,.48)!important;
}
[data-testid="stChatInput"],[data-testid="stChatInput"]>div {
  border-radius:22px!important;padding:4px!important;
  box-shadow:0 7px 0 rgba(75,52,110,.025),0 17px 38px var(--nx-shadow),inset 0 1px 0 __TOP_HIGHLIGHT__!important;
  backdrop-filter:blur(22px)!important;
}
[data-testid="stChatMessage"] {
  border-radius:22px!important;padding:13px 16px!important;
  box-shadow:0 6px 0 rgba(75,52,110,.02),0 14px 32px var(--nx-shadow),inset 0 1px 0 __TOP_HIGHLIGHT__!important;
}
[data-testid="stDialog"] [role="dialog"] {
  position:relative!important;overflow:hidden!important;
  width:min(94vw,540px)!important;max-width:540px!important;
  border-radius:34px!important;
  background:
    radial-gradient(ellipse at 50% 0%,rgba(144,103,245,.17),transparent 52%),
    linear-gradient(150deg,__DIALOG_SURFACE_A__,__DIALOG_SURFACE_B__)!important;
  box-shadow:0 40px 120px rgba(0,0,0,.23),0 8px 0 rgba(90,63,135,.04),inset 0 1px 0 __TOP_HIGHLIGHT__!important;
  animation:nx-login-entrance .6s cubic-bezier(.2,.8,.2,1) both!important;
}
[data-testid="stDialog"] [role="dialog"]:before {
  content:"";position:absolute;pointer-events:none;inset:9px;border:1px solid __HERO_INNER__;
  border-radius:26px;z-index:0;
}
[data-testid="stDialog"] [role="dialog"]>* { position:relative;z-index:1; }
.welcome-card { padding:10px 14px 13px!important; }
.welcome-robot-wrap {
  width:116px!important;height:116px!important;border-radius:35px!important;margin:10px auto 23px!important;
  transform-style:preserve-3d!important;perspective:1000px!important;
  background:
    radial-gradient(ellipse at 24% 12%,rgba(255,255,255,.96),transparent 23%),
    radial-gradient(ellipse at 76% 84%,rgba(239,123,216,.46),transparent 32%),
    linear-gradient(145deg,#e4d7ff,#b99bff 48%,#efbde5)!important;
  box-shadow:0 28px 45px rgba(107,71,180,.24),0 7px 0 rgba(103,69,161,.05),
    inset 0 3px 4px rgba(255,255,255,.95),inset 0 -10px 15px rgba(91,51,144,.13)!important;
}
.welcome-robot-wrap:before {
  content:"";position:absolute;inset:-13px;border-radius:42px;
  border:1px solid __ORBIT_LINE__;transform:rotate(-18deg) rotateX(65deg);
  animation:nx-login-ring 25s linear infinite;pointer-events:none;
}
.welcome-robot {
  width:68px!important;height:68px!important;border-radius:23px!important;font-size:37px!important;
  transform-style:preserve-3d!important;
  box-shadow:0 17px 27px rgba(91,55,158,.27),inset 0 3px 4px rgba(255,255,255,.9),inset 0 -8px 12px rgba(62,29,127,.2)!important;
}
.welcome-title { font-size:clamp(28px,5vw,34px)!important;letter-spacing:-.9px!important; }
.welcome-copy { max-width:370px!important;margin:0 auto 15px!important;line-height:1.8!important; }
.welcome-features span {
  border-radius:12px!important;padding:8px 10px!important;
  box-shadow:0 6px 15px var(--nx-shadow),inset 0 1px 0 __TOP_HIGHLIGHT__!important;
}
[data-testid="stDialog"] [data-testid="stForm"] {
  margin-top:12px!important;padding:16px!important;border-radius:19px!important;
  box-shadow:0 10px 26px var(--nx-shadow),inset 0 1px 0 __TOP_HIGHLIGHT__!important;
}
.creator-credit-main { padding-top:7px!important;opacity:.88; }
@media(max-width:640px) {
  .hero { border-radius:25px!important;padding:17px 10px 20px!important;margin-top:1rem!important; }
  .hero:before { inset:6px!important;border-radius:19px!important; }
  .orb-wrap { width:160px!important;height:125px!important; }
  .orb { width:74px!important;height:74px!important;min-width:74px!important;border-radius:24px!important;font-size:35px!important; }
  .orbit { width:102px!important;height:102px!important;border-radius:31px!important; }
  .hero h1 { font-size:clamp(25px,7.4vw,36px)!important;line-height:1.2!important;letter-spacing:-.7px!important; }
  .hero-subtitle { font-size:12.5px!important; }
  .hero-trust-row span { border-radius:11px!important; }
  .welcome-robot-wrap { width:92px!important;height:92px!important;border-radius:28px!important;margin-bottom:17px!important; }
  .welcome-robot { width:57px!important;height:57px!important;border-radius:19px!important;font-size:32px!important; }
  .welcome-title { font-size:26px!important; }
}
@media(prefers-reduced-motion:reduce) {
  .workspace-topbar:after,.orb,.orbit,.welcome-robot-wrap,.welcome-robot,[data-testid="stDialog"] [role="dialog"] { animation:none!important; }
}


/* FINAL CANVAS / CONTRAST FIX — scoped so Streamlit wrappers cannot wash out the hero. */
:root { color-scheme:__SCHEME__; }
html, body, [data-testid="stAppViewContainer"], .stApp {
  background:__BG__!important; color:var(--nx-ink)!important;
}
[data-testid="stMain"],[data-testid="stMainBlockContainer"] { background:transparent!important; }
[data-testid="stHeader"] { background:__HEADER__!important; }
[data-testid="stBottom"],[data-testid="stBottomBlockContainer"],
[data-testid="stChatInputContainer"],[data-testid="stBottom"]>div,
[data-testid="stBottomBlockContainer"]>div {
  background:transparent!important;background-color:transparent!important;
  box-shadow:none!important;
}
[data-testid="stSidebar"] {
  background:__SIDEBAR__!important;
}
[data-testid="stSidebar"]>div:first-child {
  background:transparent!important;
}
[data-testid="stSidebar"] .eyebrow,
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
[data-testid="stSidebar"] [data-testid="stCaptionContainer"] p {
  color:var(--nx-muted)!important;
}
.workspace-topbar {
  background:linear-gradient(125deg,#28203f 0%,#252440 55%,#1b293e 100%)!important;
  border:1px solid rgba(166,135,255,.28)!important;
  box-shadow:0 18px 45px rgba(28,17,53,.16),inset 0 1px 0 rgba(255,255,255,.18)!important;
}
.workspace-topbar .workspace-brand,
.workspace-topbar .workspace-brand span { color:#f8f4ff!important; }
.workspace-topbar .workspace-status {
  background:#f7f3ff!important;color:#4a3a5d!important;border-color:rgba(176,145,255,.35)!important;
}
.hero {
  color:#f8f4ff!important;
  background:
    radial-gradient(ellipse at 50% 18%,rgba(115,78,230,.19),transparent 42%),
    radial-gradient(ellipse at 78% 54%,rgba(17,172,193,.10),transparent 32%),
    linear-gradient(135deg,#131026 0%,#1d1233 54%,#0e1728 100%)!important;
  border-color:rgba(164,127,255,.28)!important;
  box-shadow:0 2px 0 rgba(255,255,255,.10),0 28px 75px rgba(12,7,29,.20),inset 0 1px 0 rgba(255,255,255,.13)!important;
  isolation:isolate!important;
}
.hero:before { border-color:rgba(186,153,255,.14)!important; }
.hero h1 { color:#f8f4ff!important;opacity:1!important;text-shadow:0 3px 26px rgba(148,101,255,.14)!important; }
.hero h1 * { opacity:1!important; }
.hero .hero-subtitle { color:#c7bfdc!important;opacity:1!important; }
.hero .hero-kicker { color:#e1d6ff!important;background:rgba(96,64,161,.36)!important;border-color:rgba(172,139,255,.38)!important;opacity:1!important; }
.hero .hero-trust-row span { color:#e3dcf2!important;background:rgba(255,255,255,.065)!important;border-color:rgba(181,150,255,.23)!important;opacity:1!important; }
.hero .gradient-word {
  background:linear-gradient(100deg,#c0a4ff 0%,#ed8bf4 50%,#7ce5f2 100%)!important;
  -webkit-background-clip:text!important;background-clip:text!important;-webkit-text-fill-color:transparent!important;
  color:transparent!important;opacity:1!important;
}
.orb-wrap { overflow:visible!important; }
.stApp [data-testid="stChatInput"] {
  background:var(--nx-control)!important;background-color:var(--nx-control)!important;
  border:1px solid var(--nx-line)!important;border-radius:20px!important;
  box-shadow:0 12px 32px var(--nx-shadow),inset 0 1px 0 __TOP_HIGHLIGHT__!important;
}
.stApp [data-testid="stChatInput"]>div { background:transparent!important; }
.stApp [data-testid="stChatInput"] textarea {
  background:transparent!important;color:var(--nx-control-text)!important;
  -webkit-text-fill-color:var(--nx-control-text)!important;caret-color:var(--nx-link)!important;
}
.stApp [data-testid="stChatInput"] textarea::placeholder {
  color:var(--nx-muted)!important;-webkit-text-fill-color:var(--nx-muted)!important;opacity:1!important;
}
.stApp [data-testid="stChatInput"] button { background:var(--nx-surface-solid)!important;color:var(--nx-ink)!important;border:1px solid var(--nx-line)!important; }
.stApp [data-testid="stTextInput"] input,
.stApp [data-testid="stTextArea"] textarea,
.stApp [data-testid="stSelectbox"] [data-baseweb="select"]>div {
  background:var(--nx-control)!important;color:var(--nx-control-text)!important;
  -webkit-text-fill-color:var(--nx-control-text)!important;border-color:var(--nx-line)!important;
}
.stApp [data-testid="stDialog"] [role="dialog"] {
  background:radial-gradient(ellipse at 50% 0%,rgba(128,78,245,.25),transparent 52%),
             radial-gradient(ellipse at 100% 100%,rgba(22,182,201,.09),transparent 40%),
             linear-gradient(145deg,#19132d,#0c0f1f)!important;
  color:#f8f4ff!important;
}
.stApp [data-testid="stDialog"] .welcome-title { color:#f8f4ff!important; }
.stApp [data-testid="stDialog"] .welcome-copy,
.stApp [data-testid="stDialog"] .welcome-helper,
.stApp [data-testid="stDialog"] .welcome-link { color:#c5badb!important; }
.stApp [data-testid="stDialog"] [data-testid="stTextInput"] label { color:#eee8ff!important; }
.stApp [data-testid="stDialog"] [data-testid="stTextInput"] input {
  background:rgba(8,10,24,.88)!important;color:#fff!important;-webkit-text-fill-color:#fff!important;
  border-color:rgba(164,133,255,.32)!important;
}
.stApp [data-testid="stDialog"] [data-testid="stForm"] { background:rgba(255,255,255,.035)!important;border:1px solid rgba(174,142,255,.2)!important; }
.stApp .connection-pill { background:var(--nx-surface)!important;color:var(--nx-ink)!important; }
.stApp .connection-pill * { color:var(--nx-ink)!important; }
.stApp .home-footnote { color:var(--nx-muted)!important; }
@media(max-width:640px) {
  .hero { padding:18px 10px 22px!important; }
  .hero h1 { color:#f8f4ff!important;font-size:clamp(25px,7.1vw,36px)!important;line-height:1.2!important; }
  .orb { width:100px!important;height:100px!important;min-width:100px!important; }
}


/* Palette consistency pass: light controls stay light, dark controls stay dark.
   Keep the fixed Streamlit composer rail matched to the page canvas, not a white slab. */
html,body,.stApp,[data-testid="stAppViewContainer"] { background:__BG__!important; }
[data-testid="stBottom"],[data-testid="stBottomBlockContainer"],
[data-testid="stChatInputContainer"],[data-testid="stBottom"]>div,
[data-testid="stBottomBlockContainer"]>div {
  background:__BG__!important;background-color:__BG__!important;
  box-shadow:none!important;
}
[data-testid="stBottom"] [data-testid="stChatInput"],
[data-testid="stBottomBlockContainer"] [data-testid="stChatInput"] {
  background:var(--nx-control)!important;background-color:var(--nx-control)!important;
}
.stApp [data-testid="stButton"] button:not([data-testid="stBaseButton-primary"]):not([kind="primary"]),
.stApp button[data-testid="stBaseButton-secondary"],
.stApp [data-testid="stFormSubmitButton"] button:not([data-testid="stBaseButton-primary"]) {
  background:var(--nx-surface-solid)!important;
  background-color:var(--nx-surface-solid)!important;
  color:var(--nx-control-text)!important;
  -webkit-text-fill-color:var(--nx-control-text)!important;
  border:1px solid var(--nx-line)!important;
  box-shadow:0 6px 16px var(--nx-shadow),inset 0 1px 0 __TOP_HIGHLIGHT__!important;
}
.stApp [data-testid="stButton"] button:not([data-testid="stBaseButton-primary"]):not([kind="primary"]):hover,
.stApp button[data-testid="stBaseButton-secondary"]:hover {
  background:var(--nx-surface)!important;
  background-color:var(--nx-surface)!important;
  border-color:#a98aff!important;
}
.stApp button[data-testid="stBaseButton-primary"],
.stApp [data-testid="stButton"] button[kind="primary"],
.stApp [data-testid="stFormSubmitButton"] button,
.stApp [data-testid="stFormSubmitButton"] button[data-testid="stBaseButton-primary"] {
  color:#fff!important;-webkit-text-fill-color:#fff!important;
  background:linear-gradient(115deg,#6842ed 0%,#9f4dde 55%,#d957ba 100%)!important;
  background-color:#8a51e5!important;border:1px solid rgba(255,255,255,.3)!important;
  box-shadow:0 5px 0 rgba(60,30,120,.16),0 14px 26px rgba(112,68,210,.2),inset 0 1px 0 rgba(255,255,255,.4)!important;
}
.stApp [data-testid="stButton"] button[data-testid="stBaseButton-primary"]:hover {
  filter:brightness(1.05) saturate(1.05)!important;
}
.stApp .connection-pill {
  background:var(--nx-surface)!important;
  color:var(--nx-ink)!important;
  border-color:var(--nx-line)!important;
}
.stApp .connection-pill * { color:var(--nx-ink)!important; }
.stApp .connection-pill .status-dot { background:#35c98a!important; }
.stApp [data-testid="stSelectbox"] [data-baseweb="select"]>div {
  background:var(--nx-control)!important;color:var(--nx-control-text)!important;
}
.stApp [data-testid="stSelectbox"] [data-baseweb="select"] * {
  color:var(--nx-control-text)!important;fill:var(--nx-muted)!important;
}
.stApp [data-baseweb="popover"],.stApp [data-baseweb="menu"],.stApp [role="listbox"] {
  background:var(--nx-control)!important;color:var(--nx-control-text)!important;
}
.stApp [role="option"] { color:var(--nx-control-text)!important; }
.stApp [role="option"]:hover,.stApp [role="option"][aria-selected="true"] {
  background:var(--nx-surface)!important;
}
.stApp [data-testid="stTextInput"] input,.stApp [data-testid="stTextArea"] textarea,
.stApp [data-testid="stChatInput"] textarea {
  caret-color:var(--nx-link)!important;
}

</style>
"""
_premium_values = {
    "__SCHEME__": "dark" if _theme == "dark" else "light",
    "__BG__": _palette["bg"],
    "__SURFACE__": _palette["surface"],
    "__SURFACE_SOLID__": _palette["surface_solid"],
    "__INK__": _palette["ink"],
    "__MUTED__": _palette["muted"],
    "__LINE__": _palette["line"],
    "__CONTROL__": _palette["control"],
    "__CONTROL_TEXT__": _palette["control_text"],
    "__SHADOW__": _palette["shadow"],
    "__DIALOG__": _palette["dialog"],
    "__LINK__": _palette["link"],
    "__HEADER__": "rgba(20,16,27,.94)" if _theme == "dark" else "rgba(251,249,247,.78)",
    "__SIDEBAR__": "linear-gradient(160deg,#1b1524,#21172a 58%,#1a1422)" if _theme == "dark" else "linear-gradient(160deg,#fffdfc,#faf7ff 58%,#f8f4fb)",
    "__TOP_HIGHLIGHT__": "rgba(255,255,255,.08)" if _theme == "dark" else "rgba(255,255,255,.95)",
    "__ORB_EDGE__": "rgba(255,255,255,.34)" if _theme == "dark" else "rgba(255,255,255,.9)",
    "__ORB_FLOOR__": "rgba(0,0,0,.34)" if _theme == "dark" else "rgba(82,57,123,.16)",
    "__ORBIT_LINE__": "rgba(193,158,255,.42)" if _theme == "dark" else "rgba(143,105,238,.28)",
    "__ORBIT_OUTER__": "rgba(193,158,255,.035)" if _theme == "dark" else "rgba(143,105,238,.035)",
    "__DIALOG_EDGE__": "rgba(255,255,255,.16)" if _theme == "dark" else "rgba(255,255,255,.92)",
    "__CODE_BG__": "#21182c" if _theme == "dark" else "#f4f0f8",
    "__HERO_BORDER__": "rgba(191,160,255,.19)" if _theme == "dark" else "rgba(141,111,202,.18)",
    "__HERO_SURFACE_A__": "rgba(38,29,53,.83)" if _theme == "dark" else "rgba(255,255,255,.88)",
    "__HERO_SURFACE_B__": "rgba(27,21,39,.91)" if _theme == "dark" else "rgba(248,244,253,.91)",
    "__HERO_INNER__": "rgba(255,255,255,.07)" if _theme == "dark" else "rgba(133,99,189,.09)",
    "__DIALOG_SURFACE_A__": "rgba(36,27,49,.99)" if _theme == "dark" else "rgba(255,255,255,.99)",
    "__DIALOG_SURFACE_B__": "rgba(24,18,34,.99)" if _theme == "dark" else "rgba(249,245,255,.99)",
}
for _token, _value in _premium_values.items():
    _premium_css = _premium_css.replace(_token, _value)
st.markdown(_premium_css, unsafe_allow_html=True)

# Apply the dedicated 3D layer after the existing theme CSS. Keep the background static.
apply_3d_premium_theme(
    dark=st.session_state.get("dark_mode", False),
    aurora=False,
    grid_floor=False,
    tilt=False,
)

# Targeted API-key dialog repair. This stylesheet is deliberately injected after
# the legacy CSS and the 3D module, so contrast and modal sizing cannot be undone.
_dialog_dark = bool(st.session_state.get("dark_mode", False))
_dialog_palette = {
    "bg": "#171222" if _dialog_dark else "#fcfaff",
    "bg2": "#21172f" if _dialog_dark else "#f5efff",
    "ink": "#f8f2ff" if _dialog_dark else "#2b203b",
    "body": "#cbbfdd" if _dialog_dark else "#655674",
    "muted": "#b8a9cc" if _dialog_dark else "#827391",
    "line": "rgba(191,157,255,.24)" if _dialog_dark else "#e4d8f4",
    "field": "#100d1b" if _dialog_dark else "#ffffff",
    "field_ink": "#fcf8ff" if _dialog_dark else "#30243f",
    "pill": "rgba(255,255,255,.06)" if _dialog_dark else "#f1e9ff",
    "pill_ink": "#e9ddff" if _dialog_dark else "#5a4276",
    "shadow": "rgba(0,0,0,.42)" if _dialog_dark else "rgba(70,45,110,.18)",
    "close": "#f5edff" if _dialog_dark else "#3a2b4b",
}
_dialog_css = """
<style>
/* Constrain every box inside Streamlit's dialog to its actual width. */
[data-testid="stDialog"] *,
[data-testid="stDialog"] *:before,
[data-testid="stDialog"] *:after { box-sizing:border-box!important; }
[data-testid="stDialog"] [role="dialog"] {
  width:min(94vw,500px)!important; max-width:min(94vw,500px)!important;
  min-width:0!important; overflow-x:hidden!important; overflow-y:auto!important;
  padding:12px clamp(12px,3vw,24px) 18px!important;
  border-radius:28px!important;
  background:linear-gradient(155deg,__DIALOG_BG__,__DIALOG_BG2__)!important;
  color:__DIALOG_INK__!important;
  border:1px solid __DIALOG_LINE__!important;
  box-shadow:0 28px 88px __DIALOG_SHADOW__,inset 0 1px 0 rgba(255,255,255,.18)!important;
}
[data-testid="stDialog"] [data-testid="stDialogHeader"] {
  width:100%!important; min-width:0!important; padding:4px 4px 0!important;
  margin:0!important; background:transparent!important;
}
[data-testid="stDialog"] [data-testid="stDialogHeader"] button {
  color:__DIALOG_CLOSE__!important; background:transparent!important;
  border:1px solid transparent!important; box-shadow:none!important;
}
[data-testid="stDialog"] [data-testid="stVerticalBlock"],
[data-testid="stDialog"] [data-testid="stForm"],
[data-testid="stDialog"] [data-testid="stElementContainer"],
[data-testid="stDialog"] [data-testid="stTextInput"],
[data-testid="stDialog"] [data-testid="stTextInput"]>div,
[data-testid="stDialog"] [data-testid="stTextInput"]>div>div {
  width:100%!important; max-width:100%!important; min-width:0!important;
}
[data-testid="stDialog"] .welcome-card {
  width:100%!important; max-width:100%!important; min-width:0!important;
  margin:0 auto!important; padding:4px 2px 10px!important;
  text-align:center!important; overflow-wrap:anywhere!important;
}
[data-testid="stDialog"] .welcome-robot-wrap {
  width:96px!important; height:96px!important; margin:4px auto 15px!important;
}
[data-testid="stDialog"] .welcome-eyebrow {
  color:__DIALOG_MUTED__!important; font-size:9px!important;
  letter-spacing:1.7px!important; margin:4px 0 10px!important;
}
[data-testid="stDialog"] .welcome-title {
  width:100%!important; color:__DIALOG_INK__!important;
  font-size:clamp(25px,5vw,31px)!important; line-height:1.17!important;
  letter-spacing:-.7px!important; overflow-wrap:normal!important;
}
[data-testid="stDialog"] .welcome-title span {
  background:linear-gradient(100deg,#8757f5,#bf5ce5,#e961b8)!important;
  -webkit-background-clip:text!important; background-clip:text!important;
  -webkit-text-fill-color:transparent!important; color:transparent!important;
}
[data-testid="stDialog"] .welcome-copy {
  max-width:360px!important; margin:0 auto 13px!important; padding:0 4px!important;
  color:__DIALOG_BODY__!important; font-size:13px!important; line-height:1.7!important;
  overflow-wrap:break-word!important;
}
[data-testid="stDialog"] .welcome-credit {
  margin:0 auto 13px!important; color:__DIALOG_MUTED__!important;
  font-size:10px!important; line-height:1.55!important;
}
[data-testid="stDialog"] .welcome-credit strong { color:#8b5cf6!important; }
[data-testid="stDialog"] .welcome-features {
  display:flex!important; justify-content:center!important; align-items:center!important;
  width:100%!important; max-width:100%!important; flex-wrap:wrap!important;
  gap:7px!important; margin:0 auto 14px!important; padding:0!important;
}
[data-testid="stDialog"] .welcome-features span {
  display:inline-flex!important; align-items:center!important; justify-content:center!important;
  min-width:0!important; max-width:100%!important; padding:7px 10px!important;
  border-radius:12px!important; background:__DIALOG_PILL__!important;
  color:__DIALOG_PILL_INK__!important; -webkit-text-fill-color:__DIALOG_PILL_INK__!important;
  border:1px solid __DIALOG_LINE__!important; box-shadow:0 5px 13px __DIALOG_SHADOW__!important;
  font-size:10px!important; line-height:1.35!important; font-weight:700!important;
}
[data-testid="stDialog"] [data-testid="stForm"] {
  display:block!important; width:100%!important; max-width:100%!important; min-width:0!important;
  margin:0!important; padding:14px!important; overflow:hidden!important;
  border-radius:17px!important; border:1px solid __DIALOG_LINE__!important;
  background:__DIALOG_PILL__!important; box-shadow:inset 0 1px 0 rgba(255,255,255,.12)!important;
}
[data-testid="stDialog"] [data-testid="stForm"] [data-testid="stVerticalBlock"] {
  gap:10px!important; width:100%!important; min-width:0!important;
}
[data-testid="stDialog"] [data-testid="stTextInput"] label {
  color:__DIALOG_INK__!important; font-size:12px!important; font-weight:750!important;
  padding-bottom:5px!important;
}
[data-testid="stDialog"] [data-testid="stTextInput"] input {
  display:block!important; width:100%!important; min-width:0!important; max-width:100%!important;
  height:45px!important; background:__DIALOG_FIELD__!important;
  color:__DIALOG_FIELD_INK__!important; -webkit-text-fill-color:__DIALOG_FIELD_INK__!important;
  border:1px solid __DIALOG_LINE__!important; border-radius:11px!important;
  box-shadow:inset 0 1px 3px rgba(30,20,50,.06)!important;
}
[data-testid="stDialog"] [data-testid="stTextInput"] input::placeholder {
  color:__DIALOG_MUTED__!important; -webkit-text-fill-color:__DIALOG_MUTED__!important;
  opacity:1!important;
}
[data-testid="stDialog"] [data-testid="stFormSubmitButton"],
[data-testid="stDialog"] [data-testid="stFormSubmitButton"]>button {
  width:100%!important; min-width:0!important; max-width:100%!important;
}
[data-testid="stDialog"] [data-testid="stFormSubmitButton"]>button {
  min-height:46px!important; height:auto!important; white-space:normal!important;
  padding:10px 12px!important; border-radius:12px!important;
  color:#fff!important; -webkit-text-fill-color:#fff!important;
  background:linear-gradient(110deg,#7650ed,#9d4fe0 54%,#e45bb7)!important;
  border:1px solid rgba(255,255,255,.35)!important;
  box-shadow:0 4px 0 rgba(70,35,130,.15),0 10px 20px rgba(128,87,245,.20),inset 0 1px 0 rgba(255,255,255,.4)!important;
}
[data-testid="stDialog"] .welcome-helper,
[data-testid="stDialog"] .welcome-link,
[data-testid="stDialog"] [data-testid="stCaptionContainer"],
[data-testid="stDialog"] [data-testid="stCaptionContainer"] p {
  width:100%!important; max-width:100%!important; color:__DIALOG_MUTED__!important;
  -webkit-text-fill-color:__DIALOG_MUTED__!important; font-size:10px!important;
  line-height:1.6!important; text-align:center!important; overflow-wrap:anywhere!important;
}
[data-testid="stDialog"] .welcome-link a {
  color:#9466f5!important; -webkit-text-fill-color:#9466f5!important;
  font-weight:800!important; text-decoration:none!important;
}
[data-testid="stDialog"] [data-testid="stAlert"] {
  width:100%!important; max-width:100%!important; color:__DIALOG_INK__!important;
}

/* Hide Streamlit's floating "Press Enter to submit form" instruction in the
   API-key field. Submission by Enter and the password visibility toggle still work. */
[data-testid="stDialog"] [data-testid="InputInstructions"],
[data-testid="stDialog"] div[data-testid="InputInstructions"],
[data-testid="stDialog"] [data-testid="InputInstructions"] * {
  display:none!important;
  visibility:hidden!important;
  opacity:0!important;
  width:0!important;
  height:0!important;
  max-height:0!important;
  margin:0!important;
  padding:0!important;
  overflow:hidden!important;
  pointer-events:none!important;
}
@media(max-width:520px) {
  [data-testid="stDialog"] [role="dialog"] {
    width:calc(100vw - 18px)!important; max-width:calc(100vw - 18px)!important;
    padding:10px 10px 14px!important; border-radius:22px!important;
  }
  [data-testid="stDialog"] .welcome-card { padding:2px 0 8px!important; }
  [data-testid="stDialog"] .welcome-title { font-size:25px!important; }
  [data-testid="stDialog"] .welcome-copy { font-size:12px!important; }
  [data-testid="stDialog"] [data-testid="stForm"] { padding:11px!important; }
  [data-testid="stDialog"] .welcome-features { gap:5px!important; }
  [data-testid="stDialog"] .welcome-features span { font-size:9px!important; padding:6px 8px!important; }
}
@media(prefers-reduced-motion:reduce) {
  [data-testid="stDialog"] [role="dialog"],[data-testid="stDialog"] .welcome-robot-wrap { animation:none!important; }
}
</style>
"""
_dialog_values = {
    "__DIALOG_BG__": _dialog_palette["bg"],
    "__DIALOG_BG2__": _dialog_palette["bg2"],
    "__DIALOG_INK__": _dialog_palette["ink"],
    "__DIALOG_BODY__": _dialog_palette["body"],
    "__DIALOG_MUTED__": _dialog_palette["muted"],
    "__DIALOG_LINE__": _dialog_palette["line"],
    "__DIALOG_FIELD__": _dialog_palette["field"],
    "__DIALOG_FIELD_INK__": _dialog_palette["field_ink"],
    "__DIALOG_PILL__": _dialog_palette["pill"],
    "__DIALOG_PILL_INK__": _dialog_palette["pill_ink"],
    "__DIALOG_SHADOW__": _dialog_palette["shadow"],
    "__DIALOG_CLOSE__": _dialog_palette["close"],
}
for _token, _value in _dialog_values.items():
    _dialog_css = _dialog_css.replace(_token, _value)
st.markdown(_dialog_css, unsafe_allow_html=True)

st.markdown(
    "<style>\n/* Final layer for the live header reactor and the two appearance modes. */\n.workspace-topbar-right{display:flex!important;align-items:center!important;justify-content:flex-end!important;gap:10px!important;min-width:0!important}\n.workspace-status{flex-shrink:0!important}\n.nx-creator-ribbon.nx-theme-light{\n  background:linear-gradient(130deg,rgba(255,255,255,.90),rgba(246,240,255,.88) 56%,rgba(236,249,255,.86))!important;\n  border-color:rgba(159,128,240,.30)!important;\n  box-shadow:0 4px 0 rgba(102,70,150,.025),0 15px 32px rgba(55,35,88,.09),inset 0 1px 0 rgba(255,255,255,.98)!important;\n}\n.nx-creator-ribbon.nx-theme-light .nx-creator-kicker{color:#88779f!important}\n.nx-creator-ribbon.nx-theme-light .nx-creator-name{color:#2b203f!important}\n.nx-creator-ribbon.nx-theme-light .nx-creator-caption{color:#746584!important}\n.nx-creator-ribbon.nx-theme-dark{\n  background:linear-gradient(130deg,rgba(42,31,65,.97),rgba(27,26,52,.95) 56%,rgba(20,34,52,.95))!important;\n  border-color:rgba(169,133,255,.32)!important;\n  box-shadow:0 5px 0 rgba(0,0,0,.05),0 16px 34px rgba(5,3,20,.20),inset 0 1px 0 rgba(255,255,255,.13)!important;\n}\n.nx-creator-ribbon.nx-theme-dark .nx-creator-kicker{color:#c2b4de!important}\n.nx-creator-ribbon.nx-theme-dark .nx-creator-name{color:#fbf7ff!important}\n.nx-creator-ribbon.nx-theme-dark .nx-creator-caption{color:#d4c8e7!important}\n.nx-creator-ribbon.nx-theme-dark .nx-creator-mark{\n  box-shadow:0 7px 0 rgba(0,0,0,.15),0 13px 25px rgba(126,87,245,.32),inset 0 2px 3px rgba(255,255,255,.65),inset 0 -5px 8px rgba(52,24,113,.28)!important;\n}\n/* Keep the small animated core visible without crowding the status pill. */\n.workspace-topbar .nx-header-reactor{margin-left:auto!important;margin-right:0!important;flex:0 0 64px!important}\n.workspace-topbar .workspace-status{align-self:center!important}\n@media(max-width:900px){\n  .workspace-topbar-right{gap:6px!important}\n  .workspace-topbar .nx-header-reactor{flex-basis:48px!important;scale:.82!important;margin:0 -4px!important}\n  .workspace-status{font-size:9px!important;padding:6px 8px!important}\n}\n@media(max-width:640px){\n  .workspace-topbar-right{gap:4px!important}\n  .workspace-topbar .nx-header-reactor{flex-basis:38px!important;scale:.68!important;margin:0 -7px!important}\n  .workspace-status{font-size:8px!important;padding:5px 6px!important;max-width:108px!important}\n  .nx-creator-ribbon{max-width:calc(100% - 12px)!important;padding:8px 12px 8px 8px!important}\n}\n@media(prefers-reduced-motion:reduce){\n  .workspace-topbar .nx-header-reactor *,.nx-creator-ribbon,.nx-creator-mark,.nx-creator-mark:after{animation:none!important;transition:none!important}\n}\n</style>",
    unsafe_allow_html=True,
)


# Final identity layer — shared by the landing page and the API-key welcome screen.
st.markdown(
    """
    <style>
    @keyframes nx-credit-float { 0%,100% { transform:translateY(0) rotateX(0deg); } 50% { transform:translateY(-3px) rotateX(2deg); } }
    @keyframes nx-credit-sheen { 0% { transform:translateX(-130%) skewX(-18deg); } 100% { transform:translateX(240%) skewX(-18deg); } }
    @keyframes nx-credit-spin { from { transform:rotate(0deg) rotateX(62deg); } to { transform:rotate(360deg) rotateX(62deg); } }
    @keyframes nx-credit-glow { 0%,100% { opacity:.52; } 50% { opacity:.95; } }

    .stApp {
      background:
        radial-gradient(ellipse at 51% -7%,rgba(123,86,232,.13),transparent 38%),
        radial-gradient(ellipse at 0% 50%,rgba(41,170,199,.045),transparent 28%),
        radial-gradient(ellipse at 100% 65%,rgba(207,84,185,.045),transparent 28%),
        var(--nx-bg)!important;
      background-attachment:fixed!important;
    }
    [data-testid="stMain"],[data-testid="stMainBlockContainer"] { background:transparent!important; }
    [data-testid="stBottom"],[data-testid="stBottomBlockContainer"],
    [data-testid="stChatInputContainer"],[data-testid="stBottom"]>div,
    [data-testid="stBottomBlockContainer"]>div { background:var(--nx-bg)!important;background-color:var(--nx-bg)!important;box-shadow:none!important; }
    [data-testid="stBottom"] [data-testid="stChatInput"],
    [data-testid="stBottomBlockContainer"] [data-testid="stChatInput"] { background:var(--nx-control)!important;background-color:var(--nx-control)!important; }

    .nx-creator-ribbon {
      display:flex;align-items:center;justify-content:center;gap:12px;
      position:relative;isolation:isolate;overflow:hidden;
      width:max-content;max-width:calc(100% - 8px);box-sizing:border-box;
      margin:0 auto 16px;padding:9px 18px 9px 10px;
      border-radius:18px;border:1px solid rgba(159,128,240,.27);
      background:linear-gradient(130deg,rgba(255,255,255,.78),rgba(246,240,255,.76) 56%,rgba(236,249,255,.72));
      box-shadow:0 4px 0 rgba(102,70,150,.035),0 14px 30px rgba(55,35,88,.09),inset 0 1px 0 rgba(255,255,255,.95);
      backdrop-filter:blur(18px);
      animation:nx-credit-float 6s ease-in-out infinite;
    }
    .nx-creator-ribbon:before {
      content:"";position:absolute;z-index:-1;inset:0;pointer-events:none;
      background:linear-gradient(100deg,transparent 20%,rgba(255,255,255,.52) 48%,transparent 72%);
      animation:nx-credit-sheen 8s ease-in-out infinite;
    }
    .nx-creator-mark {
      position:relative;display:grid;place-items:center;flex:0 0 40px;width:40px;height:40px;
      border-radius:13px;color:#fff;font-size:21px;font-weight:700;
      background:radial-gradient(ellipse at 28% 14%,rgba(255,255,255,.88),transparent 26%),linear-gradient(145deg,#bda2ff,#7950eb 57%,#d75bb9);
      border:1px solid rgba(255,255,255,.84);
      box-shadow:0 7px 0 rgba(91,55,160,.10),0 12px 20px rgba(128,87,245,.24),inset 0 2px 3px rgba(255,255,255,.72),inset 0 -5px 8px rgba(52,24,113,.2);
      transform-style:preserve-3d;animation:nx-credit-glow 4s ease-in-out infinite;
    }
    .nx-creator-mark:after {
      content:"";position:absolute;inset:-5px;border-radius:16px;border:1px solid rgba(158,127,246,.30);
      transform:rotateX(62deg);animation:nx-credit-spin 18s linear infinite;pointer-events:none;
    }
    .nx-login-credit {
      width:max-content;max-width:100%;display:flex;align-items:center;justify-content:center;gap:8px;
      margin:0 auto 13px;padding:6px 11px;border:1px solid rgba(159,128,240,.22);border-radius:14px;
      background:linear-gradient(135deg,rgba(255,255,255,.82),rgba(244,237,255,.73));
      box-shadow:0 5px 0 rgba(102,70,150,.025),0 10px 22px rgba(55,35,88,.07),inset 0 1px 0 rgba(255,255,255,.96);
      color:#342547;font:700 10px/1.4 'DM Sans',sans-serif;text-align:left;
    }
    .nx-login-credit-mark {
      flex:0 0 26px;width:26px;height:26px;display:grid;place-items:center;border-radius:9px;color:#fff;
      background:linear-gradient(145deg,#bda2ff,#7950eb 57%,#d75bb9);
      box-shadow:0 4px 9px rgba(128,87,245,.2),inset 0 1px 0 rgba(255,255,255,.55);
    }
    .nx-login-credit strong { display:block;color:#342547;font-weight:800; }
    .nx-login-credit small { display:block;color:#857595;font-size:9px;font-weight:500; }
    [data-testid="stDialog"] .nx-login-credit { color:#342547!important; }
    [data-testid="stDialog"] .nx-login-credit strong { color:#342547!important; }
    [data-testid="stDialog"] .nx-login-credit small { color:#857595!important; }
    @media(max-width:520px) {
      .nx-login-credit { margin-bottom:10px;padding:5px 9px;gap:7px; }
      .nx-login-credit-mark { width:24px;height:24px;flex-basis:24px; }
    }
    .nx-creator-copy { display:flex;flex-direction:column;gap:1px;text-align:left;min-width:0; }
    .nx-creator-kicker { font:800 8px/1.4 'DM Sans',sans-serif;letter-spacing:1.5px;color:#88779f; }
    .nx-creator-name { font:800 13px/1.35 'Manrope',sans-serif;letter-spacing:-.2px;color:#2b203f; }
    .nx-creator-caption { font:500 10px/1.4 'DM Sans',sans-serif;color:#80728e; }

    /* Confident, readable hero title and controlled liquid-core emblem. */
    .hero h1 { color:#fbf8ff!important;opacity:1!important;text-shadow:0 4px 26px rgba(150,103,255,.18)!important; }
    .hero h1 * { opacity:1!important; }
    .hero .gradient-word {
      background:linear-gradient(105deg,#b9a1ff 0%,#eb8af0 48%,#78e5f1 100%)!important;
      background-clip:text!important;-webkit-background-clip:text!important;
      color:transparent!important;-webkit-text-fill-color:transparent!important;
    }
    .hero .hero-subtitle { color:#d1c9e0!important;opacity:1!important; }
    .hero .hero-kicker { color:#dfd3ff!important;opacity:1!important; }
    .hero .hero-trust-row span { color:#e8e1f5!important; }
    .orb-wrap { isolation:isolate!important; }
    .nx-cube { filter:drop-shadow(0 20px 24px rgba(58,38,120,.24))!important; }
    .nx-out i { backface-visibility:visible!important;-webkit-backface-visibility:visible!important; }
    .nx-out i:nth-child(2),.nx-out i:nth-child(4) { filter:brightness(.78) saturate(1.12); }
    .nx-out i:nth-child(3),.nx-out i:nth-child(6) { filter:brightness(.58) saturate(1.10); }
    .nx-out i:nth-child(5) { filter:brightness(1.15); }

    /* Keep light-mode controls genuinely light and dark-mode controls genuinely dark. */
    .stApp [data-testid="stButton"] button:not([kind="primary"]):not([data-testid="stBaseButton-primary"]),
    .stApp button[data-testid="stBaseButton-secondary"] {
      background:var(--nx-surface-solid)!important;color:var(--nx-control-text)!important;
      -webkit-text-fill-color:var(--nx-control-text)!important;border:1px solid var(--nx-line)!important;
    }
    .stApp [data-testid="stButton"] button[kind="primary"],
    .stApp button[data-testid="stBaseButton-primary"],
    .stApp [data-testid="stFormSubmitButton"] button {
      color:#fff!important;-webkit-text-fill-color:#fff!important;
      background:linear-gradient(110deg,#7045ee,#a14cde 54%,#e45db9)!important;
      border:1px solid rgba(255,255,255,.32)!important;
    }

    /* Modal-specific contrast and fit: all content stays inside the dialog. */
    [data-testid="stDialog"] [role="dialog"] {
      width:min(94vw,500px)!important;max-width:min(94vw,500px)!important;min-width:0!important;
      overflow-x:hidden!important;box-sizing:border-box!important;
      background:linear-gradient(150deg,rgba(255,255,255,.99),rgba(246,240,255,.99))!important;
      color:#2b203b!important;border:1px solid rgba(177,151,236,.35)!important;
      box-shadow:0 35px 100px rgba(25,14,48,.26),inset 0 1px 0 rgba(255,255,255,.98)!important;
    }
    [data-testid="stDialog"] [data-testid="stVerticalBlock"],
    [data-testid="stDialog"] [data-testid="stForm"],
    [data-testid="stDialog"] [data-testid="stElementContainer"],
    [data-testid="stDialog"] [data-testid="stTextInput"],
    [data-testid="stDialog"] [data-testid="stTextInput"]>div,
    [data-testid="stDialog"] [data-testid="stTextInput"]>div>div { max-width:100%!important;min-width:0!important;box-sizing:border-box!important; }
    [data-testid="stDialog"] .welcome-title { color:#2b203b!important; }
    [data-testid="stDialog"] .welcome-copy { color:#665775!important; }
    [data-testid="stDialog"] .welcome-eyebrow { color:#8c79a5!important; }
    [data-testid="stDialog"] .welcome-credit { color:#827391!important; }
    [data-testid="stDialog"] .welcome-features span { color:#5a4276!important;-webkit-text-fill-color:#5a4276!important;background:#f1e9ff!important;border-color:#e4d8f4!important; }
    [data-testid="stDialog"] [data-testid="stTextInput"] label { color:#30243f!important; }
    [data-testid="stDialog"] [data-testid="stTextInput"] input { background:#fff!important;color:#30243f!important;-webkit-text-fill-color:#30243f!important;border:1px solid #d9cbea!important; }
    [data-testid="stDialog"] .welcome-helper,[data-testid="stDialog"] .welcome-link,
    [data-testid="stDialog"] [data-testid="stCaptionContainer"],
    [data-testid="stDialog"] [data-testid="stCaptionContainer"] p { color:#827391!important;-webkit-text-fill-color:#827391!important; }
    [data-testid="stDialog"] [data-testid="InputInstructions"],
    [data-testid="stDialog"] div[data-testid="InputInstructions"] { display:none!important;visibility:hidden!important;opacity:0!important;pointer-events:none!important; }

    @media(max-width:640px) {
      .nx-creator-ribbon { gap:9px;padding:8px 12px 8px 8px;margin-bottom:12px;border-radius:15px; }
      .nx-creator-mark { width:35px;height:35px;flex-basis:35px;font-size:18px;border-radius:11px; }
      .nx-creator-kicker { font-size:7px;letter-spacing:1.15px; }
      .nx-creator-name { font-size:12px; }
      .nx-creator-caption { font-size:9px; }
      .hero h1 { font-size:clamp(25px,7.1vw,36px)!important;line-height:1.2!important; }
      [data-testid="stDialog"] [role="dialog"] { width:calc(100vw - 18px)!important;max-width:calc(100vw - 18px)!important;padding:10px!important; }
    }
    @media(prefers-reduced-motion:reduce) {
      .nx-creator-ribbon,.nx-creator-mark,.nx-creator-mark:after { animation:none!important; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)





def get_api_key():
    """Resolve the key in safe precedence order: session entry, Streamlit Secrets, then environment."""
    session_key = st.session_state.get("api_key_session", "").strip()
    if session_key:
        return session_key

    try:
        secret_key = str(st.secrets.get("OPENAI_API_KEY", "")).strip()
        if secret_key:
            return secret_key
    except Exception:
        # Streamlit Secrets is optional for local development.
        pass

    return os.getenv("OPENAI_API_KEY", "").strip()


def create_chat():
    chat_id = str(uuid.uuid4())
    st.session_state.chats[chat_id] = {
        "title": "New conversation",
        "messages": [],
        "created": datetime.now().strftime("%b %d, %H:%M"),
    }
    st.session_state.active_chat = chat_id


def get_active_chat():
    if not st.session_state.active_chat or st.session_state.active_chat not in st.session_state.chats:
        create_chat()
    return st.session_state.chats[st.session_state.active_chat]


def get_response_text(response):
    text = getattr(response, "output_text", None)
    if text:
        return text
    parts = []
    for item in getattr(response, "output", []) or []:
        if getattr(item, "type", None) == "message":
            for content in getattr(item, "content", []) or []:
                if getattr(content, "type", None) == "output_text":
                    parts.append(getattr(content, "text", ""))
    return "\n".join(p for p in parts if p)


def get_citations(response):
    """Collect source URLs from Responses API citation annotations and search metadata."""
    found = []
    seen = set()

    def attr(obj, name, default=None):
        if isinstance(obj, dict):
            return obj.get(name, default)
        return getattr(obj, name, default)

    for item in attr(response, "output", []) or []:
        for content in attr(item, "content", []) or []:
            for annotation in attr(content, "annotations", []) or []:
                citation = attr(annotation, "url_citation", annotation)
                url = attr(citation, "url")
                title = attr(citation, "title") or url
                if url and url not in seen:
                    seen.add(url)
                    found.append({"title": title, "url": url})

    for item in attr(response, "output", []) or []:
        if attr(item, "type") != "web_search_call":
            continue
        action = attr(item, "action", {})
        for source in attr(action, "sources", []) or []:
            url = attr(source, "url")
            title = attr(source, "title") or url
            if url and url not in seen:
                seen.add(url)
                found.append({"title": title, "url": url})
    return found


def ask_openai(history, latest_question, use_web):
    """Generate an answer, with live web research and source metadata when enabled."""
    key = get_api_key()
    if not key:
        raise ValueError("API key missing")

    client = OpenAI(api_key=key, timeout=90, max_retries=2)
    styles = {
        "Concise": "Be direct and concise, but do not omit key evidence or necessary caveats.",
        "Balanced": "Give a clear, useful answer with enough detail to support the conclusion.",
        "Detailed": "Give a thorough, well-structured answer with examples and evidence where useful.",
    }
    system_text = (
        st.session_state.system_prompt.strip()
        + "\n\nResponse style: " + styles[st.session_state.response_style]
    )

    input_messages = [{"role": "system", "content": system_text}]
    for message in history:
        if message.get("role") in ("user", "assistant"):
            input_messages.append({"role": message["role"], "content": message["content"]})
    input_messages.append({"role": "user", "content": latest_question})

    request = {
        "model": st.session_state.selected_model,
        "input": input_messages,
    }

    if use_web:
        input_messages[0]["content"] += (
            "\n\nNEXORA LIVE RESEARCH STANDARD:"
            "\n- For current, recent, disputed, technical, financial, legal, health, product, or otherwise changeable facts, actually use live web search before answering."
            "\n- Treat a claim as verified only to the extent supported by the sources actually retrieved. Never claim you searched if no search call occurred."
            "\n- Prefer primary and authoritative sources: official documentation, government or regulator pages, original research, official company statements, and direct data providers."
            "\n- For important claims, seek corroboration from a second independent, credible source when practical. If sources disagree, explain the disagreement and dates instead of hiding it."
            "\n- Check publication/update dates and distinguish the event date from the article date. Do not present stale material as current."
            "\n- Make specific claims traceable with inline source citations. Use the supplied citations and never invent titles, URLs, quotations, statistics, or references."
            "\n- Separate sourced facts from interpretation, estimates, and uncertainty. State when the evidence is limited or a claim could not be verified."
            "\n- Answer the user's actual question directly. Avoid generic filler, generic disclaimers, and unsupported confident wording."
            "\n- For stable, timeless questions, answer from knowledge without forcing an unnecessary search."
        )
        request["tools"] = [{
            "type": "web_search",
            "search_context_size": "high",
        }]
        # Required for time-sensitive research questions, so the model cannot quietly skip searching.
        research_trigger = any(term in latest_question.lower() for term in (
            "search", "latest", "today", "current", "recent", "this week", "2026",
            "price", "pricing", "compare", "review", "source", "citation", "news",
            "official", "verify", "fact check", "research", "internet", "web",
            "update", "release", "version", "status", "available", "market",
        ))
        request["tool_choice"] = "required" if research_trigger else "auto"
        request["include"] = ["web_search_call.action.sources"]

    response = client.responses.create(**request)
    answer = get_response_text(response)
    citations = get_citations(response)

    # Fail transparently rather than presenting a web-research answer without source evidence.
    if use_web and not answer:
        raise RuntimeError("The model returned an empty response.")
    if use_web and citations:
        source_list = "\n".join(
            f"- {item['title']}: {item['url']}" for item in citations[:12]
        )
        answer += (
            "\n\n---\n**Sources consulted**\n"
            + source_list
        )
    return answer, citations


# -------------------- API KEY POPUP --------------------
@st.dialog(" ", width="small")
def key_dialog():
    st.markdown(
        """
        <div class="welcome-card">
          <div class="nx-login-credit">
            <span class="nx-login-credit-mark">✦</span>
            <span><strong>Designed &amp; developed by Atta ur Rehman</strong><small>A student of Sir Iqbal</small></span>
          </div>
          <div class="welcome-robot-wrap">
            <div class="welcome-robot">✦</div>
            <span class="robot-spark spark-one">✦</span>
            <span class="robot-spark spark-two">✧</span>
          </div>
          <div class="welcome-eyebrow">YOUR PERSONAL AI STUDIO</div>
          <h2 class="welcome-title">Welcome to<br>your <span> NEXORA AI</span></h2>
          <p class="welcome-copy">A smarter space to think, create, and explore. Connect your OpenAI API key to enter your personal AI workspace.</p>
          <div class="welcome-features">
            <span>⚡ Smart answers</span><span>🌐 Web search</span><span>💬 Chat history</span>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    with st.form("nexora_key_form"):
        entered_key = st.text_input("🔑 OpenAI API key", type="password", placeholder="Paste your API key (sk-...)")
        connect = st.form_submit_button("✦  Connect & enter workspace", type="primary", use_container_width=True)
    st.markdown('<div class="welcome-helper">🔒 Your key stays in this active session and is not saved to the source file.</div>', unsafe_allow_html=True)
    st.markdown('<div class="welcome-link">Need a key? <a href="https://platform.openai.com/api-keys" target="_blank">Create an API key ↗</a></div>', unsafe_allow_html=True)
    st.caption("API usage may incur charges. ChatGPT subscriptions do not include API credits.")
    if connect:
        if not entered_key.strip():
            st.error("Please enter your API key to continue.")
        elif len(entered_key.strip()) < 20:
            st.warning("This key looks too short. Please copy the complete API key from your OpenAI Platform account.")
        else:
            st.session_state.api_key_session = entered_key.strip()
            st.session_state.key_prompt_seen = True
            st.rerun()
    if os.getenv("OPENAI_API_KEY", "").strip():
        if st.button("Use the key configured on this computer", use_container_width=True):
            st.session_state.key_prompt_seen = True
            st.rerun()


if not st.session_state.key_prompt_seen and not st.session_state.api_key_session:
    key_dialog()

# -------------------- SIDEBAR --------------------
with st.sidebar:
    st.markdown(
        """
        <div class="brand-row"><div class="brand-icon">✦</div><div class="brand-name">NEXORA <span style="color:#8057f5">AI</span></div></div>
        <div class="brand-caption">YOUR PERSONAL AI WORKSPACE</div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("＋  New chat", type="primary", use_container_width=True):
        create_chat()
        st.session_state.show_settings = False
        st.rerun()

    st.markdown('<div class="eyebrow">Workspace</div>', unsafe_allow_html=True)
    theme_label_side = "☀️  Switch to Day Mode" if st.session_state.dark_mode else "🌙  Switch to Night Mode"
    if st.button(theme_label_side, key="sidebar_theme_toggle", use_container_width=True):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()
    if st.button("⚙  Assistant settings", use_container_width=True):
        st.session_state.show_settings = not st.session_state.show_settings
        st.rerun()

    st.markdown('<div class="eyebrow">Recent conversations</div>', unsafe_allow_html=True)
    search = st.text_input("Search conversations", placeholder="⌕  Search chats...", label_visibility="collapsed")
    count = 0
    for chat_id in list(st.session_state.chats.keys())[::-1]:
        item = st.session_state.chats[chat_id]
        if search:
            query = search.lower()
            if query not in item["title"].lower() and not any(query in m["content"].lower() for m in item["messages"]):
                continue
        count += 1
        title = item["title"] if len(item["title"]) <= 24 else item["title"][:21] + "..."
        prefix = "●  " if chat_id == st.session_state.active_chat else "   "
        if st.button(prefix + title, key=f"select_{chat_id}", use_container_width=True):
            st.session_state.active_chat = chat_id
            st.session_state.show_settings = False
            st.rerun()
    if count == 0:
        st.caption("No chats yet — say hi!")

    st.markdown('<div class="eyebrow">Live internet search</div>', unsafe_allow_html=True)
    st.session_state.web_search_enabled = st.toggle(
        "Search the web for current answers",
        value=st.session_state.web_search_enabled,
        help="When enabled, the OpenAI Responses API may search the live public web and return citations.",
    )
    st.caption("Search can add API usage/cost. The model decides when a search is useful.")

    st.markdown('<div class="eyebrow">Connection</div>', unsafe_allow_html=True)
    if get_api_key():
        st.markdown('<div class="connection-pill"><span class="status-dot"></span><div><b>API key configured</b><br><span style="color:#92899e">Ready to send requests</span></div></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="connection-pill">○ &nbsp; Add an API key to start chatting</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        if st.button("🔑 API key", use_container_width=True):
            key_dialog()
    with c2:
        if st.button("Clear key", use_container_width=True):
            st.session_state.api_key_session = ""
            st.session_state.key_prompt_seen = False
            st.rerun()

    st.markdown('<div class="eyebrow">Model</div>', unsafe_allow_html=True)
    models = list(dict.fromkeys([DEFAULT_MODEL, "gpt-5.4", "gpt-5.2", "gpt-4.1-mini", "gpt-4.1"]))
    idx = models.index(st.session_state.selected_model) if st.session_state.selected_model in models else 0
    st.session_state.selected_model = st.selectbox("Choose model", models, index=idx, label_visibility="collapsed")
    st.caption("Web search availability depends on model and API account access.")

    if st.session_state.chats and st.button("▤  Delete current chat", use_container_width=True):
        st.session_state.chats.pop(st.session_state.active_chat, None)
        st.session_state.active_chat = None
        st.rerun()

    st.markdown('<div class="fine-print">NEXORA AI · Think beyond</div><div class="creator-credit-sidebar">Designed &amp; developed by <strong>Atta ur Rehman</strong><br><span>A student of Sir Iqbal</span></div>', unsafe_allow_html=True)

# -------------------- SETTINGS --------------------
if st.session_state.show_settings:
    st.title("Assistant settings")
    st.caption("Personalize how NEXORA AI works for you.")
    with st.container(border=True):
        with st.form("settings_form"):
            system_prompt = st.text_area("System instructions", value=st.session_state.system_prompt, height=160)
            response_style = st.selectbox(
                "Response style", ["Concise", "Balanced", "Detailed"],
                index=["Concise", "Balanced", "Detailed"].index(st.session_state.response_style),
            )
            save = st.form_submit_button("Save settings", type="primary")
        if save:
            if not system_prompt.strip():
                st.error("System instructions cannot be empty.")
            else:
                st.session_state.system_prompt = system_prompt.strip()
                st.session_state.response_style = response_style
                st.success("Settings saved.")
                st.rerun()
    st.stop()

# Centered creator signature — displayed above the app header.
creator_theme_class = "nx-theme-dark" if st.session_state.get("dark_mode", False) else "nx-theme-light"
st.markdown(
    f"""
    <div class="nx-creator-ribbon {creator_theme_class}" role="note" aria-label="Creator credit">
      <div class="nx-creator-mark">✦</div>
      <div class="nx-creator-copy">
        <span class="nx-creator-kicker">DESIGNED &amp; DEVELOPED BY</span>
        <strong class="nx-creator-name">Atta ur Rehman</strong>
        <span class="nx-creator-caption">A student of Sir Iqbal</span>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# -------------------- MAIN CHAT --------------------
header_col, theme_col = st.columns([7, 1.7], vertical_alignment="center")
with header_col:
    st.markdown(
        f"""
        <div class="workspace-topbar">
          <div class="workspace-brand"><span class="workspace-mark">✦</span><span>NEXORA <span style="color:#8057f5">AI</span><br><span style="font:500 10px 'DM Sans',sans-serif;color:#958aa4;letter-spacing:.35px">YOUR PERSONAL AI WORKSPACE</span></span></div>
          <div class="workspace-topbar-right">
            {header_reactor_html()}
            <div class="workspace-status"><span class="workspace-status-dot"></span> AI workspace ready</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with theme_col:
    theme_label = "☀️  Day mode" if st.session_state.dark_mode else "🌙  Night mode"
    if st.button(theme_label, key="theme_toggle_button", type="primary" if not st.session_state.dark_mode else "secondary", use_container_width=True, help="Switch between light/day and dark/night appearance"):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()

active_chat = get_active_chat()
history = active_chat["messages"]

if not history:
    st.markdown(
        f"""
        <div class="hero">
          <div class="orb-wrap"><div class="orb-floor-shadow"></div>{hero_cube_html()}<span class="orb-spark orb-spark-a">✦</span><span class="orb-spark orb-spark-b">✧</span></div>
          <div class="hero-kicker">✦&nbsp; YOUR IDEAS, WITH MORE CLARITY</div>
          <h1>What are we <span class="gradient-word">working on</span> today?</h1>
          <p class="hero-subtitle">From quick questions to deep research, coding, writing, and planning — turn your next idea into progress.</p>
          <div class="hero-trust-row"><span>✦ Thoughtful answers</span><span>⌕ Source-aware research</span><span>⌘ Coding & creativity</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown('<div class="section-heading">A good place to start</div>', unsafe_allow_html=True)
    prompts = [
        ("✧", "Learn something new", "Explain a complex topic in simple language, with a useful example and a short summary."),
        ("✎", "Write & create", "Help me create polished, original content. Ask a brief question if key details are missing."),
        ("⌕", "Research a topic", "Research this topic using reliable, current web sources. Compare evidence and cite the sources for key claims."),
        ("⌘", "Build with code", "Help me solve a coding problem. Explain the root cause and provide a practical approach."),
    ]
    col_a, col_b = st.columns(2)
    for i, (icon, title, prompt) in enumerate(prompts):
        with (col_a if i % 2 == 0 else col_b):
            if st.button(f"{icon}   {title}", key=f"prompt_{i}", use_container_width=True):
                st.session_state.pending_prompt = prompt
                st.rerun()
else:
    title_color = "#f3effb" if st.session_state.dark_mode else "#292238"
    st.markdown(f"<h3 style='font-family:Manrope,sans-serif;color:{title_color}'>{active_chat['title']}</h3>", unsafe_allow_html=True)
    for message_index, message in enumerate(history):
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if message["role"] == "user":
                edit_col, spacer_col = st.columns([1, 5])
                with edit_col:
                    if st.button("✎ Edit", key=f"edit_message_{st.session_state.active_chat}_{message_index}", help="Edit this message and regenerate the conversation from this point"):
                        st.session_state.edit_message_index = message_index
                        st.rerun()
            if message["role"] == "assistant" and message.get("citations"):
                with st.expander("Sources from the web"):
                    for source in message["citations"]:
                        st.markdown(f"- [{source['title']}]({source['url']})")

# Edit a prior user message; regenerate the thread from the edited point onward.
if st.session_state.get("edit_message_index") is not None:
    edit_index = st.session_state.edit_message_index
    if 0 <= edit_index < len(history) and history[edit_index].get("role") == "user":
        st.markdown('<div class="edit-message-heading">✦ Refine your prompt</div>', unsafe_allow_html=True)
        with st.form(f"edit_message_form_{st.session_state.active_chat}_{edit_index}"):
            edited_text = st.text_area(
                "Edit your message",
                value=history[edit_index]["content"],
                height=120,
                label_visibility="collapsed",
                key=f"edit_message_text_{st.session_state.active_chat}_{edit_index}",
            )
            save_col, cancel_col = st.columns(2)
            with save_col:
                save_edit = st.form_submit_button("✦ Save & regenerate", type="primary", use_container_width=True)
            with cancel_col:
                cancel_edit = st.form_submit_button("Cancel", use_container_width=True)
        if save_edit and edited_text.strip():
            active_chat["messages"] = active_chat["messages"][:edit_index]
            st.session_state.pending_prompt = edited_text.strip()
            st.session_state.edit_message_index = None
            st.rerun()
        if cancel_edit:
            st.session_state.edit_message_index = None
            st.rerun()
    else:
        st.session_state.edit_message_index = None

st.markdown('<div class="home-footnote">✦ NEXORA AI can make mistakes. For important decisions, check cited sources and verify critical details.</div><div class="creator-credit-main">Designed &amp; developed by <strong>Atta ur Rehman</strong><span>A student of Sir Iqbal</span></div>', unsafe_allow_html=True)

# -------------------- INPUT / RESPONSE --------------------
pending = st.session_state.pop("pending_prompt", "")
user_text = st.chat_input("Message NEXORA AI...")

if pending:
    user_text = pending

if user_text and user_text.strip():
    if not get_api_key():
        st.warning("Add your OpenAI API key to send a message.")
        key_dialog()
        st.stop()

    active_chat = get_active_chat()
    clean_text = user_text.strip()
    previous_history = list(active_chat["messages"])
    active_chat["messages"].append({
        "role": "user",
        "content": clean_text,
        "timestamp": datetime.now().isoformat(),
    })
    if active_chat["title"] == "New conversation":
        active_chat["title"] = clean_text[:36] + ("..." if len(clean_text) > 36 else "")

    with st.chat_message("user"):
        st.markdown(clean_text)

    with st.chat_message("assistant"):
        with st.spinner("Thinking" + (" and searching the web..." if st.session_state.web_search_enabled else "...")):
            try:
                answer, citations = ask_openai(
                    previous_history,
                    clean_text,
                    st.session_state.web_search_enabled,
                )
                if not answer:
                    answer = "I couldn't produce a text response. Please try again."
                st.markdown(answer)
                if citations:
                    with st.expander(f"Web sources ({len(citations)})"):
                        for source in citations:
                            st.markdown(f"- [{source['title']}]({source['url']})")
                active_chat["messages"].append({
                    "role": "assistant",
                    "content": answer,
                    "citations": citations,
                    "timestamp": datetime.now().isoformat(),
                })
            except Exception as exc:
                # Keep user question available to retry; never display raw exception/key.
                st.error(
                    "NEXORA could not complete this request. Check the API key, available API credits, selected model access, and web-search support. Your message is kept in the chat so you can retry."
                )
                st.caption("If the error continues, switch to gpt-4.1-mini or temporarily turn off web search, then retry.")
                print(f"NEXORA AI request failed: {type(exc).__name__}: {str(exc)[:240]}")

    st.rerun()
