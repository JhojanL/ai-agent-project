from functions.get_files_info import get_files_info

if __name__ == "__main__":
    # Test 1: Valid directory within working directory
    print(get_files_info("calculator", "."))
    
    # Test 2: Absolute path external to working directory
    print(get_files_info("calculator", "/bin"))
    
    # Test 3: Path attempting to escape via parent directory directory
    print(get_files_info("calculator", "../"))
    
    # Test 4: Path pointing to a file instead of a directory
    print(get_files_info("calculator", "main.py"))