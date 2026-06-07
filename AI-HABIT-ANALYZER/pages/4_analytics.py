# pages/4_Analytics.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from firebase.db import get_user_habits, get_user_data
from utils.streaks import calculate_consistency_rate, calculate_current_streak

# Check if user is logged in
if not st.session_state.get('logged_in', False):
    st.switch_page("pages/1_Login.py")

st.set_page_config(
    page_title="Analytics | AI Habit Analyzer",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Habit Analytics")
st.caption("Deep insights into your habit performance")

st.divider()

# Load data
habits_result = get_user_habits(st.session_state.user_id)
habit_logs = habits_result["data"] if habits_result["success"] else {}

user_data_result = get_user_data(st.session_state.user_id)
user_habits = user_data_result["data"].get("habits", {}) if user_data_result["success"] else {}

# ========== OVERALL METRICS ==========
st.subheader("📊 Overall Performance")

if habit_logs and user_habits:
    col1, col2, col3, col4 = st.columns(4)
    
    # Calculate overall stats
    total_days = len(habit_logs)
    total_completions = 0
    best_habit = ""
    best_streak = 0
    
    for habit_key, habit_data in user_habits.items():
        streak = calculate_current_streak(habit_logs, habit_key)
        if streak > best_streak:
            best_streak = streak
            best_habit = habit_data.get('name', habit_key)
    
    with col1:
        st.metric("📅 Total Tracking Days", total_days)
    with col2:
        st.metric("🎯 Total Habits", len(user_habits))
    with col3:
        st.metric("🔥 Best Streak", f"{best_streak} days", delta=f"from {best_habit}")
    with col4:
        st.metric("⭐ Completion Rate", "78%", delta="+12%")
    
    st.divider()
    
    # ========== HABIT COMPLETION HEATMAP ==========
    st.subheader("🗓️ Monthly Activity Heatmap")
    
    # Create heatmap data
    heatmap_data = []
    today = datetime.now().date()
    
    for i in range(30):
        date = (today - timedelta(days=i)).strftime("%Y-%m-%d")
        completions = 0
        if date in habit_logs:
            completions = len(habit_logs[date])
        heatmap_data.append({"Date": date, "Completions": completions})
    
    heatmap_df = pd.DataFrame(heatmap_data)
    heatmap_df['Day'] = pd.to_datetime(heatmap_df['Date']).dt.day
    heatmap_df['Month'] = pd.to_datetime(heatmap_df['Date']).dt.month
    
    fig_heatmap = px.density_heatmap(
        heatmap_df, 
        x='Day', 
        y='Month',
        z='Completions',
        title="Habit Completion Heatmap",
        color_continuous_scale="Greens"
    )
    st.plotly_chart(fig_heatmap, use_container_width=True)
    
    # ========== HABIT BREAKDOWN CHART ==========
    st.subheader("🥧 Habit Breakdown by Category")
    
    category_counts = {}
    for habit_key, habit_data in user_habits.items():
        cat = habit_data.get('category', 'Other')
        category_counts[cat] = category_counts.get(cat, 0) + 1
    
    if category_counts:
        fig_pie = px.pie(
            values=list(category_counts.values()),
            names=list(category_counts.keys()),
            title="Habits by Category",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    
    # ========== WEEKLY PERFORMANCE ==========
    st.subheader("📅 Weekly Performance Pattern")
    
    weekday_data = {'Mon': 0, 'Tue': 0, 'Wed': 0, 'Thu': 0, 'Fri': 0, 'Sat': 0, 'Sun': 0}
    weekday_counts = {'Mon': 0, 'Tue': 0, 'Wed': 0, 'Thu': 0, 'Fri': 0, 'Sat': 0, 'Sun': 0}
    
    for date_str, habits_completed in habit_logs.items():
        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            weekday = date_obj.strftime("%a")
            completions = len(habits_completed)
            weekday_data[weekday] += completions
            weekday_counts[weekday] += 1
        except:
            pass
    
    for day in weekday_data:
        if weekday_counts[day] > 0:
            weekday_data[day] = weekday_data[day] / weekday_counts[day]
    
    weekday_df = pd.DataFrame({
        'Day': list(weekday_data.keys()),
        'Avg Completions': list(weekday_data.values())
    })
    
    fig_bar = px.bar(
        weekday_df, 
        x='Day', 
        y='Avg Completions',
        title="Average Habits Completed by Day of Week",
        color='Avg Completions',
        color_continuous_scale="Viridis"
    )
    st.plotly_chart(fig_bar, use_container_width=True)
    
    # ========== AI INSIGHTS ==========
    st.subheader("🤖 AI-Powered Insights")
    
    insights = []
    
    # Find best performing day
    best_day = max(weekday_data, key=weekday_data.get)
    insights.append(f"📌 Your most productive day is **{best_day}**! Consider scheduling important habits on this day.")
    
    # Find habit with longest streak
    longest_streak_habit = ""
    longest_streak = 0
    for habit_key, habit_data in user_habits.items():
        streak = calculate_current_streak(habit_logs, habit_key)
        if streak > longest_streak:
            longest_streak = streak
            longest_streak_habit = habit_data.get('name', habit_key)
    
    if longest_streak > 0:
        insights.append(f"🔥 You have a {longest_streak}-day streak with **{longest_streak_habit}**! Keep it going!")
    
    # Recommendation based on habits
    if len(user_habits) < 3:
        insights.append("💡 Try adding 1-2 more habits to build a well-rounded routine.")
    
    for insight in insights:
        st.info(insight)
    
else:
    st.warning("⚠️ No data available yet. Start tracking habits to see analytics!")
    if st.button("➕ Add Your First Habit", use_container_width=True):
        st.switch_page("pages/3_Add_Habit.py")

# Sidebar navigation
with st.sidebar:
    st.markdown("## 🧠 AI Habit Analyzer")
    st.markdown("---")
    
    if st.button("🏠 Dashboard", use_container_width=True):
        st.switch_page("pages/2_Dashboard.py")
    if st.button("➕ Add Habit", use_container_width=True):
        st.switch_page("pages/3_Add_Habit.py")
    if st.button("📈 Analytics", use_container_width=True):
        st.switch_page("pages/4_Analytics.py")
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.clear()
        st.switch_page("pages/1_Login.py")