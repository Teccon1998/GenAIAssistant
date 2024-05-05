import json
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import AsyncChromiumLoader
from langchain_community.document_transformers import BeautifulSoupTransformer
from langchain_openai import ChatOpenAI
from langchain_core.pydantic_v1 import BaseModel, Field
import pydantic
from typing import List
from langchain.tools import tool
import streamlit as st

# The Pydantic model that (roughly) instructs the llm what the output should be
class LinkedInProfile(BaseModel):
    name: str = Field(description="The person's name")
    education: str = Field(description="The person's educational background, including degrees, institutions, and years attended.")
    experience: List[str] = Field(description="A list of dictionaries, where each dictionary represents a job or work experience. Each dictionary should have keys for 'job_title', 'company', 'start_date', 'end_date' (if applicable), and 'description' <job-title> <start-date> <end-date> <job-description> ex) {"'experience'": [{'job-title': 'baby-sitter', 'start-date':'1999', 'end-date': 'present', 'job-description':'Was the primary guardian for 2 children ages 4, and 8'},{'job-title': 'porter', 'start-date':'2003', 'end-date': '2020', 'job-description':'Was in charge of cleaning the lobby, and prepping apartments for new incoming residents'}]}.")
    skills: List[str] = Field(description="A list of skills, including technical skills, soft skills, and domain-specific skills related to the person's field or industry.")

# The llm that would be in charge of reading the provided text and infer information out of it 
llm = ChatOpenAI(temperature=0.0)
# with_structured_output is a funciton that takes in a model and assigns it to an LLM, this is actually assigning the Pydantic model from above 
structured_llm = llm.with_structured_output(LinkedInProfile)

def scrape_with_playwright():
    """ This tool takes a profile link from LinkedIn and pulls the users information and returns json information on it """
   
    profile = st.session_state['link']
    skills = profile + "details/skills/"
    experience = profile + "detials/experience/"
    education = profile + "details/education/"

    urls = [profile,skills,experience,education]

    # Gets the web pages and prepares them to load them to transform them into Document objects
    loader = AsyncChromiumLoader(urls)
    # loads the found web pages into Documents
    docs = loader.load()
    # An object that is designed to take HTML and strip text out of it 
    bs_transformer = BeautifulSoupTransformer()
    # configuring the transformer to pull text out of the div, li and span containers
    docs_transformed = bs_transformer.transform_documents(
        docs, tags_to_extract=["div", "span", "li"]
    )
    print("Extracting content with LLM")

    # Grab the first 1000 tokens of the site
    splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=1500, chunk_overlap=0
    )
    splits = splitter.split_documents(docs_transformed)

    if splits:
        try:
            # Define the prompt
            prompt = """
            Extract the following information from the profile page and return a output in JSON format:

            Step 1) Find the name over the person who ownes the profile 
            Step 2) With the text given Search for the persons Education, include the name of the school, and their degree 
            Step 3) Find the list of Work experience in the text given and add them in a list, with each index being a dict with the keys <job-title> <start-date> <end-date> <job-description> ex) {"experience": [{'job-title': 'baby-sitter', 'start-date':'1999', 'end-date': 'present', 'job-description':'Was the primary guardian for 2 children ages 4, and 8'},{'job-title': 'porter', 'start-date':'2003', 'end-date': '2020', 'job-description':'Was in charge of cleaning the lobby, and prepping apartments for new incoming residents'}]}
            Step 4) With the text given look for Skills within the text that are within the <li> containers
            """

            # Combine the prompt with the content of the handfull of splits
            input_text = prompt + splits[0].page_content + splits[1].page_content + splits[2].page_content + splits[3].page_content

            # Process the input text
            extracted_content = structured_llm.invoke(input_text)
            # Convert the Pydantic model instance to a dictionary
            json_data = extracted_content.dict()
            # Convert the dictionary to JSON
            json_output = json.dumps(json_data, indent=4)
            print(json_output)
            return json_output
        except pydantic.error_wrappers.ValidationError as e:
            print(f"Error: {e}")
            return None
    else:
        print("No content found to extract.")
        return 



# extracted_content = scrape_with_playwright(urls)