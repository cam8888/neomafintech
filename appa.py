import hashlib
import requests
import streamlit as st
from datetime import datetime, timezone

# --- CONFIG & LOGIC ---
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

st.set_page_config(page_title="NEOMA | Beauty Contest", page_icon="⚖️", layout="centered")

# --- CLEAN LUXE UI ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');

/* Reset & Base */
html, body, [data-testid="stAppViewContainer"] {
    background-color: #F8F9FA !important;
    font-family: 'Inter', sans-serif !important;
    color: #2D3436 !important;
}

.block-container { padding-top: 2rem !important; max-width: 550px !important; }

/* Typography */
h1 { font-weight: 700 !important; letter-spacing: -1px; color: #2D3436 !important; margin-bottom: 0.2rem !important; }
p { color: #636E72 !important; font-size: 0.95rem; }

/* Pink Labels (Readable & Aesthetic) */
label[data-testid="stWidgetLabel"] p {
    color: #D87093 !important;
    font-weight: 600 !important;
    text-transform: uppercase;
    font-size: 0.75rem !important;
    letter-spacing: 0.05rem;
    margin-bottom: 8px;
}

/* Elegant Cards */
.stCard {
    background: #FFFFFF;
    border: 1px solid #EDF2F7;
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 20px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.03);
}

/* Buttons */
.stButton > button {
    border-radius: 12px !important;
    padding: 12px 24px !important;
    font-weight: 600 !important;
    border: none !important;
    transition: all 0.2s ease;
}
.btn-commit button { background-color: #2D3436 !important; color: white !important; }
.btn-reveal button { background-color: #D87093 !important; color: white !important; }

/* Status Chips */
.status-bar { display: flex; gap: 10px; margin-bottom: 2rem; }
.chip { padding: 4px 12px; border-radius: 100px; font-size: 0.7rem; font-weight: 700; text-transform: uppercase; }

/* Footer */
.footer { border-top: 1px solid #EEE; margin-top: 4rem; padding-top: 2rem; text-align: center; font-size: 0.8rem; color: #B2BEC3; }
.camelia { color: #D87093; font-weight: 700; margin-top: 5px; font-size: 0.9rem; }
</style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown("<h1>Beauty Contest</h1>", unsafe_allow_html=True)
st.markdown("<p>Blockchain-based Commit-Reveal protocol for game theory simulation.</p>", unsafe_allow_html=True)

# --- STATUS ---
now = now_utc()
c_open = now <= COMMIT_DEADLINE_UTC
r_open = now >= REVEAL_OPEN_UTC

st.markdown(f"""
<div class="status-bar">
    <span class="chip" style="background:{'#E3F9E5' if c_open else '#FFE3E3'}; color:{'#1F7A33' if c_open else '#A91515'};">
        ● Commit: {'Open' if c_open else 'Closed'}
    </span>
    <span class="chip" style="background:{'#E3F9E5' if r_open else '#FFE3E3'}; color:{'#1F7A33' if r_open else '#A91515'};">
        ● Reveal: {'Open' if r_open else 'Closed'}
    </span>
</div>
""", unsafe_allow_html=True)

# --- INPUT SECTION ---
with st.container():
    st.markdown('<div class="stCard">', unsafe_allow_html=True)
    uni_id = st.text_input("NEOMA Student ID", placeholder="S000...")
    val_number = st.number_input("Chosen Value (0-100)", min_value=0, max_value=100, value=50)
    nonce = st.text_input("Security Nonce (Private)", type="password", placeholder="Secret code...")
    
    if uni_id and nonce:
        h = sha256(f"{uni_id.strip()}|{int(val_number)}|{nonce.strip()}")
        st.markdown(f"""
        <div style="background:#F8F9FA; padding:12px; border-radius:8px; border-left:4px solid #D87093; margin-top:15px;">
            <span style="font-size:0.65rem; font-weight:700; color:#D87093; display:block;">SHA-256 IDENTIFIER</span>
            <code style="font-size:0.75rem; color:#2D3436; word-break:break-all;">{h}</code>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- ACTIONS ---
col_a, col_b = st.columns(2)

with col_a:
    st.markdown('<div class="btn-commit">', unsafe_allow_html=True)
    if st.button("Submit Commit", use_container_width=True):
        if not c_open: st.error("Commit phase closed.")
        elif not uni_id: st.warning("Enter ID.")
        else:
            h = sha256(f"{uni_id.strip()}|{int(val_number)}|{nonce.strip()}")
            res, txt = post({"kind": "commit", "uni_id": uni_id.strip(), "commit": h})
            st.toast(f"Result: {res}")
    st.markdown('</div>', unsafe_allow_html=True)

with col_b:
    st.markdown('<div class="btn-reveal">', unsafe_allow_html=True)
    if st.button("Submit Reveal", use_container_width=True):
        if not r_open: st.error("Reveal phase not yet open.")
        else:
            res, txt = post({"kind": "reveal", "uni_id": uni_id.strip(), "number": int(val_number), "nonce": nonce.strip()})
            st.toast(f"Result: {res}")
    st.markdown('</div>', unsafe_allow_html=True)

# --- FOOTER ---
st.markdown(f"""
<div class="footer">
    NEOMA BUSINESS SCHOOL &nbsp;•&nbsp; FINTECH MODULE &nbsp;•&nbsp; 2026<br>
    <div class="camelia">Project by Camélia El Rhabi</div>
</div>
""", unsafe_allow_html=True)
