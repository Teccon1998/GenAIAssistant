#Run this file to test that you have LangChain and Open AI installed

from langchain_openai import OpenAI
from dotenv import load_dotenv,find_dotenv #Find and Load Enviroment Variables

load_dotenv(find_dotenv())

def generate_pet_name():
    llm=OpenAI(temperature=0.7)
    name=llm("Suggest me 5 Cool Names")
    return name

if __name__ == "__main__":
    print(generate_pet_name())