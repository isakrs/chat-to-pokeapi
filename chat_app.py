import streamlit as st
import requests
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Retrieve API key and URL from environment
api_key = os.getenv("API_KEY")
api_url = os.getenv("API_URL")

# Streamlit layout
st.title("Simple Chat with AI")

# Textbox for user input
user_input = st.text_input("Say something to the AI:")

# Function to send request to the API
def send_to_api(user_text):
    headers = {
        "Content-Type": "application/json",
        "api-key": api_key
    }
    data = {
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant who translates natural language into API calls."
            },
            {
                "role": "user",
                "content": user_text
            }
        ]
    }
    response = requests.post(api_url, headers=headers, json=data)
    return response.json()

# Button to send message
if st.button("Send"):
    if user_input:
        response = send_to_api(user_input)
        ai_response = response['choices'][0]['message']['content']
        st.write(f"AI: {ai_response}")

# Button to clear chat
if st.button("Clear Chat"):
    st.experimental_rerun()
