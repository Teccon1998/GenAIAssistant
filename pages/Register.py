import streamlit as st
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from tools import JSONIFYTool

load_dotenv()


# Ensure session state keys are initialized at the start
if "username" not in st.session_state:
    st.session_state["username"] = "Anonymous"  # Default value or a login function
if "linkedInLink" not in st.session_state:
    st.session_state["linkedInLink"] = "#"


def connect_with_server(username, password,firstName,lastName,link,jsonObject):
    # Used to connect with the MongoDB
    uri = os.environ.get('URI_FOR_Mongo')

    # Create a new client and connect to the server
    client = MongoClient(uri, tlsCAFile="C:\\Python312\\Lib\\site-packages\\certifi\\cacert.pem",
                         server_api=ServerApi('1'))

    # Select the database and collection
    database_name = "Elijuwon_Database_499"
    collection_name = "login_info"
    db = client[database_name]
    collection = db[collection_name]

    # Data to be inserted
    data_to_insert = {
        "username": username,
        "password": password,
        "firstName":firstName,
        "lastName":lastName,
        "link":link
    }

    # Query for the specified username
    query = {"username": username}
    result = collection.find_one(query)

    # Check if username already exists
    if result:
        st.error("Username already exists")
    else:
        try:
            # Insert data into the collection
            collection.insert_one(data_to_insert)

        except Exception as e:
            st.error("Error inserting data:", e)
        finally:
            # Close the MongoDB connection and switch page
            client.close()
            st.switch_page("pages/chatbot.py")


st.title("Register")

with st.form("my_form", clear_on_submit=True):
    st.text("First Name:")
    firstName = st.text_input("Enter first name")
    st.text("Last Name:")
    lastName = st.text_input("Enter last name")
    st.text("Username:")
    username = st.text_input("Enter username")
    st.text("Password:")
    password = st.text_input("Enter password")
    st.text("LinkedIn Link:")
    link = st.text_input("Please enter your linkedIn profile page link")
    register = st.form_submit_button("Register")
    
    
    ##TODO: Add DOCX and TXT
    ##TODO: make this a part of a mongo user profile: Elijuwon task.
    fileUpload = st.file_uploader("Upload your file:",type="pdf")

    if fileUpload:
        res = JSONIFYTool.pdf_to_json(fileUpload)
        print(res.get("text"))
        st.write(res.get("text"))
    if register:
        # Initialize session state keys
        if 'linkedInLink' not in st.session_state:
            st.session_state['linkedInLink'] = link
        if 'username' not in st.session_state:
            st.session_state['username'] = username

        connect_with_server(username, password, firstName, lastName, link)