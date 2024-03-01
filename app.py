from dotenv import load_dotenv
import streamlit as st
from langchain import hub
from langchain.agents import AgentExecutor,  create_openai_tools_agent
import fitz
from langchain_core.prompts import PromptTemplate
from langchain.tools import tool
from langchain_openai import ChatOpenAI
import os
from langchain_community.chat_models import ChatOpenAI
from langchain.chains import LLMChain

load_dotenv()


def convert_pdf_to_text(upload) -> str:
    document = fitz.open(stream=upload.getvalue(), filetype="pdf")
    pdf_text = ""
    for page in document:
        pdf_text += page.get_text()
    return pdf_text


@tool
def input_text_to_json(input_text: str) -> dict:
    """Takes the text given to the agent and turns it into JSON """
    Json_prompt = """
    Role: You are a summary robot that reads a resume and tries to create a JSON from an input text of a resume.
    Instructions: Read the following text and turn it into a JSON of common information found on resumes. Leave blank what is not included.
    Steps: Read each line of text and try to fit it into a standardized JSON format. 
    End Goal: A JSON with standardized format whos fields would be common amongst almost all resumes.
    Narrowing: You may not simply place text from the input straight into a field. You must come up with field names and their values using the resume as a base.

    Execute this with the following text: {information}
    """

    prompt_template = PromptTemplate(
        input_variables=["information"], template=Json_prompt,
    )

    llm = ChatOpenAI(
        temperature=0,
        model_name="gpt-3.5-turbo",
        openai_api_key=os.environ["OPENAI_API_KEY"],
    )

    chain = LLMChain(llm=llm, prompt=prompt_template, verbose=True)
    result = chain.invoke({"information": input_text})
    return result.get('text')


def generate_response(input_text, uploaded_file=None):
    tools = [input_text_to_json]
    prompt = hub.pull("hwchase17/openai-tools-agent")
    print("PROMPT: " + str(prompt))
    prompt += "\n Do not summarize what is responded. Return the 'text' field directly"
    model = ChatOpenAI()
    res = ""
    if uploaded_file:
        agent = create_openai_tools_agent(model, tools, prompt)
        agent_executor = AgentExecutor(
            agent=agent, tools=tools, verbose=True, handle_parsing_errors=True
        )
        input_text = convert_pdf_to_text(upload=uploaded_file)
        res = agent_executor.invoke({"input": input_text})
        return res.get("output")
    else:
        res = agent_executor.invoke({"input": input_text})
        return res.get("output")


st.title("QUICK START APP🗣️")
with st.form("my_form", clear_on_submit=True):
    text = st.text_input("Enter Text:")
    uploaded_file = st.file_uploader("File Uploader (optional):", type=["pdf"])
    submitted = st.form_submit_button("Submit")
    if submitted:
        response = generate_response(text, uploaded_file)
        st.write(response)
