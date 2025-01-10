import streamlit as st
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(
    page_title="Download DB",
    page_icon="⬇️",
    layout="centered",
    initial_sidebar_state="expanded",
)


# Navigation back to home
if st.button("🏠 Go Back to Home"):
    switch_page("Home")
