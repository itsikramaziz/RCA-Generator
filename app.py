import streamlit as st
from groq import Groq
from datetime import date, timedelta
import io
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY

# ── Groq API Key ─────────────────────────────────────────────────────────────
GROQ_API_KEY = "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"   # 👈 Yahan apni Groq key daalo

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Auto RCA Generator",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Merchant data ─────────────────────────────────────────────────────────────

# Remittance merchants — grouped by region (Payout)
REMITTANCE_MERCHANTS = {
    "PK": [
        "3000001 - Dlocal PK",
        "3000002 - Thunes PK",
        "3000006 - GCC Remit PK",
        "3000007 - Dlocal PK",
        "3000008 - Dlocal PK-LNK",
        "3000009 - Dlocal PK-B2C",
        "3000010 - Voo PK",
        "3000012 - Cadanapay PK",
        "3000019 - SINGX PK",
        "3000025 - Lemfi PK",
        "3000026 - Thunes-UK PK",
        "3000030 - Elevate Pay PK",
        "3000031 - Fuze PK",
        "3000032 - SingX P2P PK",
    ],
    "BD": [
        "3000003 - Dlocal BD",
        "3000011 - Voo BD",
        "3000013 - Cadanapay BD",
        "3000014 - Remitbee BD",
        "3000022 - Thunes BD",
        "3000023 - GCC Remit BD",
        "3000024 - Lemfi BD",
    ],
    "NP": [],
    "OTHER": [
        "3000004 - Binance",
        "3000005 - Terrapay",
        "3000015 - Swiftx",
        "3000017 - Remitbee",
        "3000018 - Swiftx",
    ],
}

# Disbursement merchants — flat list
DISBURSEMENT_MERCHANTS = [
    "1000004 - Tapmad",
    "1000005 - Haipay",
    "1000006 - Haipay",
    "1000176 - Coda",
    "1000188 - FreeFire",
    "2000001 - Simpaisa",
    "2000002 - Dlocal Service",
    "2000003 - Jindou",
    "2000006 - Lavieinno",
    "2000010 - Simpaisa Refund",
    "2000016 - Payyd",
    "2000021 - THUNES",
    "2000040 - Sada Farooq",
    "2000042 - KYC Test",
    "2000048 - Coda",
    "2000055 - SunshineTech",
    "2000059 - Maqsood CEO",
    "2000061 - Muzz",
    "2000069 - Khoso Amanullah",
    "2000070 - Humraah",
    "2000076 - WOLF",
    "2000077 - Tazapay",
    "2000091 - EPAY Global",
    "2000093 - MerchantGlobe",
    "2000103 - StarBazaar",
    "2000105 - Payyd",
    "2000117 - IPID",
    "2000122 - SSOPS",
    "2000124 - Tangopay",
    "2000126 - MyCo",
    "2000128 - INFINITEHOPETECH",
    "2000184 - PMAX",
    "2000193 - Gamifly",
    "2000194 - Blue Ocean",
    "2000329 - BJSPORTS66",
    "2000347 - BCGame",
    "2000349 - BJHoldingFunds",
    "2000462 - BJHoldingFunds",
    "2000463 - SS-DT",
    "2000626 - GG Den",
    "2000640 - 20BET",
    "2000665 - BJ-DT",
    "2000666 - SS-DT",
    "2000668 - DTR Limited",
    "2000704 - DTR Limited",
    "2000705 - DTR Limited",
    "2000706 - Vegas",
    "2000774 - Vegas",
    "2000775 - Wolf Disb",
    "2000777 - Jeet Buzz MG",
    "2000778 - PayGames",
    "2000782 - Yoda",
    "2000784 - MXW(bj)",
    "2000787 - Wolf Disb",
    "2000788 - Blue Ocean",
    "2000789 - Ubank",
    "2000795 - PRYZE",
    "2000800 - MP(BJ)",
    "2000807 - Wooshpay HighRisk",
    "2000808 - Monetix",
    "2000809 - Poseidon",
    "2000812 - Vegas 2 MG",
    "2000814 - Betjee",
    "2000815 - Phantom",
    "2000827 - PayGames",
    "2000829 - CBet",
    "2000830 - FCMoon",
    "2000831 - JokerBet",
    "2000832 - Mostbet",
    "2000836 - V5-Pay",
    "2000838 - Haipay",
    "2000839 - Sunshine",
    "2000854 - BetJeeli",
    "2000855 - Quarktech",
    "2000870 - Royal X Casino",
    "2000875 - Quarktech",
    "2000878 - Temu",
    "2000879 - Faspal 8Hexa",
    "2000880 - VPBet Yoda",
    "2000883 - Yoda 22Bet",
    "2000884 - E28",
    "2000891 - 249 Tec",
    "2000898 - Thunes-Daraz",
    "2000904 - Yahalamingo",
    "2000905 - JW7PKR",
    "2000909 - Temu Tokenization",
    "2000910 - Monetix",
    "2000914 - UsolvePay",
    "2000925 - KVS247",
    "2000938 - Faspal8Hexa",
    "2000944 - Faspal8Hexa",
    "2000945 - Faspal8Hexa",
    "2000946 - Faspal8Hexa",
    "2000947 - Faspal8Hexa",
    "2000949 - Haipay",
    "2000950 - Faspal8Hexa",
    "2000951 - Wolf999",
    "2000953 - Indrive Courier",
    "2000956 - V5Pay",
    "2000957 - MGSAT",
    "2000958 - Onerway",
    "2000977 - Payloco",
    "2000983 - F7",
    "2000986 - PMAX",
    "2000996 - OMAZA",
    "2001003 - VoltaicSystems",
    "2001021 - Jeelo Chat",
    "2001023 - Exness",
    "2001024 - 99AB",
    "2001026 - Monetix",
    "2001031 - WE999",
    "2001033 - IPID",
    "2001036 - Winpkr11",
    "2001037 - IPID",
    "2001043 - Bitslap",
    "2001046 - Clipspay",
    "2001047 - MG-REFUND",
    "2001048 - 8 Hexa-hifami",
    "2001051 - MostPlay",
    "2001058 - VideLyy",
    "2001068 - MG-REFUND",
    "2001074 - Pay2Play",
    "2001078 - SUGO",
    "2001079 - HOLLA",
    "2001081 - ZeepLive",
    "2001082 - SIYA",
    "2001083 - POPSHOWS",
    "2001087 - TekkaBuzz",
    "2001092 - MG-SAT",
    "2001097 - MOSTBET",
    "2001098 - MOSTBET",
    "2001100 - UsolvePay",
    "2001103 - OnlineBaat",
    "2001108 - Haalawa",
    "2001116 - Lova 8hexa",
    "2001119 - Promptive",
    "2001125 - VoiceChat",
    "2001132 - Yango",
    "2001145 - Dafabet",
    "2001146 - VertexGlobal",
    "2001151 - T7 PakJackpot",
    "2001153 - Okaypay",
    "2001154 - TCG-P7",
    "2001155 - Hightribe",
    "2001156 - OKEXPKR",
    "2001159 - Vahaflix",
    "2001160 - Seagm",
    "2001161 - Party",
    "2001162 - Jolly",
    "2001163 - Oner",
    "2001164 - Starmate",
    "2001166 - Xena Live",
    "2001168 - Usolvepay LowRisk",
    "2001170 - MTC-Game",
    "2001173 - MPBJ DarazPlay",
    "2001174 - MPBJ Khelo",
    "2001175 - MPBJ HeyBaji",
    "2001176 - MPBJ SuperBaji",
    "2001177 - MPBJ Slotbji",
    "2001178 - MPBJ Jetwin",
    "2001181 - Crosspay",
    "4600004 - Tapmad",
]

