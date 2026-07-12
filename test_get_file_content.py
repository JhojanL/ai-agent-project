from functions.get_file_content import get_file_content

if __name__ == "__main__":
    # Test 1: lorem.txt (Truncation check)
    result = get_file_content("calculator", "lorem.txt")
    print(f"lorem.txt length: {len(result)}")
    print(f"lorem.txt truncated: {'truncated' in result}")
    print()

    # Test 2: main.py
    print("get_file_content('calculator', 'main.py'):")
    print(get_file_content("calculator", "main.py"))
    print()

    # Test 3: pkg/calculator.py
    print("get_file_content('calculator', 'pkg/calculator.py'):")
    print(get_file_content("calculator", "pkg/calculator.py"))
    print()

    # Test 4: /bin/cat (Outside directory error)
    print("get_file_content('calculator', '/bin/cat'):")
    print(get_file_content("calculator", "/bin/cat"))
    print()

    # Test 5: pkg/does_not_exist.py (Missing file error)
    print("get_file_content('calculator', 'pkg/does_not_exist.py'):")
    print(get_file_content("calculator", "pkg/does_not_exist.py"))