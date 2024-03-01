#This file will implement the chatbot feature
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationChain
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain.memory import ConversationTokenBufferMemory,ChatMessageHistory
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_openai import ChatOpenAI
from langchain_core.runnables.history import RunnableWithMessageHistory
from dotenv import load_dotenv,find_dotenv 
import os

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

if __name__ == "__main__":
    input=input(">>>")
    conversationHandler(input)
