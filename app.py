import streamlit as st
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate


# Constants
MODEL_NAME = 'deepseek-r1:1.5b' 
SYSTEM_PROMPET = 'You are a helpful assistant'


# build a streamlit app

with st.sidebar:
    st.title("Settings")

    # define sittings
    systm_prompt = st.text_area("Systm Prompt",value=SYSTEM_PROMPET)
    temprature = st.slider("Temprature")
    max_tokens = st.slider("Max Tokens")
# initilize chat
llm = ChatOllama(model=MODEL_NAME)













