import os
from langchain.document_loaders import UnstructuredFileLoader
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain

def file_to_json(file_path) -> str:
    # Load the file using UnstructuredFileLoader
    loader = UnstructuredFileLoader(file_path)
    documents = loader.load()
    text = " ".join([doc.page_content for doc in documents])

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
    return result

# Example usage
file_path = "C:\\Users\\bgome\\OneDrive\\Documents\\My Resume\\Bryan Gomez Resume .docx"
json_output = file_to_json(file_path)
print(json_output.get("text"))