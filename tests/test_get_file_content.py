"""Tests for functions.get_file_content."""

from functions.get_file_content import get_file_content


class TestGetFileContentSuccess:
    """Happy-path tests for reading file contents."""

    def test_read_existing_file_returns_content(self, working_dir):
        """Reading an existing text file should return its full content."""
        result = get_file_content(working_dir, "notes.txt")
        assert result == "some notes"

    def test_read_python_file_returns_content(self, working_dir):
        """Reading a .py file should return its source code."""
        result = get_file_content(working_dir, "hello.py")
        assert 'print("hello world")' in result

    def test_read_nested_file_returns_content(self, working_dir):
        """Reading a file in a subdirectory should work with a relative path."""
        result = get_file_content(working_dir, "sub/nested.py")
        assert 'print("nested")' in result

    def test_large_file_is_truncated(self, working_dir):
        """Files exceeding MAX_CHARS should be truncated with a notice."""
        result = get_file_content(working_dir, "big_file.txt")
        assert "truncated" in result
        assert len(result) > 0


class TestGetFileContentErrors:
    """Error-handling tests for invalid paths and missing files."""

    def test_nonexistent_file_returns_error(self, working_dir):
        """Requesting a file that does not exist should return an error string."""
        result = get_file_content(working_dir, "does_not_exist.txt")
        assert "Error" in result

    def test_path_outside_working_dir_returns_error(self, working_dir):
        """Absolute paths outside the working directory should be rejected."""
        result = get_file_content(working_dir, "/etc/passwd")
        assert "Error" in result
        assert "outside" in result

    def test_traversal_attack_returns_error(self, working_dir):
        """Relative paths escaping the working directory should be rejected."""
        result = get_file_content(working_dir, "../../etc/passwd")
        assert "Error" in result

    def test_directory_path_returns_error(self, working_dir):
        """Passing a directory instead of a file should return an error."""
        result = get_file_content(working_dir, "sub")
        assert "Error" in result
