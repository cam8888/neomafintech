import hashlib
import requests
import streamlit as st
from datetime import datetime, timezonest.markdown("""
<style>

/* ---------- GLOBAL ---------- */
:root {
    --font: 'Aeonik', 'DM Sans', sans-serif;

    --bg: #f8f6fb;
    --white: #ffffff;
    --text: #111111;
    --sub: #6b6b6b;
    --border: #e5def0;

    --primary: #d946ef;        /* rose élégant */
    --primary-soft: #f3e8ff;

    --green: #00b07a;
    --green-bg: #e6faf3;

    --red: #e02020;
    --red-bg: #fdecec;

    --r: 14px;
}

html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg) !important;
    font-family: var(--font) !important;
    color: var(--text) !important;
}

[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stSidebar"] { display: none !important; }
footer, #MainMenu { display: none !important; }

/* ---------- LAYOUT ---------- */
.block-container {
    max-width: 520px !important;
    padding: 2.5rem 1.4rem 5rem !important;
    margin: 0 auto !important;
}

/* ---------- NAV ---------- */
.nav { display:flex; justify-content:space-between; align-items:center; margin-bottom:2.5rem; }

.nav-brand {
    font-size:1.1rem;
    font-weight:700;
}

.nav-tag {
    font-size:0.72rem;
    color:var(--sub);
    background:var(--white);
    border:1px solid var(--border);
    padding:4px 10px;
    border-radius:100px;
}

/* ---------- HERO ---------- */
.hero h1 {
    font-size:2.2rem !important;
    font-weight:700 !important;
    margin-bottom:0.4rem !important;
}

.hero p {
    font-size:0.92rem;
    color:var(--sub);
}

/* ---------- STATUS ---------- */
.chips { display:flex; gap:10px; margin-bottom:2rem; }

.chip {
    font-size:0.75rem;
    font-weight:600;
    padding:6px 12px;
    border-radius:100px;
}

.chip.on  { background:var(--green-bg); color:var(--green); }
.chip.off { background:var(--red-bg); color:var(--red); }

/* ---------- CARDS ---------- */
.card {
    background: var(--white);
    border-radius: var(--r);
    border: 1px solid var(--border);
    padding: 1.6rem;
    margin-bottom: 1rem;

    box-shadow: 0 6px 18px rgba(0,0,0,0.05);
}

.card-label {
    font-size:0.7rem;
    font-weight:700;
    letter-spacing:0.08em;
    text-transform:uppercase;
    color:var(--sub);
    margin-bottom:1rem;
}

/* ---------- INPUTS (FIX VISIBILITY) ---------- */
input {
    background: #ffffff !important;
    border: 1.5px solid var(--border) !important;
    border-radius: 10px !important;

    padding: 10px !important;

    font-size: 0.95rem !important;
    font-weight: 600 !important;
    color: #111 !important;
}

input::placeholder {
    color: #9b8bb0 !important;
}

input:focus {
    border-color: var(--primary) !important;
    box-shadow: 0 0 0 3px rgba(217, 70, 239, 0.15) !important;
}

/* ---------- HASH ---------- */
.hash-box {
    margin-top:1rem;
    background:#faf5ff;
    border:1px solid #e9d5ff;
    border-radius:10px;
    padding:0.9rem 1rem;
}

.hash-box-title {
    font-size:0.65rem;
    font-weight:700;
    color:var(--primary);
}

.hash-mono {
    font-family:monospace;
    font-size:0.7rem;
    color:#7e22ce;
}

/* ---------- BUTTONS ---------- */
.stButton > button {
    font-weight:700 !important;
    border-radius:10px !important;
    padding:0.7rem !important;
}

.btn-commit .stButton > button {
    background: linear-gradient(135deg, #d946ef, #c026d3) !important;
    color:white !important;
}

.btn-reveal .stButton > button {
    background: linear-gradient(135deg, #22c55e, #16a34a) !important;
    color:white !important;
}

/* ---------- FOOTER ---------- */
.footer {
    text-align:center;
    margin-top:3rem;
    font-size:0.75rem;
    color:#aaa;
}

</style>
""", unsafe_allow_html=True)