# ── Galaxy CSS + custom styles ────────────────────────────────────────────────
GALAXY_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;600;700&display=swap');

/* ── Reset & base ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
    background: #020010 !important;
    color: #e0e8ff !important;
    font-family: 'Rajdhani', sans-serif !important;
}

[data-testid="stAppViewContainer"] > .main { background: transparent !important; }
[data-testid="stHeader"] { background: transparent !important; }
section[data-testid="stSidebar"] { background: #05001a !important; }

/* ── Galaxy canvas ── */
#galaxy-canvas {
    position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
    z-index: 0; pointer-events: none;
}

/* ── Nebula overlay ── */
.nebula-overlay {
    position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
    background:
        radial-gradient(ellipse 80% 60% at 20% 30%, rgba(120,40,200,0.15) 0%, transparent 70%),
        radial-gradient(ellipse 60% 80% at 80% 70%, rgba(0,100,255,0.12) 0%, transparent 70%),
        radial-gradient(ellipse 50% 50% at 50% 50%, rgba(0,200,180,0.06) 0%, transparent 70%);
    z-index: 0; pointer-events: none;
    animation: nebulaPulse 12s ease-in-out infinite alternate;
}
@keyframes nebulaPulse {
    0%  { opacity: 0.7; }
    100%{ opacity: 1.2; }
}

/* ── All streamlit content above canvas ── */
.block-container { position: relative; z-index: 10; padding-top: 2rem !important; }

/* ── Main title ── */
.main-title {
    font-family: 'Orbitron', monospace !important;
    font-size: clamp(2rem, 5vw, 3.8rem) !important;
    font-weight: 900;
    text-align: center;
    letter-spacing: 4px;
    background: linear-gradient(135deg, #00f5ff 0%, #a855f7 40%, #ec4899 70%, #f59e0b 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    text-shadow: none;
    margin-bottom: 0.3rem;
    filter: drop-shadow(0 0 30px rgba(168,85,247,0.6));
    animation: titleGlow 3s ease-in-out infinite alternate;
}
@keyframes titleGlow {
    0%  { filter: drop-shadow(0 0 20px rgba(0,245,255,0.5)); }
    100%{ filter: drop-shadow(0 0 40px rgba(168,85,247,0.8)); }
}

.subtitle {
    text-align: center;
    font-size: 1.1rem;
    color: rgba(160,200,255,0.7);
    letter-spacing: 6px;
    text-transform: uppercase;
    margin-bottom: 3rem;
    font-weight: 300;
}

/* ── Cards ── */
.card-container {
    display: flex;
    gap: 2rem;
    justify-content: center;
    flex-wrap: wrap;
    padding: 1rem;
}

.rca-card {
    background: linear-gradient(135deg, rgba(255,255,255,0.04) 0%, rgba(120,80,200,0.08) 100%);
    border: 1px solid rgba(120,80,200,0.3);
    border-radius: 20px;
    padding: 2.5rem 2rem;
    width: 300px;
    text-align: center;
    cursor: pointer;
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    backdrop-filter: blur(20px);
    position: relative;
    overflow: hidden;
}
.rca-card::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; bottom: 0;
    background: linear-gradient(135deg, rgba(0,245,255,0.05), rgba(168,85,247,0.05));
    opacity: 0;
    transition: opacity 0.4s;
    border-radius: 20px;
}
.rca-card:hover::before { opacity: 1; }
.rca-card:hover {
    transform: translateY(-8px) scale(1.02);
    border-color: rgba(0,245,255,0.6);
    box-shadow: 0 20px 60px rgba(0,245,255,0.2), 0 0 40px rgba(168,85,247,0.3);
}
.card-icon { font-size: 3.5rem; margin-bottom: 1rem; filter: drop-shadow(0 0 10px rgba(0,245,255,0.5)); }
.card-title {
    font-family: 'Orbitron', monospace;
    font-size: 1.3rem;
    font-weight: 700;
    color: #00f5ff;
    margin-bottom: 0.5rem;
    letter-spacing: 2px;
}
.card-desc { font-size: 0.9rem; color: rgba(160,200,255,0.7); line-height: 1.5; }

/* ── Section heading ── */
.section-heading {
    font-family: 'Orbitron', monospace;
    font-size: clamp(1.3rem, 3vw, 2rem);
    font-weight: 700;
    color: #00f5ff;
    text-align: center;
    letter-spacing: 3px;
    margin-bottom: 0.5rem;
    text-shadow: 0 0 20px rgba(0,245,255,0.5);
}
.section-sub {
    text-align: center;
    color: rgba(160,200,255,0.6);
    font-size: 0.95rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-bottom: 2.5rem;
}

