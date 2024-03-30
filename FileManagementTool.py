
from langchain_community.agent_toolkits import FileManagementToolkit
import json
from langchain.tools import BaseTool
from langchain_core.tools import ToolException

class FileTool(BaseTool):
    name = "file_tool"
    description = """This tool performs file operations like read, write, and list directory contents. 
                     The input should be a dict in the format: '<action> <file_path>' for read and <action> <file_path> <content> for write actions, or just '<action>' for the list action. 
                     Allowed actions are 'read', 'write', and 'list'. For example: {"action": "read", "file_path": "example.txt"'}  or {"action": "write", "file_path": "example2.txt", "text": "hello world"'}."

                     This tool would output if the action wa sucessfull or not
                """

    # Initialize the FileManagementToolkit with the root directory
    toolkit = FileManagementToolkit(
        root_dir='C:\\Users\\bgome\\OneDrive\\Desktop\\Senior Year 2nd Semester\\499 - Capstone\\LangChain\\GenAIAssistant\\rootFileSystem', #fix hard coded path 
        selected_tools=["read_file", "write_file", "list_directory","copy_file"]
    )
    # Get a list of available tools in a form of a array 
    tools = toolkit.get_tools()

    #The main function of the class 
    def _run(self, input_dir:dict):
        """This is a tool that uses ToolkitManagement Tools to perform file actions"""
    
        #This takes the JSON formatted string passed by the Agent anf turns it into a dictionary ex) {"action": "read", "file_path": "example.txt"'}
        dic = json.loads(input_dir)
        ACTIONS = ["read", "Write", "List"]

        if 'action' in dic:
            # using key values of the dictionary to assign the file action to be performed 
            action = dic['action']
        else:
            # {', '.join(ACTIONS)}-> .join is a string function that takes a iterable and concats them together, the string that appears before join behaves as the seperator
            # This error does not stop the agent, but gives it a message with helpful information (list of ACTIONS) and allows it a chance to correct itself
            raise ToolException(f"Invalid action: {action}. Allowed actions are: {', '.join(ACTIONS)}")

        if action == "write": 
            # Write action requires a target file and text to be written into, if neither exist then throw an error
            if 'file_path' in dic:
                file_path = dic['file_path']
                print("File_path:", file_path)
            else:
                 # error reminnds the agent of the neccesary parameters for this action 
                 raise ToolException("For the 'write' action, 'file_path' is required")
            if 'text' in dic:
                text = dic['text']
                print("Text:", text)
            else: 
                 # error reminds the agent of the neccesary parameters for this action 
                 raise ToolException("For the 'write' action, 'text' is required")
            
            write_tool = self.tools[1] # selects the write tool 
            res = write_tool.invoke({"file_path": file_path, "text": text})
            print(res)
            return res
        elif action == "read":
            if 'file_path' in dic:
                file_path = dic['file_path']
                print("File_path:", file_path)
            else: 
                # error reminds the agent of the neccesary parameters for this action 
                raise ToolException("For the 'write' action, 'file_path' is required")
            read_tool = self.tools[0] # selects the read tool 
            res = read_tool.invoke({"file_path": file_path})
            print("RESULT: " + res)
            return res
        elif action == "list":
            print("List Function")
            list_tool = self.tools[2] # selects the list tool 
            res = list_tool.invoke({})
            return res
        


   






