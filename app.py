import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import json
from streamlit_lottie import st_lottie
from parser import extract_text
from clause_splitter import split_clauses
from risk_analyzer import analyze_clause
from report_generator import generate_pdf_report, generate_txt_report
from hindi_fixer import kruti_to_unicode

# --- Page Config ---
st.set_page_config(page_title="Contract Insight AI", layout="wide", page_icon="⚖️")

# --- Animation Loader (With Error Handling) ---
def load_lottieurl(url):
    try:
        r = requests.get(url, timeout=5)
        if r.status_code != 200:
            return None
        return r.json()
    except Exception:
        return None

# UPDATED 3D ANIMATION LINKS
# 1. 3D Legal Scale Character
lottie_main_char = load_lottieurl("https://lottie.host/82823654-e403-4c91-9e73-982d1c60a87a/7xYpX4mQ6J.json")
# 2. 3D Security Shield
lottie_risk = load_lottieurl("https://lottie.host/41993780-0015-4405-8731-182066376635/pY1G4d8d7a.json")
# 3. 3D Global Language
lottie_hindi = load_lottieurl("https://lottie.host/98685764-8834-4576-8767-664854344847/g444544555.json")

# --- Premium Glassmorphism CSS ---
st.markdown("""
    <style>
    /* Gradient Background */
    .stApp {
        background: radial-gradient(circle at top right, #1e1b4b, #0f172a);
        color: #f8fafc;
    }
    
    /* 3D Title Styling */
    .hero-title {
        font-size: 4rem !important;
        font-weight: 800 !important;
        background: linear-gradient(to right, #f1c40f, #e67e22);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        filter: drop-shadow(0 5px 15px rgba(241, 196, 15, 0.3));
        margin-bottom: 0px;
    }

    /* Animated Glass Cards */
    .feature-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(12px);
        border-radius: 24px;
        padding: 30px;
        text-align: center;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    .feature-card:hover {
        transform: translateY(-15px) rotateX(5deg);
        background: rgba(255, 255, 255, 0.07);
        border: 1px solid #f1c40f;
        box-shadow: 0 20px 50px rgba(0,0,0,0.5);
    }

    /* Custom Buttons */
    .stButton>button {
        background: linear-gradient(90deg, #f1c40f 0%, #f39c12 100%) !important;
        color: #0f172a !important;
        border: none !important;
        border-radius: 50px !important;
        padding: 15px 40px !important;
        font-weight: 800 !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* Metrics Visibility Fix */
    div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 20px !important;
        padding: 20px !important;
    }
    div[data-testid="stMetricValue"] > div { color: #f1c40f !important; }
    </style>
""", unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.markdown("## ⚙️ Control Center")
    uploaded_file = st.file_uploader("📂 Drop Contract File", type=["pdf", "docx", "txt"])
    st.divider()
    use_legacy_fix = st.checkbox("🛠️ Legacy Hindi Fix", help="Use if text looks like 'Hkkxhnkjh'")
    

# --- Main Page UI ---
if not uploaded_file:
    # --- UPGRADED 3D HOME PAGE ---
    col_left, col_right = st.columns([1.2, 1])
    
    with col_left:
        st.markdown('<p class="hero-title">Contract Insight AI</p>', unsafe_allow_html=True)
        st.markdown("### Next-Gen Legal Intelligence.")
        st.write("Stop wasting hours on manual review. Our AI character scans your documents for red flags, missing clauses, and legal traps in seconds.")
        
        st.write("") # Spacer
        st.markdown("#### ✨ How to start:")
        st.info("Please upload a document in the **Sidebar** to activate the 3D Scanner.")

    with col_right:
        # The "Character" Animation
        if lottie_main_char:
            st_lottie(lottie_main_char, height=450, key="main_hero")
        else:
            # High-end fallback image if Lottie fails
            st.image("https://cdn-icons-png.flaticon.com/512/2621/2621040.png", width=350)

    st.divider()

    # Feature Grid
    f1, f2, f3 = st.columns(3)
    
    with f1:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        if lottie_risk: st_lottie(lottie_risk, height=150, key="f1")
        st.markdown("<h3 style='color:#f1c40f'>Risk Shield</h3>", unsafe_allow_html=True)
        st.write("Automatically scores every clause from Safe to Critical.")
        st.markdown('</div>', unsafe_allow_html=True)

    with f2:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        if lottie_hindi: st_lottie(lottie_hindi, height=150, key="f2")
        st.markdown("<h3 style='color:#f1c40f'>Bilingual AI</h3>", unsafe_allow_html=True)
        st.write("Native-level understanding of English & Hindi legal text.")
        st.markdown('</div>', unsafe_allow_html=True)

    with f3:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        # Use a high-quality static icon as a secondary character if lottie fails
        st.image("https://cdn-icons-png.flaticon.com/512/3222/3222642.png", width=120)
        st.markdown("<h3 style='color:#f1c40f'>Deep Audit</h3>", unsafe_allow_html=True)
        st.write("Summarizes complex legal jargon into plain language.")
        st.markdown('</div>', unsafe_allow_html=True)

else:
    # --- ANALYSIS WORKFLOW ---
    with st.spinner("🕵️ AI Character is scanning your contract..."):
        raw_text = extract_text(uploaded_file)
        text = kruti_to_unicode(raw_text) if use_legacy_fix else raw_text
        
        if not text:
            st.error("Text extraction failed. Try a digital PDF.")
            st.stop()

        clauses = split_clauses(text)
        analysis_data = []
        risk_counts = {"High": 0, "Medium": 0, "Low": 0}
        
        # UI Progress Bar for 3D Feel
        progress_bar = st.progress(0)
        for i, clause_text in enumerate(clauses, start=1):
            res = analyze_clause(clause_text)
            res['clause'] = clause_text
            res['id'] = i
            analysis_data.append(res)
            risk_counts[res['risk']] += 1
            progress_bar.progress(i / len(clauses))
        
        df = pd.DataFrame(analysis_data)
        
        # Overall Score
        status = "CRITICAL" if risk_counts["High"] >= 3 else "MODERATE" if risk_counts["High"] >= 1 else "SAFE"

    # --- Dashboard View ---
    st.title(f"📊 Audit: {uploaded_file.name}")
    
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Overall Score", status)
    m2.metric("Total Clauses", len(clauses))
    m3.metric("Red Flags 🚩", risk_counts["High"])
    m4.metric("Review Items ⚠️", risk_counts["Medium"])

    st.divider()
    
    tab1, tab2, tab3 = st.tabs(["🎯 Visual Insights", "🔍 Detailed Audit", "📥 Reports"])

    with tab1:
        c1, c2 = st.columns([1, 1.2])
        with c1:
            fig = px.pie(df, names='risk', hole=0.6, 
                         color='risk',
                         color_discrete_map={'High':'#ef4444', 'Medium':'#f59e0b', 'Low':'#10b981'})
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color="white")
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            st.subheader("⚠️ Critical Red Flags")
            for _, r in df[df["risk"] == "High"].iterrows():
                st.error(f"**Clause {r['id']}:** {r['explanation']}")

    with tab2:
        for _, r in df.iterrows():
            with st.expander(f"Clause {r['id']} — {r['risk']} Risk"):
                st.write(f"**AI Analysis:** {r['explanation']}")
                st.success(f"**Fix:** {r['suggestion']}")
                st.text_area("Original Text", r['clause'], height=80, disabled=True)

    with tab3:
        # Download Logic
        col_pdf, col_txt = st.columns(2)
        pdf = generate_pdf_report(uploaded_file.name, status, analysis_data)
        st.download_button("📄 Download PDF Report", data=pdf, file_name="Audit.pdf")