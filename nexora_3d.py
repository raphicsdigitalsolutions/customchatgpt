"""
nexora_3d.py — NEXORA AI 3D / premium visual layer
---------------------------------------------------
Drop this file next to chatgpt.py. It only adds CSS (+ one tiny optional
mouse-parallax script). It does NOT touch your app logic.

Usage in chatgpt.py (call it AFTER your last st.markdown("<style>...") block):

    from nexora_3d import apply_3d_premium_theme, hero_cube_html
    apply_3d_premium_theme(dark=st.session_state.get("dark_mode", False))

Optional: replace  <div class="orb">...</div>  inside .orb-wrap with
    {hero_cube_html()}
to get a real rotating glass cube instead of the flat orb.
"""

import streamlit as st

_TOKENS = {
    "light": {
        "A1": "rgba(167,139,250,.20)", "A2": "rgba(244,143,199,.14)",
        "A3": "rgba(129,140,248,.12)", "A4": "rgba(216,180,254,.16)",
        "GRID": "rgba(128,87,245,.10)", "H1SH": "rgba(95,63,171,.15)",
        "MSG1": "rgba(255,255,255,.94)", "MSG2": "rgba(249,244,255,.80)",
        "USR1": "rgba(240,231,255,.96)", "USR2": "rgba(255,237,248,.84)",
        "USRB": "rgba(190,160,250,.55)", "HL": "rgba(255,255,255,.90)",
        "SH1": "rgba(70,45,120,.26)", "SH2": "rgba(70,45,120,.14)",
        "RING": "rgba(150,110,240,.50)", "DLGSH": "rgba(60,35,110,.32)",
    },
    "dark": {
        "A1": "rgba(120,80,220,.24)", "A2": "rgba(200,70,160,.13)",
        "A3": "rgba(80,90,220,.15)", "A4": "rgba(150,90,230,.15)",
        "GRID": "rgba(170,140,255,.13)", "H1SH": "rgba(150,100,255,.22)",
        "MSG1": "rgba(48,36,64,.96)", "MSG2": "rgba(34,26,46,.90)",
        "USR1": "rgba(72,48,102,.97)", "USR2": "rgba(74,40,80,.92)",
        "USRB": "rgba(140,105,210,.55)", "HL": "rgba(255,255,255,.07)",
        "SH1": "rgba(0,0,0,.55)", "SH2": "rgba(0,0,0,.35)",
        "RING": "rgba(180,150,255,.55)", "DLGSH": "rgba(0,0,0,.70)",
    },
}

