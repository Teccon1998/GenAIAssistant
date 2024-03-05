from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import streamlit as st


def check_credentials(username, password):
    # MongoDB connection URI
    uri = "mongodb+srv://elijuwonjmitchell:Abaiba%4012@cluster0.59qhs8a.mongodb.net/?retryWrites=true&w=majority"

    # Create a new client and connect to the server
    client = MongoClient(uri, tlsCAFile="C:\\Python312\\Lib\\site-packages\\certifi\\cacert.pem",
                         server_api=ServerApi('1'))

    # Select the database and collection
    database_name = "Elijuwon_Database_499"
    collection_name = "login_info"
    db = client[database_name]
    collection = db[collection_name]

    # Query for the specified username and password
    query = {"username": username, "password": password}
    result = collection.find_one(query)

    # Check if the result is not None (credentials exist)
    if result:
        st.switch_page("pages/chatbox.py")
    else:
        st.error("Incorrect username or password!")

    # Close the MongoDB connection
    client.close()


st.title("Login")
st.sidebar.page_link("Login.py", label="Log In")
st.sidebar.page_link("pages/Register.py", label="Register")

with st.form("my_form", clear_on_submit=True):
    st.text("Username:")
    username = st.text_input("Enter Username")
    st.text("Password:")
    password = st.text_input("Enter Password")
    login = st.form_submit_button("Log In")
    if login:
        check_credentials(username, password)
