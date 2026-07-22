"""Shared fixtures for all tool function tests."""

import pytest


@pytest.fixture()
def working_dir(tmp_path):
    """Create a temporary working directory with sample files for testing.

    Layout:
        tmp_path/
        ├── hello.py        -> print("hello world")
        ├── error_script.py -> raise RuntimeError("boom")
        ├── args_echo.py    -> prints sys.argv[1:]
        ├── notes.txt       -> "some notes"
        ├── big_file.txt    -> 15 000 'x' characters (for truncation tests)
        └── sub/
            └── nested.py   -> print("nested")
    """
    # Simple Python scripts
    (tmp_path / "hello.py").write_text('print("hello world")\n', encoding="utf-8")

    (tmp_path / "error_script.py").write_text(
        'raise RuntimeError("boom")\n', encoding="utf-8"
    )

    (tmp_path / "args_echo.py").write_text(
        "import sys\nprint(sys.argv[1:])\n", encoding="utf-8"
    )

    # Plain text files
    (tmp_path / "notes.txt").write_text("some notes", encoding="utf-8")

    # Large file for truncation testing (exceeds MAX_CHARS = 10 000)
    (tmp_path / "big_file.txt").write_text("x" * 15_000, encoding="utf-8")

    # Nested directory
    sub = tmp_path / "sub"
    sub.mkdir()
    (sub / "nested.py").write_text('print("nested")\n', encoding="utf-8")

    return str(tmp_path)
