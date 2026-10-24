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
DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-5.5")
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


def get_api_key():
    return st.session_state.api_key_session.strip() or os.getenv("OPENAI_API_KEY", "").strip()


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
            <div class="welcome-robot">🤖</div>
            <span class="robot-spark spark-one">✦</span>
            <span class="robot-spark spark-two">✧</span>
          </div>
          <div class="welcome-eyebrow">YOUR PERSONAL AI STUDIO</div>
          <h2 class="welcome-title">Welcome to<br>your <span> NEXORA AI</span></h2>
          <p class="welcome-copy">A smarter space to think, create, and explore. Connect your OpenAI API key to get started.</p>
          <div class="welcome-features">
            <span>⚡ Smart answers</span><span>🌐 Web search</span><span>💬 Chat history</span>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    with st.form("nexora_key_form"):
        entered_key = st.text_input("🔑 OpenAI API key", type="password", placeholder="Paste your API key (sk-...)")
        connect = st.form_submit_button("🚀  Unlock NEXORA AI", type="primary", use_container_width=True)
    st.markdown('<div class="welcome-helper">🔒 Your key stays in this active session and is not saved to the source file.</div>', unsafe_allow_html=True)
    st.markdown('<div class="welcome-link">Need a key? <a href="https://platform.openai.com/api-keys" target="_blank">Create an API key ↗</a></div>', unsafe_allow_html=True)
    st.caption("API usage may incur charges. ChatGPT subscriptions do not include API credits.")
    if connect:
        if not entered_key.strip():
            st.error("Please enter your API key to continue.")
        elif not entered_key.strip().startswith("sk-"):
            st.warning("This key format looks unusual. Check that you copied an OpenAI API key.")
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

    st.markdown('<div class="fine-print">NEXORA AI · Think beyond</div>', unsafe_allow_html=True)

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
    if st.button(theme_label, key="theme_toggle_button", use_container_width=True, help="Switch between light/day and dark/night appearance"):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()

active_chat = get_active_chat()
history = active_chat["messages"]

if not history:
    st.markdown(
        """
        <div class="hero">
          <div class="orb-wrap"><div class="orb-halo"></div><div class="orbit"></div><div class="orb">✦</div></div>
          <div class="hero-kicker">✦&nbsp; YOUR IDEAS, WITH MORE CLARITY</div>
          <h1>What are we <span class="gradient-word">working on</span> today?</h1>
          <p class="hero-subtitle">From quick questions to deep research, coding, writing, and planning — start a conversation and turn your next idea into progress.</p>
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

st.markdown('<div class="home-footnote">✦ NEXORA AI can make mistakes. For important decisions, check cited sources and verify critical details.</div>', unsafe_allow_html=True)

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
                active_chat["messages"].pop()
                st.error(
                    "I couldn't generate a response. Check your API key, selected model, "
                    "internet connection, API quota, and whether the model supports web search."
                )
                print(f"NEXORA AI request failed: {type(exc).__name__}")

    st.rerun()
