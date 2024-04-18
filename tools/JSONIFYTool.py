import fitz
import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain


def extract_text_from_pdf(pdf_file):
    """Function to extract text from a PDF file."""
    doc = fitz.open("pdf", pdf_file.read())
    text = ""
    
    for page in doc:
        text += page.get_text()
    doc.close()
    
    return text


def pdf_to_json(pdfFile)->str:
    extractedText = extract_text_from_pdf(pdfFile)
    JSONIFY_prompt_template = """Given this text input, give a JSON that returns all relevant info, 
    be sure to make it looks like a proper resume in JSON format and exclude no information unless it is completely irrelevant to the resume itself.
    
    Here is the Resume's raw text: {information}
    
    Begin."""
    
    
    prompt_template=PromptTemplate(
        input_variables=['information'],template = JSONIFY_prompt_template
    )
    
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.2,openai_api_key=os.environ['OPENAI_API_KEY'])
    chain = LLMChain(llm = llm,prompt=prompt_template,verbose=True)
    result=chain.invoke({"information":extractedText})
    return result
    
    
    
    
    