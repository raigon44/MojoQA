import time

import streamlit as st
from mojoqa.executor.inference import Inference
from mojoqa.config.conf import CFGLog
from mojoqa.utils.logger import logger


st.set_page_config(page_title="Mojo QA", page_icon="🔥", layout="wide", )
st.markdown(f"""
            <style>
            .stApp {{ 
                     background-attachment: fixed;
                     background-size: cover}}
         </style>
         """, unsafe_allow_html=True)

st.title("🔥 🔥 Mojo QA Bot 🔥 🔥")

infer_obj = Inference(CFGLog)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What do you want to know about Mojo programming language?"):
    with st.chat_message("user:"):
        st.markdown(prompt)

    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        assistant_response = infer_obj.get_answer(prompt)
        full_response = ""

        for chunk in assistant_response.split():
            full_response += chunk + " "
            time.sleep(0.05)
            message_placeholder.markdown(full_response + " ")
        message_placeholder.markdown(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})












