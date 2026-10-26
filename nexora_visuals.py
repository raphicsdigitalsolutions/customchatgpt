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
        "A1": "rgba(37,170,177,.19)", "A2": "rgba(201,162,80,.17)",
        "A3": "rgba(26,125,137,.13)", "A4": "rgba(230,198,127,.18)",
        "GRID": "rgba(20,125,137,.11)", "H1SH": "rgba(20,98,113,.16)",
        "MSG1": "rgba(255,255,255,.96)", "MSG2": "rgba(243,247,241,.88)",
        "USR1": "rgba(223,241,237,.98)", "USR2": "rgba(243,237,220,.94)",
        "USRB": "rgba(103,164,157,.46)", "HL": "rgba(255,255,255,.92)",
        "SH1": "rgba(25,81,92,.23)", "SH2": "rgba(25,81,92,.13)",
        "RING": "rgba(20,125,137,.44)", "DLGSH": "rgba(22,59,68,.24)",
    },
    "dark": {
        "A1": "rgba(58,207,205,.25)", "A2": "rgba(224,190,112,.20)",
        "A3": "rgba(40,139,160,.19)", "A4": "rgba(236,211,149,.17)",
        "GRID": "rgba(102,215,215,.13)", "H1SH": "rgba(57,180,195,.20)",
        "MSG1": "rgba(20,41,53,.97)", "MSG2": "rgba(12,28,39,.94)",
        "USR1": "rgba(22,63,72,.97)", "USR2": "rgba(63,57,41,.85)",
        "USRB": "rgba(91,185,183,.48)", "HL": "rgba(232,246,239,.09)",
        "SH1": "rgba(0,0,0,.48)", "SH2": "rgba(0,0,0,.30)",
        "RING": "rgba(101,220,215,.54)", "DLGSH": "rgba(0,0,0,.66)",
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

/* NEXORA's own glass-shell assistant with low-amplitude 3D idle motion. */
.nx-robot-stage{position:relative!important;display:grid!important;place-items:center!important;min-width:0;overflow:visible!important;perspective:1000px!important;isolation:isolate}
.nx-hero-robot{--bot-a:#fbfff8;--bot-b:#7ab8b0;--bot-c:#d7b56c;--bot-eye:#a5fff0;position:relative;width:min(100%,360px);height:100%;min-height:220px;display:grid;place-items:center;perspective:1000px;transform-style:preserve-3d;isolation:isolate}
.nx-theme-dark .nx-hero-robot{--bot-a:#e6fff7;--bot-b:#378e91;--bot-c:#d6b76f;--bot-eye:#b6fff4}
.nx-robot-aura{position:absolute;width:74%;aspect-ratio:1;border-radius:50%;background:radial-gradient(circle,rgba(69,195,186,.25),rgba(219,183,107,.12) 43%,transparent 72%);filter:blur(12px);animation:nx-robot-aura 5s ease-in-out infinite}
.nx-robot-orbit{position:absolute;z-index:1;left:50%;top:48%;border:1px solid rgba(50,161,162,.48);border-radius:50%;pointer-events:none;transform-style:preserve-3d}
.nx-robot-orbit-a{width:80%;height:28%;margin:-14% 0 0 -40%;transform:rotateX(68deg) rotateZ(-18deg);border-top-color:rgba(220,186,109,.94);border-bottom-color:transparent;animation:nx-robot-orbit-a 14s linear infinite}
.nx-robot-orbit-b{width:66%;height:66%;margin:-33% 0 0 -33%;transform:rotateY(68deg) rotateZ(24deg);border-style:dashed;border-left-color:rgba(211,175,101,.72);animation:nx-robot-orbit-b 19s linear infinite reverse}
.nx-robot-orbit-c{width:94%;height:38%;margin:-19% 0 0 -47%;transform:rotateX(72deg) rotateZ(38deg);border-color:rgba(111,216,207,.30);animation:nx-robot-orbit-c 23s linear infinite}
.nx-robot-node{position:absolute;z-index:4;width:8px;height:8px;border-radius:50%;background:#e2c373;box-shadow:0 0 15px rgba(221,190,119,.95);top:24%;right:17%;animation:nx-robot-node 3.2s ease-in-out infinite}
.nx-robot-node-b{width:5px;height:5px;top:auto;right:auto;left:17%;bottom:27%;background:#81e8dd;box-shadow:0 0 14px rgba(93,222,208,.95);animation-delay:-1.5s}
.nx-robot-figure{position:relative;z-index:3;width:clamp(190px,22vw,270px);max-width:88%;aspect-ratio:260/300;display:grid;place-items:center;transform-style:preserve-3d;filter:drop-shadow(0 25px 24px rgba(8,42,50,.30));animation:nx-robot-float 6.2s ease-in-out infinite}
.nx-robot-figure svg{display:block;width:100%;height:100%;overflow:visible;transform:rotateY(-8deg) rotateX(3deg);transform-style:preserve-3d}
.nx-bot-head{transform-box:fill-box;transform-origin:50% 82%;animation:nx-robot-look 8s ease-in-out infinite}
.nx-bot-arm-left{transform-box:fill-box;transform-origin:86% 23%;animation:nx-robot-wave 7s ease-in-out infinite}
.nx-bot-arm-right{transform-box:fill-box;transform-origin:14% 23%;animation:nx-robot-arm 6.2s ease-in-out infinite}
.nx-bot-eye{transform-box:fill-box;transform-origin:center;animation:nx-robot-blink 5.8s ease-in-out infinite}
.nx-robot-status{position:absolute;z-index:5;left:50%;bottom:5px;display:flex;align-items:center;gap:7px;padding:6px 10px;border:1px solid rgba(92,174,171,.25);border-radius:999px;background:rgba(251,255,248,.72);color:#42666a;font:700 9px/1 'DM Sans',sans-serif;letter-spacing:1.1px;white-space:nowrap;box-shadow:0 9px 24px rgba(18,67,73,.12),inset 0 1px 0 rgba(255,255,255,.8);backdrop-filter:blur(9px);transform:translateX(-50%) translateZ(24px)}
.nx-robot-status:before{content:"";width:6px;height:6px;border-radius:50%;background:#37bd91;box-shadow:0 0 10px rgba(55,189,145,.9)}
.nx-theme-dark .nx-robot-status{background:rgba(9,29,39,.76);color:#d8eee8;border-color:rgba(108,207,199,.28)}
@keyframes nx-robot-float{0%,100%{transform:translate3d(0,2px,18px) rotateX(2deg) rotateY(-4deg)}50%{transform:translate3d(0,-8px,22px) rotateX(-1deg) rotateY(5deg)}}
@keyframes nx-robot-look{0%,100%{transform:rotateZ(0) translateY(0)}28%{transform:rotateZ(-2deg) translateY(-1px)}55%{transform:rotateZ(1.5deg) translateY(1px)}78%{transform:rotateZ(0)}}
@keyframes nx-robot-wave{0%,72%,100%{transform:rotate(0)}80%{transform:rotate(-7deg)}86%{transform:rotate(4deg)}92%{transform:rotate(-3deg)}}
@keyframes nx-robot-arm{0%,100%{transform:rotate(0)}50%{transform:rotate(-4deg)}}
@keyframes nx-robot-blink{0%,44%,47%,92%,95%,100%{transform:scaleY(1)}45%,46%,93%,94%{transform:scaleY(.12)}}
@keyframes nx-robot-aura{0%,100%{opacity:.56;transform:scale(.92)}50%{opacity:1;transform:scale(1.08)}}
@keyframes nx-robot-orbit-a{from{transform:rotateX(68deg) rotateZ(-18deg)}to{transform:rotateX(68deg) rotateZ(342deg)}}
@keyframes nx-robot-orbit-b{from{transform:rotateY(68deg) rotateZ(24deg)}to{transform:rotateY(68deg) rotateZ(384deg)}}
@keyframes nx-robot-orbit-c{from{transform:rotateX(72deg) rotateZ(38deg)}to{transform:rotateX(72deg) rotateZ(-322deg)}}
@keyframes nx-robot-node{0%,100%{opacity:.55;transform:scale(.8)}50%{opacity:1;transform:scale(1.3)}}
@media(prefers-reduced-motion:reduce){.nx-robot-aura,.nx-robot-orbit,.nx-robot-node,.nx-robot-figure,.nx-bot-head,.nx-bot-arm-left,.nx-bot-arm-right,.nx-bot-eye{animation:none!important;transition:none!important}.nx-robot-figure,.nx-robot-figure svg{transform:none!important}}


/* Optional rotating glass cube for use with hero_cube_html(). */
.nx-cube{
  position:relative;width:112px;height:112px;flex:0 0 112px;
  transform-style:preserve-3d;transform-origin:50% 50%;
  animation:nx3d-cube 18s cubic-bezier(.45,0,.55,1) infinite;
  z-index:2;filter:drop-shadow(0 27px 26px rgba(22,10,55,.38));
  isolation:isolate;
}
.nx-out,.nx-in{position:absolute;inset:0;transform-style:preserve-3d}
.nx-in{inset:31px;animation:nx3d-cube-rev 15s linear infinite}
.nx-out i,.nx-in i{
  position:absolute;inset:0;display:block;box-sizing:border-box;
  backface-visibility:hidden;-webkit-backface-visibility:hidden;
  transform-style:preserve-3d;overflow:hidden;
}
.nx-out i{
  border:1px solid rgba(248,245,255,.72);
  background:linear-gradient(145deg,rgba(176,146,255,.55),rgba(64,38,130,.72));
  box-shadow:inset 0 0 20px rgba(255,255,255,.15),inset 0 -12px 22px rgba(4,3,21,.26);
  backdrop-filter:blur(5px);-webkit-backdrop-filter:blur(5px);
}
/* Each plane has its own material and luminance so the object reads as a cube, not a flat glyph. */
.nx-out i:nth-child(1){
  border-radius:16px;
  background:radial-gradient(ellipse at 28% 18%,rgba(255,255,255,.58),transparent 26%),
    linear-gradient(145deg,rgba(153,119,255,.60),rgba(39,25,79,.92) 72%);
  box-shadow:inset 0 0 26px rgba(200,177,255,.28),inset 0 -14px 22px rgba(0,0,0,.32),inset 1px 1px 0 rgba(255,255,255,.6);
}
.nx-out i:nth-child(2){
  border-radius:13px;
  background:linear-gradient(135deg,rgba(99,226,244,.40),rgba(24,58,93,.96) 48%,rgba(43,22,81,.97));
  box-shadow:inset 0 0 24px rgba(84,232,255,.20),inset -12px 0 18px rgba(0,0,0,.35);
}
.nx-out i:nth-child(3){
  border-radius:13px;
  background:linear-gradient(145deg,rgba(69,49,118,.94),rgba(15,13,35,.98));
  box-shadow:inset 0 0 22px rgba(126,97,255,.15),inset 0 -16px 20px rgba(0,0,0,.42);
}
.nx-out i:nth-child(4){
  border-radius:13px;
  background:linear-gradient(135deg,rgba(236,104,213,.45),rgba(84,34,107,.92) 48%,rgba(30,18,64,.98));
  box-shadow:inset 0 0 24px rgba(246,108,220,.18),inset 12px 0 18px rgba(0,0,0,.25);
}
.nx-out i:nth-child(5){
  border-radius:14px;
  background:linear-gradient(145deg,rgba(255,255,255,.82),rgba(154,135,218,.74) 35%,rgba(69,66,129,.88));
  box-shadow:inset 0 0 24px rgba(255,255,255,.38),inset 0 -12px 15px rgba(35,22,85,.24);
}
.nx-out i:nth-child(6){
  border-radius:13px;
  background:linear-gradient(145deg,rgba(22,21,52,.98),rgba(8,10,28,.99));
  box-shadow:inset 0 0 24px rgba(92,88,180,.12),inset 0 14px 19px rgba(0,0,0,.4);
}
.nx-in i{
  border:1px solid rgba(255,255,255,.8);border-radius:7px;
  background:radial-gradient(circle at 28% 18%,#fff,transparent 23%),
    linear-gradient(145deg,#9df5ff 0%,#8a6aff 48%,#f16dd1 100%);
  opacity:.98;
  box-shadow:0 0 18px rgba(135,105,255,.42),inset 0 1px 5px rgba(255,255,255,.85),inset 0 -6px 10px rgba(47,21,96,.24);
}
.nx-out i:nth-child(1){transform:translateZ(56px)}
.nx-out i:nth-child(2){transform:rotateY(90deg) translateZ(56px)}
.nx-out i:nth-child(3){transform:rotateY(180deg) translateZ(56px)}
.nx-out i:nth-child(4){transform:rotateY(-90deg) translateZ(56px)}
.nx-out i:nth-child(5){transform:rotateX(90deg) translateZ(56px)}
.nx-out i:nth-child(6){transform:rotateX(-90deg) translateZ(56px)}
.nx-in i:nth-child(1){transform:translateZ(25px)}
.nx-in i:nth-child(2){transform:rotateY(90deg) translateZ(25px)}
.nx-in i:nth-child(3){transform:rotateY(180deg) translateZ(25px)}
.nx-in i:nth-child(4){transform:rotateY(-90deg) translateZ(25px)}
.nx-in i:nth-child(5){transform:rotateX(90deg) translateZ(25px)}
.nx-in i:nth-child(6){transform:rotateX(-90deg) translateZ(25px)}
/* Removed the oversized transparent plate that made the cube look mounted on a panel. */
.nx-cube:after{
  content:"✦";position:absolute;left:50%;top:50%;width:40px;height:40px;
  display:grid;place-items:center;transform:translate(-50%,-50%) translateZ(57px);
  color:#fff;font-size:30px;line-height:1;text-shadow:0 0 9px rgba(255,255,255,.9),0 0 24px rgba(138,108,255,.95);
  pointer-events:none;backface-visibility:hidden;
}
@keyframes nx3d-cube{
  0%,100%{transform:rotateX(-12deg) rotateY(-24deg) rotateZ(-2deg) translateY(0)}
  25%{transform:rotateX(4deg) rotateY(-8deg) rotateZ(1deg) translateY(-3px)}
  50%{transform:rotateX(12deg) rotateY(24deg) rotateZ(2deg) translateY(-5px)}
  75%{transform:rotateX(-3deg) rotateY(8deg) rotateZ(-1deg) translateY(-2px)}
}
@keyframes nx3d-cube-rev{
  from{transform:rotate3d(1,1,0,0deg)}
  to{transform:rotate3d(1,1,0,-360deg)}
}

/* Continuously animated glass reactor for the top-right app header. */
.nx-header-reactor{
  position:relative;display:grid;place-items:center;flex:0 0 94px;width:94px;height:82px;
  perspective:700px;transform-style:preserve-3d;isolation:isolate;overflow:visible;
}
.nx-header-reactor:before{
  content:"";position:absolute;left:50%;top:50%;width:78px;height:78px;margin:-39px 0 0 -39px;
  border-radius:50%;background:radial-gradient(circle,__A1__,transparent 68%);filter:blur(4px);
  opacity:.8;pointer-events:none;animation:nx-reactor-aura 5s ease-in-out infinite;
}
.nx-reactor-ring{
  position:absolute;left:50%;top:50%;border-radius:50%;pointer-events:none;
  border:1px solid __RING__;transform-style:preserve-3d;backface-visibility:visible;
}
.nx-reactor-ring-a{
  width:72px;height:32px;margin:-16px 0 0 -36px;border-top-color:#e879d2;border-bottom-color:rgba(112,230,246,.6);
  animation:nx-reactor-spin-a 7s linear infinite;
}
.nx-reactor-ring-b{
  width:68px;height:68px;margin:-34px 0 0 -34px;border-left-color:#7ce8f1;border-right-color:rgba(182,142,255,.35);
  animation:nx-reactor-spin-b 9s linear infinite;
}
.nx-reactor-ring-c{
  width:86px;height:40px;margin:-20px 0 0 -43px;border-style:dashed;border-color:rgba(177,145,255,.45);
  animation:nx-reactor-spin-c 13s linear infinite;
}
.nx-reactor-cube{position:absolute;z-index:2;width:38px;height:38px;transform-style:preserve-3d;animation:nx-reactor-cube-spin 12s linear infinite}
.nx-reactor-cube i{
  position:absolute;inset:0;display:block;border:1px solid rgba(255,255,255,.78);border-radius:7px;
  background:linear-gradient(145deg,__A1__,rgba(30,22,62,.74));
  box-shadow:inset 0 0 12px rgba(255,255,255,.22),inset 0 -8px 11px rgba(0,0,0,.23);
  backface-visibility:visible;-webkit-backface-visibility:visible;
}
.nx-reactor-cube i:nth-child(2){background:linear-gradient(145deg,__A2__,rgba(31,31,78,.78))}
.nx-reactor-cube i:nth-child(3){background:linear-gradient(145deg,__A3__,rgba(27,20,58,.82))}
.nx-reactor-cube i:nth-child(4){background:linear-gradient(145deg,__A4__,rgba(50,23,68,.78))}
.nx-reactor-cube i:nth-child(5){background:linear-gradient(145deg,rgba(255,255,255,.62),__A1__)}
.nx-reactor-cube i:nth-child(6){background:linear-gradient(145deg,rgba(20,18,47,.9),__A3__)}
.nx-reactor-cube i:nth-child(1){transform:translateZ(19px)}
.nx-reactor-cube i:nth-child(2){transform:rotateY(90deg) translateZ(19px)}
.nx-reactor-cube i:nth-child(3){transform:rotateY(180deg) translateZ(19px)}
.nx-reactor-cube i:nth-child(4){transform:rotateY(-90deg) translateZ(19px)}
.nx-reactor-cube i:nth-child(5){transform:rotateX(90deg) translateZ(19px)}
.nx-reactor-cube i:nth-child(6){transform:rotateX(-90deg) translateZ(19px)}
.nx-reactor-core{
  position:relative;z-index:3;display:grid;place-items:center;width:25px;height:25px;border-radius:50%;
  color:#fff;font-size:13px;line-height:1;transform:translateZ(21px);
  background:radial-gradient(circle at 27% 19%,#fff 0%,#dcd0ff 7%,#9b7cff 25%,#6341cc 54%,#1e1743 78%,#ec7bdb 100%);
  border:1px solid rgba(255,255,255,.74);
  box-shadow:0 8px 16px rgba(81,51,157,.32),0 0 25px rgba(133,107,255,.48),
    inset 0 2px 3px rgba(255,255,255,.82),inset 0 -5px 8px rgba(8,7,34,.45);
  transform-style:preserve-3d;animation:nx-reactor-hover 4.5s ease-in-out infinite,nx-reactor-glow 4s ease-in-out infinite;
}
.nx-reactor-core:after{
  content:"";position:absolute;inset:4px;border-radius:50%;border:1px solid rgba(255,255,255,.3);
  box-shadow:inset 0 0 8px rgba(255,255,255,.15);pointer-events:none;
}
.nx-reactor-node{position:absolute;z-index:4;width:6px;height:6px;border-radius:50%;background:#91f5fa;box-shadow:0 0 10px rgba(105,233,246,.95);top:9px;right:11px;animation:nx-reactor-node 3s ease-in-out infinite;}
.nx-reactor-node-b{top:auto;right:auto;left:11px;bottom:9px;width:4px;height:4px;background:#f3a6ec;box-shadow:0 0 9px rgba(243,166,236,.95);animation-delay:-1.4s}
.nx-header-reactor:after{content:"";position:absolute;bottom:2px;left:50%;width:36px;height:7px;margin-left:-18px;border-radius:50%;background:rgba(103,80,180,.30);filter:blur(5px);}
@keyframes nx-reactor-aura{0%,100%{opacity:.48;transform:scale(.86)}50%{opacity:.95;transform:scale(1.12)}}
@keyframes nx-reactor-cube-spin{from{transform:rotateX(-18deg) rotateY(0deg) rotateZ(0deg)}to{transform:rotateX(342deg) rotateY(360deg) rotateZ(180deg)}}
@keyframes nx-reactor-spin-a{from{transform:rotateX(68deg) rotateZ(0deg)}to{transform:rotateX(68deg) rotateZ(360deg)}}
@keyframes nx-reactor-spin-b{from{transform:rotateY(68deg) rotateZ(360deg)}to{transform:rotateY(68deg) rotateZ(0deg)}}
@keyframes nx-reactor-spin-c{from{transform:rotateX(72deg) rotateZ(0deg)}to{transform:rotateX(72deg) rotateZ(-360deg)}}
@keyframes nx-reactor-hover{0%,100%{transform:translateZ(21px) translateY(0) rotateX(7deg) rotateY(-9deg)}50%{transform:translateZ(21px) translateY(-4px) rotateX(-4deg) rotateY(10deg)}}
@keyframes nx-reactor-glow{0%,100%{filter:brightness(1);box-shadow:0 8px 16px rgba(81,51,157,.28),0 0 18px rgba(133,107,255,.23),inset 0 2px 3px rgba(255,255,255,.82),inset 0 -5px 8px rgba(8,7,34,.45)}50%{filter:brightness(1.13);box-shadow:0 9px 18px rgba(81,51,157,.32),0 0 27px rgba(133,107,255,.38),inset 0 2px 3px rgba(255,255,255,.9),inset 0 -5px 8px rgba(8,7,34,.45)}}
@keyframes nx-reactor-node{0%,100%{opacity:.5;transform:scale(.8)}50%{opacity:1;transform:scale(1.25)}}
@media(max-width:900px){.nx-header-reactor{flex-basis:64px;width:64px;height:58px;scale:.86;margin:0 -3px}}
@media(max-width:640px){.nx-header-reactor{flex-basis:42px;width:42px;height:46px;scale:.72;margin:0 -6px}.nx-reactor-ring-c{opacity:.6}}
@media(prefers-reduced-motion:reduce){.nx-header-reactor:before,.nx-reactor-ring,.nx-reactor-cube,.nx-reactor-core,.nx-reactor-node{animation:none!important}}

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
@media(max-width:640px){.orb-wrap::before{width:104px;height:104px;margin:-52px 0 0 -52px}.orb-wrap::after{width:126px;height:126px;margin:-63px 0 0 -63px}.nx-cube{scale:.76;width:112px;height:112px}}
@media(prefers-reduced-motion:reduce){.orb-wrap::before,.orb-wrap::after,.welcome-robot-wrap::before,.nx-cube,.nx-in,.brand-icon,[data-testid="stMain"] [data-testid="stColumn"],[data-testid="stChatMessage"],[data-testid="stDialog"] [role="dialog"]{animation:none!important;transition:none!important}.orb-wrap,[data-testid="stDialog"] [role="dialog"]{transform:none!important}}
</style>
"""

def hero_cube_html() -> str:
    """Return markup for a lightweight CSS 3D glass cube."""
    faces = "<i></i>" * 6
    return '<div class="nx-cube" aria-hidden="true"><div class="nx-out">' + faces + '</div><div class="nx-in">' + faces + '</div></div>'

def header_reactor_html() -> str:
    """Return an accessible, lightweight, continuously animated 3D reactor for the app header."""
    faces = "<i></i>" * 6
    return (
        '<div class="nx-header-reactor" role="img" aria-label="Continuously rotating 3D NEXORA energy core">'
        '<div class="nx-reactor-ring nx-reactor-ring-a"></div>'
        '<div class="nx-reactor-ring nx-reactor-ring-b"></div>'
        '<div class="nx-reactor-ring nx-reactor-ring-c"></div>'
        '<div class="nx-reactor-cube" aria-hidden="true">' + faces + '</div>'
        '<div class="nx-reactor-core">✦</div>'
        '<span class="nx-reactor-node"></span>'
        '<span class="nx-reactor-node nx-reactor-node-b"></span>'
        '</div>'
    )





def hero_robot_html() -> str:
    """Return accessible markup for the theme-aware animated assistant robot."""
    return """
    <div class="nx-hero-robot" role="img" aria-label="NEXORA AI assistant robot">
      <span class="nx-robot-aura"></span><span class="nx-robot-orbit nx-robot-orbit-a"></span>
      <span class="nx-robot-orbit nx-robot-orbit-b"></span><span class="nx-robot-orbit nx-robot-orbit-c"></span>
      <span class="nx-robot-node"></span><span class="nx-robot-node nx-robot-node-b"></span>
      <div class="nx-robot-figure" aria-hidden="true">
        <svg viewBox="0 0 260 300" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <linearGradient id="nx-robot-shell" x1="0" y1="0" x2="1" y2="1"><stop offset="0" style="stop-color:var(--bot-a)"/><stop offset=".48" style="stop-color:var(--bot-b)"/><stop offset="1" style="stop-color:var(--bot-c)"/></linearGradient>
            <linearGradient id="nx-robot-side" x1="0" y1="0" x2="1" y2="1"><stop offset="0" style="stop-color:var(--bot-b)"/><stop offset="1" style="stop-color:var(--bot-a)"/></linearGradient>
            <linearGradient id="nx-robot-face" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#193b46"/><stop offset="1" stop-color="#081c29"/></linearGradient>
            <radialGradient id="nx-robot-glass" cx=".25" cy=".12" r=".9"><stop offset="0" stop-color="#fff" stop-opacity=".82"/><stop offset=".4" stop-color="#d8fff2" stop-opacity=".16"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>
          </defs>
          <ellipse cx="130" cy="274" rx="68" ry="12" fill="#0b3039" opacity=".16"/><ellipse cx="130" cy="271" rx="48" ry="7" fill="#66cfc4" opacity=".35"/>
          <g class="nx-bot-arm-left"><rect x="43" y="157" width="42" height="91" rx="20" fill="url(#nx-robot-side)" stroke="#f4fff7" stroke-opacity=".74" stroke-width="2"/><rect x="52" y="170" width="24" height="56" rx="12" fill="url(#nx-robot-glass)"/><circle cx="64" cy="238" r="10" fill="url(#nx-robot-shell)" stroke="#e5fff6" stroke-opacity=".65" stroke-width="2"/></g>
          <g class="nx-bot-arm-right"><rect x="175" y="157" width="42" height="91" rx="20" fill="url(#nx-robot-side)" stroke="#f4fff7" stroke-opacity=".74" stroke-width="2"/><rect x="184" y="170" width="24" height="56" rx="12" fill="url(#nx-robot-glass)"/><circle cx="196" cy="238" r="10" fill="url(#nx-robot-shell)" stroke="#e5fff6" stroke-opacity=".65" stroke-width="2"/></g>
          <rect x="112" y="129" width="36" height="35" rx="14" fill="url(#nx-robot-side)" stroke="#f4fff7" stroke-opacity=".75" stroke-width="2"/>
          <rect x="78" y="149" width="104" height="111" rx="34" fill="url(#nx-robot-shell)" stroke="#f5fff8" stroke-opacity=".9" stroke-width="2.5"/>
          <path d="M91 170Q130 145 169 170v24q-39-20-78 0Z" fill="url(#nx-robot-glass)"/>
          <rect x="91" y="181" width="78" height="58" rx="20" fill="#092633" fill-opacity=".82" stroke="#e3fff4" stroke-opacity=".42" stroke-width="1.5"/>
          <circle cx="130" cy="210" r="12" fill="url(#nx-robot-shell)"/><path d="M130 201l3 7 7 2-7 3-3 7-3-7-7-3 7-2Z" fill="#f2d990"/>
          <g class="nx-bot-head"><path d="M130 45V31" stroke="#91e9db" stroke-width="5" stroke-linecap="round"/><circle cx="130" cy="26" r="8" fill="#d7b66e" stroke="#fff6d8" stroke-width="2"/>
            <rect x="53" y="47" width="154" height="105" rx="37" fill="url(#nx-robot-shell)" stroke="#f9fff8" stroke-opacity=".96" stroke-width="3"/>
            <path d="M68 65q62-29 124 0v27Q130 66 68 92Z" fill="url(#nx-robot-glass)"/>
            <rect x="70" y="66" width="120" height="66" rx="25" fill="url(#nx-robot-face)" stroke="#e7fff5" stroke-opacity=".48" stroke-width="1.5"/>
            <rect class="nx-bot-eye" x="94" y="87" width="13" height="22" rx="7" fill="var(--bot-eye)" style="filter:drop-shadow(0 0 7px var(--bot-eye))"/>
            <rect class="nx-bot-eye" x="153" y="87" width="13" height="22" rx="7" fill="var(--bot-eye)" style="filter:drop-shadow(0 0 7px var(--bot-eye))"/>
            <path d="M112 116q18 12 36 0" fill="none" stroke="#d1fff3" stroke-width="2.5" stroke-linecap="round"/>
          </g>
          <path d="M93 260l-5 13q-2 6 5 8h23q6-1 5-7l-2-14Zm48 0-2 14q-1 6 5 7h23q7-2 4-8l-4-13Z" fill="url(#nx-robot-side)" stroke="#f6fff8" stroke-opacity=".8" stroke-width="2"/>
        </svg>
      </div><span class="nx-robot-status">NEXORA · READY</span>
    </div>
    """.strip()

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
