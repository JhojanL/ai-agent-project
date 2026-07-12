from functions.write_file import write_file

def test() -> None:
    # Test 1: Overwriting an existing file
    print('write_file("calculator", "lorem.txt", ...):')
    print(write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"))
    print()

    # Test 2: Writing to a file within a missing nested directory
    print('write_file("calculator", "pkg/morelorem.txt", ...):')
    print(write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))
    print()

    # Test 3: Attempting to write outside the working directory
    print('write_file("calculator", "/tmp/temp.txt", ...):')
    print(write_file("calculator", "/tmp/temp.txt", "this should not be allowed"))

if __name__ == "__main__":
    test()