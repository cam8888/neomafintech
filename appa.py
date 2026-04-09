import hashlib
import requests
import streamlit as st
from datetime import datetime, timezone

# --- CONFIGURATION ---
API_URL = "https://script.google.com/macros/s/AKfycbyNZNOE1DYNbd4GbGTISJsGrnJ4PYCuip0yjSw3Lr8KkD6-kadKI9mfpKNfiAHEWb0Osw/exec"
COMMIT_DEADLINE_UTC = datetime(2026, 11, 30, 22, 59, 59, tzinfo=timezone.utc)
REVEAL_OPEN_UTC     = datetime(2024, 10, 21, 22,  0,  0, tzinfo=timezone.utc)

def sha256(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

def post(payload):
    try:
        r = requests.post(API_URL, json=payload, timeout=15)
        return r.status_code, r.text
    except Exception as e:
        return None, str(e)

# --- INTERFACE ---
st.set_page_config(page_title="Beauty Contest", layout="centered")

st.title("Beauty Contest")
st.subheader("Keynesian Game Simulation")
st.write("Pick the number closest to 2/3 of the class average.")

st.divider()

# Formulaire simple et propre
uni_id = st.text_input("NEOMA ID", placeholder="S033...")
number = st.number_input("Chosen Number (0-100)", min_value=0, max_value=100, value=50)
nonce  = st.text_input("Secret Nonce", type="password", help="Keep this secret for the reveal phase")

if uni_id and nonce:
    commit_hash = sha256(f"{uni_id.strip()}|{int(number)}|{nonce.strip()}")
    st.info(f"**Your identifier (SHA-256):** {commit_hash}")

st.divider()

# Actions
col1, col2 = st.columns(2)

with col1:
    if st.button("1. Lock Commit", use_container_width=True):
        h = sha256(f"{uni_id.strip()}|{int(number)}|{nonce.strip()}")
        status, resp = post({"kind": "commit", "uni_id": uni_id.strip(), "commit": h})
        st.write(f"Status: {status}")

with col2:
    if st.button("2. Submit Reveal", use_container_width=True):
        status, resp = post({"kind": "reveal", "uni_id": uni_id.strip(), "number": int(number), "nonce": nonce.strip()})
        st.write(f"Status: {status}")

# Signature
st.write("")
st.write("")
st.divider()
st.markdown("### Project by **Camélia El Rhabi**")
st.caption("NEOMA Business School • Blockchain & Fintech 2026")
