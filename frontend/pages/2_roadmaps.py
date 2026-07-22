import streamlit as st
from utils.api import create_roadmap, get_roadmap, get_roadmap_by_id, update_roadmap, delete_roadmap, get_category
from datetime import date

st.set_page_config(page_title="Roadmaps", page_icon="🗺️", layout="wide")

st.markdown("""
<style>
.main-title {
    background: linear-gradient(90deg, #FF512F, #F09819);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 42px;
    font-weight: 800;
}
.subtitle { color: #9b9b9b; font-size: 16px; margin-top: -10px; }
div[data-testid="stExpander"] {
    border-radius: 14px;
    border: 1px solid rgba(255,255,255,0.08);
    background: linear-gradient(135deg, rgba(255,81,47,0.08), rgba(240,152,25,0.05));
    margin-bottom: 10px;
}
div.stButton > button { border-radius: 10px; font-weight: 600; transition: 0.2s; }
div.stButton > button:hover { transform: scale(1.03); }
.create-card {
    background: linear-gradient(135deg, #FF512F22, #F0981922);
    padding: 20px;
    border-radius: 16px;
    border: 1px solid rgba(240,152,25,0.25);
    margin-bottom: 20px;
}
.deadline-badge {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 20px;
    background: linear-gradient(90deg,#FF512F,#F09819);
    color: white;
    font-size: 13px;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-title">🗺️ My Roadmaps</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Plan the path, track the milestones 🚩</p>', unsafe_allow_html=True)

if not st.session_state.get("token"):
    st.warning("⚠️ Please login first from the main page.")
    st.stop()

token = st.session_state.token


st.markdown('<div class="create-card">', unsafe_allow_html=True)
st.subheader("✨ Create a Roadmap")

title = st.text_input("Roadmap Title", placeholder="e.g. 🚀 Become a Full-Stack Developer")
deadline = st.date_input("🗓️ Deadline", value=date.today())

categories_response = get_category(token)
category_options = {"None": None}
if categories_response.status_code == 200:
    categories = categories_response.json()
    for cat in categories:
        category_options[cat['name']] = cat['id']

selected_category_name = st.selectbox("🏷️ Category (optional)", list(category_options.keys()))
selected_category_id = category_options[selected_category_name]

if st.button("🚀 Create Roadmap", use_container_width=True):
    if not title.strip():
        st.error("Please enter a roadmap title.")
    else:
        response = create_roadmap(token, title, deadline)
        if response.status_code == 200:
            st.success(f"🎉 Roadmap **{title}** created!")
            st.balloons()
            st.rerun()
        else:
            st.error("❌ Failed to create roadmap.")
st.markdown('</div>', unsafe_allow_html=True)

st.divider()


st.subheader("📌 Your Roadmaps")

icons = ["🧭", "🛤️", "🎯", "📍", "🚀", "🏁", "🌱", "⭐"]

response = get_roadmap(token)
if response.status_code == 200:
    roadmaps = response.json()

    if not roadmaps:
        st.info("No roadmaps yet — create your first one above! 🌟")

    for i, rm in enumerate(roadmaps):
        icon = icons[i % len(icons)]
        with st.expander(f"{icon} {rm['title']}"):
            st.markdown(f"<span class='deadline-badge'>⏳ Deadline: {rm['deadline']}</span>", unsafe_allow_html=True)
            st.write("")
            new_title = st.text_input("Title", value=rm['title'], key=f"title_{rm['id']}")
            new_deadline = st.date_input("Deadline", value=date.fromisoformat(rm['deadline']), key=f"deadline_{rm['id']}")

            col1, col2 = st.columns(2)
            with col1:
                if st.button("💾 Update", key=f"update_{rm['id']}", use_container_width=True):
                    update_roadmap(token, new_title, new_deadline, rm['id'])
                    st.success("✅ Updated!")
                    st.rerun()
            with col2:
                if st.button("🗑️ Delete", key=f"delete_{rm['id']}", use_container_width=True):
                    delete_roadmap(token, rm['id'])
                    st.success("🗑️ Deleted!")
                    st.rerun()
else:
    st.error("❌ Failed to load roadmaps.")