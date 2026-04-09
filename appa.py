import hashlib
import requests
import streamlit as st
from datetime import datetime, timezone

API_URL = (
    "https://script.google.com/macros/s/"
    "AKfycbyNZNOE1DYNbd4GbGTISJsGrnJ4PYCuip0yjSw3Lr8KkD6-kadKI9mfpKNfiAHEWb0Osw/exec"
)
COMMIT_DEADLINE_UTC = datetime(2026, 11, 30, 22, 59, 59, tzinfo=timezone.utc)
REVEAL_OPEN_UTC     = datetime(2024, 10, 21, 22,  0,  0, tzinfo=timezone.utc)

def sha256(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

def now_utc():
    return datetime.now(timezone.utc)

def post(payload):
    try:
        r = requests.post(API_URL, json=payload, timeout=15)
        return r.status_code, r.text
    except Exception as e:
        return None, str(e)

def validate(uni_id, nonce, number):
    if not uni_id.strip():       return "NEOMA ID cannot be empty."
    if not nonce.strip():        return "Nonce cannot be empty."
    if not (0 <= number <= 100): return "Number must be between 0 and 100."
    return None

st.set_page_config(page_title="Beauty Contest", page_icon="🔐", layout="centered")

st.markdown("""
<style>
@font-face {
    font-family: 'Aeonik';
    src: url('https://cdn.jsdelivr.net/gh/GervinFung/aeonik-font@main/fonts/Aeonik-Regular.woff2') format('woff2');
    font-weight: 400;
}
@font-face {
    font-family: 'Aeonik';
    src: url('https://cdn.jsdelivr.net/gh/GervinFung/aeonik-font@main/fonts/Aeonik-Medium.woff2') format('woff2');
    font-weight: 500;
}
@font-face {
    font-family: 'Aeonik';
    src: url('https://cdn.jsdelivr.net/gh/GervinFung/aeonik-font@main/fonts/Aeonik-Bold.woff2') format('woff2');
    font-weight: 700;
}
:root {
    --font: 'Aeonik', 'DM Sans', sans-serif;
    --bg:      #f2f2f2;
    --white:   #ffffff;
    --text:    #0a0a0a;
    --sub:     #555;
    --border:  #ddd;
    --blue:    #0c05f5;
    --blue-bg: #e8e7fe;
    --green:   #00b07a;
    --green-bg:#d6f5eb;
    --red:     #e02020;
    --red-bg:  #fde8e8;
    --r:       14px;
}
* { box-sizing: border-box; }
html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg) !important;
    font-family: var(--font) !important;
    color: var(--text) !important;
}
[data-testid="stHeader"]  { background: transparent !important; }
[data-testid="stSidebar"] { display: none !important; }
footer, #MainMenu { display: none !important; }
.block-container {
    max-width: 500px !important;
    padding: 2.5rem 1.2rem 6rem !important;
    margin: 0 auto !important;
}
.nav { display:flex; justify-content:space-between; align-items:center; margin-bottom:2.8rem; }
.nav-brand { font-size:1.05rem; font-weight:700; letter-spacing:-0.03em; }
.nav-tag { font-size:0.72rem; font-weight:500; color:var(--sub); background:var(--white); border:1px solid var(--border); padding:4px 10px; border-radius:100px; }
.hero { margin-bottom:2.4rem; }
.hero h1 { font-size:2rem !important; font-weight:700 !important; letter-spacing:-0.04em !important; line-height:1.15 !important; margin:0 0 0.5rem !important; color:var(--text) !important; }
.hero p { font-size:0.9rem; color:var(--sub); margin:0; line-height:1.6; }
.chips { display:flex; gap:8px; margin-bottom:2rem; flex-wrap:wrap; }
.chip { display:inline-flex; align-items:center; gap:6px; font-size:0.75rem; font-weight:600; padding:6px 13px; border-radius:100px; }
.chip-dot { width:7px; height:7px; border-radius:50%; }
.chip.on  { background:var(--green-bg); color:var(--green); }
.chip.on  .chip-dot { background:var(--green); }
.chip.off { background:var(--red-bg); color:var(--red); }
.chip.off .chip-dot { background:var(--red); }
.card { background:var(--white); border-radius:var(--r); border:1px solid var(--border); padding:1.6rem 1.6rem 1.4rem; margin-bottom:1rem; }
.card-label { font-size:0.65rem; font-weight:700; letter-spacing:0.1em; text-transform:uppercase; color:var(--sub); margin-bottom:1.1rem; }
.steps { display:flex; flex-direction:column; gap:1rem; padding:0.2rem 0; }
.step { display:flex; gap:13px; align-items:flex-start; }
.step-n { width:26px; height:26px; border-radius:50%; font-size:0.72rem; font-weight:700; display:flex; align-items:center; justify-content:center; flex-shrink:0; margin-top:1px; }
.step-n.b { background:var(--blue-bg); color:var(--blue); }
.step-n.g { background:var(--green-bg); color:var(--green); }
.step-h { font-size:0.88rem; font-weight:600; color:var(--text); }
.step-p { font-size:0.8rem; color:var(--sub); line-height:1.55; margin-top:2px; }
label[data-testid="stWidgetLabel"] > div > p {
    font-family:var(--font) !important; font-size:0.72rem !important; font-weight:700 !important;
    color:var(--sub) !important; text-transform:uppercase !important; letter-spacing:0.08em !important;
}
input[type="text"], input[type="number"], input[type="password"] {
    background:var(--bg) !important; border:1.5px solid #ccc !important; border-radius:10px !important;
    font-family:var(--font) !important; font-size:0.95rem !important; font-weight:500 !important; color:var(--text) !important;
}
input:focus { border-color:var(--blue) !important; box-shadow:0 0 0 3px rgba(12,5,245,0.08) !important; background:var(--white) !important; }
.hash-box { margin-top:1rem; background:var(--bg); border:1.5px solid #c4c2fc; border-radius:10px; padding:0.9rem 1rem; }
.hash-box-title { font-size:0.62rem; font-weight:700; text-transform:uppercase; letter-spacing:0.1em; color:var(--blue); margin-bottom:5px; }
.hash-mono { font-family:'Courier New',monospace; font-size:0.68rem; color:var(--blue); word-break:break-all; line-height:1.65; }
.hash-pre { font-size:0.68rem; color:#999; margin-top:5px; }
.hash-pre code { background:#eee; padding:1px 5px; border-radius:4px; font-size:0.65rem; color:#555; }
.stButton > button {
    font-family:var(--font) !important; font-weight:700 !important; font-size:0.92rem !important;
    letter-spacing:-0.01em !important; border:none !important; border-radius:10px !important;
    padding:0.68rem 1.2rem !important; width:100% !important;
    transition:opacity 0.14s, transform 0.1s !important;
}
.stButton > button:hover  { opacity:0.85 !important; transform:translateY(-1px) !important; }
.stButton > button:active { transform:scale(0.98) !important; }
.btn-commit .stButton > button { background:var(--blue)  !important; color:#fff !important; }
.btn-reveal .stButton > button { background:var(--green) !important; color:#fff !important; }
[data-testid="stAlert"] { border-radius:10px !important; font-size:0.85rem !important; border:none !important; font-family:var(--font) !important; }
details > summary { font-family:var(--font) !important; font-size:0.88rem !important; font-weight:500 !important; }
details { background:var(--white) !important; border:1px solid var(--border) !important; border-radius:var(--r) !important; }
.footer { text-align:center; margin-top:3rem; font-size:0.72rem; color:#bbb; letter-spacing:0.02em; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="nav">
    <div class="nav-brand">NEOMA · Fintech</div>
    <div class="nav-tag">Blockchain 2026</div>
</div>
<div class="hero">
    <h1>Beauty<br>Contest</h1>
    <p>Commit–Reveal scheme — pick the number<br>closest to ⅔ of the class average.</p>
</div>
""", unsafe_allow_html=True)

now         = now_utc()
commit_open = now <= COMMIT_DEADLINE_UTC
reveal_open = now >= REVEAL_OPEN_UTC

st.markdown(f"""
<div class="chips">
    <span class="chip {'on' if commit_open else 'off'}">
        <span class="chip-dot"></span>{'Commit open' if commit_open else 'Commit closed'}
    </span>
    <span class="chip {'on' if reveal_open else 'off'}">
        <span class="chip-dot"></span>{'Reveal open' if reveal_open else 'Reveal closed'}
    </span>
</div>
""", unsafe_allow_html=True)

with st.expander("How does it work?"):
    st.markdown("""
<div class="steps">
  <div class="step"><div class="step-n b">1</div><div>
    <div class="step-h">Commit — lock your number</div>
    <div class="step-p">Choose a number and a secret nonce. The app hashes them with SHA-256 and sends only the hash. Nobody sees your number yet.</div>
  </div></div>
  <div class="step"><div class="step-n g">2</div><div>
    <div class="step-h">Reveal — prove your choice</div>
    <div class="step-p">After the deadline, reveal your number and nonce. The server checks the hash matches.</div>
  </div></div>
  <div class="step"><div class="step-n b">3</div><div>
    <div class="step-h">Winner — closest to ⅔ × average</div>
    <div class="step-p">The player nearest to <strong>⅔ of the class average</strong> wins.</div>
  </div></div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="card"><div class="card-label">Your details</div>', unsafe_allow_html=True)
uni_id = st.text_input("NEOMA ID", placeholder="e.g. S033001234567X")
number = st.number_input("Number (0 – 100)", min_value=0, max_value=100, value=50, step=1)
nonce  = st.text_input("Secret nonce", placeholder="e.g. MySecret42", type="password")

if uni_id.strip() and nonce.strip():
    preimage    = f"{uni_id.strip()}|{int(number)}|{nonce.strip()}"
    commit_hash = sha256(preimage)
    st.markdown(f"""
    <div class="hash-box">
        <div class="hash-box-title">SHA-256 hash</div>
        <div class="hash-mono">{commit_hash}</div>
        <div class="hash-pre">Preimage: <code>{preimage}</code></div>
    </div>""", unsafe_allow_html=True)
else:
    st.markdown('<p style="font-size:0.8rem;color:#bbb;margin-top:0.5rem;font-style:italic;">Enter your ID and nonce to see the hash.</p>', unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

st.markdown('<div class="card"><div class="card-label">Phase 1 — Commit</div>', unsafe_allow_html=True)
st.caption("Your number stays hidden. Only the hash is sent.")
st.markdown('<div class="btn-commit">', unsafe_allow_html=True)
if st.button("Lock in my commit →", key="btn_commit"):
    err = validate(uni_id, nonce, number)
    if not commit_open:
        st.error("⛔ The commit window is closed.")
    elif err:
        st.error(f"❌ {err}")
    else:
        preimage = f"{uni_id.strip()}|{int(number)}|{nonce.strip()}"
        h = sha256(preimage)
        with st.spinner("Sending…"):
            status, text = post({"kind": "commit", "uni_id": uni_id.strip(), "commit": h})
        if status == 200:
            st.success(f"✅ Commit sent! (HTTP {status})")
            st.markdown(f'<div class="hash-box"><div class="hash-box-title">Save this hash!</div><div class="hash-mono">{h}</div></div>', unsafe_allow_html=True)
            st.info(f"Server: {text}")
        else:
            st.error(f"❌ Error (HTTP {status}): {text}")
st.markdown("</div></div>", unsafe_allow_html=True)

st.markdown('<div class="card"><div class="card-label">Phase 2 — Reveal</div>', unsafe_allow_html=True)
st.caption("Reveal your number and nonce after the commit deadline.")
st.markdown('<div class="btn-reveal">', unsafe_allow_html=True)
if st.button("Reveal my number →", key="btn_reveal"):
    err = validate(uni_id, nonce, number)
    if not reveal_open:
        st.error("⛔ The reveal window is not open yet.")
    elif err:
        st.error(f"❌ {err}")
    else:
        with st.spinner("Sending…"):
            status, text = post({"kind": "reveal", "uni_id": uni_id.strip(), "number": int(number), "nonce": nonce.strip()})
        if status == 200:
            st.success(f"✅ Reveal accepted! (HTTP {status})")
            st.info(f"Server: {text}")
        else:
            st.error(f"❌ Error (HTTP {status}): {text}")
st.markdown("</div></div>", unsafe_allow_html=True)

st.markdown('<div class="footer">NEOMA Business School · Blockchain & Fintech · 2026</div>', unsafe_allow_html=True)
