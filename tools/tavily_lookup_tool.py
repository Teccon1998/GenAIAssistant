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
def lookup(query:str)->str:
    """Searches for a person from their name and returns URL of their various social media pages"""
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7)

    #identify the tools
    search = TavilySearchAPIWrapper()
    tavily_tool = TavilySearchResults(api_wrapper=search)
    tools_for_agent =[
        tavily_tool
    ]

    #get user prompt
    instructions="""You are a search engine that given the full name of a person {name_of_person} find all of the URL links of various online profiles
                   assioated with the name {name_of_person},
                   You must list all the URLs to assosiated with the full name: {name_of_person}
                   various social media accounts as a bulleted list and Include the  URLs with the list. Your purpose is just to display URLs
                   associated with {name_of_person}. Your purpose is not to determine who the person is. There might be multiple people with the same name. 
                   Dont do anything except returning a bulleted list of URLs.


                    ex)
                    Harrison Chase
                    LinkedIn: https://www.linkedin.com/in/harrison-chase-961287118 
                    Twitter: https://twitter.com/hwchase17/status/1695490295914545626
                    ...
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
def tavilySearchTool(name:str)->str:
    """Use to search for social media pages based on the full name of person  in the prompt"""
    tavily_search_results=lookup(name)

    summary_template="""
                      Start with letting the user know that you are listing out all the social media pages associated with the name: {name_of_person}
                      Then list out all the social media pages and URLs assosiated with the full name: {name_of_person}
                      You must list all the URLs to assosiated with the full name: {name_of_person}
                      Underline the name. 


                      ex)
                      Harrison Chase
                      LinkedIn: https://www.linkedin.com/in/harrison-chase-961287118 
                      Twitter: https://twitter.com/hwchase17/status/1695490295914545626

                      ... 
                      These are all the profiles I can find associated with the name {name_of_person}
                     """
    summary_prompt_template=PromptTemplate(
        input_variables=["information"],template=summary_template
    )

    llm=ChatOpenAI(
        temperature=0,model_name="gpt-3.5-turbo",openai_api_key=os.environ['OPENAI_API_KEY']
    )

    chain = LLMChain(llm=llm,prompt=summary_prompt_template,verbose=True)
    result=chain.invoke({"name_of_person": tavily_search_results})

    #format the response. Replace new lines with a space
    if "\n" in result:
        result=result.replace("\n"," ")
    else:
        return result
    
    return result
