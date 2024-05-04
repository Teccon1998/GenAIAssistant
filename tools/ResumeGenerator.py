import json
from langchain.tools import tool
from tools.ProxyCurlLinkedIn import scrapelinkedinprofile
from tools.JSONIFYTool import file_to_json
from tools.ProxyCurlJob import scrape_job
import streamlit as st

@tool
def create_enhanced_resume(job_desc_url):
    """
    Enhances a given resume based on LinkedIn data and job description fetched from URLs.
    :param job_desc_url: URL to fetch job description data
    :return: JSON object with enhanced resume details
    """
    if 'link' in st.session_state:
        linkedin_data = scrapelinkedinprofile(st.session_state['link'])
        resume_data = file_to_json()  # Assuming this function is corrected to actually return JSON data
        job_description = scrape_job(job_desc_url)  # Assuming this fetches and returns JSON

        # Merge LinkedIn and resume details
        enhanced_resume = {**resume_data, **linkedin_data}

        # Deduplicate and combine skills from all sources
        all_skills = set()
        for source in [linkedin_data, resume_data, job_description]:
            all_skills.update(source.get('skills', []))

        enhanced_resume['skills'] = list(all_skills)

        # Include job description summary as an objective
        if 'summary' in job_description:
            enhanced_resume['objective'] = job_description['summary']

        print(enhanced_resume)
        return json.dumps(enhanced_resume, indent=4)
    else:
        print("LinkedIn link is not set in session state.")
        return {}

# Example usage: Assuming you have a Streamlit widget setting 'link' and a job description URL
# result = create_enhanced_resume("https://example.com/job_description")
