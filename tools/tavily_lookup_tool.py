from langchain_openai import ChatOpenAI
from langchain.tools.tavily_search import TavilySearchResults
from langchain.agents import create_openai_functions_agent, AgentExecutor
from langchain.utilities.tavily_search import TavilySearchAPIWrapper
from langchain_core.prompts import PromptTemplate
from langchain.tools import tool
from langchain.chains import LLMChain
from langchain import hub

from dotenv import load_dotenv,find_dotenv 
import os

#Find and Load Enviroment Variables
load_dotenv(find_dotenv())
#This function uses the Tavily Search Engine to return all the social media accounts of a person
def lookup(query:str,limiters=None)->str:
    """Searches for a person from their name and reurns information from their various social media pages"""
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7)

    #identify the tools
    search = TavilySearchAPIWrapper()
    tavily_tool = TavilySearchResults(api_wrapper=search)
    tools_for_agent =[
        tavily_tool
    ]

    #get user prompt
    instructions="""You are a search engine that given the full name of a person {name_of_person}, I want 
                    you to get as much information as possible using  {name_of_person} various social media.

                    Include the occupation of the person based on their linkedin profile {occupation_of_person},
                    the education associated with the person {education_of_person},
                    the professional work experience of the person based on their linkedin profile {experience_of_person},
                    social Media links of the person {social_media_links_of_person}

                    
                    I want you to give me as much detailed information as possible on that individual based on the 
                    social media of that person.

                    The following limiters are required: {limiters}
                 """
    
    base_prompt=hub.pull("langchain-ai/openai-functions-template")
    prompt=base_prompt.partial(instructions=instructions)

    # initialize the agent
    agent = create_openai_functions_agent(llm,tools_for_agent,prompt)
    #Execute the agent
    agent_executor=AgentExecutor(
        agent=agent,
        tools=tools_for_agent,
        verbose=True,
    )
    tavily_results=agent_executor.invoke({"input": {query}})
    return tavily_results

@tool #Create Tavily Search Tool
def tavilySearchTool(query:str)->str:
    """Use to search information about people and create a summary in the format of the summary template"""
    tavily_search_results=lookup(query)

    summary_template="""
                      summerize this information {information}. 
                      Make sure to list the following:
                      1) Details on the work experience of the individual
                      2) Details on the education of the individual
                      3) Details on how I can contact the individual
                      4) Details on the individual's various social media accounts
                      5) Links to the individual's various social media accounts
                     """
    summary_prompt_template=PromptTemplate(
        input_variables=["information"],template=summary_template
    )

    llm=ChatOpenAI(
        temperature=0,model_name="gpt-3.5-turbo",openai_api_key=os.environ['OPENAI_API_KEY']
    )

    chain = LLMChain(llm=llm,prompt=summary_prompt_template,verbose=True)
    result=chain.invoke({"information": tavily_search_results})
    return result
