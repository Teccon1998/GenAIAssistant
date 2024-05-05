import json
from langchain.tools import tool
from tools.ProxyCurlLinkedIn import scrapelinkedinprofile
from tools.JSONIFYTool import file_to_json
from tools.ProxyCurlJob import scrape_job
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
import os

@tool
def create_enhanced_resume(job_desc_url):
    """
    Enhances a given resume based on LinkedIn data and job details fetched from a given URL.
    :param job_desc_url: URL to fetch job description data
    :return: JSON string with enhanced resume details
    """
    if 'link' not in st.session_state:
        return json.dumps({"error": "LinkedIn link is not set in session state."})

    linkedin_data = scrapelinkedinprofile(st.session_state['link'])
    resume_data = file_to_json() 
    job_desc_data = scrape_job(job_desc_url)

    # Prepare a comprehensive input for the LLM
    combined_input = f"""
    LinkedIn Profile:
    {json.dumps(linkedin_data, indent=2)}

    Resume Details:
    {json.dumps(resume_data, indent=2)}

    Job Description:
    {json.dumps(job_desc_data, indent=2)}

    Instructions:
    Generate an updated resume that aligns the LinkedIn profile and existing resume with the requirements of the job description.
    """

    # Setup the prompt template
    prompt_template = PromptTemplate(
        input_variables=['information'],
        template="""
            Given the LinkedIn data, existing resume, and job description below, integrate and update the resume accordingly:
            {information}
            Begin.
        """
    )

    # Setup LLMChain
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.2, openai_api_key=os.getenv('OPENAI_API_KEY'))
    chain = LLMChain(llm=llm, prompt=prompt_template, verbose=True)
    result = chain.invoke({"information": combined_input})

    # Parse the LLM output and return JSON string

    print(result.get('text'))
    return result.get('text')
# This function now correctly returns JSON formatted strings.
