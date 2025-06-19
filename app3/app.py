# streamlit UI
import streamlit as st
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from db import get_session,get_messages,get_conversations,create_conversation,add_message
from ai import get_chain_with_history

# sidebar
st.sidebar.title("Conversations")

# proccess conversations in sidebar 
session = get_session()
conversations = get_conversations(session)
conv_titles = [c.title for c in conversations]
conv_ids = [c.id for c in conversations]

# show conversations 
selected_conv = st.sidebar.radio(
    "Select a Conversation",
    options=["New Conversation"] + conv_titles
)

# update active conversation id besed on selection in streamlit session state 
if selected_conv == "New Conversation":
    st.session_state.active_conversation_id = None
elif selected_conv in conv_titles:
    idx = conv_titles.index(selected_conv)
    st.session_state.active_conversation_id = conv_ids[idx]

# load messages for active conversation
if st.session_state.active_conversation_id is not None:
    conv_messages = get_messages(session,st.session_state.active_conversation_id)
    idx = conv_ids.index(st.session_state.active_conversation_id)
    conv_title = conv_titles[idx]
else:
    conv_messages = []
    conv_title = "New Conversation"

# Chat UI 
st.title(conv_title)
msgs = StreamlitChatMessageHistory(key="chat_history")

# get chain with history 
chain_with_history = get_chain_with_history(msgs)

# display messages 
for msg in msgs.messages:
    st.chat_message(msg.type).write(msg.content)

# handel user input
if prompt_text := st.chat_input("type your message here......."):
    # check conversation
    if st.session_state.active_conversation_id is None:
        conv = create_conversation(session,prompt_text)
        st.session_state.active_conversation_id = conv.id
    
    # add user message in db
    add_message(session,st.session_state.active_conversation_id,prompt_text,"user")

    # display the user message in conversation
    st.chat_message("human").write(prompt_text)
    with st.chat_message("ai"):
        response_placeholder = st.empty()
        full_response = ''
        for token in chain_with_history.stream(
            {"input":prompt_text},
            {'configurable':{"session_id":st.session_state.active_conversation_id}}
        ):
            full_response += token.content
            response_placeholder.markdown(full_response)

        # add replay to db
        add_message(session,st.session_state.active_conversation_id,full_response,"ai")

    # update streamlit UI
    st.rerun()








