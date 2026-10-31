"""NEXORA AI - 3D design layer (pure CSS, no JavaScript, no extra dependencies).

Usage in chatgpt.py (after the existing CSS blocks, before the sidebar/chat code):

    from nexora_3d import inject_3d
    inject_3d(st.session_state.get("dark_mode", False))
"""

import streamlit as st

_CUBES = [
    # (css class, left/right, top/bottom, size px, spin seconds)
    ("left:3%;top:20%", 56, 26),
    ("right:4%;top:48%", 74, 34),
    ("left:7%;bottom:16%", 40, 22),
]

_FACES = [
    "rotateY(0deg) translateZ(calc(var(--s)/2))",
    "rotateY(180deg) translateZ(calc(var(--s)/2))",
    "rotateY(90deg) translateZ(calc(var(--s)/2))",
    "rotateY(-90deg) translateZ(calc(var(--s)/2))",
    "rotateX(90deg) translateZ(calc(var(--s)/2))",
    "rotateX(-90deg) translateZ(calc(var(--s)/2))",
]

_CSS = """
<style>
:root{
  --nx3-line:__LINE__; --nx3-face:__FACE__; --nx3-edge:__EDGE__;
  --nx3-shadow:__SHADOW__; --nx3-hi:__HI__; --nx3-thick:__THICK__;
}
@keyframes nx3-grid{from{background-position:0 0}to{background-position:0 64px}}
@keyframes nx3-cube{
  0%{transform:rotateX(18deg) rotateY(0deg) translateY(0)}
  50%{transform:rotateX(198deg) rotateY(180deg) translateY(-18px)}
  100%{transform:rotateX(378deg) rotateY(360deg) translateY(0)}}
@keyframes nx3-ring-a{from{transform:rotateX(68deg) rotateZ(0)}to{transform:rotateX(68deg) rotateZ(360deg)}}
@keyframes nx3-ring-b{from{transform:rotateY(68deg) rotateZ(360deg)}to{transform:rotateY(68deg) rotateZ(0)}}
@keyframes nx3-sway{0%,100%{transform:translateY(0) rotateX(10deg) rotateY(-22deg)}
  50%{transform:translateY(-9px) rotateX(14deg) rotateY(22deg)}}
@keyframes nx3-enter{from{opacity:0;transform:perspective(900px) rotateX(-14deg) translateY(22px) scale(.97)}
  to{opacity:1;transform:perspective(900px) rotateX(0) translateY(0) scale(1)}}
@keyframes nx3-sheen{0%{transform:translateX(-120%)}60%,100%{transform:translateX(120%)}}

/* ---------- stacking: scene sits behind all content ---------- */
html body .stApp [data-testid="stMainBlockContainer"]{position:relative!important;z-index:1!important}
.nx3-scene{position:fixed;inset:0;z-index:-1;pointer-events:none;overflow:hidden;perspective:1100px}
.nx3-floor{position:absolute;left:-60%;right:-60%;bottom:-34%;height:78%;
  transform:rotateX(74deg);transform-origin:50% 100%;
  background-image:linear-gradient(var(--nx3-line) 1px,transparent 1px),
                   linear-gradient(90deg,var(--nx3-line) 1px,transparent 1px);
  background-size:64px 64px;animation:nx3-grid 9s linear infinite;
  -webkit-mask-image:linear-gradient(to top,#000 0%,transparent 78%);
  mask-image:linear-gradient(to top,#000 0%,transparent 78%)}
.nx3-cube{position:absolute;width:var(--s);height:var(--s);transform-style:preserve-3d;
  animation:nx3-cube var(--d) linear infinite;opacity:.9}
.nx3-cube i{position:absolute;inset:0;border:1px solid var(--nx3-edge);border-radius:6px;
  background:linear-gradient(135deg,var(--nx3-face),rgba(237,99,187,.07))}

/* ---------- hero orb: real 3D rings + swaying emblem ---------- */
html body .stApp .orb-wrap{transform-style:preserve-3d!important;perspective:900px!important}
html body .stApp .orb-wrap:before,html body .stApp .orb-wrap:after{
  content:"";position:absolute;left:50%;top:50%;width:124px;height:124px;margin:-62px 0 0 -62px;
  border-radius:50%;pointer-events:none;z-index:1}
html body .stApp .orb-wrap:before{border:1.5px solid rgba(160,120,255,.55);animation:nx3-ring-a 9s linear infinite}
html body .stApp .orb-wrap:after{width:104px;height:104px;margin:-52px 0 0 -52px;
  border:1.5px solid rgba(237,99,187,.5);animation:nx3-ring-b 12s linear infinite}
html body .stApp .orb{animation:nx3-sway 6s ease-in-out infinite!important;
  box-shadow:0 26px 34px rgba(83,54,146,.30),0 2px 0 rgba(255,255,255,.4) inset,
  0 -10px 18px rgba(45,20,100,.28) inset,-6px 0 0 rgba(74,42,145,.35),6px 6px 0 rgba(74,42,145,.2)!important}

/* ---------- depth for every surface ---------- */
html body .stApp [data-testid="stChatMessage"]{
  transform-style:preserve-3d;animation:nx3-enter .5s cubic-bezier(.2,.8,.2,1) both;
  box-shadow:0 1px 0 var(--nx3-hi) inset,0 5px 0 -1px var(--nx3-thick),0 20px 34px var(--nx3-shadow)!important;
  transition:transform .25s ease,box-shadow .25s ease!important}
html body .stApp [data-testid="stChatMessage"]:hover{
  transform:perspective(1000px) rotateX(1.2deg) translateY(-3px)!important}
html body .stApp .workspace-topbar{
  box-shadow:0 1px 0 var(--nx3-hi) inset,0 6px 0 -2px var(--nx3-thick),0 22px 38px var(--nx3-shadow)!important}
html body .stApp .hero-trust-row span,html body .stApp .connection-pill{
  box-shadow:0 1px 0 var(--nx3-hi) inset,0 3px 0 var(--nx3-thick),0 12px 22px var(--nx3-shadow)!important}

/* ---------- tactile 3D buttons ---------- */
html body .stApp .stButton>button:not([kind="primary"]){
  box-shadow:0 1px 0 var(--nx3-hi) inset,0 5px 0 var(--nx3-thick),0 14px 24px var(--nx3-shadow)!important;
  transition:transform .18s cubic-bezier(.2,.8,.2,1),box-shadow .18s ease!important}
html body .stApp .stButton>button:not([kind="primary"]):hover{
  transform:perspective(600px) rotateX(5deg) translateY(-4px)!important;
  box-shadow:0 1px 0 var(--nx3-hi) inset,0 9px 0 var(--nx3-thick),0 22px 32px var(--nx3-shadow)!important}
html body .stApp .stButton>button:active{
  transform:translateY(4px)!important;box-shadow:0 1px 0 var(--nx3-thick),0 4px 8px var(--nx3-shadow)!important}
html body .stApp .stButton>button[kind="primary"]:after{
  content:"";position:absolute;top:0;bottom:0;width:40%;left:0;pointer-events:none;
  background:linear-gradient(100deg,transparent,rgba(255,255,255,.35),transparent);
  animation:nx3-sheen 3.6s ease-in-out infinite}

/* ---------- input bar + sidebar ---------- */
html body .stApp [data-testid="stChatInput"]{
  box-shadow:0 1px 0 var(--nx3-hi) inset,0 6px 0 -1px var(--nx3-thick),0 24px 40px var(--nx3-shadow)!important}
html body .stApp [data-testid="stSidebar"]{box-shadow:10px 0 40px var(--nx3-shadow)!important}
html body .stApp [data-testid="stSidebar"] .brand-icon{
  animation:nx3-sway 7s ease-in-out infinite;
  box-shadow:0 10px 18px rgba(128,87,245,.35),-3px 0 0 rgba(74,42,145,.35),3px 4px 0 rgba(74,42,145,.2)!important}

/* ---------- login / welcome dialog: 3D flip-in + floating emblem ---------- */
html body [data-testid="stDialog"] [role="dialog"]{
  animation:nx3-enter .6s cubic-bezier(.2,.8,.2,1) both!important;transform-style:preserve-3d;
  box-shadow:0 1px 0 var(--nx3-hi) inset,0 10px 0 -3px var(--nx3-thick),0 40px 90px var(--nx3-shadow)!important}
html body [data-testid="stDialog"] .welcome-robot-wrap:before{
  content:"";position:absolute;inset:-14px;border-radius:50%;pointer-events:none;
  border:1.5px solid rgba(160,120,255,.5);animation:nx3-ring-a 8s linear infinite}
html body [data-testid="stDialog"] .welcome-robot{animation:nx3-sway 5s ease-in-out infinite!important}

@media(max-width:700px){
  .nx3-cube{display:none}
  .nx3-floor{height:50%}
  html body .stApp .orb-wrap:before{width:96px;height:96px;margin:-48px 0 0 -48px}
  html body .stApp .orb-wrap:after{width:80px;height:80px;margin:-40px 0 0 -40px}
}
@media(prefers-reduced-motion:reduce){
  .nx3-floor,.nx3-cube,.orb-wrap:before,.orb-wrap:after,[data-testid="stChatMessage"],
  .stButton>button:after,[data-testid="stDialog"] *{animation:none!important}
}
</style>
"""


