# pages/2_Dashboard.py (TEST VERSION - No Firebase)
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Check if user is logged in
if not st.session_state.get('logged_in', False):
    st.switch_page("pages/1_Login.py")

st.set_page_config(
    page_title="Dashboard | AI Habit Analyzer",
    page_icon="📊",
    layout="wide"
)

st.title(f"📊 Welcome, {st.session_state.user_email}!")
st.caption(f"User ID: {st.session_state.user_id} | Demo Mode (Firebase not connected)")

# ========== METRICS ROW ==========
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("🔥 Current Streak", "5 days", delta="+2")
with col2:
    st.metric("📈 Consistency Rate", "85%", delta="+5%")
with col3:
    st.metric("✅ Total Habits", "3", delta="+1")
with col4:
    st.metric("🤖 Success Probability", "78%", delta="High")

st.divider()

# ========== TODAY'S HABITS ==========
st.subheader("✅ Track Today's Habits")

col1, col2, col3 = st.columns(3)

with col1:
    exercise_done = st.checkbox("🏃‍♀️ Exercise", key="exercise_today")
with col2:
    prayer_done = st.checkbox("🕌 Prayer (5 times)", key="prayer_today")
with col3:
    study_done = st.checkbox("📚 Study", key="study_today")

if st.button("💾 Save Today's Progress", type="primary", use_container_width=True):
    st.success("✅ Habits saved! (Demo mode)")
    st.balloons()

st.divider()

# ========== PROGRESS CHART ==========
st.subheader("📈 Your Weekly Progress")

chart_data = pd.DataFrame({
    'Day': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
    'Completion': [80, 85, 90, 85, 95, 100, 90]
})

fig = px.line(chart_data, x='Day', y='Completion', markers=True)
st.plotly_chart(fig, use_container_width=True)

# ========== AI RECOMMENDATION ==========
st.subheader("🤖 AI Insight")
st.info("💡 You're doing great! Try to maintain your current streak by exercising before 8 PM.")

# ========== SIDEBAR ==========
with st.sidebar:
    st.markdown("## 🧠 AI Habit Analyzer")
    st.markdown("---")
    st.markdown("**Quick Stats**")
    st.metric("📅 Member since", "June 2026")
    st.metric("🏆 Longest Streak", "12 days")
    st.markdown("---")
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.clear()
        st.switch_page("pages/1_Login.py")