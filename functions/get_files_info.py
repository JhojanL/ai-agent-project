import os

def get_files_info(working_directory: str, directory: str = ".") -> str:
    """
    Validates if the target directory is within the permitted working directory
    and ensures it exists.
    """
    try:
        # Get the absolute path of the working directory
        working_dir_abs = os.path.abspath(working_directory)
        
        # Safely combine and normalize the paths
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
        
        # Verify the target directory does not escape the working directory
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        
        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
            
        # Verify that the path is an actual directory
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'
            
        return f'Success: "{directory}" is within the working directory'
        
    except Exception as e:
        return f"Error: {str(e)}"