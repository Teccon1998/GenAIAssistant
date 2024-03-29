import streamlit as st
from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent
from langchain_openai import OpenAI
import fitz
from langchain_core.prompts import PromptTemplate
from langchain.tools import tool
from langchain_openai import ChatOpenAI
import os
from langchain_community.chat_models import ChatOpenAI
from langchain.chains import LLMChain


def convert_pdf_to_text(upload) -> str:
    document = fitz.open(stream=upload.getvalue(), filetype="pdf")
    pdf_text = ""
    for page in document:
        pdf_text += page.get_text()
    return pdf_text


@tool
def convert_txt_to_json(resume_text):
    """Converts text of a resume to JSON with the text in the PDF"""
    # text = convert_pdf_to_text(resume_pdf)
    Json_prompt = """
    Summarize the text {information} into a JSON:
    """

    prompt_template = PromptTemplate(
        input_variables=["information"], template=Json_prompt
    )

    llm = ChatOpenAI(
        temperature=0,
        model_name="gpt-3.5-turbo",
        openai_api_key=os.environ["OPENAI_API_KEY"],
    )

    chain = LLMChain(llm=llm, prompt=prompt_template, verbose=True)
    result = chain.invoke({"information": resume_text})
    return result


def generate_response(input_text, uploaded_file=None):
    tools = [convert_txt_to_json,]
    prompt = hub.pull("hwchase17/react")
    print("PROMPT: " + str(prompt))
    llm = OpenAI()
    agent = create_react_agent(llm, tools, prompt)

    agent_executor = AgentExecutor(
        agent=agent, tools=tools, verbose=True, handle_parsing_errors=True
    )
    res = ""
    if uploaded_file:
        resume_text = convert_pdf_to_text(uploaded_file)
        Json_prompt = """
        Role: You are a summary robot that reads a resume and tries to create a JSON from an input text of a resume.
        Instructions: Read the following text and turn it into a JSON of common information found on resumes. Leave blank what is not included.
        Steps: Read each line of text and try to fit it into a standardized JSON format. 
        End Goal: A JSON with standardized format whos fields would be common amongst almost all resumes.
        Narrowing: You may not simply place text from the input straight into a field. You must come up with field names and their values using the resume as a base.

        Execute this with the following text: {information}
        """

        prompt_template = PromptTemplate(
            input_variables=["information"], template=Json_prompt
        )

        llm = ChatOpenAI(
            temperature=0,
            model_name="gpt-3.5-turbo",
            openai_api_key=os.environ["OPENAI_API_KEY"],
        )

        chain = LLMChain(llm=llm, prompt=prompt_template, verbose=True)
        result = chain.invoke({"information": resume_text})
        return result.get("text")
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
