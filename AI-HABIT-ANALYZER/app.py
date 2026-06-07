# app.py
import streamlit as st

# Set page configuration (MUST be first Streamlit command)
st.set_page_config(
    page_title="AI Habit Analyzer",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="auto"
)

# Initialize session state for login
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_email' not in st.session_state:
    st.session_state.user_email = ""
if 'user_id' not in st.session_state:
    st.session_state.user_id = ""

# This is just a landing page
# The actual pages are in the "pages/" folder
# Streamlit will automatically show them in the sidebar

st.title("✨ AI Habit Analyzer")
st.markdown("## Your Personal Habit Tracking Assistant")

st.markdown("""
### Features:
- 📊 Track multiple habits daily
- 🔥 Monitor streaks and consistency
- 🤖 AI-powered predictions and insights
- 📈 Visual analytics and progress charts

### Getting Started:
Use the sidebar menu to navigate:
- **Login** - Sign in or create an account
- **Dashboard** - View your progress
- **Add Habit** - Create new habits to track
- **Analytics** - See detailed insights
""")

# Show login status in sidebar
with st.sidebar:
    st.markdown("---")
    if st.session_state.logged_in:
        st.success(f"✅ Logged in as: {st.session_state.user_email}")
        if st.button("🚪 Logout"):
            st.session_state.logged_in = False
            st.session_state.user_email = ""
            st.session_state.user_id = ""
            st.rerun()
    else:
        st.info("🔐 Not logged in")
        if st.button("Go to Login Page"):
            st.switch_page("pages/1_Login.py")