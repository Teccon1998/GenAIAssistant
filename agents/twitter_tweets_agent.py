from langchain_community.document_loaders import TwitterTweetLoader
from langchain.tools import tool
from langchain.tools.retriever import create_retriever_tool
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain import hub
from langchain.agents import create_openai_functions_agent
from langchain.agents import AgentExecutor
import os


@tool
def get_tweets(text: str):
    """Searches through Twitter and returns their username,tweets and hashtags"""
    loader = TwitterTweetLoader.from_bearer_token(
        oauth2_bearer_token=os.environ["Bearer_Token"],
        twitter_users=[f"{text}"],
        number_tweets=10,  # Default value is 100
    )
    docs = loader.load()

    print(docs)

    # documents = RecursiveCharacterTextSplitter(
    #     chunk_size=1000, chunk_overlap=200
    # ).split_documents(docs)
    # vector = FAISS.from_documents(documents, OpenAIEmbeddings())
    # retriever = vector.as_retriever()
    #
    # retriever_tool = create_retriever_tool(retriever, "twitter_hashtags", "Grab twitter hashtags from a certain set "
    #                                                                       "of tweets")
    #
    # tools = [retriever_tool]
    #
    # llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    #
    # prompt = hub.pull("elijuwon/interest_generator")
    #
    # agent = create_openai_functions_agent(llm, tools, prompt)
    #
    # agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    #
    # result = agent_executor.invoke({"input": f"{docs}"})
    #
    # print(result)
    # return result
