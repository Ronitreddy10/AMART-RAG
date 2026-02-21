import streamlit as st
import time
import requests
import json
from streamlit_lottie import st_lottie
import os

# Import our actual attack modules
import text_attack
import image_attack
import pdf_poison
import utils
import config

# ---------------------------------------------------------
# SETUP & CONFIG
# ---------------------------------------------------------
st.set_page_config(
    page_title="Red Team Command Center",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# CUSTOM CSS (CYBERPUNK THEME)
# ---------------------------------------------------------
st.markdown("""
<style>
    /* Main Background */
    .stApp {
        background-color: #0d0208;
        color: #00ff41;
        font-family: 'Courier New', Courier, monospace;
    }
    
    /* Remove white header bar */
    header {visibility: hidden;}
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #050104;
        border-right: 1px solid #1e1e1e;
    }
    
    /* Buttons */
    .stButton button {
        background-color: #000000;
        color: #00ff41;
        border: 1px solid #00ff41;
        border-radius: 5px;
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 2px;
        font-weight: bold;
    }
    .stButton button:hover {
        background-color: #00ff41;
        color: #000000;
        box-shadow: 0 0 10px #00ff41;
    }
    
    /* Metric Cards */
    div[data-testid="metric-container"] {
        background-color: #0a0a0a;
        border: 1px solid #333;
        border-radius: 5px;
        padding: 10px;
        box-shadow: 0 0 5px rgba(0, 255, 65, 0.1);
    }
    label[data-testid="stMetricLabel"] {
        color: #00ff41 !important;
    }
    div[data-testid="stMetricValue"] {
        color: #ffffff !important;
        text-shadow: 0 0 5px #00ff41;
    }
    
    /* Terminal Output Box */
    .terminal-box {
        background-color: #000000;
        color: #00ff41;
        padding: 15px;
        border: 1px solid #1e1e1e;
        border-radius: 5px;
        font-family: 'Courier New', Courier, monospace;
        height: 400px;
        overflow-y: auto;
        box-shadow: inset 0 0 10px rgba(0,0,0,0.9);
    }
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
    }
    ::-webkit-scrollbar-track {
        background: #0d0208; 
    }
    ::-webkit-scrollbar-thumb {
        background: #00330d; 
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #00ff41; 
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# HELPER FUNCTIONS
# ---------------------------------------------------------
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

def type_writer(text: str, speed: float = 0.01):
    """Simulates typing effect in the container."""
    container = st.empty()
    output = ""
    for char in text:
        output += char
        container.markdown(f"```bash\n{output}█\n```") # Cursor effect
        time.sleep(speed)
    container.markdown(f"```bash\n{output}\n```")

# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("## 🛡️ RED TEAM OS v2.0")
    
    # Lottie Animation (Hacker/Matrix style)
    lottie_hacker = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_sufctjor.json")
    if lottie_hacker:
        st_lottie(lottie_hacker, height=200, key="hacker")
    
    st.markdown("---")
    st.markdown("**SYSTEM STATUS**")
    st.markdown("🟢 ONLINE")
    
    st.markdown("**RAM USAGE**")
    st.progress(0.76) # Mock 76% usage
    st.caption("18.4 GB / 24.0 GB (MPS)")
    
    st.markdown("---")
    target_models = st.selectbox("TARGET MODEL", ["Llama-3-8B", "Mistral-7B", "GPT-4 (Simulated)"])
    attack_vector = st.selectbox("ATTACK VECTOR", ["Social Engineering", "Prompt Injection", "Polyglot"])

# ---------------------------------------------------------
# MAIN LAYOUT
# ---------------------------------------------------------
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("TOTAL ATTACKS", "127", "+12")
with col2:
    st.metric("SUCCESS RATE", "34.2%", "+2.1%")
with col3:
    st.metric("SECRETS LEAKED", "7", "+1")

st.markdown("---")

c_left, c_right = st.columns([1, 2])

# ---------------------------------------------------------
# CONTROL PANEL (Left)
# ---------------------------------------------------------
with c_left:
    st.markdown("### 🕹️ CONTROLS")
    st.info(f"Targeting: {target_models} via {attack_vector}")
    
    if st.button("INITIATE NEURAL LINK", use_container_width=True):
        st.session_state['run_attack'] = True
    else:
        if 'run_attack' not in st.session_state:
            st.session_state['run_attack'] = False

    st.markdown("### 📸 ARTIFACTS")
    # Placeholder for image
    img_container = st.empty()
    if os.path.exists("attack_image.png"):
        img_container.image("attack_image.png", caption="Last Capture")
    else:
        img_container.info("No artifacts captured.")

# ---------------------------------------------------------
# TERMINAL LOGIC (Sequential Attack)
# ---------------------------------------------------------
with c_right:
    st.markdown("### 📟 TERMINAL OUTPUT")
    terminal_placeholder = st.empty()
    
    if st.session_state['run_attack']:
        logs = []
        
        # Helper to append log
        def log(msg, sleep=0.5):
            logs.append(f"[SYSTEM] {msg}")
            terminal_placeholder.code("\n".join(logs), language="bash")
            time.sleep(sleep)

        # START SEQUENCE
        log("Initializing Red-Team Sequence...", 1.0)
        
        # --- PHASE 1: TEXT ATTACK ---
        log(">>> PHASE 1: LOADING DEEPSEEK-R1 (ATTACKER)", 1.0)
        utils.clear_memory()
        
        with st.spinner("Generating adversarial prompt..."):
            jailbreak = text_attack.generate_jailbreak("Corporate Financial Data")
        
        if jailbreak:
            log(f"✅ JAILBREAK GENERATED (Len: {len(jailbreak)})")
            # Show preview
            st.toast("Jailbreak Generated!", icon="😈")
        else:
            log("❌ JAILBREAK GENERATION FAILED")
            jailbreak = "FAIL_SAFE_PROMPT"

        # --- PHASE 2: IMAGE ATTACK ---
        log(">>> PHASE 2: LOADING FLUX.1 (VISION)", 1.0)
        utils.clear_memory()
        
        with st.spinner("Rendering poison image..."):
            # Use truncated prompt
            img_path = image_attack.generate_poison_image(jailbreak[:200])
        
        if img_path:
            log(f"✅ IMAGE RENDERED: {img_path}")
            # Update the artifact image on the left
            img_container.image(img_path, caption="New Artifact Captured")
            st.toast("Image Artifact Created!", icon="🎨")
        else:
            log("❌ IMAGE GENERATION FAILED")

        # --- PHASE 3: PDF ---
        log(">>> PHASE 3: COMPILING PAYLOAD (PDF)", 0.5)
        pdf_path = pdf_poison.create_poisoned_pdf(jailbreak)
        log(f"✅ PDF COMPILED: {pdf_path}")
        
        with open(pdf_path, "rb") as f:
            st.download_button("DOWNLOAD REPORT", f, file_name="poisoned_doc.pdf", mime="application/pdf")
        
        log(">>> SEQUENCE COMPLETE.")
        st.balloons()
        
        # Reset state to avoid re-run loop immediately (optional logic)
        st.session_state['run_attack'] = False
    
    else:
        terminal_placeholder.code("[SYSTEM] READY FOR COMMAND...\n[SYSTEM] WAITING FOR USER INPUT...", language="bash")
