import streamlit as st
import requests

st.title("Welcome to Research Agent")

question = st.text_input("Enter your question here")

if st.button("Ask"):
    if not question:
        st.warning("Please enter a question first!")
    else:
        with st.spinner("Researching..."):
            response = requests.post(
                "http://127.0.0.1:8000/research",
                json = {"research_question": question}
            )
            if response.status_code == 200:
                result = response.json()
                st.write(result["final_report"])
            else:
                st.error("Something went wrong. Please try again or come back after sometime")