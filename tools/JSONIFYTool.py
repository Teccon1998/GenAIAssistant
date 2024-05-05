import os
import io
import json
from pymongo import MongoClient, server_api
import PyPDF2
import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain

load_dotenv()

def file_to_json() -> dict:
    uri = os.getenv('URI_FOR_MONGO')
    tlsCAFile = os.getenv('tlsCAFile')
    client = MongoClient(uri, tlsCAFile=tlsCAFile)

    db = client['Elijuwon_Database_499']
    collection = db['files_uploaded']
    document = collection.find_one({'username': st.session_state['username']})

    text = ""
    if document:
        file_bytes = document['data']
        pdf_file = io.BytesIO(file_bytes)
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = "".join(page.extract_text() or "" for page in pdf_reader.pages)  # Safeguard against None

    JSONIFY_prompt_template = """
        Given this text input, provide a JSON that returns all relevant information. Ensure it is formatted as a proper resume, excluding irrelevant details.
        Here is the Resume's raw text: {information}
        Begin.
    """

    prompt_template = PromptTemplate(
        input_variables=['information'],
        template=JSONIFY_prompt_template
    )

    llm = ChatOpenAI(model="gpt-4-turbo", temperature=0.0, openai_api_key=os.getenv('OPENAI_API_KEY'))
    chain = LLMChain(llm=llm, prompt=prompt_template, verbose=True)
    result = chain.invoke({"information": text})

    # Since we want to return a dictionary, ensure result's text is correctly formatted JSON, then parse it.
    try:
        # Parse JSON directly to a dictionary
        print(result.get("text"))
        return json.loads(result.get("text", "{}"))
    except json.JSONDecodeError as e:
        # Return an error message within a dictionary if JSON decoding fails
        return {"error": "Failed to decode JSON", "details": str(e), "raw_output": result.get("text")}

# Example usage of the function within a Streamlit application or another context
