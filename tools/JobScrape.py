import streamlit as st
import json
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain.tools import tool
import pydantic
from typing import List
import asyncio
from streamlit import experimental_singleton as stx

class LinkedInJob(BaseModel):
    job_title: str = Field(description="The name of the job title")
    location: str = Field(description="The area where the job is located, including work from home options")
    salary: int = Field(description="The salary amount offered by the job")
    skills: List[str] = Field(description="List of required skills, including technical, soft, and domain-specific skills")

llm = ChatOpenAI(temperature=0.0)
structured_llm = llm.with_structured_output(LinkedInJob)

@stx.singleton
async def scrape_job(urls):
    """Scrape job information from the given URLs asynchronously."""
    loader = AsyncChromiumLoader(urls)
    docs = await loader.load()
    bs_transformer = BeautifulSoupTransformer()
    docs_transformed = bs_transformer.transform_documents(docs, tags_to_extract=["div", "span", "li"])

    splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(chunk_size=1500, chunk_overlap=0)
    splits = splitter.split_documents(docs_transformed)

    if splits:
        try:
            prompt = "Extract as much information possible from the job posting page and return an output in JSON format:"
            input_text = prompt + ' '.join(split.page_content for split in splits[:4])

            extracted_content = await structured_llm.invoke(input_text)
            json_data = extracted_content.dict()
            json_output = json.dumps(json_data, indent=4)
            return json_output
        except pydantic.error_wrappers.ValidationError as e:
            return f"Validation error: {e}"
    else:
    else:
        print("No content found to extract.")
        return
        return "No extractable content found."