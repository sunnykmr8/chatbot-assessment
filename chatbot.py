import streamlit as st
import google.generativeai as genai
import os
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Retrieve API key from .env file
api_key = os.getenv("API_KEY")

# Initialize the API key
genai.configure(api_key=api_key)

# Load the JSON data from a file
json_file_path = "bank_data.json"  # Update with actual file path
with open(json_file_path, "r") as file:
    json_data = json.load(file)

def get_response(prompt):
    try:
        # Generate content using Gemini model
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        return response.text if hasattr(response, "text") else "No response generated."
    except Exception as e:
        return f"An error occurred: {e}"

def get_bank_info(bank_name):
    for bank in json_data["banks"]:
        if bank_name.lower() in bank["name"].lower():
            return json.dumps(bank, indent=4)
    return "Bank not found."

def main():
    # Page Styling
    st.set_page_config(page_title="Chatbot for a FinTech Company", page_icon="🏦", layout="wide")

    st.markdown(
        """
        <style>
            body {
                background-color: #f4f4f4;
                font-family: 'Arial', sans-serif;
            }
            .main-title {
                color: #2c3e50;
                text-align: center;
                font-size: 36px;
                font-weight: bold;
                padding: 10px;
            }
            .chat-container {
                background-color: #ffffff;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
                margin: auto;
                max-width: 700px;
            }
            .chat-box {
                background-color: #f8f9fa;
                padding: 15px;
                border-radius: 8px;
                margin-top: 10px;
                font-size: 16px;
                color: #000000;
            }
            .stTextArea textarea {
                font-size: 16px;
                background-color: #eef2f3;
                border-radius: 6px;
                border: 1px solid #ccc;
            }
            .send-button {
                background-color: #007bff !important;
                color: white !important;
                font-size: 16px !important;
                padding: 8px 15px !important;
                border-radius: 6px !important;
                text-align: center;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<div class='main-title'>💰 Chatbot for a FinTech Company 💰</div>", unsafe_allow_html=True)

    st.write("Ask me about loans, interest rates, credit reports, and more.")

    # Initialize session state variable
    if "submit_button" not in st.session_state:
        st.session_state.submit_button = False

    user_input = st.text_input("You:", "", key="chat_input", help="Type your query here")

    if st.button("Send", key="send_button", help="Click to send your query", use_container_width=True):
        st.session_state.submit_button = True

    if st.session_state.submit_button:
        if user_input.lower().startswith("bank info"):
            bank_name = user_input.replace("bank info", "").strip()
            response = get_bank_info(bank_name)
        else:
            prompt = f"As a FinTech expert, please provide a concise explanation: {user_input}"
            response = get_response(prompt)

        st.markdown(f"<div class='chat-box'>{response}</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
