import streamlit as st 

import config  
import rag    


st.set_page_config(page_title="My Local RAG Chatbot", page_icon="🦙")

st.title("Chat with your documents")
st.caption(f"Running locally on {config.MODEL} via Ollama")

if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []

if not rag.has_documents():
    st.info(
        "No documents ingested yet — run `python ingest.py path/to/file.pdf` "
        "in a terminal first if you want answers grounded in your own PDF. "
        "Chatting normally for now."
    )


for message in st.session_state.conversation_history:
    with st.chat_message(message["role"]):  
        st.markdown(message["content"])


user_input = st.chat_input("Ask something...")

if user_input:
    with st.chat_message("user"):
        st.markdown(user_input)

    st.session_state.conversation_history.append(
        {"role": "user", "content": user_input}
    )

    try:
      
        with st.spinner("Thinking..."):
            context = rag.retrieve_context(user_input)
            reply = rag.get_response(st.session_state.conversation_history, context)
    except Exception as e:
       
        st.error(f"Error calling local model: {e}")
        st.error("Is Ollama running? Try 'ollama serve' in a terminal.")
      
        st.session_state.conversation_history.pop()
    else:
        with st.chat_message("assistant"):
            st.markdown(reply)
        st.session_state.conversation_history.append(
            {"role": "assistant", "content": reply}
        )