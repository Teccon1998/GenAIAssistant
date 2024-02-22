

from langchain_openai import OpenAI
import os
from dotenv import load_dotenv
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
import streamlit as st
from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent
from third_party.linkedin import scrape_linkedin_profile
import streamlit as st
from typing import Union

from langchain import hub 
from langchain.agents import AgentExecutor, create_react_agent
from langchain_openai import OpenAI 

from ice_breaker import icebreaker

load_dotenv()
def generate_response(input_text):
    tools=[icebreaker]
    prompt = hub.pull("hwchase17/react")
    print("PROMPT: " + str(prompt))
    llm = OpenAI()
    agent = create_react_agent(llm,tools,prompt)

    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True,handle_parsing_errors=True)
    res = agent_executor.invoke({"input": input_text})
    return res.get("output")

st.title("QUICK START APP🗣️")
with st.form("my_form", clear_on_submit=True):
    text = st.text_input("Enter Text:")
    submitted = st.form_submit_button("Submit")
    if submitted:
        response = generate_response(text)
        st.write(response)