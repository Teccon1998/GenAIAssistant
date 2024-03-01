import streamlit as st
from dotenv import load_dotenv
from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent
from langchain_openai import OpenAI

from ice_breaker import icebreaker

from agents.twitter_tweets_agent import get_tweets

load_dotenv()


def generate_response(input_text):
    tools = [get_tweets(input_text)]
    prompt = hub.pull("elijuwon/interest_generator")
    # prompt += "\n Do not summarize or condense the response, simply reformat the response to make it look better readable. "
    print("PROMPT: " + str(prompt))
    llm = OpenAI()
    agent = create_react_agent(llm, tools, prompt)

    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)
    res = agent_executor.invoke({"input": input_text})
    return res.get("output")


st.title("QUICK START APP🗣️")
with st.form("my_form", clear_on_submit=True):
    text = st.text_input("Enter Text:")
    submitted = st.form_submit_button("Submit")
    if submitted:
        response = generate_response(text)
        st.write(response)