def inject_3d(dark: bool = False) -> None:
    """Render the 3D background scene and 3D styling for the whole app."""
    p = (
        {
            "LINE": "rgba(176,140,255,.20)", "FACE": "rgba(176,140,255,.16)",
            "EDGE": "rgba(190,160,255,.42)", "SHADOW": "rgba(0,0,0,.42)",
            "HI": "rgba(255,255,255,.07)", "THICK": "rgba(10,6,18,.75)",
        }
        if dark
        else {
            "LINE": "rgba(128,87,245,.15)", "FACE": "rgba(150,110,245,.13)",
            "EDGE": "rgba(128,87,245,.30)", "SHADOW": "rgba(60,38,100,.16)",
            "HI": "rgba(255,255,255,.9)", "THICK": "rgba(214,201,236,.95)",
        }
    )
    css = _CSS
    for key, value in p.items():
        css = css.replace(f"__{key}__", value)

    cubes = "".join(
        f'<div class="nx3-cube" style="{pos};--s:{size}px;--d:{spin}s">'
        + "".join(f'<i style="transform:{f}"></i>' for f in _FACES)
        + "</div>"
        for pos, size, spin in _CUBES
    )
    scene = f'<div class="nx3-scene"><div class="nx3-floor"></div>{cubes}</div>'
    st.markdown(css + scene, unsafe_allow_html=True)