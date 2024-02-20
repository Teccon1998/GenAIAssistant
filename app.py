import streamlit as st
from dotenv import load_dotenv
from typing import Union

from langchain import hub 
from langchain.agents import AgentExecutor, create_react_agent
from langchain_openai import OpenAI 
from langchain.tools import tool


import os

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

print(openai_api_key)

@tool
def get_word_length(word: str) -> int:
    """Returns the length of a word based on the amount of characters on the target word."""
    return len(word)


def generate_response(input_text):
    tools=[get_word_length]
    prompt = hub.pull("hwchase17/react")
    print(prompt)
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
        response = generate_response("where is dad?")
        st.write(response)
