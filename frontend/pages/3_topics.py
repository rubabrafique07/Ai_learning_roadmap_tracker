import streamlit as st
from utils.api import get_roadmap, get_topics, create_topic, update_topic, delete_topic
from datetime import date

st.set_page_config(page_title="Topics", page_icon="📚", layout="wide")

st.markdown("""
<style>
.main-title {
    background: linear-gradient(90deg, #11998e, #38ef7d);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 42px;
    font-weight: 800;
}
.subtitle { color: #9b9b9b; font-size: 16px; margin-top: -10px; }
div[data-testid="stExpander"] {
    border-radius: 14px;
    border: 1px solid rgba(255,255,255,0.08);
    background: linear-gradient(135deg, rgba(17,153,142,0.08), rgba(56,239,125,0.05));
    margin-bottom: 10px;
}
div.stButton > button { border-radius: 10px; font-weight: 600; transition: 0.2s; }
div.stButton > button:hover { transform: scale(1.03); }
.create-card {
    background: linear-gradient(135deg, #11998e22, #38ef7d22);
    padding: 20px;
    border-radius: 16px;
    border: 1px solid rgba(56,239,125,0.25);
    margin-bottom: 20px;
}
.status-badge {
    display: inline-block;
    padding: 3px 12px;
    border-radius: 20px;
    font-size: 13px;
    font-weight: 700;
    color: white;
}
.status-not_started { background: #7f7f7f; }
.status-in_progress { background: linear-gradient(90deg,#f7971e,#ffd200); color:#222; }
.status-completed { background: linear-gradient(90deg,#11998e,#38ef7d); }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-title">📚 Topics</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Break your roadmap into bite-sized wins 🍬</p>', unsafe_allow_html=True)

if not st.session_state.get("token"):
    st.warning("⚠️ Please login first from the main page.")
    st.stop()

token = st.session_state.token

roadmaps_response = get_roadmap(token)
if roadmaps_response.status_code != 200:
    st.error("❌ Failed to load roadmaps.")
    st.stop()

roadmaps = roadmaps_response.json()
if not roadmaps:
    st.info("Create a roadmap first! 🗺️")
    st.stop()

roadmap_titles = {rm['title']: rm['id'] for rm in roadmaps}
selected_title = st.selectbox("🗺️ Select Roadmap", list(roadmap_titles.keys()))
selected_roadmap_id = roadmap_titles[selected_title]

st.divider()

STATUS_EMOJI = {
    "not_started": "⚪ Not Started",
    "in_progress": "🟡 In Progress",
    "completed": "🟢 Completed",
}

# ---------- Add Topic ----------
st.markdown('<div class="create-card">', unsafe_allow_html=True)
st.subheader("✨ Add New Topic")
title = st.text_input("Topic Title", placeholder="e.g. 🔐 Authentication & JWT")
target_date = st.date_input("🎯 Target Date", value=date.today())
status = st.selectbox("📊 Status", list(STATUS_EMOJI.keys()), format_func=lambda x: STATUS_EMOJI[x])
notes = st.text_area("📝 Notes", placeholder="Any resources, links, or reminders...")

if st.button("➕ Add Topic", use_container_width=True):
    if not title.strip():
        st.error("Please enter a topic title.")
    else:
        response = create_topic(token, title, target_date, status, notes, selected_roadmap_id)
        if response.status_code == 200:
            st.success(f"🎉 Topic **{title}** added!")
            st.rerun()
        else:
            st.error("❌ Failed to add topic.")
st.markdown('</div>', unsafe_allow_html=True)

st.divider()

# ---------- List Topics ----------
st.subheader(f"📋 Topics in '{selected_title}'")

topics_response = get_topics(token, selected_roadmap_id)

if topics_response.status_code == 200:
    topics = topics_response.json()

    if not topics:
        st.info("No topics yet — add your first one above! 🌱")

    for tp in topics:
        badge_class = f"status-{tp['status']}"
        with st.expander(f"📖 {tp['title']}"):
            st.markdown(
                f"<span class='status-badge {badge_class}'>{STATUS_EMOJI.get(tp['status'], tp['status'])}</span>",
                unsafe_allow_html=True,
            )
            st.write("")
            new_title = st.text_input("Title", value=tp['title'], key=f"t_title_{tp['id']}")
            new_date = st.date_input("Target Date", value=date.fromisoformat(tp['target_date']), key=f"t_date_{tp['id']}")
            new_status = st.selectbox(
                "Status",
                list(STATUS_EMOJI.keys()),
                index=list(STATUS_EMOJI.keys()).index(tp['status']),
                format_func=lambda x: STATUS_EMOJI[x],
                key=f"t_status_{tp['id']}",
            )
            new_notes = st.text_area("Notes", value=tp.get('notes', ''), key=f"t_notes_{tp['id']}")

            col1, col2 = st.columns(2)
            with col1:
                if st.button("💾 Update", key=f"t_update_{tp['id']}", use_container_width=True):
                    update_topic(token, new_title, new_date, tp['id'], new_status, new_notes)
                    st.success("✅ Updated!")
                    st.rerun()
            with col2:
                if st.button("🗑️ Delete", key=f"t_delete_{tp['id']}", use_container_width=True):
                    delete_topic(token, tp['id'])
                    st.success("🗑️ Deleted!")
                    st.rerun()
else:
    st.error("❌ Failed to load topics.")