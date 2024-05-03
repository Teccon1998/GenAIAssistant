#This file will implement the chatbot feature
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.schema import AIMessage, HumanMessage


from dotenv import load_dotenv,find_dotenv 
from langchain.agents import AgentExecutor, create_react_agent, create_openai_tools_agent

#LangChain Messages
from langchain_core.messages import SystemMessage
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
import secrets # for generating random session ID


#Message Prompt Tools
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder, 
    SystemMessagePromptTemplate
)

from langchain_core.runnables.history import RunnableWithMessageHistory

# frontend tool 
import streamlit as st
from streamlit_chat import message
from tools.tavily_lookup_tool import tavilySearchTool
from tools.FileManagementTool import FileTool
from langchain import hub



#load enviroment variables
load_dotenv(find_dotenv())
#intialize chat model
chat = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

chat_session_token=secrets.token_hex(16)


def generate_response(query:str):
    
    file_tool = FileTool()
    tools = [tavilySearchTool, file_tool]
    
    # Create prompt template
    prompt = ChatPromptTemplate.from_messages([
        ("system", 
         "You are a helpful assistant. You may not need to use tools for every query - the user may just want to chat!",
         ),
        #MessagesPlaceholder(variable_name="messages"),
        #MessagesPlaceholder(variable_name="messages"),
        MessagesPlaceholder(variable_name="chat_history"), ("human", "{query}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])
    
    
    #initialize memory
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    #agent = create_react_agent(llm=llm, tools=tools, prompt=prompt,)
    agent = create_openai_tools_agent(chat, tools, prompt,)

    agent_executor = AgentExecutor(
        agent=agent, 
        tools=tools,
        verbose=True,
        memory=memory
    )          
    agent_with_chat_history = RunnableWithMessageHistory(
        agent_executor,
        get_session_history,
        input_messages_key="query",
        history_messages_key="chat_history",
    )
    res = agent_with_chat_history.invoke({"query": query},config={"configurable": {"session_id": chat_session_token}},) 

    return res.get("output")

#get session histor function
def get_session_history(session_id:str)-> BaseChatMessageHistory:
    #add chat history
    if session_id not in st.session_state:
        st.session_state[session_id]=ChatMessageHistory()
        
    return st.session_state[session_id]


#######################################################################################################
#USER INTERFACE
st.header("AI Chat Assistant")
prompt=st.text_input("Prompt", placeholder="Enter your message")
#check for previouse user prompts.
if "user_prompt_history" not in st.session_state:
    st.session_state["user_prompt_history"]=[]

#check for chat answers
if "chat_message_history" not in st.session_state:
    st.session_state["chat_message_history"]=[]
    

if prompt:
    with st.spinner("Generating Response..."):
        response=generate_response(prompt)
        #Variable that will be displayed to the user when
        formated_response=(
            f"{response}"
        )

        st.session_state["user_prompt_history"].append(prompt)
        st.session_state["chat_message_history"].append(formated_response)
        #add context to memory
        messages = [
            HumanMessage(content=prompt),
            AIMessage(content=formated_response)
        ]
        
        st.session_state[chat_session_token].add_message(messages)
        

#if the streamlit session state is not empty. Output responses
if st.session_state["chat_message_history"]:
    for response, user_query in zip(st.session_state["chat_message_history"], st.session_state["user_prompt_history"]):
        #give each message widget a unique key not based off of output
        message(user_query,is_user=True, key=secrets.token_hex(8))
        message(response, key=secrets.token_hex(8))

