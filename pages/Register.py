import streamlit as st
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
from tools import JSONIFYTool

load_dotenv()


def connect_with_server(username, password):
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
        "password": password
    }

    # Query for the specified username and password
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
    st.text("Username:")
    username = st.text_input("Enter Username")
    st.text("Password:")
    password = st.text_input("Enter Password")
    register = st.form_submit_button("Register")
    
    
    ##TODO: Add DOCX and TXT
    ##TODO: make this a part of a mongo user profile: Elijuwon task.
    fileUpload = st.file_uploader("Upload your file:",type="pdf")

    if fileUpload:
        res = JSONIFYTool.pdf_to_json(fileUpload)
        print(res.get("text"))
        st.write(res.get("text"))
    if register:
        connect_with_server(username, password)
