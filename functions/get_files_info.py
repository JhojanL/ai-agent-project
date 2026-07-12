import os

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        abs_working_dir = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(abs_working_dir, directory))
        
        # Path validation
        if os.path.commonpath([abs_working_dir, target_dir]) != abs_working_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
            
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'
            
        # Explicit type hinting with accurate variable naming
        files_info: list[str] = []
        for item in os.listdir(target_dir):
            item_path = os.path.join(target_dir, item)
            is_dir = os.path.isdir(item_path)
            file_size = os.path.getsize(item_path)
            files_info.append(
                f"- {item}: file_size={file_size} bytes, is_dir={is_dir}"
            )
            
        return "\n".join(files_info)
        
    except Exception as e:
        # Contextual error description
        return f"Error listing files: {e}"