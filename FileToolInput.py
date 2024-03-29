
from typing import Dict, Optional
from langchain.tools import BaseTool
from openai import BaseModel
from pydantic import Field, validator

class FileToolInput(BaseModel):
    action: str = Field(..., description="The action to perform (write, read, list)")
    file_path: Optional[str] = Field(None, description="The file path for read/write actions")
    text: Optional[str] = Field(None, description="The text to write for the write action")

    @validator('action', 'file_path', 'text', pre=True)
    def validate_input(cls, values):
        action = values.get("action")
        file_path = values.get("file_path")
        text = values.get("text")

        if action == "write" and (file_path is None or text is None):
            raise ValueError("file_path and text are required for write action")
        elif action == "read" and file_path is None:
            raise ValueError("file_path is required for read action")
        return values