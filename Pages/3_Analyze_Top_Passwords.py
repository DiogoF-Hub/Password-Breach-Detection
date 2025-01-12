import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from Utils.top_10_hashes import find_top_hashes


st.set_page_config(
    page_title="Analyze Top Passwords",
    page_icon="📊",
    layout="centered",
    initial_sidebar_state="expanded",
)

st.title("📊 Analyze Top Passwords")

# Input field for specifying `top_n`
top_n = st.number_input(
    "Enter the number of top hashes to analyze (e.g., 10):",
    min_value=1,
    max_value=100,
    value=10,
    step=1,
)

# Placeholder for processing and results
status_placeholder = st.empty()
result_placeholder = st.empty()
info_var = st.empty()

# Button to trigger `find_top_hashes`
if st.button(f"Analyze Top {top_n} Password Hashes"):
    # Validation for top_n before calling the func
    if not isinstance(top_n, int):
        st.error("The value of 'top_n' must be an integer.")
    elif top_n < 1 or top_n > 100:
        st.error("Please enter a number between 1 and 100 for 'top_n'.")
    else:
        try:
            # Call the function and get the formatted results
            formatted_results = find_top_hashes(top_n)
            if formatted_results:
                st.markdown(f"**Top {top_n} hashes with the highest counts:**")
                for result in formatted_results:
                    st.text(result)
        except Exception as e:
            st.error(f"An error occurred: {e}")


# Navigation back to home
if st.button("🏠 Go Back to Home"):
    switch_page("Home")
