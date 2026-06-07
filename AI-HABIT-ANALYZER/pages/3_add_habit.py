# pages/3_Add_Habit.py
import streamlit as st
from datetime import datetime
from firebase.db import save_user_data, get_user_data

# Check if user is logged in
if not st.session_state.get('logged_in', False):
    st.switch_page("pages/1_Login.py")

st.set_page_config(
    page_title="Add Habit | AI Habit Analyzer",
    page_icon="➕",
    layout="centered"
)

# Page title
st.title("➕ Add New Habit")
st.caption("Create a new habit to track and build consistency")

st.divider()

# ========== HABIT FORM ==========
with st.form(key="add_habit_form"):
    
    # Habit Name
    habit_name = st.text_input(
        "**Habit Name**",
        placeholder="e.g., Meditation, Reading, Water, Walking",
        help="Give your habit a clear, memorable name"
    )
    
    # Habit Category
    category = st.selectbox(
        "**Category**",
        options=["Health & Fitness", "Spiritual", "Education", "Productivity", "Personal Growth", "Other"],
        help="Categorize your habit for better analytics"
    )
    
    # Goal Type
    goal_type = st.radio(
        "**Goal Type**",
        options=["Daily", "Weekly", "Custom"],
        horizontal=True,
        help="How often do you want to track this habit?"
    )
    
    # Custom frequency (if chosen)
    custom_frequency = None
    if goal_type == "Custom":
        custom_frequency = st.number_input(
            "Times per week",
            min_value=1,
            max_value=7,
            value=3,
            step=1
        )
    
    # Target value
    target_value = st.number_input(
        "**Daily Target**",
        min_value=1,
        max_value=100,
        value=1,
        step=1,
        help="Example: For 'Water' you might set target as 8 glasses"
    )
    
    # Unit
    unit = st.text_input(
        "**Unit** (optional)",
        placeholder="e.g., minutes, glasses, pages, times",
        help="Example: 'minutes', 'km', 'glasses'"
    )
    
    # Reminder Time
    reminder_time = st.time_input(
        "**Reminder Time** (optional)",
        value=datetime.strptime("08:00", "%H:%M").time(),
        help="Get a reminder at this time (future feature)"
    )
    
    # Color picker for habit card
    habit_color = st.color_picker(
        "**Habit Color**",
        value="#4CAF50",
        help="Choose a color to represent this habit"
    )
    
    # Motivation note
    motivation_note = st.text_area(
        "**Why do you want to build this habit?** (optional)",
        placeholder="e.g., I want to meditate daily to reduce stress and improve focus...",
        max_chars=200,
        help="This will appear as motivation when you track the habit"
    )
    
    st.divider()
    
    # Submit button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        submitted = st.form_submit_button(
            "✨ Create Habit", 
            type="primary", 
            use_container_width=True
        )
    
    if submitted:
        if not habit_name:
            st.error("❌ Please enter a habit name")
        else:
            # Prepare habit data
            new_habit = {
                "name": habit_name.strip(),
                "category": category,
                "goal_type": goal_type,
                "target_value": target_value,
                "unit": unit if unit else "times",
                "reminder_time": str(reminder_time),
                "color": habit_color,
                "motivation": motivation_note if motivation_note else "Stay consistent!",
                "created_at": datetime.now().isoformat(),
                "current_streak": 0,
                "longest_streak": 0,
                "total_completions": 0
            }
            
            if goal_type == "Custom":
                new_habit["weekly_target"] = custom_frequency
            
            # Get existing habits from Firebase
            user_data_result = get_user_data(st.session_state.user_id)
            
            if user_data_result["success"] and user_data_result["data"]:
                existing_habits = user_data_result["data"].get("habits", {})
            else:
                existing_habits = {}
            
            # Check if habit already exists
            habit_key = habit_name.strip().lower().replace(" ", "_")
            
            if habit_key in existing_habits:
                st.warning(f"⚠️ You already have a habit called '{habit_name}'")
            else:
                # Add new habit to the list
                existing_habits[habit_key] = new_habit
                
                # Save back to Firebase
                save_result = save_user_data(st.session_state.user_id, {"habits": existing_habits})
                
                if save_result["success"]:
                    st.success(f"✅ Habit '{habit_name}' created successfully!")
                    st.balloons()
                    
                    # Option to add another habit
                    if st.button("➕ Add Another Habit", use_container_width=True):
                        st.rerun()
                    
                    # Option to go to dashboard
                    if st.button("📊 Go to Dashboard", use_container_width=True):
                        st.switch_page("pages/2_Dashboard.py")
                else:
                    st.error(f"❌ Failed to save habit: {save_result['error']}")

st.divider()

# ========== SHOW EXISTING HABITS ==========
st.subheader("📋 Your Existing Habits")

# Load and display existing habits
user_data_result = get_user_data(st.session_state.user_id)

if user_data_result["success"] and user_data_result["data"]:
    habits = user_data_result["data"].get("habits", {})
    
    if habits:
        # Display habits as cards
        for habit_key, habit_data in habits.items():
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                st.markdown(
                    f"<div style='display: flex; align-items: center; gap: 10px;'>"
                    f"<div style='width: 12px; height: 12px; background-color: {habit_data.get('color', '#4CAF50')}; border-radius: 50%;'></div>"
                    f"<strong>{habit_data.get('name', habit_key)}</strong>"
                    f"<span style='color: gray; font-size: 0.8em;'>({habit_data.get('category', 'Uncategorized')})</span>"
                    f"</div>",
                    unsafe_allow_html=True
                )
                st.caption(f"🎯 Target: {habit_data.get('target_value', 1)} {habit_data.get('unit', 'times')} per day")
            
            with col2:
                st.metric("🔥 Streak", habit_data.get('current_streak', 0))
            
            with col3:
                if st.button("🗑️", key=f"delete_{habit_key}", help=f"Delete {habit_data.get('name', habit_key)}"):
                    # Remove habit from the list
                    del habits[habit_key]
                    save_user_data(st.session_state.user_id, {"habits": habits})
                    st.rerun()
            
            st.divider()
    else:
        st.info("💡 You haven't created any habits yet. Use the form above to add your first habit!")
else:
    st.info("💡 You haven't created any habits yet. Use the form above to add your first habit!")

# ========== HELPFUL TIPS ==========
with st.expander("💡 Tips for Building Better Habits"):
    st.markdown("""
    - **Start Small**: Begin with habits that take less than 5 minutes
    - **Be Specific**: Instead of "exercise", try "10-minute morning walk"
    - **Track Daily**: Consistency matters more than intensity
    - **Link Habits**: Attach new habits to existing ones (e.g., "after brushing teeth, meditate for 2 minutes")
    - **Celebrate Small Wins**: Every completed habit is a victory!
    """)

# Sidebar
with st.sidebar:
    st.markdown("## 🧠 AI Habit Analyzer")
    st.markdown("---")
    st.markdown("### 📊 Your Stats")
    
    if habits:
        total_habits = len(habits)
        total_streak = sum(h.get('current_streak', 0) for h in habits.values())
        avg_streak = total_streak // total_habits if total_habits > 0 else 0
        
        st.metric("📌 Total Habits", total_habits)
        st.metric("🔥 Average Streak", f"{avg_streak} days")
    else:
        st.caption("Create your first habit to see stats!")
    
    st.markdown("---")
    if st.button("🏠 Back to Dashboard", use_container_width=True):
        st.switch_page("pages/2_Dashboard.py")