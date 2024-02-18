import streamlit as st 
from langchain.llms import OpenAI
from langchain_community.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.tools.render import render_text_description
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
from langchain.agents import AgentExecutor
from langchain_core.tools import tool, Tool
from langchain.agents.format_scratchpad import format_log_to_str
from langchain.agents.output_parsers import ReActSingleInputOutputParser
from typing import Union
from langchain_core.agents import AgentFinish, AgentAction

import os

load_dotenv()


@tool
def get_text_length(text: str) -> int:
    """Retruns the length of a text by characters"""
    return len(text)


def find_tool_by_name(tools: list[Tool], tool_name: str) -> Tool:
    for tool in tools:
        if tool.name == tool_name:
            return tool
        raise ValueError("Tool with name {tool_name} not found}")

def generate_response(input_text):
    tools = [get_text_length]

    template = """ 
    Answer the following questions as best you can. You have access to the following tools:

    {tools}

    Use the following format:

    Question: the input question you must answer
    Thought: you should always think about what to do
    Action: the action to take, should be one of [{tool_names}]
    Action Input: the input to the action
    Observation: the result of the action
    ... (this Thought/Action/Action Input/Observation can repeat N times)
    Thought: I now know the final answer
    Final Answer: the final answer to the original input question

    Begin!

    Question: {input}
    Thought: {agent_scratchpad}
    """

    prompt = PromptTemplate.from_template(template=template).partial(
        tools=render_text_description(tools),
        tool_names=", ".join([t.name for t in tools]),
    )

    llm = ChatOpenAI(temperature=0, stop=["\nObservation"])
    intermediate_steps = []
    agent = (
        {
            "input": lambda x: x["input"],
            "agent_scratchpad": lambda x: format_log_to_str(x["agent_scratchpad"]),
        }
        | prompt
        | llm
        | ReActSingleInputOutputParser()
    )
    agent_step: Union[AgentAction, AgentFinish] = agent.invoke(
        {"input": input_text,
         "agent_scratchpad": intermediate_steps,
         }
    )
    print(agent_step)

    if isinstance(agent_step, AgentAction):
        tool_name = agent_step.tool
        tool_to_use = find_tool_by_name(tools, tool_name)
        tool_input = agent_step.tool_input

        observation = tool_to_use.func(str(tool_input))
        intermediate_steps.append(agent_step, str(observation))

        print(f"{observation}")
  
    


st.title("QUICK START APP🗣️")
with st.form('my_form', clear_on_submit=True):
    text = st.text_input('Enter Text:')
    submitted = st.form_submit_button('Submit')
    if submitted:
        response = generate_response(text)
        st.write("Final Answer: " + response)