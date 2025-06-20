import streamlit as st
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
import re

# Constants
MODEL_NAME = 'deepseek-r1:1.5b' 

SYSTEM_PROMPET = 'You are a helpful assistant'


# build a streamlit app

with st.sidebar:
    st.title("Settings")

    # define sittings
    systm_prompt = st.text_area("Systm Prompt",value=SYSTEM_PROMPET)
    temprature = st.slider("Temprature",0.0,1.0)
    max_tokens = st.slider("Max Tokens",0,5000,10)
# initilize chat
llm = ChatOllama(
    model=MODEL_NAME,
    temperature=temprature,
    num_predict=max_tokens

    )
# define prompt
prompt = ChatPromptTemplate.from_messages([
    ("system",systm_prompt),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human","{input}")

])

# create chain | chat history

chain = prompt | llm

# create memory
msgs = StreamlitChatMessageHistory(key="chat_history")

# show mesage if no history
if not msgs.messages:
    msgs.add_ai_message("how can i help you?")

# create chain in memory runnuble 
chain_with_history = RunnableWithMessageHistory(
    chain,
    lambda session_id:msgs,
    input_messages_key="input",
    history_messages_key="chat_history"


)


# chat ui 

st.title("Chat")
# populate messages 
for msg in msgs.messages:
    st.chat_message(msg.type).write(msg.content) #msg.type provide chat icon like ai or user


# send message

# prompt_text = st.chat_input("type your message here.......")

# if prompt_text:
#     pass


if prompt_text := st.chat_input("type your message here......."):
    st.chat_message("human").write(prompt_text) 
    with st.chat_message("ai"):
        response_placeholder = st.empty()
        full_response = ''
        for token in chain_with_history.stream(
            {"input":prompt_text},
            {'configurable':{"session_id":"test"}}
        ):
            full_response += token.content
            response_placeholder.markdown(full_response)
            












