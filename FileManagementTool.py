
from langchain_community.agent_toolkits import FileManagem entToolkit
from langchain.tools import tool

# Initialize the FileManagementToolkit with the root directory
toolkit = FileManagementToolkit(
    root_dir='C:\\Users\\bgome\\OneDrive\Desktop\\Senior Year 2nd Semester\\499 - Capstone\\LangChain\\GenAIAssistant\\rootFileSystem',
    selected_tools=["read_file", "write_file", "list_directory"]
)

# Get a list of available tools in a form of a array 
tools = toolkit.get_tools()

@tool
def FileTool(input_dict: dict):
    """
    This function handles file operations.  

    Args:
        input_dict: A dictionary containing the action and parameters.
            Example: {"action": "write", "file_path": "example.txt", "text": "hello world"}
        
    """
    print(dict)

    FileAction = input_dict.get("action")
    File_path = input_dict.get("file_path")
    Text = input_dict.get("text")

        
    # Printing the variables to verify
    print("FileAction:", FileAction)
    print("File_path:", File_path)
    print("Text:", Text)
  
  

    if FileAction == "write":
        print("Write Function")
        write_tool = tools[1]  # Assuming 'write_file' is the second too
        res = write_tool.invoke({"file_path": File_path, "text": Text})
        print(res)
        return res
    elif FileAction == "read":
        print("Hello read")
        read_tool = tools[0]
        res = read_tool.invoke({"file_path": File_path})
        print("RESULT: " + res)
        return res
    elif FileAction == "list":
        print("List Function")
        list_tool = tools[2]
        res = list_tool.invoke({})
  






