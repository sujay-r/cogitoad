import time
from typing import Optional

import streamlit as st

# Set page configuration
st.set_page_config(page_title="Cogitoad")

# Initialize session state variables if they don't exist
if "messages" not in st.session_state:
    st.session_state.messages = []
if "document_content" not in st.session_state:
    st.session_state.document_content = None
if "document_name" not in st.session_state:
    st.session_state.document_name = None
if "parsed_document" not in st.session_state:
    st.session_state.parsed_document = None


def process_uploaded_file(uploaded_file) -> Optional[str]:
    pass


def get_ai_response(user_query: str, document_content: Optional[str]) -> str:
    """Generate AI response based on user query and document content"""
    # This is a placeholder. In a real app, you would call your AI model here.
    time.sleep(1)  # Simulate processing time

    if document_content:
        return f"I've analyzed the document and found relevant information about '{user_query}'. The document contains {len(document_content)} characters."
    else:
        return f"I understand you're asking about '{user_query}', but no document has been uploaded yet for reference."


# Sidebar for document upload
with st.sidebar:
    st.title("Document Upload")
    uploaded_file = st.file_uploader(
        "Upload a document or image", type=["pdf", "png", "jpg", "jpeg", "txt", "csv"]
    )

    if uploaded_file and uploaded_file.name != st.session_state.document_name:
        with st.spinner("Processing document..."):
            document_content = process_uploaded_file(uploaded_file)
            if document_content:
                st.session_state.document_content = document_content
                st.session_state.document_name = uploaded_file.name
                st.success(f"Successfully processed: {uploaded_file.name}")
            else:
                st.error("Failed to extract content from the document")

    if st.session_state.document_name:
        st.info(f"Current document: {st.session_state.document_name}")
        if st.button("Clear document"):
            st.session_state.document_content = None
            st.session_state.document_name = None
            st.rerun()

# Main chat interface
st.title("Cogitoad")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Chat input
user_input = st.chat_input("Ask a question")
if user_input:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Display user message
    with st.chat_message("user"):
        st.write(user_input)

    # Generate AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = get_ai_response(user_input, st.session_state.document_content)
            st.write(response)

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
