st.markdown("""
<style>

/* ---------- FONTS ---------- */
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

/* ---------- COLORS (PASTEL ROSE THEME) ---------- */
:root {
    --font: 'Aeonik', 'DM Sans', sans-serif;

    --bg:      #faf7fb;
    --white:   #ffffff;
    --text:    #1a1a1a;
    --sub:     #6b6b6b;
    --border:  #e7dff0;

    --primary: #e8b4f0;
    --primary-dark: #d48ce6;

    --accent:  #f9d5ec;
    --accent-strong: #ec9ed6;

    --green:   #00b07a;
    --green-bg:#d6f5eb;

    --red:     #e02020;
    --red-bg:  #fde8e8;

    --r: 16px;
}

/* ---------- GLOBAL ---------- */
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

/* ---------- NAV ---------- */
.nav {
    display:flex;
    justify-content:space-between;
    align-items:center;
    margin-bottom:2.8rem;
}

.nav-brand {
    font-size:1.05rem;
    font-weight:700;
    letter-spacing:-0.03em;
}

.nav-tag {
    font-size:0.72rem;
    font-weight:500;
    color:var(--sub);
    background:var(--white);
    border:1px solid var(--border);
    padding:4px 10px;
    border-radius:100px;
}

/* ---------- HERO ---------- */
.hero h1 {
    font-size:2rem !important;
    font-weight:700 !important;
    letter-spacing:-0.04em !important;
    line-height:1.15 !important;
    margin:0 0 0.5rem !important;
}

.hero p {
    font-size:0.9rem;
    color:var(--sub);
}

/* ---------- CHIPS ---------- */
.chips { display:flex; gap:8px; margin-bottom:2rem; flex-wrap:wrap; }

.chip {
    display:inline-flex;
    align-items:center;
    gap:6px;
    font-size:0.75rem;
    font-weight:600;
    padding:6px 13px;
    border-radius:100px;
}

.chip-dot {
    width:7px;
    height:7px;
    border-radius:50%;
}

.chip.on  { background:var(--green-bg); color:var(--green); }
.chip.on  .chip-dot { background:var(--green); }

.chip.off { background:var(--red-bg); color:var(--red); }
.chip.off .chip-dot { background:var(--red); }

/* ---------- CARDS ---------- */
.card {
    background: var(--white);
    border-radius: var(--r);
    border: 1px solid var(--border);
    padding: 1.6rem;
    margin-bottom: 1rem;

    box-shadow: 0 8px 25px rgba(232, 180, 240, 0.15);
}

.card-label {
    font-size:0.65rem;
    font-weight:700;
    letter-spacing:0.1em;
    text-transform:uppercase;
    color:var(--sub);
    margin-bottom:1.1rem;
}

/* ---------- INPUTS ---------- */
label[data-testid="stWidgetLabel"] > div > p {
    font-family:var(--font) !important;
    font-size:0.72rem !important;
    font-weight:700 !important;
    color:var(--sub) !important;
    text-transform:uppercase !important;
    letter-spacing:0.08em !important;
}

input[type="text"],
input[type="number"],
input[type="password"] {
    background: #ffffff !important;
    border: 1.8px solid var(--border) !important;
    border-radius: 12px !important;

    padding: 10px 12px !important;

    font-family: var(--font) !important;
    font-size: 0.95rem !important;
    font-weight: 600 !important;
    color: var(--text) !important;
}

input::placeholder {
    color: #b8a8c2 !important;
    font-weight: 500;
}

input:focus {
    border-color: var(--primary-dark) !important;
    box-shadow: 0 0 0 3px rgba(232, 180, 240, 0.25) !important;
    background: #fff !important;
}

/* ---------- HASH BOX ---------- */
.hash-box {
    margin-top: 1rem;
    background: #fff0fb;
    border: 1.5px solid #f3c6ec;
    border-radius: 12px;
    padding: 0.9rem 1rem;
}

.hash-box-title {
    font-size:0.62rem;
    font-weight:700;
    text-transform:uppercase;
    letter-spacing:0.1em;
    color:#d48ce6;
    margin-bottom:5px;
}

.hash-mono {
    font-family:'Courier New',monospace;
    font-size:0.68rem;
    color:#b14fc5;
    word-break:break-all;
}

/* ---------- BUTTONS ---------- */
.stButton > button {
    font-family:var(--font) !important;
    font-weight:700 !important;
    font-size:0.92rem !important;
    border:none !important;
    border-radius:12px !important;
    padding:0.7rem 1.2rem !important;
    width:100% !important;
}

.btn-commit .stButton > button {
    background: linear-gradient(135deg, #e8b4f0, #f3c6ec) !important;
    color:#fff !important;
}

.btn-reveal .stButton > button {
    background: linear-gradient(135deg, #ec9ed6, #f7b6e6) !important;
    color:#fff !important;
}

/* ---------- FOOTER ---------- */
.footer {
    text-align:center;
    margin-top:3rem;
    font-size:0.72rem;
    color:#bbb;
}

</style>
""", unsafe_allow_html=True)