_BASE_CSS = """
<style>
:root{--nx-mx:0;--nx-my:0}
.stApp{isolation:isolate!important}
[data-testid="stMainBlockContainer"]{animation:fadeUp .5s cubic-bezier(.2,.8,.2,1) backwards!important}
.orb-wrap{transform-style:preserve-3d!important;transform:rotateX(calc(var(--nx-my)*-4deg)) rotateY(calc(var(--nx-mx)*5deg));transition:transform .5s cubic-bezier(.2,.8,.2,1)}
.orb-wrap::before,.orb-wrap::after{content:"";position:absolute;left:50%;top:50%;border-radius:50%;pointer-events:none;z-index:1}
.orb-wrap::before{width:136px;height:136px;margin:-68px 0 0 -68px;border:1.5px solid __RING__;border-top-color:#ed63bb;border-bottom-color:transparent;animation:nx3d-ring-a 9s linear infinite}
.orb-wrap::after{width:164px;height:164px;margin:-82px 0 0 -82px;border:1px dashed __RING__;border-left-color:#8057f5;animation:nx3d-ring-b 15s linear infinite}
.orbit{opacity:0!important}
@keyframes nx3d-ring-a{from{transform:rotateX(74deg) rotateZ(0deg)}to{transform:rotateX(74deg) rotateZ(360deg)}}
@keyframes nx3d-ring-b{from{transform:rotateY(72deg) rotateZ(360deg)}to{transform:rotateY(72deg) rotateZ(0deg)}}
.hero h1{filter:drop-shadow(0 12px 22px __H1SH__)}
.hero-trust-row span{transition:translate .25s ease,box-shadow .25s ease}
.hero-trust-row span:hover{translate:0 -3px;box-shadow:0 12px 24px -10px __SH1__!important}

/* Optional rotating glass cube for use with hero_cube_html(). */
.nx-cube{position:relative;width:92px;height:92px;transform-style:preserve-3d;animation:nx3d-cube 16s linear infinite;z-index:2;filter:drop-shadow(0 20px 24px rgba(73,46,144,.30))}
.nx-out,.nx-in{position:absolute;inset:0;transform-style:preserve-3d}
.nx-in{inset:27px;animation:nx3d-cube-rev 10s linear infinite}
.nx-out i,.nx-in i{position:absolute;inset:0;display:block}
.nx-out i{border-radius:15px;border:1px solid rgba(255,255,255,.68);background:linear-gradient(145deg,rgba(210,196,255,.42),rgba(128,87,245,.22) 48%,rgba(237,99,187,.30));box-shadow:inset 0 0 24px rgba(255,255,255,.27),inset 0 -10px 18px rgba(28,10,70,.12);backdrop-filter:blur(3px)}
.nx-in i{border-radius:7px;background:linear-gradient(145deg,#e9dcff,#9a6bff 55%,#ed63bb);opacity:.95;box-shadow:inset 0 1px 4px rgba(255,255,255,.55)}
.nx-out i:nth-child(1){transform:translateZ(46px)}
.nx-out i:nth-child(2){transform:rotateY(90deg) translateZ(46px)}
.nx-out i:nth-child(3){transform:rotateY(180deg) translateZ(46px)}
.nx-out i:nth-child(4){transform:rotateY(-90deg) translateZ(46px)}
.nx-out i:nth-child(5){transform:rotateX(90deg) translateZ(46px)}
.nx-out i:nth-child(6){transform:rotateX(-90deg) translateZ(46px)}
.nx-in i:nth-child(1){transform:translateZ(19px)}
.nx-in i:nth-child(2){transform:rotateY(90deg) translateZ(19px)}
.nx-in i:nth-child(3){transform:rotateY(180deg) translateZ(19px)}
.nx-in i:nth-child(4){transform:rotateY(-90deg) translateZ(19px)}
.nx-in i:nth-child(5){transform:rotateX(90deg) translateZ(19px)}
.nx-in i:nth-child(6){transform:rotateX(-90deg) translateZ(19px)}
@keyframes nx3d-cube{from{transform:rotateX(-22deg) rotateY(0deg)}to{transform:rotateX(-22deg) rotateY(360deg)}}
@keyframes nx3d-cube-rev{from{transform:rotate3d(1,1,0,0deg)}to{transform:rotate3d(1,1,0,-360deg)}}

/* Glass chat messages with real depth */
[data-testid="stChatMessage"]{position:relative;background:linear-gradient(150deg,__MSG1__,__MSG2__)!important;border:1px solid var(--nx-line)!important;box-shadow:inset 0 1px 0 __HL__,0 22px 44px -22px __SH1__,0 8px 18px -10px __SH2__!important;-webkit-backdrop-filter:blur(14px);backdrop-filter:blur(14px);transition:translate .3s cubic-bezier(.2,.8,.2,1),box-shadow .3s ease,border-color .3s ease;animation:nx3d-msg-in .55s cubic-bezier(.2,.8,.2,1) backwards!important}
[data-testid="stChatMessage"]:hover{translate:0 -2px;border-color:rgba(160,120,255,.55)!important;box-shadow:inset 0 1px 0 __HL__,0 30px 56px -22px __SH1__,0 10px 22px -10px __SH2__!important}
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]),[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]){background:linear-gradient(150deg,__USR1__,__USR2__)!important;border-color:__USRB__!important}
@keyframes nx3d-msg-in{from{opacity:0;transform:perspective(900px) translateY(18px) rotateX(-7deg) scale(.975)}to{opacity:1;transform:none}}
[data-testid="stChatInput"]{transition:box-shadow .3s ease,border-color .3s ease}
[data-testid="stChatInput"]:focus-within{border-color:rgba(160,120,255,.85)!important;box-shadow:0 0 0 3px rgba(128,87,245,.18),0 22px 46px -14px rgba(128,87,245,.38)!important}
.stButton>button::after,[data-testid="stFormSubmitButton"]>button::after{content:"";position:absolute;top:-10%;left:-70%;width:45%;height:120%;pointer-events:none;background:linear-gradient(100deg,transparent,rgba(255,255,255,.38),transparent);transform:skewX(-20deg);transition:left .7s cubic-bezier(.2,.8,.2,1)}
.stButton>button:hover::after,[data-testid="stFormSubmitButton"]>button:hover::after{left:130%}
.stButton>button:hover,[data-testid="stFormSubmitButton"]>button:hover{transform:perspective(700px) translateY(-3px) rotateX(4deg)!important}
[data-testid="stSidebar"]{box-shadow:18px 0 50px -28px __SH1__!important}
.brand-icon{animation:nx3d-brand 7s ease-in-out infinite!important;transform-style:preserve-3d}
@keyframes nx3d-brand{0%,100%{transform:perspective(160px) rotateY(-14deg) rotateX(6deg)}50%{transform:perspective(160px) rotateY(14deg) rotateX(-4deg)}}
[data-testid="stMain"] [data-testid="stColumn"]{animation:nx3d-card-in .65s cubic-bezier(.2,.8,.2,1) backwards}
[data-testid="stMain"] [data-testid="stColumn"]:nth-child(2){animation-delay:.07s}
[data-testid="stMain"] [data-testid="stColumn"]:nth-child(3){animation-delay:.14s}
[data-testid="stMain"] [data-testid="stColumn"]:nth-child(4){animation-delay:.21s}
@keyframes nx3d-card-in{from{opacity:0;transform:perspective(900px) translateY(18px) rotateX(-9deg) scale(.98)}to{opacity:1;transform:none}}

/* Premium API-key dialog motion, but no injected JavaScript / mouse tracking required. */
[data-testid="stDialog"],[data-baseweb="modal"]{-webkit-backdrop-filter:blur(14px) saturate(1.2);backdrop-filter:blur(14px) saturate(1.2)}
[data-testid="stDialog"] [role="dialog"]{animation:nx3d-dialog-in .65s cubic-bezier(.2,.9,.25,1) both!important;box-shadow:0 42px 92px -30px __DLGSH__,0 18px 40px -18px __SH2__,inset 0 1px 0 __HL__!important}
@keyframes nx3d-dialog-in{from{opacity:0;transform:perspective(1200px) translateY(24px) rotateX(10deg) scale(.97)}to{opacity:1;transform:perspective(1200px) translateY(0) rotateX(0deg) scale(1)}}
.welcome-robot-wrap::before{content:"";position:absolute;inset:-14px;border-radius:50%;pointer-events:none;border:1.5px solid __RING__;border-top-color:#ed63bb;border-bottom-color:transparent;animation:nx3d-ring-a 8s linear infinite}
::selection{background:rgba(128,87,245,.28)}
*{scrollbar-width:thin;scrollbar-color:rgba(140,100,230,.45) transparent}
::-webkit-scrollbar{width:8px;height:8px}
::-webkit-scrollbar-thumb{background:linear-gradient(180deg,#a98bff,#e66cbc);border-radius:99px}
@media(max-width:640px){.orb-wrap::before{width:104px;height:104px;margin:-52px 0 0 -52px}.orb-wrap::after{width:126px;height:126px;margin:-63px 0 0 -63px}.nx-cube{scale:.85}}
@media(prefers-reduced-motion:reduce){.orb-wrap::before,.orb-wrap::after,.welcome-robot-wrap::before,.nx-cube,.nx-in,.brand-icon,[data-testid="stMain"] [data-testid="stColumn"],[data-testid="stChatMessage"],[data-testid="stDialog"] [role="dialog"]{animation:none!important;transition:none!important}.orb-wrap,[data-testid="stDialog"] [role="dialog"]{transform:none!important}}
</style>
"""

