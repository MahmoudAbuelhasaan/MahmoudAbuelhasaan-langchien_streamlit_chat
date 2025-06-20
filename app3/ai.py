# AI oparations
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory


# Constants
MODEL_NAME = 'deepseek-r1:1.5b' 
SYSTEM_PROMPET = 'You are a helpful assistant'

# initilize chat
llm = ChatOllama(
    model=MODEL_NAME,
    num_predict=500
    )


# define prompt
prompt = ChatPromptTemplate.from_messages([
    ("system",SYSTEM_PROMPET),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human","{input}")
])


# create chain | chat history

chain = prompt | llm


def get_chain_with_history(msgs):
    return RunnableWithMessageHistory(
        chain,
        lambda session_id:msgs,
        input_messages_key="input",
        history_messages_key="chat_history"
    )