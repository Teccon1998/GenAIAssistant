import os
from langchain.document_loaders import UnstructuredFileLoader
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
import streamlit as st
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import PyPDF2
import io

load_dotenv()

def file_to_json() -> str:
     # MongoDB URI without the tlsCAFile option
    uri = os.environ.get('URI_FOR_MONGO')

    # Create MongoClient object with tlsCAFile option
    client = MongoClient(uri, tlsCAFile="C:\\Python312\\Lib\\site-packages\\certifi\\cacert.pem",
                         server_api=ServerApi('1'))
   
    # Select the database and collection
    database_name = "Elijuwon_Database_499"
    collection_name = "files_uploaded"
    db = client[database_name]
    collection = db[collection_name]

    # Query the collection to get the document
    document = collection.find_one({'username': st.session_state['username']})

    if document:
        file_bytes = document['data']

        # Convert bytes to a readable stream for PyPDF2
        pdf_file = io.BytesIO(file_bytes)

        # Initialize the PDF reader from the binary stream
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        # Extract text from each page of the PDF
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        # # Load the file using UnstructuredFileLoader
        # loader = UnstructuredFileLoader(file_path)
        # documents = loader.load()
        # text = " ".join([doc.page_content for doc in documents])

    JSONIFY_prompt_template = """Given this text input, give a JSON that returns all relevant info,
    be sure to make it look like a proper resume in JSON format and exclude no information unless it is completely irrelevant to the resume itself.

    Here is the Resume's raw text: {information}

    Begin."""

    prompt_template = PromptTemplate(
        input_variables=['information'], template=JSONIFY_prompt_template
    )

    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.2, openai_api_key=os.environ['OPENAI_API_KEY'])
    chain = LLMChain(llm=llm, prompt=prompt_template, verbose=True)
    result = chain.invoke({"information": text})
    return result.get("text")