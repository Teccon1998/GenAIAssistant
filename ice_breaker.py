import os
from dotenv import load_dotenv
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent
from agents.tavily_lookup_agent import lookup as tavily_lookup_agent
from third_party.linkedin import scrape_linkedin_profile
from langchain.tools import tool


@tool
def icebreaker(name: str) -> str:
    """Used to search information about people and creates a summary in the format of the summary template."""
    linkedin_profile_url = tavily_lookup_agent(name=name)
    print(linkedin_profile_url)

    summary_template = """
        given the following information {information} about a person I want you to create:
        1. A long summary about who they are, what they do, their interests and their experience.
        2. A shorter summary about who they are, what they do
        3. A few ice breakers to speak to them about.
        """

    summary_prompt_template = PromptTemplate(
        input_variables=["information"], template=summary_template
    )

    openai_api_key = os.environ['OPENAI_API_KEY']

    llm = ChatOpenAI(
        temperature=0, model_name="gpt-3.5-turbo", openai_api_key=openai_api_key
    )

    chain = LLMChain(llm=llm, prompt=summary_prompt_template,verbose=True)
    result = chain.invoke({"information": linkedin_profile_url})
    print(result)
    return result
