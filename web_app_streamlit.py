import requests
import streamlit as st


def get_openai_response(input_text):
    response = requests.post(
        "http://localhost:8000/generate",
        json={'inputs': input_text,
              "parameters": {"temperature": 0.1,
                             "max_tokens": 200}})
    return response.json().get("generated_text")


st.title('Langchain LLM Demo')
input_text = st.text_input("USING OPENAI API: Write an essay on")  # interact with openai
if input_text:
    st.write(get_openai_response(input_text))
