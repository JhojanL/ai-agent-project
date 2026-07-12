import os

def write_file(working_directory: str, file_path: str, content: str) -> str:
    """
    Validates the target path, ensures parent directories exist, 
    and writes content to the specified file safely.
    """
    try:
        abs_working_dir = os.path.abspath(working_directory)
        target_path = os.path.normpath(os.path.join(abs_working_dir, file_path))
        
        # Path validation
        if os.path.commonpath([abs_working_dir, target_path]) != abs_working_dir:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
            
        if os.path.isdir(target_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
            
        # Ensure parent directory structure exists
        parent_dir = os.path.dirname(target_path)
        os.makedirs(parent_dir, exist_ok=True)
        
        # Write content to the file
        with open(target_path, "w", encoding="utf-8") as f:
            f.write(content)
            
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        
    except Exception as e:
        return f"Error writing file: {e}"