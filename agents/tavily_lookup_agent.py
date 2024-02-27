import os
from langchain.utilities.tavily_search import TavilySearchAPIWrapper
from langchain.agents import initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI
from langchain.tools.tavily_search import TavilySearchResults

from dotenv import load_dotenv,find_dotenv #Find and Load Enviroment Variables
load_dotenv(find_dotenv())

def lookup(name:str)->str:
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7)
    search = TavilySearchAPIWrapper()
    tavily_tool = TavilySearchResults(api_wrapper=search)

    # initialize the agent
    agent_chain = initialize_agent(
        [tavily_tool],
        llm,
        agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
)