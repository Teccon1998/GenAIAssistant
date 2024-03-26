import streamlit as st
from langchain_openai import OpenAI
import os
from dotenv import load_dotenv
import streamlit as st

from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent
from langchain_openai import OpenAI

load_dotenv()

#main agent execution process
def generate_response(query):
    tools = []
    prompt = hub.pull("hwchase17/react")
    prompt += "\n Do not summarize or condense the response, simply reformat the response to make it look better readable. "
    print("PROMPT: " + str(prompt))
    llm = OpenAI()
    agent = create_react_agent(llm, tools, prompt)

    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)
    res = agent_executor.invoke({"input": query})
    return res.get("output")



st.title("QUICK START APP🗣️")
with st.form("my_form", clear_on_submit=True):
    query = st.text_input("Enter Text:")
    submitted = st.form_submit_button("Submit")
    if submitted:
        response = generate_response(query)
        st.write(response)
