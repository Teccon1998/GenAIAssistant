import json
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import AsyncChromiumLoader
from langchain_community.document_transformers import BeautifulSoupTransformer
from langchain_openai import ChatOpenAI
from langchain_core.pydantic_v1 import BaseModel, Field
import pydantic

class LinkedInProfile(BaseModel):
    name: str = Field(description="The person's name")
    education: str = Field(description="The person's educational background, including degrees, institutions, and years attended.")
    experience: str = Field(description="A list of dictionaries, where each dictionary represents a job or work experience. Each dictionary should have keys for 'job_title', 'company', 'start_date', 'end_date' (if applicable), and 'description'.")
    skills: str = Field(description="A list of skills, including technical skills, soft skills, and domain-specific skills related to the person's field or industry.")

llm = ChatOpenAI(temperature=0)
structured_llm = llm.with_structured_output(LinkedInProfile)

def scrape_with_playwright(urls):
    loader = AsyncChromiumLoader(urls)
    docs = loader.load()
    bs_transformer = BeautifulSoupTransformer()
    docs_transformed = bs_transformer.transform_documents(
        docs, tags_to_extract=["div", "span"]
    )
    print("Extracting content with LLM")

    # Grab the first 1000 tokens of the site
    splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=1000, chunk_overlap=0
    )
    splits = splitter.split_documents(docs_transformed)

    if splits:
        try:
            # Define the prompt
            prompt = """
                Take the output found and form it into a JSON format, if proper information can't be default to the value ""
            """

            # Combine the prompt with the content of the first split
            input_text = prompt + splits[0].page_content

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
        return None

urls = ["https://www.linkedin.com/in/manfred-fong-532548300/"]
extracted_content = scrape_with_playwright(urls)