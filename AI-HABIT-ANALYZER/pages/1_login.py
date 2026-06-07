# pages/1_Login.py (TEST VERSION - No Firebase)
import streamlit as st

st.set_page_config(
    page_title="Login | AI Habit Analyzer",
    page_icon="🔐",
    layout="centered"
)

st.title("✨ AI Habit Analyzer")
st.markdown("### Track habits · Get AI predictions · Build consistency")
st.divider()

tab1, tab2 = st.tabs(["🔐 **Sign In**", "📝 **Create Account**"])

# ========== TAB 1: SIGN IN ==========
with tab1:
    st.subheader("Welcome Back")
    
    login_email = st.text_input(
        "Email", 
        placeholder="you@example.com",
        key="login_email"
    )
    login_password = st.text_input(
        "Password", 
        type="password", 
        placeholder="Enter your password",
        key="login_password"
    )
    
    if st.button("Sign In", type="primary", use_container_width=True):
        if login_email and login_password:
            # TEMPORARY: Just store in session state without Firebase
            st.session_state.logged_in = True
            st.session_state.user_email = login_email
            st.session_state.user_id = "test_user_123"
            st.success("✅ Login successful! Redirecting...")
            st.switch_page("pages/2_Dashboard.py")
        else:
            st.warning("⚠️ Please enter email and password")

# ========== TAB 2: SIGN UP ==========
with tab2:
    st.subheader("Create New Account")
    
    signup_email = st.text_input(
        "Email", 
        placeholder="you@example.com",
        key="signup_email"
    )
    signup_password = st.text_input(
        "Password", 
        type="password", 
        placeholder="Choose a password",
        key="signup_password"
    )
    confirm_password = st.text_input(
        "Confirm Password", 
        type="password", 
        placeholder="Confirm your password",
        key="confirm_password"
    )
    
    if st.button("Create Account", type="primary", use_container_width=True):
        if signup_email and signup_password:
            if signup_password == confirm_password:
                # TEMPORARY: Just store in session state without Firebase
                st.session_state.logged_in = True
                st.session_state.user_email = signup_email
                st.session_state.user_id = "test_user_123"
                st.success("🎉 Account created! Redirecting...")
                st.switch_page("pages/2_Dashboard.py")
            else:
                st.warning("⚠️ Passwords do not match")
        else:
            st.warning("⚠️ Please fill all fields")