#This file will implement the chatbot feature
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.schema import AIMessage, HumanMessage


from dotenv import load_dotenv,find_dotenv 
from langchain.agents import AgentExecutor, create_react_agent

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
import os
from tools.tavily_lookup_tool import tavilySearchTool
from tools.FileManagementTool import FileTool



#load enviroment variables
load_dotenv(find_dotenv())
#intialize chat model
chat = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.2)
chat_model_with_stop = chat.bind(stop=["\nObservation"])
#secrets.token_hex(16) used to generate a random hex token to act as session ID. 16 Byte Length
chat_session_token=secrets.token_hex(16)

#initialize LLM
llm=chat_model_with_stop
#handles converstations between Ai and User``
#Helps keep conversations within the token limit

#TODO: ADD TO MONGO SO USERS CAN GO BACK ON CONVERSATIONS AND TO GO BACK ON TOPICS
#SO AI CAN MAKE RECOMMENDATIONS 

def generate_response(query:str):
    
    file_tool = FileTool()
    tools = [tavilySearchTool, file_tool]
    
    prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessage(
                content="""You are a chatbot having a conversation with a human.
                Try to answer the questions to the best of your ability.
                """
            ),  # The persistent system prompt
            
            SystemMessagePromptTemplate.from_template(
                """
                You have access to these tools {tools}
                Action: You can optionally use the following tools if needed: [{tool_names}]
                Thought: I know what to respond
                
                Use a json blob to specify a tool by providing an action key (tool name) 
                and an action_input key (tool input).
                Provide only ONE action per $JSON_BLOB, as shown:
                ```
                {{
                    "action": $TOOL_NAME, Use tools if necessary. Respond directly if appropriate.
                    "action_input": The input to the action
                    "Thought: {agent_scratchpad}
                }}
                
                ```
                Begin!
                """
            ),
            
            MessagesPlaceholder(
                variable_name="chat_history"
            ),  # Where the memory will be stored.
            
            HumanMessagePromptTemplate.from_template(
                "{query},"
            ),  # Where the human input will injected
        ]
    )
    
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    agent = create_react_agent(llm=llm, tools=tools, prompt=prompt,)

    agent_executor = AgentExecutor.from_agent_and_tools(
        agent=agent, 
        tools=tools, 
        verbose=True,
        memory=memory, 
        handle_parsing_errors=True,
        early_stopping_method="force", # Applies final pass to generate an output if max iterations is reached
        max_iterations=5 # Sets the number of intermediate steps
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