/* ── Form glass panel ── */
.glass-panel {
    background: linear-gradient(135deg, rgba(255,255,255,0.03), rgba(120,80,200,0.06));
    border: 1px solid rgba(120,80,200,0.25);
    border-radius: 16px;
    padding: 2rem;
    backdrop-filter: blur(30px);
    margin-bottom: 1.5rem;
    position: relative;
}
.glass-panel::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 1px;
    background: linear-gradient(90deg, transparent, rgba(0,245,255,0.5), transparent);
    border-radius: 16px 16px 0 0;
}
.panel-label {
    font-family: 'Orbitron', monospace;
    font-size: 0.75rem;
    letter-spacing: 3px;
    color: rgba(0,245,255,0.7);
    text-transform: uppercase;
    margin-bottom: 0.8rem;
    font-weight: 600;
}

/* ── Streamlit widget overrides ── */
[data-testid="stSelectbox"] > div > div,
[data-testid="stMultiSelect"] > div > div {
    background: rgba(10,5,30,0.8) !important;
    border: 1px solid rgba(120,80,200,0.4) !important;
    border-radius: 10px !important;
    color: #e0e8ff !important;
    backdrop-filter: blur(10px) !important;
}
[data-testid="stSelectbox"] > div > div:hover,
[data-testid="stMultiSelect"] > div > div:hover {
    border-color: rgba(0,245,255,0.6) !important;
    box-shadow: 0 0 15px rgba(0,245,255,0.15) !important;
}

[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea,
[data-testid="stDateInput"] input {
    background: rgba(10,5,30,0.8) !important;
    border: 1px solid rgba(120,80,200,0.4) !important;
    border-radius: 10px !important;
    color: #e0e8ff !important;
    backdrop-filter: blur(10px) !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 1rem !important;
}
[data-testid="stTextInput"] input:focus,
[data-testid="stTextArea"] textarea:focus {
    border-color: rgba(0,245,255,0.7) !important;
    box-shadow: 0 0 20px rgba(0,245,255,0.2) !important;
    outline: none !important;
}

/* ── Tone buttons ── */
.tone-btn {
    background: linear-gradient(135deg, rgba(10,5,30,0.9), rgba(40,20,80,0.9)) !important;
    border: 1px solid rgba(120,80,200,0.5) !important;
    border-radius: 12px !important;
    color: #c0d0ff !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    letter-spacing: 1px;
    padding: 0.6rem 1.2rem !important;
    cursor: pointer;
    transition: all 0.3s ease !important;
    width: 100% !important;
}
.tone-btn:hover {
    border-color: rgba(0,245,255,0.7) !important;
    box-shadow: 0 0 20px rgba(0,245,255,0.25) !important;
    color: #00f5ff !important;
    transform: translateY(-2px) !important;
}

/* ── Streamlit buttons ── */
.stButton > button {
    background: linear-gradient(135deg, rgba(0,100,180,0.6), rgba(120,40,200,0.6)) !important;
    border: 1px solid rgba(0,245,255,0.5) !important;
    border-radius: 12px !important;
    color: #e0f0ff !important;
    font-family: 'Orbitron', monospace !important;
    font-size: 0.85rem !important;
    font-weight: 700 !important;
    letter-spacing: 2px !important;
    padding: 0.7rem 1.5rem !important;
    cursor: pointer;
    transition: all 0.3s ease !important;
    width: 100% !important;
    text-transform: uppercase !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, rgba(0,150,220,0.8), rgba(160,60,250,0.8)) !important;
    box-shadow: 0 0 30px rgba(0,245,255,0.4), 0 0 60px rgba(168,85,247,0.3) !important;
    transform: translateY(-3px) !important;
    border-color: #00f5ff !important;
}

/* ── Tone selector custom ── */
.tone-card {
    background: linear-gradient(135deg, rgba(10,5,30,0.9), rgba(30,15,60,0.9));
    border: 1px solid rgba(120,80,200,0.35);
    border-radius: 14px;
    padding: 1.2rem;
    text-align: center;
    transition: all 0.35s ease;
    cursor: pointer;
    position: relative;
    overflow: hidden;
}
.tone-card.selected {
    border-color: #00f5ff !important;
    box-shadow: 0 0 25px rgba(0,245,255,0.35), inset 0 0 20px rgba(0,245,255,0.05);
}
.tone-card:hover { transform: translateY(-4px); border-color: rgba(0,245,255,0.5); }
.tone-icon { font-size: 2rem; margin-bottom: 0.4rem; }
.tone-name {
    font-family: 'Orbitron', monospace;
    font-size: 0.85rem;
    font-weight: 700;
    letter-spacing: 2px;
    color: #a0c0ff;
}
.tone-desc { font-size: 0.78rem; color: rgba(160,200,255,0.55); margin-top: 0.3rem; line-height: 1.4; }

/* ── Status / output ── */
.output-panel {
    background: linear-gradient(135deg, rgba(0,30,10,0.6), rgba(0,60,40,0.3));
    border: 1px solid rgba(0,200,100,0.3);
    border-radius: 14px;
    padding: 1.5rem;
    backdrop-filter: blur(20px);
}
.output-text {
    font-family: 'Rajdhani', sans-serif;
    font-size: 1rem;
    color: #a0ffcc;
    white-space: pre-wrap;
    line-height: 1.7;
}

/* ── Back button ── */
.back-btn > button {
    background: transparent !important;
    border: 1px solid rgba(120,80,200,0.4) !important;
    color: rgba(160,200,255,0.7) !important;
    font-size: 0.8rem !important;
    padding: 0.4rem 1rem !important;
    width: auto !important;
}

/* ── Divider ── */
.cosmic-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(0,245,255,0.4), rgba(168,85,247,0.4), transparent);
    margin: 2rem 0;
    border: none;
}

/* ── Radio buttons ── */
[data-testid="stRadio"] > div { gap: 0.5rem !important; }
[data-testid="stRadio"] label {
    background: rgba(10,5,30,0.7) !important;
    border: 1px solid rgba(120,80,200,0.35) !important;
    border-radius: 10px !important;
    padding: 0.5rem 1rem !important;
    transition: all 0.3s !important;
}
[data-testid="stRadio"] label:hover {
    border-color: rgba(0,245,255,0.5) !important;
    box-shadow: 0 0 15px rgba(0,245,255,0.15) !important;
}

