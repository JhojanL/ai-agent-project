from functions.get_files_info import get_files_info

def print_formatted_result(result: str, indent_spaces: int):
    """Helper function to match the assignment's exact indentation layout."""
    for line in result.splitlines():
        print(" " * indent_spaces + line)

if __name__ == "__main__":
    # Test 1: Current directory ('.')
    print('get_files_info("calculator", "."):')
    print('Result for current directory:')
    print_formatted_result(get_files_info("calculator", "."), indent_spaces=2)
    print()

    # Test 2: Subdirectory ('pkg')
    print('get_files_info("calculator", "pkg"):')
    print("Result for 'pkg' directory:")
    print_formatted_result(get_files_info("calculator", "pkg"), indent_spaces=2)
    print()

    # Test 3: Outside working directory ('/bin')
    print('get_files_info("calculator", "/bin"):')
    print("Result for '/bin' directory:")
    print_formatted_result(get_files_info("calculator", "/bin"), indent_spaces=4)
    print()

    # Test 4: Escape attempt ('../')
    print('get_files_info("calculator", "../"):')
    print("Result for '../' directory:")
    print_formatted_result(get_files_info("calculator", "../"), indent_spaces=4)