import os
from config import MAX_CHARS

def get_file_content(working_directory: str, file_path: str) -> str:
    """
    Validates the file path, ensures it is within the working directory,
    and returns its content up to the maximum character limit.
    """
    try:
        abs_working_dir = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(abs_working_dir, file_path))
        
        # Path validation
        if os.path.commonpath([abs_working_dir, target_path]) != abs_working_dir:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
            
        if not os.path.isfile(target_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
            
        # Read file with character limitation
        with open(target_path, "r", encoding="utf-8") as f:
            content = f.read(MAX_CHARS)
            if f.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                
        return content
        
    except Exception as e:
        return f'Error reading file "{file_path}": {e}'

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": f"Retrieves the content (at most {MAX_CHARS} characters) of a specified file within the working directory",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file to read, relative to the working directory",
                },
            },
            "required": ["file_path"],
        },
    },
}