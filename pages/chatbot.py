# This file will implement the chatbot feature
from langchain_openai import ChatOpenAI

from dotenv import load_dotenv, find_dotenv 
from langchain.agents import AgentExecutor, create_openai_tools_agent

# LangChain Messages
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
import secrets  # for generating random session ID

# Message Prompt Tools
from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder, 
)

from langchain_core.runnables.history import RunnableWithMessageHistory

# frontend tool 
import streamlit as st
from streamlit_chat import message
from tools.tavily_lookup_tool import tavilySearchTool
from tools.ResumeGenerator import create_enhanced_resume

# Load environment variables
load_dotenv(find_dotenv())

# Initialize chat model
chat = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

# Function to generate response
def generate_response(query:str, chat_session_token):
    tools = [tavilySearchTool,create_enhanced_resume]
    
    # Create prompt template
    prompt = ChatPromptTemplate.from_messages([
        ("system", 
         "You are a helpful assistant. You may not need to use tools for every query - the user may just want to chat!",
         ),
        MessagesPlaceholder(variable_name="chat_history"), ("human", "{query}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])
    
    agent = create_openai_tools_agent(chat, tools, prompt,)

    agent_executor = AgentExecutor(
        agent=agent, 
        tools=tools,
        verbose=True,
    )          
    agent_with_chat_history = RunnableWithMessageHistory(
        agent_executor,
        get_session_history,
        input_messages_key="query",
        history_messages_key="chat_history",
    )
    res = agent_with_chat_history.invoke({"query": query}, config={"configurable": {"session_id": chat_session_token}})
    print(f"#2: {chat_session_token}")  # For Debugging purposes

    return res.get("output")

# Get session history function
def get_session_history(session_id:str) -> BaseChatMessageHistory:
    if session_id not in st.session_state:
        st.session_state[session_id] = ChatMessageHistory()
        
    return st.session_state[session_id]

#######################################################################################################
# USER INTERFACE
st.header("BEMA")

# Check for previous user prompts.
if "user_prompt_history" not in st.session_state:
    st.session_state["user_prompt_history"] = []

# Check for chat answers
if "chat_message_history" not in st.session_state:
    # Create Chat Session Token
    st.session_state["chat_message_history"] = []
    chat_session_token = secrets.token_hex(16)
    st.session_state["chat_session_token"] = chat_session_token
    print(f"#1: {chat_session_token}")  # For debugging purposes

chat_session_token = st.session_state.get("chat_session_token")

if prompt := st.chat_input("Enter your message"):
    with st.spinner("Generating Response..."):
        response = generate_response(prompt, chat_session_token)
        formated_response = f"{response}"

        st.session_state["user_prompt_history"].append(prompt)
        st.session_state["chat_message_history"].append(formated_response)
        st.session_state["chat_session_token"] = chat_session_token

# if the Streamlit session state is not empty, output responses
if st.session_state["chat_message_history"]:
    for response, user_query in zip(st.session_state["chat_message_history"], st.session_state["user_prompt_history"]):
        # give each message widget a unique key not based off of output
        message(user_query, is_user=True, key=secrets.token_hex(8))
        message(response, key=secrets.token_hex(8))
