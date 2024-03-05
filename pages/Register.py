import streamlit as st
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


def connect_with_server(username, password):
    # Send a ping to confirm a successful connection
    uri = "mongodb+srv://elijuwonjmitchell:Abaiba%4012@cluster0.59qhs8a.mongodb.net/?retryWrites=true&w=majority"

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

    try:
        # Insert data into the collection
        result = collection.insert_one(data_to_insert)
        print("Inserted document ID:", result.inserted_id)
    except Exception as e:
        print("Error inserting data:", e)
    finally:
        # Close the MongoDB connection
        client.close()


st.title("Register")

with st.form("my_form", clear_on_submit=True):
    st.text("Username:")
    username = st.text_input("Enter Username")
    st.text("Password:")
    password = st.text_input("Enter Password")
    login = st.form_submit_button("Register")
    if login:
        connect_with_server(username, password)
