import streamlit as st
from utils.api import create_category, get_category, update_category, delete_category
from datetime import date

st.set_page_config(page_title="Categories", page_icon="🗂️", layout="wide")


st.markdown("""
<style>
.main-title {
    background: linear-gradient(90deg, #7F00FF, #E100FF);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 42px;
    font-weight: 800;
    padding-bottom: 0px;
}
.subtitle {
    color: #9b9b9b;
    font-size: 16px;
    margin-top: -10px;
}
div[data-testid="stExpander"] {
    border-radius: 14px;
    border: 1px solid rgba(255,255,255,0.08);
    background: linear-gradient(135deg, rgba(127,0,255,0.08), rgba(225,0,255,0.05));
    margin-bottom: 10px;
}
div.stButton > button {
    border-radius: 10px;
    font-weight: 600;
    transition: 0.2s;
}
div.stButton > button:hover {
    transform: scale(1.03);
}
.create-card {
    background: linear-gradient(135deg, #7F00FF22, #E100FF22);
    padding: 20px;
    border-radius: 16px;
    border: 1px solid rgba(225,0,255,0.25);
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-title">🗂️ Categories</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Organize your learning journey into colorful buckets ✨</p>', unsafe_allow_html=True)

if not st.session_state.get("token"):
    st.warning("⚠️ Please login first from the main page.")
    st.stop()

token = st.session_state.token

st.markdown('<div class="create-card">', unsafe_allow_html=True)
st.subheader("✨ Create a New Category")
name = st.text_input("Category Name", placeholder="e.g. 🖥️ Backend Dev, 🤖 ML, 🎨 Design")

if st.button("🚀 Create Category", use_container_width=True):
    if not name.strip():
        st.error("Please enter a category name.")
    else:
        response = create_category(token, name)
        if response.status_code == 200:
            st.success(f"🎉 Category **{name}** created!")
            st.balloons()
            st.rerun()
        else:
            st.error("❌ Failed to create category.")
st.markdown('</div>', unsafe_allow_html=True)

st.divider()

st.subheader("📋 Your Categories")


palette = ["🔵", "🟣", "🟢", "🟠", "🔴", "🟡", "🟤", "⚪"]

response = get_category(token)
if response.status_code == 200:
    categories = response.json()

    if not categories:
        st.info("No categories yet — create your first one above! 🌱")

    for i, cat in enumerate(categories):
        emoji = palette[i % len(palette)]
        with st.expander(f"{emoji} {cat['name']}"):
            new_name = st.text_input("Name", value=cat['name'], key=f"cat_name_{cat['id']}")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("💾 Update", key=f'cat_update_{cat["id"]}', use_container_width=True):
                    update_category(token, new_name, cat["id"])
                    st.success("✅ Updated!")
                    st.rerun()
            with col2:
                if st.button("🗑️ Delete", key=f'cat_delete_{cat["id"]}', use_container_width=True):
                    delete_category(token, cat["id"])
                    st.success("🗑️ Deleted!")
                    st.rerun()
else:
    st.error("❌ Failed to load categories.")
