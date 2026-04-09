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

# --- CSS CORRECTIF (LISIBILITÉ MAXIMALE) ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');

:root {
    --font: 'Inter', sans-serif;
    --bg:      #F5F5F5; /* Gris clair pour le fond */
    --white:   #ffffff;
    --dark-text: #1A1A1A; /* Noir profond pour la lisibilité */
    --sub-text:  #4A4A4A;
    --pastel-pink: #D81B60; /* Rose plus foncé pour que les labels soient lisibles */
    --border-color: #CCCCCC;
}

html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--bg) !important;
    font-family: var(--font) !important;
    color: var(--dark-text) !important;
}

/* On force TOUS les textes Streamlit en sombre */
.stMarkdown, p, span, div {
    color: var(--dark-text) !important;
}

/* Titre principal bien visible */
h1 {
    color: var(--dark-text) !important;
    font-weight: 800 !important;
}

/* LABELS (NEOMA ID, Number, Nonce) en Rose Pastel Lisible */
label[data-testid="stWidgetLabel"] p {
    color: var(--pastel-pink) !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

/* Champs de saisie - On ajoute des bordures pour la structure */
input {
    color: var(--dark-text) !important;
    background-color: white !important;
    border: 2px solid var(--border-color) !important;
}

.card {
    background: var(--white);
    border-radius: 15px;
    padding: 2rem;
    border: 1px solid #E0E0E0;
    margin-bottom: 1.5rem;
    box-shadow: 0 4px 6px rgba(0,0,0,0.02);
}

.footer {
    text-align: center;
    margin-top: 3rem;
    font-size: 0.85rem;
    color: var(--sub-text) !important;
    border-top: 1px solid #DDD;
    padding-top: 1rem;
}

.footer-name {
    color: var(--pastel-pink) !important;
    font-weight: 700;
}
</style>
""", unsafe_allow_html=True)

# --- CONTENU ---
st.markdown('<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:1rem;"><strong>NEOMA · Fintech</strong><span style="background:white; padding:4px 10px; border-radius:100px; font-size:0.7rem; border:1px solid #DDD;">Blockchain 2026</span></div>', unsafe_allow_html=True)

st.title("Beauty Contest")
st.markdown("<p style='font-size:1.1rem;'>Commit–Reveal scheme — pick the number closest to ⅔ of the class average.</p>", unsafe_allow_html=True)

now = now_utc()
commit_open = now <= COMMIT_DEADLINE_UTC
reveal_open = now >= REVEAL_OPEN_UTC

# Chips de statut
c1, c2 = st.columns(2)
with c1:
    st.markdown(f"<div style='background:{'#D1FAE5' if commit_open else '#FEE2E2'}; color:{'#065F46' if commit_open else '#991B1B'}; padding:8px; border-radius:10px; text-align:center; font-weight:700;'>● Commit: {'Open' if commit_open else 'Closed'}</div>", unsafe_allow_html=True)
with c2:
    st.markdown(f"<div style='background:{'#D1FAE5' if reveal_open else '#FEE2E2'}; color:{'#065F46' if reveal_open else '#991B1B'}; padding:8px; border-radius:10px; text-align:center; font-weight:700;'>● Reveal: {'Open' if reveal_open else 'Closed'}</div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- CARD DETAILS ---
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown("<h4 style='margin-top:0; color:#4A4A4A;'>YOUR DETAILS</h4>", unsafe_allow_html=True)
uni_id = st.text_input("NEOMA ID", placeholder="e.g. S033...")
number = st.number_input("Number (0 – 100)", min_value=0, max_value=100, value=50)
nonce  = st.text_input("Secret nonce", placeholder="Your secret key", type="password")

if uni_id.strip() and nonce.strip():
    preimage = f"{uni_id.strip()}|{int(number)}|{nonce.strip()}"
    commit_hash = sha256(preimage)
    st.info(f"**SHA-256 Hash:** {commit_hash}")
st.markdown('</div>', unsafe_allow_html=True)

# --- CARD ACTIONS ---
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown("<h4 style='margin-top:0; color:#4A4A4A;'>PHASE 1 — COMMIT</h4>", unsafe_allow_html=True)
if st.button("Lock in my commit →", use_container_width=True):
    err = validate(uni_id, nonce, number)
    if not commit_open: st.error("Window closed.")
    elif err: st.error(err)
    else:
        h = sha256(f"{uni_id.strip()}|{int(number)}|{nonce.strip()}")
        status, text = post({"kind": "commit", "uni_id": uni_id.strip(), "commit": h})
        if status == 200: st.success("✅ Success!")
        else: st.error(f"Error: {text}")

st.markdown("<hr style='margin:1.5rem 0; opacity:0.1;'>", unsafe_allow_html=True)

st.markdown("<h4 style='margin-top:0; color:#4A4A4A;'>PHASE 2 — REVEAL</h4>", unsafe_allow_html=True)
if st.button("Reveal my number →", use_container_width=True):
    err = validate(uni_id, nonce, number)
    if not reveal_open: st.error("Not open yet.")
    elif err: st.error(err)
    else:
        status, text = post({"kind": "reveal", "uni_id": uni_id.strip(), "number": int(number), "nonce": nonce.strip()})
        if status == 200: st.success("✅ Accepted!")
        else: st.error(f"Error: {text}")
st.markdown('</div>', unsafe_allow_html=True)

# --- FOOTER ---
st.markdown(f"""
<div class="footer">
    NEOMA Business School · Blockchain & Fintech · 2026<br>
    <div class="footer-name">Project by Camélia El Rhabi</div>
</div>
""", unsafe_allow_html=True)
