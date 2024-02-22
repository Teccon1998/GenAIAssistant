import os
from dotenv import load_dotenv
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent
from third_party.linkedin import scrape_linkedin_profile
from langchain.tools import tool

@tool
def icebreaker(name: str) -> str:
    """Used to search information about people and creates a summary in the format of the summary template."""
    linkedin_profile_url = linkedin_lookup_agent(name=name)
    linkedin_data = scrape_linkedin_profile(linkedin_profile_url=linkedin_profile_url)
    print(linkedin_data)

    summary_template = """
        given the following information {information} about a person I want you to create:
        1. A short summary
        2. Two short interesting facts about them
        3. A long summary
        4. 2-3 creative icebreakers based on the knowledge given.
       
        """

    summary_prompt_template = PromptTemplate(
        input_variables=["information"], template=summary_template
    )

    openai_api_key = os.environ['OPENAI_API_KEY']

    llm = ChatOpenAI(
        temperature=0, model_name="gpt-3.5-turbo", openai_api_key=openai_api_key
    )

    chain = LLMChain(llm=llm, prompt=summary_prompt_template)
    result = chain.invoke({"information": linkedin_data})
    print(result)
    return result


# if __name__ == "__main__":
#     load_dotenv()
#     name = "Pradeep Atrey"
#     res = icebreaker(name=name)
#     print(res)
