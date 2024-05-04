from langchain_openai import ChatOpenAI
from langchain.tools.tavily_search import TavilySearchResults
from langchain.agents import create_openai_functions_agent, AgentExecutor
from langchain.utilities.tavily_search import TavilySearchAPIWrapper
from langchain_core.prompts import PromptTemplate
from langchain.tools import tool
from langchain.chains import LLMChain
from langchain import hub

#Tavily
from tavily import TavilyClient

from dotenv import load_dotenv,find_dotenv 
import os

#Find and Load Enviroment Variables
load_dotenv(find_dotenv())
tavily = TavilyClient(api_key=os.environ['TAVILY_API_KEY'])

#This function uses the Tavily Search Engine    to return all the social media accounts of a person
def lookup(query:str)->str:
    results=tavily.search(query,search_depth='advanced')
    return results
#Function to get the URL links from the Tavily search
def get_url_links(query:str)->str:
    """Performs a search and returns a string of content and sources within token limit"""
    searchContext=tavily._search(query=query,search_depth='advanced')
    #TODO: NARROW DOWN SEARCH CONTEXT RESULTS AND KEEP THE PARTS THE ARE USEFUL SO IT STAYS IN THE TOKEN LIMIT
    #good=LINKEDIN BAD=YOUTUBE
    #get source contexts from the tavily search
    sources = searchContext.get("results", [])
    context = [{"url": obj["url"]} for obj in sources]
    #iterate through list of Dictionary to target specific contexts
    for item in context:
        #gets and return it as a list
        urls=list(item.get("url"))
    
    return urls
    

@tool #Create Tavily Search Tool
def tavilySearchTool(name:str)->str:
    """Use to search for social media pages based on the full name of person  in the prompt"""
    tavily_search_results=lookup(name)
    tavily_link_results=get_url_links(name)

    summary_template="""
                      Given this block of data provide a summary of that person. The final response must be at least 3 sentences.
                      Also provide a list of links to their social media underlined and formatted.

                    Example:
                      
                    Harrison Chase
                    LinkedIn: https://www.linkedin.com/in/harrison-chase-961287118 
                    Twitter: https://twitter.com/hwchase17/status/1695490295914545626
                    etc..

                    Here is the data that is returned from the internet: {data},

                    and here is the list of links that needs to be outputted: {urls}.

                    Begin.
                     """
    summary_prompt_template=PromptTemplate(
        input_variables=["information"],template=summary_template
    )

    llm=ChatOpenAI(
        temperature=0,model_name="gpt-3.5-turbo",openai_api_key=os.environ['OPENAI_API_KEY']
    )

    chain = LLMChain(llm=llm,prompt=summary_prompt_template,verbose=True)
    result=chain.invoke({"data": tavily_search_results, "urls": tavily_link_results})
    return result


#Helper function to format the response. Replace new lines with a space
    
def format_response(response:str)->str:

    if "\n" in response:
        response=response.replace("\n"," ")
    else:
        return response
    
    return response