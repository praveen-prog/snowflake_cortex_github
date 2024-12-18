import streamlit as st
import os
import sys
from datetime import datetime

# Import custom modules
from src.logger import logging
from src.exception import snowflakecortexerror
from src.entity.config_entity import SetUpConfig
from src.entity.artifacts_entity import DataIngestionArtifact
from src.data_ingestion import DataIngestionClass
from src.training_pipeline import TrainingPipeline

# Set page configuration
st.set_page_config(
    page_title="Code Analysis Chatbot",
    page_icon="🤖",
    layout="wide",
)

@st.cache_resource
def get_training_pipeline():
    """Initialize the TrainingPipeline object and cache it to prevent multiple sessions."""
    return TrainingPipeline()

def main():
    # Title and subheader with emoji
    st.title("💡 Code Analysis Chatbot")
    st.subheader("Ask me anything about your source code!")

    # CSS for styling chat bubbles and timestamps
    st.markdown(
        """
        <style>
        .user-bubble {
            background-color: #DCF8C6;
            padding: 10px;
            border-radius: 10px;
            margin-bottom: 5px;
            max-width: 70%;
            text-align: left;
        }
        .bot-bubble {
            background-color: #E4E6EB;
            padding: 10px;
            border-radius: 10px;
            margin-bottom: 5px;
            max-width: 70%;
            text-align: left;
        }
        .chat-container {
            display: flex;
            flex-direction: column;
        }
        .user-row {
            justify-content: flex-end;
            display: flex;
        }
        .bot-row {
            justify-content: flex-start;
            display: flex;
        }
        .timestamp {
            font-size: 0.8rem;
            color: gray;
            margin-top: -5px;
            margin-bottom: 10px;
        }
        img.chat-icon {
            width: 30px;
            height: 30px;
            margin-right: 10px;
            border-radius: 50%;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Initialize session state to store chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []  # List of {"role": "user"/"bot", "content": "message", "timestamp": "time"}

    # Chat interface: Display conversation history
    for msg in st.session_state.messages:
        timestamp = msg.get("timestamp", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        if msg["role"] == "user":
            st.markdown(
                f"""
                <div class="chat-container">
                    <div class="user-row">
                        <div>
                            <div class="user-bubble">{msg['content']}</div>
                            <div class="timestamp">{timestamp}</div>
                        </div>
                        <img class="chat-icon" src="https://img.icons8.com/color/48/user.png"/>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        elif msg["role"] == "bot":
            st.markdown(
                f"""
                <div class="chat-container">
                    <div class="bot-row">
                        <img class="chat-icon" src="https://img.icons8.com/color/48/robot.png"/>
                        <div>
                            <div class="bot-bubble">{msg['content']}</div>
                            <div class="timestamp">{timestamp}</div>
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # Checkbox to toggle the `run_only_search_retriever` value
    run_only_search_retriever = st.checkbox("Run only search retriever", value=True)

    # Input field for the user's query
    query = st.text_input("Your query:", placeholder="Type your question here...")

    # Execute on query submission
    if st.button("Send"):
        if query.strip():  # Ensure query is not empty
            # Append user query to chat history with timestamp
            st.session_state.messages.append({"role": "user", "content": query, "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})

            obj = get_training_pipeline()  # Get the cached TrainingPipeline instance
            try:
                if run_only_search_retriever:
                    st.write("Analysing the code...")
                    result = obj.run_pipeline(query=query, run_only_search_retriever=run_only_search_retriever)
                    st.success("Answer retrieved successfully!")
                    # Append bot response to chat history with timestamp
                    st.session_state.messages.append({"role": "bot", "content": result, "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
                    st.rerun()  # Rerun to refresh the chat interface

                else:
                    st.write("Pipeline Execution in progress...Please wait.")
                    result = obj.run_pipeline(query=query, run_only_search_retriever=run_only_search_retriever)
                    st.success("Pipeline refreshed successfully!")
                    st.session_state.messages.append({"role": "bot", "content": result, "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
                    st.rerun()  # Rerun to refresh the chat interface           
            except Exception as e:
                error_msg = f"An error occurred: {str(e)}"
                st.session_state.messages.append({"role": "bot", "content": error_msg, "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
                st.rerun()

if __name__ == "__main__":
    main()
