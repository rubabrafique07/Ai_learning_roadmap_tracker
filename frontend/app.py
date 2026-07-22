import streamlit as st
from utils.api import register, login

st.set_page_config(page_title="AI Learning Roadmap Tracker", page_icon="🧭", layout="centered")

st.markdown("""
<style>
.main-title {
    background: linear-gradient(90deg, #7F00FF, #4facfe, #38ef7d);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 46px;
    font-weight: 800;
    text-align: center;
    padding-bottom: 0px;
}
.subtitle {
    text-align: center;
    color: #9b9b9b;
    font-size: 16px;
    margin-top: -10px;
    margin-bottom: 20px;
}
.auth-card {
    background: linear-gradient(135deg, rgba(127,0,255,0.08), rgba(79,172,254,0.06));
    border: 1px solid rgba(127,0,255,0.2);
    border-radius: 18px;
    padding: 28px;
    margin-top: 10px;
}
.welcome-card {
    background: linear-gradient(135deg, rgba(17,153,142,0.15), rgba(56,239,125,0.08));
    border: 1px solid rgba(56,239,125,0.3);
    border-radius: 18px;
    padding: 30px;
    text-align: center;
}
div.stButton > button {
    border-radius: 10px;
    font-weight: 700;
    transition: 0.2s;
    background: linear-gradient(90deg, #7F00FF, #4facfe);
    color: white;
    border: none;
}
div.stButton > button:hover {
    transform: scale(1.02);
    filter: brightness(1.1);
}
div[data-testid="stTabs"] button[aria-selected="true"] {
    background: linear-gradient(90deg, #7F00FF22, #4facfe22);
    border-radius: 10px 10px 0 0;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-title">🧭 AI Learning Roadmap Tracker</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Plan it. Track it. Master it. 🚀</p>', unsafe_allow_html=True)

if "token" not in st.session_state:
    st.session_state.token = None

if st.session_state.token:
    st.markdown('<div class="welcome-card">', unsafe_allow_html=True)
    st.markdown("### 🎉 You're logged in!")
    st.write("Use the sidebar 👉 to navigate to your **Categories**, **Roadmaps**, **Topics**, and **Progress**.")
    st.markdown('</div>', unsafe_allow_html=True)
    st.write("")
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.token = None
        st.rerun()
else:
    tab1, tab2 = st.tabs(["🔐 Login", "📝 Register"])

    with tab1:
        st.markdown('<div class="auth-card">', unsafe_allow_html=True)
        st.subheader("🔐 Welcome Back")
        email = st.text_input("📧 Email", key="login_email")
        password = st.text_input("🔑 Password", type="password", key="login_password")

        if st.button("➡️ Login", use_container_width=True):
            if not email.strip() or not password.strip():
                st.error("Please enter both email and password.")
            else:
                response = login(email, password)
                if response.status_code == 200:
                    st.session_state.token = response.json()
                    st.success("✅ Login successful!")
                    st.balloons()
                    st.rerun()
                else:
                    st.error("❌ Invalid email or password.")
        st.markdown('</div>', unsafe_allow_html=True)

    with tab2:
        st.markdown('<div class="auth-card">', unsafe_allow_html=True)
        st.subheader("📝 Create an Account")
        email = st.text_input("📧 Email", key="reg_email")
        name = st.text_input("🙋 Name", key="reg_name")
        password = st.text_input("🔑 Password", type="password", key="reg_password")

        if st.button("🚀 Register", use_container_width=True):
            if not name.strip() or not email.strip() or not password.strip():
                st.error("Please fill in all fields.")
            else:
                response = register(name, email, password)
                if response.status_code == 200:
                    st.success("🎉 Registration successful! Please login from the Login tab.")
                    st.balloons()
                else:
                    st.error(f"❌ Registration failed: {response.json().get('detail')}")
        st.markdown('</div>', unsafe_allow_html=True)