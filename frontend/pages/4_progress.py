import streamlit as st
from utils.api import get_roadmap, get_topics, get_progress_history
st.set_page_config( page_title="Progress", page_icon="📈", layout="wide"  )
st.markdown("""<style>
.main-title {
    background: linear-gradient(90deg, #4facfe, #00f2fe);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 42px;
    font-weight: 800;
}
.subtitle { color: #9b9b9b; font-size: 16px; margin-top: -10px; }
div[data-testid="stMetric"] {
    background: linear-gradient(135deg, rgba(79,172,254,0.12), rgba(0,242,254,0.06));
    border: 1px solid rgba(0,242,254,0.25);
    border-radius: 16px;
    padding: 16px;
}
.history-card {
    padding: 10px 16px;
    border-radius: 10px;
    margin-bottom: 6px;
    background: rgba(255,255,255,0.04);
    border-left: 4px solid #4facfe;
}
.status-pill {
    padding: 2px 10px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 700;
    color: white;
    margin-right: 8px;
}
.status-pill-not_started { background: #7f7f7f; }
.status-pill-in_progress { background: linear-gradient(90deg,#f7971e,#ffd200); color:#222; }
.status-pill-completed { background: linear-gradient(90deg,#11998e,#38ef7d); }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-title">📈 Progress</p>', unsafe_allow_html=True  )
st.markdown('<p class="subtitle">See how far you\'ve come 🌟</p>', unsafe_allow_html=True)

if not st.session_state.get("token"):
    st.warning("⚠️ Please login first from the main page" )
    st.stop()

token = st.session_state.token

roadmaps_response = get_roadmap(token)
if roadmaps_response.status_code != 200:
    st.error("❌ Failed to load roadmaps")
    st.stop()

roadmaps = roadmaps_response.json()
if not roadmaps:
    st.info("Create a roadmap first! 🗺️")
    st.stop()

roadmap_titles = {rm['title']: rm['id'] for rm in roadmaps}
selected_title = st.selectbox("🗺️ Select Roadmap", list(roadmap_titles.keys()))
selected_roadmap_id = roadmap_titles[selected_title]

STATUS_EMOJI = {
    "not_started": "⚪ Not Started",
    "in_progress": "🟡 In Progress",
    "completed": "🟢 Completed",
}

topics_response = get_topics(token, selected_roadmap_id)
if topics_response.status_code == 200:
    topics = topics_response.json()
    total = len(topics)
    completed = len([t for t in topics if t['status'] == 'completed'])
    in_progress = len([t for t in topics if t['status'] == 'in_progress'])
    not_started = len([t for t in topics if t['status'] == 'not_started'])

    if total>0:
        progress_percent = (completed / total) * 100

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("🎯 Overall Progress", f"{progress_percent:.0f}%")
        col2.metric("🟢 Completed", completed)
        col3.metric("🟡 In Progress", in_progress)
        col4.metric("⚪ Not Started", not_started)

        st.write("")
        st.progress(progress_percent / 100)

        if progress_percent == 100:
            st.success("🏆 Amazing! You've completed this roadmap!")
            st.balloons()
        elif progress_percent >= 50:
            st.info("🔥 More than halfway there — keep going!")
        else:
            st.info("🌱 Just getting started — every topic counts!")
    else:
        st.info("No topics yet in this roadmap. 🌱")

    st.divider()

    st.subheader("🕒 Progress History")
    topic_titles = {t['title']: t['id'] for t in topics}
    if topic_titles:
        selected_topic_title = st.selectbox("📖 Select Topic", list(topic_titles.keys()))
        selected_topic_id = topic_titles[selected_topic_title]

        history_response = get_progress_history(token, selected_roadmap_id, selected_topic_id)
        if history_response.status_code == 200:
            history = history_response.json()
            if not history:
                st.info("No history yet for this topic.")
            for entry in history:
                pill_class = f"status-pill-{entry['status']}"
                label = STATUS_EMOJI.get(entry['status'], entry['status'])
                st.markdown(
                    f"<div class='history-card'>"
                    f"<span class='status-pill {pill_class}'>{label}</span>"
                    f"<span style='color:#aaa;'>Updated: {entry['updated_at']}</span>"
                    f"</div>",
                    unsafe_allow_html=True,
                )
        else:
            st.error("❌ Failed to load progress history.")
else:
    st.error("❌ Failed to load topics.")