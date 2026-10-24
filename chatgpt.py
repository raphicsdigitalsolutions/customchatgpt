import os
import uuid
from datetime import datetime

import streamlit as st
from dotenv import load_dotenv, find_dotenv
from openai import OpenAI

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
}
for _token, _value in _premium_values.items():
    _premium_css = _premium_css.replace(_token, _value)
st.markdown(_premium_css, unsafe_allow_html=True)



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
    key = get_api_key()
    if not key:
        raise ValueError("API key missing")

    client = OpenAI(api_key=key, timeout=90, max_retries=2)
    styles = {
        "Concise": "Prefer concise, direct answers.",
        "Balanced": "Give clear answers with useful explanations.",
        "Detailed": "Provide detailed explanations and examples when useful.",
    }
    system_text = (
        st.session_state.system_prompt.strip()
        + "\n\nResponse style: " + styles[st.session_state.response_style]
    )

    # Responses API accepts role/content messages. Keep only the current chat's history.
    input_messages = [{"role": "system", "content": system_text}]
    for message in history:
        if message["role"] in ("user", "assistant"):
            input_messages.append({"role": message["role"], "content": message["content"]})
    input_messages.append({"role": "user", "content": latest_question})

    request = {
        "model": st.session_state.selected_model,
        "input": input_messages,
    }

    if use_web:
        # OpenAI-hosted web search can retrieve current public-web information.
        request["tools"] = [{"type": "web_search", "search_context_size": "medium"}]
        request["tool_choice"] = "auto"
        request["include"] = ["web_search_call.action.sources"]
        input_messages[0]["content"] += (
            "\n\nWEB RESEARCH RULES: For current/recent information, recent events, software/API troubleshooting, "
            "prices, comparisons, or facts likely to have changed, use web search before answering. Prefer "
            "official documentation, primary sources, and recent reputable reporting. Cross-check important "
            "claims when possible. Cite sources next to the claims they support; never invent a source. "
            "If search is inconclusive, say what could not be verified. Do not search unnecessarily for stable facts."
        )

    response = client.responses.create(**request)
    return get_response_text(response), get_citations(response)


# -------------------- API KEY POPUP --------------------
@st.dialog(" ", width="small")
def key_dialog():
    st.markdown(
        """
        <div class="welcome-card">
          <div class="welcome-robot-wrap">
            <div class="welcome-robot">✦</div>
            <span class="robot-spark spark-one">✦</span>
            <span class="robot-spark spark-two">✧</span>
          </div>
          <div class="welcome-eyebrow">YOUR PERSONAL AI STUDIO</div>
          <h2 class="welcome-title">Welcome to<br>your <span> NEXORA AI</span></h2>
          <p class="welcome-copy">A smarter space to think, create, and explore. Connect your OpenAI API key to enter your personal AI workspace.</p><div class="welcome-credit">Built by <strong>Atta ur Rehman</strong><span>Student of Sir Iqbal</span></div>
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

    st.markdown('<div class="fine-print">NEXORA AI · Think beyond</div><div class="creator-credit-sidebar">Built by <strong>Atta ur Rehman</strong><br><span>Student of Sir Iqbal</span></div>', unsafe_allow_html=True)

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

# -------------------- MAIN CHAT --------------------
header_col, theme_col = st.columns([7, 1.7], vertical_alignment="center")
with header_col:
    st.markdown(
        """
        <div class="workspace-topbar">
          <div class="workspace-brand"><span class="workspace-mark">✦</span><span>NEXORA <span style="color:#8057f5">AI</span><br><span style="font:500 10px 'DM Sans',sans-serif;color:#958aa4;letter-spacing:.35px">YOUR PERSONAL AI WORKSPACE</span></span></div>
          <div class="workspace-status"><span class="workspace-status-dot"></span> AI workspace ready</div>
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
        """
        <div class="hero">
          <div class="orb-wrap"><div class="orbit"></div><div class="orb-floor-shadow"></div><div class="orb">✦</div><span class="orb-spark orb-spark-a">✦</span><span class="orb-spark orb-spark-b">✧</span></div>
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
    for message in history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if message["role"] == "assistant" and message.get("citations"):
                with st.expander("Sources from the web"):
                    for source in message["citations"]:
                        st.markdown(f"- [{source['title']}]({source['url']})")

st.markdown('<div class="home-footnote">✦ NEXORA AI can make mistakes. For important decisions, check cited sources and verify critical details.</div><div class="creator-credit-main">Built with curiosity by <strong>Atta ur Rehman</strong><span>Student of Sir Iqbal</span></div>', unsafe_allow_html=True)

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