/* ── Labels ── */
label, .stSelectbox label, .stDateInput label, .stTextInput label, .stTextArea label {
    color: rgba(160,200,255,0.8) !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 0.9rem !important;
    letter-spacing: 1px !important;
    font-weight: 600 !important;
}

/* ── Alerts / info boxes ── */
[data-testid="stAlert"] {
    background: rgba(10,5,30,0.8) !important;
    border: 1px solid rgba(120,80,200,0.4) !important;
    border-radius: 10px !important;
    color: #c0d0ff !important;
}

/* ── Spinner ── */
[data-testid="stSpinner"] { color: #00f5ff !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: rgba(10,5,30,0.5); }
::-webkit-scrollbar-thumb { background: rgba(120,80,200,0.5); border-radius: 3px; }
</style>
"""

GALAXY_JS = """
<canvas id="galaxy-canvas"></canvas>
<div class="nebula-overlay"></div>
<script>
(function(){
    const canvas = document.getElementById('galaxy-canvas');
    const ctx = canvas.getContext('2d');
    let W, H, stars=[], nebulas=[], shootingStars=[];

    function resize(){
        W = canvas.width  = window.innerWidth;
        H = canvas.height = window.innerHeight;
    }
    resize();
    window.addEventListener('resize', resize);

    // Stars
    for(let i=0;i<350;i++){
        stars.push({
            x: Math.random()*W, y: Math.random()*H,
            r: Math.random()*1.5+0.2,
            a: Math.random(),
            speed: Math.random()*0.008+0.002,
            color: ['#ffffff','#c0d8ff','#ffd0a0','#d0c0ff','#a0e8ff'][Math.floor(Math.random()*5)]
        });
    }

    // Nebula particles
    for(let i=0;i<120;i++){
        nebulas.push({
            x: Math.random()*W, y: Math.random()*H,
            r: Math.random()*3+1,
            a: Math.random()*0.4+0.05,
            dx: (Math.random()-0.5)*0.15,
            dy: (Math.random()-0.5)*0.15,
            color: ['rgba(120,40,200','rgba(0,100,255','rgba(0,200,180','rgba(200,50,150'][Math.floor(Math.random()*4)]
        });
    }

    function spawnShooting(){
        if(Math.random()<0.008){
            const y = Math.random()*H*0.5;
            shootingStars.push({
                x: Math.random()*W*0.5, y,
                dx: Math.random()*6+4, dy: Math.random()*2+1,
                len: Math.random()*120+60,
                a: 1, fade: Math.random()*0.015+0.012
            });
        }
    }

    function draw(){
        ctx.clearRect(0,0,W,H);

        // Nebula particles
        nebulas.forEach(n=>{
            n.x+=n.dx; n.y+=n.dy;
            if(n.x<0)n.x=W; if(n.x>W)n.x=0;
            if(n.y<0)n.y=H; if(n.y>H)n.y=0;
            ctx.beginPath();
            const g=ctx.createRadialGradient(n.x,n.y,0,n.x,n.y,n.r*6);
            g.addColorStop(0,n.color+','+n.a+')');
            g.addColorStop(1,n.color+',0)');
            ctx.fillStyle=g;
            ctx.arc(n.x,n.y,n.r*6,0,Math.PI*2);
            ctx.fill();
        });

        // Stars
        const t = Date.now()/1000;
        stars.forEach(s=>{
            const alpha = 0.4+0.6*Math.abs(Math.sin(t*s.speed*Math.PI*2+s.a*100));
            ctx.beginPath();
            ctx.arc(s.x,s.y,s.r,0,Math.PI*2);
            ctx.fillStyle = s.color.replace(')',`,${alpha})`).replace('rgb','rgba').replace('#','').length>7
                ? s.color : hexToRgba(s.color,alpha);
            ctx.fill();
        });

        // Shooting stars
        spawnShooting();
        shootingStars = shootingStars.filter(s=>{
            s.x+=s.dx; s.y+=s.dy; s.a-=s.fade;
            if(s.a<=0) return false;
            const g=ctx.createLinearGradient(s.x,s.y,s.x-s.len,s.y-s.len*0.3);
            g.addColorStop(0,`rgba(255,255,255,${s.a})`);
            g.addColorStop(1,'rgba(255,255,255,0)');
            ctx.beginPath();
            ctx.strokeStyle=g;
            ctx.lineWidth=1.5;
            ctx.moveTo(s.x,s.y);
            ctx.lineTo(s.x-s.len,s.y-s.len*0.3);
            ctx.stroke();
            return true;
        });

        requestAnimationFrame(draw);
    }

    function hexToRgba(hex,a){
        const r=parseInt(hex.slice(1,3),16),g=parseInt(hex.slice(3,5),16),b=parseInt(hex.slice(5,7),16);
        return `rgba(${r},${g},${b},${a})`;
    }

    draw();
})();
</script>
"""


# ── Document Number Generator ──────────────────────────────────────────────────
def generate_document_number() -> str:
    counter = st.session_state.get('doc_number_counter', 100)
    date_part = date.today().strftime('%d%m%Y')
    doc_num = f"PEX-IM-R0{counter}{date_part}"
    st.session_state.doc_number_counter = counter + 1
    return doc_num


# ── PDF Generator ─────────────────────────────────────────────────────────────
def generate_pdf(data: dict, rca_content: str, uploaded_image: bytes = None) -> bytes:
    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf, pagesize=A4,
        leftMargin=20*mm, rightMargin=20*mm,
        topMargin=20*mm, bottomMargin=20*mm
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'RCATitle', parent=styles['Normal'],
        fontSize=20, fontName='Helvetica-Bold',
        textColor=colors.HexColor('#1a237e'),
        alignment=TA_CENTER, spaceAfter=4*mm, spaceBefore=2*mm
    )
    company_style = ParagraphStyle(
        'Company', parent=styles['Normal'],
        fontSize=10, fontName='Helvetica',
        textColor=colors.HexColor('#555555'),
        alignment=TA_CENTER, spaceAfter=8*mm
    )
    section_style = ParagraphStyle(
        'Section', parent=styles['Normal'],
        fontSize=12, fontName='Helvetica-Bold',
        textColor=colors.HexColor('#0d47a1'),
        spaceBefore=5*mm, spaceAfter=2*mm,
        borderPad=2, leftIndent=0
    )
    body_style = ParagraphStyle(
        'Body', parent=styles['Normal'],
        fontSize=10, fontName='Helvetica',
        textColor=colors.HexColor('#212121'),
        spaceAfter=2*mm, leading=15,
        alignment=TA_JUSTIFY
    )
    bullet_style = ParagraphStyle(
        'Bullet', parent=styles['Normal'],
        fontSize=10, fontName='Helvetica',
        textColor=colors.HexColor('#212121'),
        leftIndent=10*mm, bulletIndent=4*mm,
        spaceAfter=1.5*mm, leading=14
    )
    meta_key_style = ParagraphStyle(
        'MetaKey', parent=styles['Normal'],
        fontSize=10, fontName='Helvetica-Bold',
        textColor=colors.HexColor('#0d47a1')
    )
    meta_val_style = ParagraphStyle(
        'MetaVal', parent=styles['Normal'],
        fontSize=10, fontName='Helvetica',
        textColor=colors.HexColor('#212121')
    )
    tone_style = ParagraphStyle(
        'Tone', parent=styles['Normal'],
        fontSize=8, fontName='Helvetica-Oblique',
        textColor=colors.HexColor('#888888'),
        alignment=TA_CENTER, spaceAfter=3*mm
    )

    story = []

    # Header bar
    header_data = [[Paragraph('<b>ROOT CAUSE ANALYSIS REPORT</b>', ParagraphStyle(
        'H', parent=styles['Normal'], fontSize=14, fontName='Helvetica-Bold',
        textColor=colors.white, alignment=TA_CENTER
    ))]]
    header_table = Table(header_data, colWidths=[170*mm])
    header_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#1a237e')),
        ('ROUNDEDCORNERS', [4]),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 4*mm))



    # Generate document number and metadata
    doc_number = data.get('doc_number', generate_document_number())
    
    # Meta info table
    meta_rows = [
        ['Service Impacted:', data['merchant']],
        ['Region:', data['region']],
        ['Date:', data['date_str']],
        ['Report Type:', data['report_type'] if 'report_type' in data else data['rca_type'].upper()],
        ['Document Number:', doc_number],
        ['Custody:', 'Service Delivery'],
        ['Incident Manager:', '@Qwais Khalid'],
        ['Heading:', data['heading']],
    ]
    meta_table_data = [[
        Paragraph(r[0], meta_key_style),
        Paragraph(r[1], meta_val_style)
    ] for r in meta_rows]
    meta_table = Table(meta_table_data, colWidths=[40*mm, 125*mm])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,-1), colors.HexColor('#e8eaf6')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#c5cae9')),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 5*mm))

    # Parse and render RCA content
    lines = rca_content.strip().split('\n')
    current_section = None

    for line in lines:
        line = line.strip()
        if not line:
            story.append(Spacer(1, 2*mm))
            continue

        # Section headers (lines ending with colon or all caps titles)
        if (line.endswith(':') and len(line) < 60 and not line.startswith('*') and not line.startswith('-')) \
           or (line.isupper() and len(line) > 3) \
           or any(line.startswith(kw) for kw in [
               'Incident Summary', 'Issue Observed', 'Impact Details',
               'Root Cause Analysis', 'Actions Taken', 'Current Status',
               'Timeline', 'Recommendations', 'Service Impacted',
               'Compliance API', 'Summary', 'Root Cause', 'Resolution'
           ]):
            story.append(HRFlowable(width='100%', thickness=1, color=colors.HexColor('#c5cae9'), spaceAfter=2*mm))
            story.append(Paragraph(line, section_style))
            current_section = line
        elif line.startswith('* ') or line.startswith('- ') or line.startswith('• '):
            text = line[2:].strip()
            story.append(Paragraph(f'• {text}', bullet_style))
        elif line.startswith('**') and line.endswith('**'):
            story.append(Paragraph(f'<b>{line[2:-2]}</b>', body_style))
        else:
            story.append(Paragraph(line, body_style))

    # Insert uploaded image if available
    if uploaded_image:
        story.append(Spacer(1, 8*mm))
        story.append(HRFlowable(width='100%', thickness=0.5, color=colors.HexColor('#9fa8da')))
        story.append(Spacer(1, 5*mm))
        story.append(Paragraph('Issue Insight', section_style))
        story.append(Spacer(1, 3*mm))
        from reportlab.platypus import Image as RLImage
        try:
            img = RLImage(io.BytesIO(uploaded_image), width=150*mm, height=100*mm)
            story.append(img)
        except:
            story.append(Paragraph('[Image could not be rendered]', body_style))

    doc.build(story)
    return buf.getvalue()


# ── BOKU RCA Generator ────────────────────────────────────────────────────────
def generate_boku_rca(data: dict) -> str:
    return """Service Impacted
JazzCash BOKU Collection - {merchant}

Date
{date_str}

Incident Summary
Transactions were failing due to an OTP delivery issue at the operator end. Users were unable to receive the OTP required to complete the transaction flow. As a result, transactions were getting failed at the hosted (tokenization) page of JazzCash (JC), as the end users could not proceed with OTP submission and verification. This issue impacted the successful completion of the payment flow and led to transaction failures from the user side, despite the transaction being successfully initiated.

Issue Observed
* OTP delivery failures at operator end
* Users unable to receive OTP for transaction verification
* Transactions stuck at hosted page (tokenization) flow
* End users unable to proceed with OTP submission

Impact Details
* Hosted page transaction failures
* User-side transaction failures despite successful initiation
* Disrupted payment completion flow
* Impacted user experience and transaction success rate

Root Cause Analysis
* Operator-side OTP delivery issue at JazzCash end
* Users could not receive OTP
* Prevention of hosted page/tokenization flow completion

Actions Taken
* Monitored issue and correlated with operator-side OTP delivery degradation
* Reviewed transaction flow logs and hosted page attempts
* Confirmed requests initiated successfully but OTP not received
* Escalated issue to operator team
* Performed continuous monitoring until OTP delivery stabilized

Current Status
The issue has been resolved through operator team intervention. OTP delivery has stabilized and transaction flows have returned to normal.

Monitoring
Yes — Continuous monitoring and alerting in place

Recommendations
* Implement monitoring and alerting for hosted page failures
* Detection of OTP-related drop-offs and anomalies
* Set threshold-based alerts for OTP delivery degradation
* Establish faster escalation procedures to operator team
* Maintain continuous monitoring for prevention of future occurrences
""".format(merchant=data['merchant'], date_str=data['date_str'])


# ── Claude RCA Generator ──────────────────────────────────────────────────────────
def generate_rca_with_claude(data: dict) -> str:
    tone = data['tone']
    issue = data['issue']
    merchant = data['merchant']
    region = data['region']
    date_str = data['date_str']
    heading = data['heading']
    rca_type = data['rca_type']

    tone_instructions = {
        'Accurate': """
Generate a completely honest and technically accurate RCA. 
- Describe EXACTLY what happened based on the issue description.
- Be precise, factual, and professional.
- Do NOT hide, downplay, or deflect responsibility.
- Clearly state what failed and why, as described.
- If it was an internal issue, state it clearly.
""",
        'Median': """
Generate a balanced RCA that presents the facts but with careful wording.
- Acknowledge the issue without being overly self-incriminating.
- Use diplomatic language: "challenges were encountered", "complexities arose".
- Partially acknowledge responsibility while also mentioning external factors.
- The tone should be professional but slightly defensive where needed.
- This is a MEDIAN / middle-ground version — not fully transparent, not fully deflecting.
""",
        'Topi': """
Generate an RCA that cleverly shifts focus/blame to an external entity or third-party vendor.
- The issue described should be subtly reframed as being caused by an external party, vendor, or upstream system.
- Write professionally and convincingly — it should sound legitimate.
- Make it seem like your team did everything right but a third-party/external API/provider caused the issue.
- This is "Topi mode" — putting the topi (blame hat) on someone else convincingly.
- Still maintain professional RCA format and language.
"""
    }

    prompt = f"""You are an expert technical writer specializing in Root Cause Analysis (RCA) documents for payment and fintech companies.

Generate a complete, professionally formatted RCA document for the following incident:

**Report Type:** {'REMITTANCE' if rca_type == 'payout_remittance' else 'DISBURSEMENT'}
**Region:** {region}
**Merchant/Service:** {merchant}
**Date/Period:** {date_str}
**Heading/Title:** {heading}
**Issue Description (may be in Urdu/Roman Urdu or English):** {issue}

**TONE INSTRUCTIONS:**
{tone_instructions[tone]}

**OUTPUT FORMAT — Follow this exact structure:**

Service Impacted:
[merchant and region details]

Date:
[formatted date]

Incident Summary
[1-2 paragraph comprehensive summary of what happened]

Issue Observed

* [bullet point 1]
* [bullet point 2]
* [bullet point 3]
* [add more as needed]

Impact Details

* [impact bullet 1]
* [impact bullet 2]
* [impact bullet 3]

Root Cause Analysis

* [root cause 1 — be specific]
* [root cause 2]
* [supporting technical details]


Actions Taken

* [action 1]
* [action 2]
* [action 3]

Current Status

[current status paragraph — 2-3 sentences]

Recommendations

* [recommendation 1]
* [recommendation 2]
* [recommendation 3]

Important notes:
- If the issue description is in Urdu or Roman Urdu, fully understand it and generate the RCA in professional English.
- Be technically sound and use appropriate fintech/payment industry terminology.
- The RCA should look like it was written by a senior technical team at a payment company.
- Do NOT include any preamble, explanation, or commentary outside the RCA format.
- Start directly with "Service Impacted:" and end after "Recommendations".
"""

    client = Groq(api_key=GROQ_API_KEY)
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content




# ── Session state init ────────────────────────────────────────────────────────
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'rca_type' not in st.session_state:
    st.session_state.rca_type = None
if 'generated_rca' not in st.session_state:
    st.session_state.generated_rca = None
if 'pdf_bytes' not in st.session_state:
    st.session_state.pdf_bytes = None
if 'form_data' not in st.session_state:
    st.session_state.form_data = None
if 'doc_number_counter' not in st.session_state:
    st.session_state.doc_number_counter = 100

# ── Inject galaxy ─────────────────────────────────────────────────────────────
st.markdown(GALAXY_CSS, unsafe_allow_html=True)
st.html(GALAXY_JS)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: HOME
# ═══════════════════════════════════════════════════════════════════════════════
if st.session_state.page == 'home':
    st.markdown('<br>', unsafe_allow_html=True)
    st.markdown('<div class="main-title">⚡ AUTO RCA GENERATOR</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Intelligent Incident Report & Root Cause Analysis</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div class="card-container">
            <div class="rca-card" id="remittance-card">
                <div class="card-icon">📥</div>
                <div class="card-title">REMITTANCE</div>
                <div class="card-desc">Generate RCA for remittance failures, inbound transaction errors, and collection issues</div>
            </div>
            <div class="rca-card" id="payout-card">
                <div class="card-icon">📤</div>
                <div class="card-title">DISBURSEMENT</div>
                <div class="card-desc">Generate RCA for disbursement failures, payout processing issues, and outbound transaction errors</div>
            </div>
            <div class="rca-card" id="boku-card">
                <div class="card-icon">🔐</div>
                <div class="card-title">COLLECTION-BOKU</div>
                <div class="card-desc">Generate RCA for BOKU collection failures and OTP delivery issues</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<br>', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("📥  REMITTANCE RCA", use_container_width=True):
                st.session_state.rca_type = 'payout_remittance'
                st.session_state.page = 'form'
                st.rerun()
        with c2:
            if st.button("📤  DISBURSEMENT RCA", use_container_width=True):
                st.session_state.rca_type = 'payout'
                st.session_state.page = 'form'
                st.rerun()
        with c3:
            if st.button("🔐  COLLECTION-BOKU", use_container_width=True):
                st.session_state.rca_type = 'collection_boku'
                st.session_state.page = 'form'
                st.rerun()

    st.markdown('<br><br>', unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align:center; color:rgba(120,160,255,0.4); font-size:0.8rem; letter-spacing:3px;">
        POWERED BY CLAUDE AI &nbsp;•&nbsp; AUTO RCA SYSTEM &nbsp;•&nbsp; v1.0
    </div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: FORM
# ═══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == 'form':
    rca_type = st.session_state.rca_type
    if rca_type == 'payout_remittance':
        type_label = "REMITTANCE"
        type_icon = "📥"
        show_merchant_form = True
        use_boku_template = False
    elif rca_type == 'collection_boku':
        type_label = "COLLECTION-BOKU"
        type_icon = "🔐"
        show_merchant_form = False
        use_boku_template = True
    else:
        type_label = "DISBURSEMENT"
        type_icon = "📤"
        show_merchant_form = True
        use_boku_template = False

    # Back button
    col_back, _ = st.columns([1, 5])
    with col_back:
        st.markdown('<div class="back-btn">', unsafe_allow_html=True)
        if st.button("← Back"):
            st.session_state.page = 'home'
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown(f'<div class="section-heading">{type_icon} {type_label} — Let\'s Build Your IRT/RCA</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Fill in the incident details below</div>', unsafe_allow_html=True)

    # ── Region/Merchant OUTSIDE form so dropdown updates live ──────────────────
    if show_merchant_form:
        st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-label">📍 Merchant Selection</div>', unsafe_allow_html=True)

        if rca_type == 'payout_remittance':
            col_r, col_m = st.columns(2)
            with col_r:
                region = st.selectbox("Select Region", options=["PK", "BD", "NP", "OTHER"], index=0)
            with col_m:
                merchant_options = REMITTANCE_MERCHANTS.get(region, [])
                if not merchant_options:
                    merchant_options = ["No merchants listed for this region"]
                merchant = st.selectbox("Select Merchant", options=merchant_options)
        else:
            region = "Disbursement"
            col_info, col_m = st.columns([1, 2])
            with col_info:
                st.markdown("""
                <div style="background:rgba(0,200,120,0.06);border:1px solid rgba(0,200,120,0.25);
                border-radius:10px;padding:0.8rem 1rem;margin-top:0.5rem;">
                    <div style="color:#00e676;font-size:0.75rem;letter-spacing:2px;font-weight:700;">DISBURSEMENT</div>
                    <div style="color:rgba(160,255,200,0.7);font-size:0.8rem;margin-top:0.3rem;">
                        Global disbursement merchants — not region-specific
                    </div>
                </div>
                """, unsafe_allow_html=True)
            with col_m:
                merchant = st.selectbox("Select Disbursement Merchant", options=DISBURSEMENT_MERCHANTS)

        st.markdown('</div>', unsafe_allow_html=True)
    else:
        region = "BOKU"
        merchant = "JazzCash BOKU Collection"

    # ── FORM ──────────────────────────────────────────────────────────────────
    with st.form("rca_form", clear_on_submit=False):
        # Date
        st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-label">📅 Date / Date Range</div>', unsafe_allow_html=True)
        col_d1, col_d2, col_d3 = st.columns([1, 1, 1])
        with col_d1:
            date_type = st.radio("Date Type", ["Single Date", "Date Range"], horizontal=True)
        with col_d2:
            start_date = st.date_input("Start Date", value=date.today())
        with col_d3:
            end_date = st.date_input("End Date", value=date.today())
        st.markdown('</div>', unsafe_allow_html=True)

        # Heading
        st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-label">📌 Incident Heading</div>', unsafe_allow_html=True)
        heading = st.text_input(
            "Incident Title / Heading",
            placeholder="e.g. Safewatch Eastnets Compliance API Outage"
        )
        st.markdown('</div>', unsafe_allow_html=True)

        # Issue Description
        st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-label">📝 Issue Description (English / Urdu / Roman Urdu)</div>', unsafe_allow_html=True)
        if use_boku_template:
            st.info("ℹ️ BOKU report will use predefined template. Custom issue description is optional for context.")
            issue = st.text_area(
                "Describe the Issue (Optional for BOKU)",
                height=80,
                placeholder="Optional: Add context or specifics..."
            )
        else:
            issue = st.text_area(
                "Describe the Issue",
                height=150,
                placeholder="Ap Urdu ya English mein issue describe kar sakte hain...\nExample: Compliance API mein intermittent errors aa rahe thy, transactions IN_PROCESS pe stuck ho gayi theen..."
            )
        st.markdown('</div>', unsafe_allow_html=True)

        # Tone Selector (skip for BOKU)
        if not use_boku_template:
            st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
            st.markdown('<div class="panel-label">🎚️ Report Mode / Tone</div>', unsafe_allow_html=True)

            tone_col1, tone_col2, tone_col3 = st.columns(3)
            with tone_col1:
                st.markdown("""
                <div class="tone-card" style="border-color: rgba(0,200,80,0.5);">
                    <div class="tone-icon">✅</div>
                    <div class="tone-name" style="color:#00e676;">ACCURATE</div>
                    <div class="tone-desc">Full transparency — exactly what happened, no filters</div>
                </div>
                """, unsafe_allow_html=True)
            with tone_col2:
                st.markdown("""
                <div class="tone-card" style="border-color: rgba(255,160,0,0.5);">
                    <div class="tone-icon">⚖️</div>
                    <div class="tone-name" style="color:#ffab40;">MEDIAN</div>
                    <div class="tone-desc">Balanced — facts presented diplomatically, some self-protection</div>
                </div>
                """, unsafe_allow_html=True)
            with tone_col3:
                st.markdown("""
                <div class="tone-card" style="border-color: rgba(180,60,255,0.5);">
                    <div class="tone-icon">🎭</div>
                    <div class="tone-name" style="color:#ce93d8;">TOPI</div>
                    <div class="tone-desc">Blame redirected — third-party / external entity is responsible</div>
                </div>
                """, unsafe_allow_html=True)

            tone = st.radio(
                "Select Mode",
                options=["Accurate", "Median", "Topi"],
                horizontal=True,
                label_visibility="collapsed"
            )
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            tone = "Accurate"

        # Image Upload
        st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
        st.markdown('<div class="panel-label">🖼️ Add Insights (Image Upload)</div>', unsafe_allow_html=True)
        uploaded_image = st.file_uploader(
            "Upload an image for insights",
            type=["jpg", "jpeg", "png", "gif"],
            label_visibility="collapsed"
        )
        st.markdown('</div>', unsafe_allow_html=True)

        # Submit
        st.markdown('<br>', unsafe_allow_html=True)
        submitted = st.form_submit_button("🚀  GENERATE RCA", use_container_width=True)

    # ── Process form ──────────────────────────────────────────────────────────
    if submitted:
        if not heading.strip():
            st.error("⚠️ Please enter an incident heading.")
        elif not use_boku_template and not issue.strip():
            st.error("⚠️ Please describe the issue.")
        else:
            if date_type == "Single Date":
                date_str = start_date.strftime("%d %B %Y")
            else:
                if start_date == end_date:
                    date_str = start_date.strftime("%d %B %Y")
                else:
                    date_str = f"{start_date.strftime('%d %B')} – {end_date.strftime('%d %B %Y')}"

            doc_number = generate_document_number()
            report_type = "Collection" if use_boku_template else ("Remittance" if rca_type == 'payout_remittance' else "Disbursement")

            form_data = {
                "rca_type": rca_type,
                "region": region,
                "merchant": merchant,
                "date_str": date_str,
                "heading": heading,
                "issue": issue,
                "tone": tone,
                "doc_number": doc_number,
                "report_type": report_type,
                "use_boku_template": use_boku_template,
            }
            st.session_state.form_data = form_data
            st.session_state.uploaded_image = uploaded_image.read() if uploaded_image else None

            with st.spinner("🌌 Generating RCA with Groq AI..."):
                try:
                    if use_boku_template:
                        rca_text = generate_boku_rca(form_data)
                    else:
                        rca_text = generate_rca_with_claude(form_data)
                    pdf_bytes = generate_pdf(form_data, rca_text, st.session_state.uploaded_image)
                    st.session_state.generated_rca = rca_text
                    st.session_state.pdf_bytes = pdf_bytes
                    st.session_state.page = 'result'
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error generating RCA: {str(e)}")


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: RESULT
# ═══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == 'result':
    data = st.session_state.form_data
    rca_text = st.session_state.generated_rca

    col_back, _ = st.columns([1, 5])
    with col_back:
        st.markdown('<div class="back-btn">', unsafe_allow_html=True)
        if st.button("← New RCA"):
            st.session_state.page = 'home'
            st.session_state.generated_rca = None
            st.session_state.pdf_bytes = None
            st.session_state.uploaded_image = None
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-heading">✅ RCA Generated Successfully</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Review, edit if needed, then download your PDF</div>', unsafe_allow_html=True)

    # Meta summary bar
    tone_colors = {'Accurate': '#00e676', 'Median': '#ffab40', 'Topi': '#ce93d8'}
    tc = tone_colors.get(data.get('tone', 'Accurate'), '#ffffff')
    if data['rca_type'] == 'payout_remittance':
        type_label_display = "REMITTANCE"
    elif data['rca_type'] == 'collection_boku':
        type_label_display = "COLLECTION-BOKU"
    else:
        type_label_display = "DISBURSEMENT"
    st.markdown(f"""
    <div class="glass-panel">
        <div style="display:flex; gap:2rem; flex-wrap:wrap; justify-content:center;">
            <div style="text-align:center;"><div style="color:rgba(160,200,255,0.6);font-size:0.75rem;letter-spacing:2px;">TYPE</div>
                <div style="color:#00f5ff;font-weight:700;font-size:1rem;">{type_label_display}</div></div>
            <div style="text-align:center;"><div style="color:rgba(160,200,255,0.6);font-size:0.75rem;letter-spacing:2px;">REGION</div>
                <div style="color:#00f5ff;font-weight:700;font-size:1rem;">{data['region']}</div></div>
            <div style="text-align:center;"><div style="color:rgba(160,200,255,0.6);font-size:0.75rem;letter-spacing:2px;">MERCHANT</div>
                <div style="color:#00f5ff;font-weight:700;font-size:1rem;">{data['merchant']}</div></div>
            <div style="text-align:center;"><div style="color:rgba(160,200,255,0.6);font-size:0.75rem;letter-spacing:2px;">DATE</div>
                <div style="color:#00f5ff;font-weight:700;font-size:1rem;">{data['date_str']}</div></div>
            <div style="text-align:center;"><div style="color:rgba(160,200,255,0.6);font-size:0.75rem;letter-spacing:2px;">MODE</div>
                <div style="color:{tc};font-weight:700;font-size:1rem;">{data['tone'].upper()}</div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Editable RCA text area ────────────────────────────────────────────────
    st.markdown("""
    <div class="glass-panel" style="border-color:rgba(0,245,255,0.25);">
        <div class="panel-label" style="color:#00f5ff;">✏️ Edit RCA Before Download</div>
        <div style="color:rgba(160,200,255,0.55);font-size:0.82rem;margin-bottom:0.8rem;">
            You can freely edit the text below — corrections will reflect in the downloaded PDF.
        </div>
    </div>
    """, unsafe_allow_html=True)

    edited_rca = st.text_area(
        label="RCA Content (Editable)",
        value=rca_text,
        height=500,
        key="rca_editor",
        label_visibility="collapsed",
    )

    # ── Action buttons ────────────────────────────────────────────────────────
    st.markdown('<br>', unsafe_allow_html=True)
    col_dl, col_regen, col_reset = st.columns(3)

    # Generate PDF from whatever is currently in the editor
    with col_dl:
        merchant_code = data['merchant'].split('-')[0].strip() if '-' in data['merchant'] else data['merchant'].split()[0]
        filename = f"RCA_{type_label_display}_{data['region']}_{merchant_code}_{date.today().strftime('%Y%m%d')}.pdf"
        live_pdf = generate_pdf(data, edited_rca, st.session_state.get('uploaded_image', None))
        st.download_button(
            label="📥  DOWNLOAD PDF",
            data=live_pdf,
            file_name=filename,
            mime="application/pdf",
            use_container_width=True
        )

    with col_regen:
        if st.button("🔄  Regenerate", use_container_width=True):
            st.session_state.page = 'form'
            st.rerun()

    with col_reset:
        if st.button("↩️  Reset Edits", use_container_width=True):
            # Restore original AI-generated text
            st.session_state.generated_rca = rca_text
            st.session_state['rca_editor_reset'] = True
            st.rerun()