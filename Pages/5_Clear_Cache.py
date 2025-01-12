import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from Utils.clear_cache import clear_txt_files


st.set_page_config(
    page_title="🗑️ Clear Cache",
    page_icon="🗑️",
    layout="centered",
    initial_sidebar_state="expanded",
)


st.title("🗑️ Clear Cache Files")


st.markdown(
    """
    **Use this tool to clear cached data.**
    This will reset the following files:

    - 📄 **File Size Cache**
    - 📄 **Top Passwords Cache**
    - 📄 **Previously Searched Passwords Cache**

    ⚠️ **Warning:** This action cannot be undone.
    """
)


if st.button("🗑️ Clear Cache Files"):
    with st.spinner("Clearing cache files..."):
        clear_txt_files()


st.markdown("---")


if st.button("🏠 Go Back to Home"):
    switch_page("Home")
