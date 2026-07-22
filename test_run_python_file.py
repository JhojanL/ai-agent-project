from functions.run_python_file import run_python_file


def test() -> None:
    # Test 1: run_python_file("calculator", "main.py") (should print the calculator's usage instructions)
    print('run_python_file("calculator", "main.py"):')
    print(run_python_file("calculator", "main.py"))
    print("-" * 40)

    # Test 2: run_python_file("calculator", "main.py", ["3 + 5"]) (should run the calculator... which gives a kinda nasty rendered result)
    print('run_python_file("calculator", "main.py", ["3 + 5"]):')
    print(run_python_file("calculator", "main.py", ["3 + 5"]))
    print("-" * 40)

    # Test 3: run_python_file("calculator", "tests.py") (should run the calculator's tests successfully)
    print('run_python_file("calculator", "tests.py"):')
    print(run_python_file("calculator", "tests.py"))
    print("-" * 40)

    # Test 4: run_python_file("calculator", "../main.py") (this should return an error)
    print('run_python_file("calculator", "../main.py"):')
    print(run_python_file("calculator", "../main.py"))
    print("-" * 40)

    # Test 5: run_python_file("calculator", "nonexistent.py") (this should return an error)
    print('run_python_file("calculator", "nonexistent.py"):')
    print(run_python_file("calculator", "nonexistent.py"))
    print("-" * 40)

    # Test 6: run_python_file("calculator", "lorem.txt") (this should return an error)
    print('run_python_file("calculator", "lorem.txt"):')
    print(run_python_file("calculator", "lorem.txt"))
    print("-" * 40)


if __name__ == "__main__":
    test()
