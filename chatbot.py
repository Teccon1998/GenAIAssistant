#This file will implement the chatbot feature
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationChain
from langchain_openai import ChatOpenAI
from langchain_core.runnables.history import RunnableWithMessageHistory
from dotenv import load_dotenv,find_dotenv 
# frontend tool 
import streamlit as st
from streamlit_chat import message
import os

from app import generate_response 

#load enviroment variables
load_dotenv(find_dotenv())
#intialize chat model
chat = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.2)
#initialize LLM
llm=ChatOpenAI(temperature=0,model_name="gpt-3.5-turbo",openai_api_key=os.environ['OPENAI_API_KEY'])
#handles converstations between Ai and User
#Helps keep conversations within the token limit
def conversationHandler(userInput):
    #intialize conversation memory chain
    conversation_with_summary = ConversationChain(
        llm=llm,
        #keeps a buffer of recent interactions in memory, and uses token length rather than number of interactions to determine when to flush interactions.
        verbose=True,
        memory = ConversationTokenBufferMemory(llm=llm, return_messages=True,max_token_limit=10),
    )
    conversation=conversation_with_summary.predict(input=userInput)
    return conversation

#Chat Interface
st.header("AI Chat Assistant")

#get user input
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
            f"{response['result']}"
        )

        st.session_state["user_prompt_history"].append(prompt)
        st.session_state["chat_message_history"].append(formated_response)

#if the streamlit session state is not empty. Output responses
if st.session_state["chat_message_history"]:
    for response, user_query in zip(st.session_state["chat_message_history"],st.session_state["user_prompt_history"]):
        message(user_query,is_user=True)
        message(response)
