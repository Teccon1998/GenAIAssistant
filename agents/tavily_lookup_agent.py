from langchain_openai import ChatOpenAI
from langchain.tools.tavily_search import TavilySearchResults
from langchain.agents import create_openai_functions_agent,AgentExecutor
from langchain.utilities.tavily_search import TavilySearchAPIWrapper
from langchain.tools.tavily_search import TavilySearchResults
from langchain import hub

from dotenv import load_dotenv,find_dotenv #Find and Load Enviroment Variables
load_dotenv(find_dotenv())


#This function uses the Tavily Search Engine to return all the social media accounts of a person
def lookup(query:str)->str:
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7)

    #identify the tools
    search = TavilySearchAPIWrapper()
    tavily_tool = TavilySearchResults(api_wrapper=search)
    tools_for_agent =[
        tavily_tool
    ]


    #get user prompt
    instructions=""" You are a search engine that 
                    given the full name of a person {name_of_person}, I want you to give me as much information 
                    about this person as you can using their various social media.
                  """
    base_prompt = hub.pull("langchain-ai/openai-functions-template")
    prompt = base_prompt.partial(instructions=instructions)

    # initialize the agent
    agent = create_openai_functions_agent(llm, tools_for_agent, prompt)
    #Execute the agent
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools_for_agent,
        verbose=True,
    )

    tavily_results=agent_executor.invoke({"input": {query}})
    return tavily_results

if __name__ == "__main__":
    lookup("Tell me about Tenzin Takchuk who currently attends the university at albany")
