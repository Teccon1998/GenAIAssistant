from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, Tool, AgentType

from tools.tools import get_profile_url


def lookup(name: str) -> str:
    llm = ChatOpenAI(temperature=0.0, model_name="gpt-3.5-turbo")
    template = """given the full name of a person {name_of_person}, I want you to give me as much information about this person as you can using their various social media."""
    tools_for_agent = [
        Tool(
            name="Crawl Google for social media profile pages",
            func=get_profile_url,
            description="Useful for when you need to get the URL of various social media.",
        )
    ]
    agent = initialize_agent(
        tools=tools_for_agent,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
    )

    prompt_template = PromptTemplate(
        template=template, input_variables=["name_of_person"]
    )

    linkedin_profile = agent.run(prompt_template.format_prompt(name_of_person=name))
    return linkedin_profile
