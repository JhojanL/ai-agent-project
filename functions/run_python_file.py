import os
import subprocess

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    """
    Validates the file path, ensures it is within the working directory,
    and executes the Python file with optional arguments, returning its output.
    """
    try:
        # Resolve working directory to an absolute path
        abs_working_dir = os.path.abspath(working_directory)
        # Resolve file path relative to working directory to an absolute path
        absolute_file_path = os.path.abspath(os.path.join(abs_working_dir, file_path))
        
        # Path validation: check if file_path is outside working_directory
        if os.path.commonpath([abs_working_dir, absolute_file_path]) != abs_working_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
            
        # Check if exists and is a regular file
        if not os.path.isfile(absolute_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
            
        # Check if ends with .py
        if not absolute_file_path.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file'
            
        # Build command list
        command = ["python", absolute_file_path]
        if args is not None:
            command.extend(args)
            
        # Run subprocess
        result = subprocess.run(
            command,
            cwd=abs_working_dir,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        output_parts = []
        if result.returncode != 0:
            output_parts.append(f"Process exited with code {result.returncode}")
            
        if not result.stdout and not result.stderr:
            output_parts.append("No output produced")
        else:
            if result.stdout:
                output_parts.append(f"STDOUT:\n{result.stdout}")
            if result.stderr:
                output_parts.append(f"STDERR:\n{result.stderr}")
                
        return "\n".join(output_parts)
        
    except Exception as e:
        return f"Error: executing Python file: {e}"

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Executes a specified Python file relative to the working directory with optional arguments, returning its output",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "File path to the Python file to execute, relative to the working directory",
                },
                "args": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Optional list of arguments to pass to the Python file",
                },
            },
            "required": ["file_path"]
        },
    },
}