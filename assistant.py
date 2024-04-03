import streamlit as st
from openai import OpenAI
import json
import os

from chatbot import Chatbot
from knowledge_chatbot import KnowledgeChatbot
from vector_database import VectorDatabase
from embeddings_utils import get_embedding

def create_database(db):
    """
    Create the database.
    """
    # Read json lines from data/faq-qa.json
    # Each line is a json object with a question and an answer
    # Upsert the question and answer into the database
    # Combine as follows: Q. <question>\nA. <answer>
    with open("data/faq_template.json", "r") as file:
        for line in file:
            record = json.loads(line)
            question = record["question"]
            answer = record["answer"]
            document = f"Q. {question} A. {answer}"
            db.upsert(document, get_embedding(document))
    # Save the database as data/faq.json
    db.save("data/faq.json")

st.title("Assistant")

# Create the chatbot (if it doesn't exist yet)
if not "chatbot" in st.session_state:
    db = VectorDatabase()
    if os.path.exists("data/faq.json"):
        db.load("data/faq.json")
    else:
        create_database(db)
    st.session_state.chatbot = KnowledgeChatbot(OpenAI(), "gpt-3.5-turbo", db, threshold=.6)
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