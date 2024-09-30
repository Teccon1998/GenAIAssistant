import streamlit as st
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
import certifi

# Load environment variables
load_dotenv()

# Ensure session state keys are initialized at the start
if "username" not in st.session_state:
    st.session_state["username"] = "Anonymous"  # Default value or a login function
if "linkedInLink" not in st.session_state:
    st.session_state["linkedInLink"] = "#"

def connect_with_server(username, password, firstName, lastName, link):
    # Used to connect with the MongoDB
    uri = os.environ.get('URI_FOR_Mongo')  # Load MongoDB URI from the environment
    #tlsCAFile = os.getenv('tlsCAFile')  # Load tlsCAFile from the environment
    tlsCAFile = certifi.where()

    # Check if tlsCAFile is loaded correctly
    if not tlsCAFile:
        raise ValueError("tlsCAFile is not defined in the environment variables")

    # Create MongoClient object with tlsCAFile
    client = MongoClient(uri, tlsCAFile=tlsCAFile, server_api=ServerApi('1'))

    # Select the database and collection
    database_name = "499"
    collection_name = "login_info"
    db = client[database_name]
    collection = db[collection_name]

    # Data to be inserted
    data_to_insert = {
        "username": username,
        "password": password,
        "firstName": firstName,
        "lastName": lastName,
        "link": link
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

            # Store username and link in session state
            st.session_state['username'] = username
            st.session_state['link'] = link

        except Exception as e:
            st.error(f"Error inserting data: {e}")
        finally:
            # Close the MongoDB connection and switch page
            client.close()
            st.success("Registration successful! Redirecting to chatbot page...")
            st.experimental_rerun()

# Main form for registration
st.title("Register")

with st.form("my_form", clear_on_submit=True):
    st.text("First Name:")
    firstName = st.text_input("Enter first name")
    st.text("Last Name:")
    lastName = st.text_input("Enter last name")
    st.text("Username:")
    username = st.text_input("Enter username")
    st.text("Password:")
    password = st.text_input("Enter password", type="password")
    st.text("LinkedIn Link:")
    link = st.text_input("Please enter your LinkedIn profile page link")

    # Add file upload option
    fileUpload = st.file_uploader("Upload your file:")

    # Submit button for the form
    register = st.form_submit_button("Register")

    # Process the form submission
    if register:
        # Initialize session state keys
        if 'linkedInLink' not in st.session_state:
            st.session_state['linkedInLink'] = link
        if 'username' not in st.session_state:
            st.session_state['username'] = username

        # Handle file upload if any
        if fileUpload is not None:
            bytes_data = fileUpload.getvalue()
            document = {
                'username': username,
                'file_name': fileUpload.name,
                'data': bytes_data,
                'file_type': fileUpload.type
            }

            # MongoDB connection to store the file
            uri = os.getenv('URI_FOR_Mongo')
            #tlsCAFile = os.getenv('tlsCAFile')
            tlsCAFile = certifi.where()
            client = MongoClient(uri, tlsCAFile=tlsCAFile, server_api=ServerApi('1'))

            db = client['499']
            collection = db['files_uploaded']
            collection.insert_one(document)
            client.close()

        # Call the connect_with_server function to store the user data
        connect_with_server(username, password, firstName, lastName, link)
