import streamlit as st
import requests

st.title("Welcome to Research Agent")

question = st.text_input("Enter your question here")

if st.button("Ask"):
    response = requests.post(
        "http://127.0.0.1:8000/research",
        json = {"research_question": question}
    )
    result = response.json()
    st.write(result["final_report"])