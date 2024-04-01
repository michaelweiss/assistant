import streamlit as st
from openai import OpenAI

from chatbot import Chatbot

st.title("Assistant")

# Create the chatbot (if it doesn't exist yet)
if not "chatbot" in st.session_state:
    st.session_state.chatbot = Chatbot(OpenAI(), "gpt-3.5-turbo")
chatbot = st.session_state.chatbot

# Show the chat history
history = st.session_state.get("history", [])
for message in history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Get the user's request and show the response
request = st.chat_input("Ask a question")
if request:
    with st.chat_message("user"):
        st.markdown(request)
    history.append({"role": "user", "content": request})
    with st.spinner("Thinking..."):
        # Get the response from the chatbot
        response = chatbot.handle_request(request)
        with st.chat_message("assistant"):
            st.markdown(response)
        history.append({"role": "assistant", "content": response})
    st.session_state["history"] = history