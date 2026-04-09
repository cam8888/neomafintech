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
:root {
    --font: 'Aeonik', sans-serif;
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
    --pastel-pink: #D87093; /* Un rose pastel un peu soutenu pour la lisibilité */
    --r:       14px;
}
* { box-sizing: border-box; }
html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg) !important;
    font-family: var(--font) !important;
}
[data-testid="stHeader"]  { background: transparent !important; }
[data-testid="stSidebar"] { display: none !important; }
footer, #MainMenu { display: none !important; }

.block-container {
    max-width: 500px !important;
    padding: 2.5rem 1.2rem 6rem !important;
    margin: 0 auto !important;
}

/* STYLE DES LABELS (NEOMA ID, NUMBER, NONCE) */
label[data-testid="stWidgetLabel"] > div > p {
    font-family: var(--font) !important; 
    font-size: 0.85rem !important; 
    font-weight: 800 !important;
    color: var(--pastel-pink) !important; /* Couleur Rose Pastel */
    text-transform: uppercase !important; 
    letter-spacing: 0.08em !important;
}

.nav { display:flex; justify-content:space-between; align-items:center; margin-bottom:2.8rem; }
.nav-brand { font-size:1.05rem; font-weight:700; letter-spacing:-0.03em; }
.nav-tag { font-size:0.72rem; font-weight:500; color:var(--sub); background:var(--white); border:1px solid var(--border); padding:4px 10px; border-radius:100px; }

.card { background:var(--white); border-radius:var(--r); border:1px solid var(--border); padding:1.6rem 1.6rem 1.4rem; margin-bottom:1rem; }
.card-label { font-size:0.65rem; font-weight:700; letter-spacing:0.1em; text-transform:uppercase; color:var(--sub); margin-bottom:1.1rem; }

input[type="text"], input[type="number"], input[type="password"] {
    background:var(--white) !important; border:2px solid #FFC0CB !important; border-radius:10px !important;
}

.stButton > button {
    font-family:var(--font) !important; font-weight:700 !important;
    border-radius:10px !important; padding:0.68rem 1.2rem !important; width:100% !important;
}
.btn-commit .stButton > button { background:var(--blue) !important; color:#fff !important; }
.btn-reveal .stButton > button { background:var(--green) !important; color:#fff !important; }

.footer { text-align:center; margin-top:3rem; font-size:0.8rem; color:#888; letter-spacing:0.02em; font-weight: 500; }
.footer-name { color: var(--pastel-pink); font-weight: 700; margin-top: 5px; }
</style>
""", unsafe_allow_html=True)

# --- UI HEADER ---
st.markdown("""
<div class="nav">
    <div class="nav-brand">NEOMA · Fintech</div>
    <div class="nav-tag">Blockchain 2026</div>
</div>
<div class="hero" style="margin-bottom:2.4rem;">
    <h1 style="font-size:2rem; font-weight:700; letter-spacing:-0.04em; margin-bottom:0.5rem;">Beauty Contest</h1>
    <p style="font-size:0.9rem; color:#555;">Commit–Reveal scheme — pick the number closest to ⅔ of the class average.</p>
</div>
""", unsafe_allow_html=True)

now = now_utc()
commit_open = now <= COMMIT_DEADLINE_UTC
reveal_open = now >= REVEAL_OPEN_UTC

st.markdown(f"""
<div class="chips" style="display:flex; gap:8px; margin-bottom:2rem;">
    <span class="chip" style="background:{'#d6f5eb' if commit_open else '#fde8e8'}; color:{'#00b07a' if commit_open else '#e02020'}; padding:6px 13px; border-radius:100px; font-size:0.75rem; font-weight:600;">
        {'● Commit open' if commit_open else '○ Commit closed'}
    </span>
    <span class="chip" style="background:{'#d6f5eb' if reveal_open else '#fde8e8'}; color:{'#00b07a' if reveal_open else '#e02020'}; padding:6px 13px; border-radius:100px; font-size:0.75rem; font-weight:600;">
        {'● Reveal open' if reveal_open else '○ Reveal closed'}
    </span>
</div>
""", unsafe_allow_html=True)

# --- FORMULAIRE ---
st.markdown('<div class="card"><div class="card-label">Your details</div>', unsafe_allow_html=True)
uni_id = st.text_input("NEOMA ID", placeholder="e.g. S033001234567X")
number = st.number_input("Number (0 – 100)", min_value=0, max_value=100, value=50, step=1)
nonce  = st.text_input("Secret nonce", placeholder="e.g. MySecret42", type="password")

if uni_id.strip() and nonce.strip():
    preimage = f"{uni_id.strip()}|{int(number)}|{nonce.strip()}"
    commit_hash = sha256(preimage)
    st.markdown(f"""
    <div style="margin-top:1rem; background:#f8f9fa; border:1.5px solid #FFC0CB; border-radius:10px; padding:0.9rem 1rem;">
        <div style="font-size:0.62rem; font-weight:700; text-transform:uppercase; color:#D87093;">SHA-256 hash</div>
        <div style="font-family:monospace; font-size:0.68rem; color:#333; word-break:break-all;">{commit_hash}</div>
    </div>""", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# --- ACTIONS ---
st.markdown('<div class="card"><div class="card-label">Phase 1 — Commit</div>', unsafe_allow_html=True)
st.markdown('<div class="btn-commit">', unsafe_allow_html=True)
if st.button("Lock in my commit →", key="btn_commit"):
    err = validate(uni_id, nonce, number)
    if not commit_open: st.error("⛔ The commit window is closed.")
    elif err: st.error(f"❌ {err}")
    else:
        h = sha256(f"{uni_id.strip()}|{int(number)}|{nonce.strip()}")
        status, text = post({"kind": "commit", "uni_id": uni_id.strip(), "commit": h})
        if status == 200: st.success("✅ Commit sent!")
        else: st.error(f"❌ Error: {text}")
st.markdown("</div></div>", unsafe_allow_html=True)

st.markdown('<div class="card"><div class="card-label">Phase 2 — Reveal</div>', unsafe_allow_html=True)
st.markdown('<div class="btn-reveal">', unsafe_allow_html=True)
if st.button("Reveal my number →", key="btn_reveal"):
    err = validate(uni_id, nonce, number)
    if not reveal_open: st.error("⛔ The reveal window is not open yet.")
    elif err: st.error(f"❌ {err}")
    else:
        status, text = post({"kind": "reveal", "uni_id": uni_id.strip(), "number": int(number), "nonce": nonce.strip()})
        if status == 200: st.success("✅ Reveal accepted!")
        else: st.error(f"❌ Error: {text}")
st.markdown("</div></div>", unsafe_allow_html=True)

# --- FOOTER ---
st.markdown(f"""
<div class="footer">
    NEOMA Business School · Blockchain & Fintech · 2026<br>
    <div class="footer-name">Project by Camélia El Rhabi</div>
</div>
""", unsafe_allow_html=True)
