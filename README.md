BEMA - The Interactive AI Model

We created BEMA using LLM, Langchain, and OpenAI. It is an interactive chatbot much like ChatGPT. It can also be used for the specific case of writing a resume based on a job link that the user provides. 

1. First clone the repository using git clone

2. Create a python virtual environment:
   
      Create a Python virtual environment for Windows
   
      `python -m venv venv`
       
      Create a Python virtual environment for Mac
   
      `python3 -m venv venv`
       
      Activating Virtual Environment in Python for Windows
   
      `venv\Scripts\activate`
       
      Activating Virtual environment in Python for Mac
   
      `source venv/bin/activate`

4. Once the virtual environment is activated please run this in the terminal command line of the project

   `pip install -r requirements.txt`

5. Finally run the command below to start the project:

   `streamlit run Login.py`

That should take you to this page where you can interact with our application.
<img width="1123" alt="image" src="https://github.com/Teccon1998/GenAIAssistant/assets/43446163/07388579-22e6-4c7c-b2d5-f016de5e4d4d">



Official Technology Stack:

`Front-End:`

Streamlit: Used to create the user interface of the application. It provides an intuitive way to build and deploy the front end of the AI-powered assistant as a web application.

`Back-end/AI:`

LangChain: A Python framework used for developing AI applications. It was employed to manage the interactions between the application and the various APIs, as well as to facilitate the decision-making process of the AI.
OpenAI LLM: Used as the main Large Language Model (LLM) for generating responses and processing user prompts. It provides the core AI capabilities for analyzing resumes and generating personalized feedback.
Data Management:

MongoDB: Used for database management, particularly for storing user data such as resumes and LinkedIn profiles. It ensures that data is securely stored and easily accessible for processing by the AI.
Web Scraping and Data Retrieval:

ProxyCurl API: A tool used to scrape data from LinkedIn profiles and job postings. This API allowed the AI to gather necessary data to tailor resume suggestions accurately.
Tavily Search Engine: Implemented to enable the chatbot to perform general web searches and retrieve relevant information from the internet as part of the data enrichment process.

`Key Components:`

LangChain: Central framework connecting the AI model with external APIs.

OpenAI LLM: Provides the AI's natural language processing and response generation.

Streamlit: Facilitates the front-end user experience.

MongoDB: Handles secure storage and management of user data.

ProxyCurl API: Enables web scraping for LinkedIn data.

Tavily Search Engine: Assists in retrieving additional contextual data from the web.
