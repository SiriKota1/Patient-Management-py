import streamlit as st
import requests

st.set_page_config(page_title="ChatBot", layout="wide")

st.title("Patient Management ChatBot")

# Sidebar chat history
st.sidebar.title("Chat History")

# Fetch and display history
history_response = requests.get("http://127.0.0.1:8000/chat-history/")
if history_response.status_code == 200:
    history = history_response.json()
    if history:
        for item in history:
            st.sidebar.markdown(f"**You:** {item['question']}")
            st.sidebar.markdown(f"**Bot:** {item['response']}")
            st.sidebar.markdown("---")
    else:
        st.sidebar.write("No history yet.")
else:
    st.sidebar.error("Failed to load chat history.")

# Main input section
st.subheader("Ask the bot anything")
question = st.text_input("Enter your prompt here:")

if st.button("Send"):
    if question.strip():
        response = requests.get(f"http://127.0.0.1:8000/ollama-chat/?question={question}")
        if response.status_code == 200:
            bot_reply = response.json().get("chat_response", "No reply")
            st.success("Bot replied:")
            st.write(bot_reply)
        else:
            st.error("Error getting response from the backend.")
    else:
        st.warning("Please enter a question.")