def hero_cube_html() -> str:
    """Return markup for a lightweight CSS 3D glass cube."""
    faces = "<i></i>" * 6
    return '<div class="nx-cube" aria-hidden="true"><div class="nx-out">' + faces + '</div><div class="nx-in">' + faces + '</div></div>'

def apply_3d_premium_theme(dark: bool = False, aurora: bool = False, grid_floor: bool = False, tilt: bool = False) -> None:
    """Apply the optional premium 3D layer with no extra JS or moving background by default."""
    tokens = _TOKENS["dark" if dark else "light"]
    css = _BASE_CSS
    # Aurora and perspective floor are intentionally opt-in to avoid background conflicts.
    if aurora:
        css += '<style>.stApp::before{content:"";position:fixed;inset:-15%;z-index:-1;pointer-events:none;background:radial-gradient(38% 34% at 18% 22%,__A1__,transparent 72%),radial-gradient(34% 38% at 82% 18%,__A2__,transparent 72%),radial-gradient(42% 36% at 72% 86%,__A3__,transparent 72%),radial-gradient(30% 30% at 12% 82%,__A4__,transparent 72%);animation:nx3d-aurora 60s ease-in-out infinite alternate}@keyframes nx3d-aurora{from{transform:scale(1)}to{transform:scale(1.06)}}</style>'
    if grid_floor:
        css += '<style>.stApp::after{content:"";position:fixed;left:-60%;right:-60%;bottom:-6vh;height:46vh;z-index:-1;pointer-events:none;background-image:linear-gradient(__GRID__ 1px,transparent 1px),linear-gradient(90deg,__GRID__ 1px,transparent 1px);background-size:64px 64px;transform:perspective(520px) rotateX(64deg);transform-origin:50% 100%;mask-image:linear-gradient(to top,#000 0%,transparent 92%);animation:nx3d-grid 14s linear infinite}@keyframes nx3d-grid{from{background-position:0 0,0 0}to{background-position:0 64px,0 0}}</style>'
    for key, value in tokens.items():
        css = css.replace(f"__{key}__", value)
    st.markdown(css, unsafe_allow_html=True)
    # Mouse parallax is intentionally not injected into the parent page; CSS motion is enough.
