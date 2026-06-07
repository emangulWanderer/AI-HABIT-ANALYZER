import streamlit as st

st.set_page_config(
    page_title="AI Habit Analyzer",
    layout="centered"
)

st.title("Welcome to AI Habit Analyzer")
st.write("Sign in to your Habit Analyzer account")

email = st.text_input(
    "Email Address",
    placeholder="you@example.com"
)

password = st.text_input(
    "Password",
    type="password",
    placeholder="Enter your password"
)

remember = st.checkbox("Remember Me")

if st.button("Sign In"):
    st.success("Login button clicked!")
