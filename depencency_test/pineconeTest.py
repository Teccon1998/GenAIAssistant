#Test if the pinecone database is working properly

import os

from dotenv import find_dotenv, load_dotenv #imports to allow us to find and load enviroment variables

from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_openai import OpenAI
from pinecone import Pinecone
from langchain_community.vectorstores import Pinecone as PineconeStore
from langchain.chains import RetrievalQA
load_dotenv()
load_dotenv(find_dotenv())

#initialize vector database
Pinecone(api_key=os.environ.get('PINECONE_API_KEY'))

if __name__ == '__main__':

    #Load in the text document
    print("Vector Store")
    #Users must change Textloader to their respective File paths
    loader=TextLoader("/Users/mafon/Desktop/GenAIAssistant/depencency_test/TestFiles/mediumblog1.txt",encoding="utf8")
    document=loader.load()

    #split the texts into its specific czhunks
    text_splitter=CharacterTextSplitter(chunk_size=50,chunk_overlap=0)
    text = text_splitter.split_documents(document)
    #print(len(text))
    #print(document)

    #Initiate the Embeddings
    embeddings = OpenAIEmbeddings()
    #PineCode: Vector Databse
    docsearch = PineconeStore.from_documents(text,embeddings,index_name="medium-blogs-embedding-index") #convert text into vectors

    #Initiate LLM chain and give it a prompt
    qa=RetrievalQA.from_chain_type(llm=OpenAI(), chain_type='stuff', retriever=docsearch.as_retriever())
    query="What is a vector data base? Give me a 15 word answer for a beginner"
    result=qa({"query":query})
    print(result)