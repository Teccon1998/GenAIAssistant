import json
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import AsyncChromiumLoader
from langchain_community.document_transformers import BeautifulSoupTransformer
from langchain_openai import ChatOpenAI
from langchain_core.pydantic_v1 import BaseModel, Field
import pydantic
from typing import List

# The Pydantic model that (roughly) instructs the llm what the output should be
class LinkedInProfile(BaseModel):
    job_title: str = Field(description="The name of the Job title")
    location: str = Field(description="The area in which the Job is located, mention if their are any work from home options")
    salary: int = Field(description="The salary amount that the Job is paying")
    skills: List[str] = Field(description="A list of skills, including technical skills, soft skills, and domain-specific skills needed for the job")

# The llm that would be in charge of reading the provided text and infer information out of it 
llm = ChatOpenAI(temperature=0.0)
# with_structured_output is a funciton that takes in a model and assigns it to an LLM, this is actually assigning the Pydantic model from above 
structured_llm = llm.with_structured_output(LinkedInProfile)

def scrape_with_playwright(urls):
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
            Extract as much information possible from the job posting page and return a output in JSON format:
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




urls = ["https://www.linkedin.com/jobs/view/3877286858/?alternateChannel=search&refId=Sbx3rE8NqZwGEhKwCU8eYQ%3D%3D&trackingId=%2BGjiTZNneFidDIjb1yOFqw%3D%3D"]
extracted_content = scrape_with_playwright(urls)