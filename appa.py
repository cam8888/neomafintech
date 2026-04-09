import hashlib
import requests
import streamlit as st
from datetime import datetime, timezone

# --- CONFIG ---
API_URL = "https://script.google.com/macros/s/AKfycbyNZNOE1DYNbd4GbGTISJsGrnJ4PYCuip0yjSw3Lr8KkD6-kadKI9mfpKNfiAHEWb0Osw/exec"
COMMIT_DEADLINE_UTC = datetime(2026, 11, 30, 22, 59, 59, tzinfo=timezone.utc)
REVEAL_OPEN_UTC     = datetime(2024, 10, 21, 22,  0,  0, tzinfo=timezone.utc)

def sha256(s): return hashlib.sha256(s.encode("utf-8")).hexdigest()
def now_utc(): return datetime.now(timezone.utc)

def post(payload):
    try:
        r = requests.post(API_URL, json=payload, timeout=15)
        return r.status_code, r.text
    except Exception as e: return None, str(e)

st.set_page_config(page_title="Beauty Contest", layout="centered")

# --- UNIFIED CSS (ONE COLOR, ONE FONT) ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

:root {
    --main-color: #262626; /* Gris anthracite unique pour tout */
    --accent-pink: #FFB6C1; /* Rose pastel uniquement pour la signature */
}

/* Application de la couleur unique partout */
html, body, [data-testid="stAppViewContainer"], .stMarkdown, p, span, label {
    color: var(--main-color) !important;
    font-family: 'Inter', sans-serif !important;
}

/* Uniformisation des titres */
h1, h2, h3, h4 {
    color: var(--main-color) !important;
    font-weight: 700 !important;
}

/* Harmonisation des Labels de saisie */
label[data-testid="stWidgetLabel"] p {
    color: var(--main-color) !important;
    font-size: 0.9rem !important;
    font-weight: 600 !important;
    text-transform: none !important;
}

/* Style des champs de saisie */
input {
    border: 1px solid #ddd !important;
    border-radius: 8px !important;
}

/* Footer & Signature */
.footer-container {
    text-align: center;
    margin-top: 4rem;
    padding-top: 1rem;
    border-top: 1px solid #eee;
}
.camelia-signature {
    color: var(--accent-pink) !important;
    font-weight: 700;
    font-size: 1rem;
}
</style>
""", unsafe_allow_html=True)

# --- UI CONTENT ---
st.title("Beauty Contest")
st.write("Commit–Reveal protocol for game theory simulation.")

# Status simple
now = now_utc()
c_open = now <= COMMIT_DEADLINE_UTC
r_open = now >= REVEAL_OPEN_UTC

st.markdown(f"""
<div style="margin-bottom: 2rem; font-size: 0.85rem; font-weight: 600;">
    <span style="margin-right: 15px;">{'●' if c_open else '○'} Commit Phase: {'Active' if c_open else 'Closed'}</span>
    <span>{'●' if r_open else '○'} Reveal Phase: {'Active' if r_open else 'Waiting'}</span>
</div>
""", unsafe_allow_html=True)

# Formulaire simple (sans card)
uni_id = st.text_input("NEOMA ID", placeholder="S033...")
val_number = st.number_input("Chosen Number", min_value=0, max_value=100, value=50)
nonce = st.text_input("Secret Nonce", type="password")

if uni_id and nonce:
    h = sha256(f"{uni_id.strip()}|{int(val_number)}|{nonce.strip()}")
    st.code(f"SHA-256 Identifier: {h}")

st.markdown("---")

# Actions
if st.button("Lock in Commit", use_container_width=True):
    if not c_open: st.error("Commit window closed.")
    else:
        h = sha256(f"{uni_id.strip()}|{int(val_number)}|{nonce.strip()}")
        s, t = post({"kind": "commit", "uni_id": uni_id.strip(), "commit": h})
        st.write(f"Server Status: {s}")

if st.button("Submit Reveal", use_container_width=True):
    if not r_open: st.error("Reveal window not open yet.")
    else:
        s, t = post({"kind": "reveal", "uni_id": uni_id.strip(), "number": int(val_number), "nonce": nonce.strip()})
        st.write(f"Server Status: {s}")

# FOOTER AVEC TON NOM
st.markdown(f"""
<div class="footer-container">
    NEOMA Business School • Blockchain & Fintech<br>
    <div style="margin-top:8px;">Project by <span class="camelia-signature">Camélia El Rhabi</span></div>
</div>
""", unsafe_allow_html=True)
