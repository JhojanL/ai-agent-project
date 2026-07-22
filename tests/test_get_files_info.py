"""Tests for functions.get_files_info."""


from functions.get_files_info import get_files_info


class TestGetFilesInfoSuccess:
    """Happy-path tests for listing directory contents."""

    def test_list_root_directory_returns_all_entries(self, working_dir):
        """Listing '.' should return info for every item in the working dir."""
        result = get_files_info(working_dir, ".")
        # The fixture creates: hello.py, error_script.py, args_echo.py,
        #                       notes.txt, big_file.txt, sub/
        assert "hello.py" in result
        assert "notes.txt" in result
        assert "sub" in result

    def test_list_subdirectory_returns_nested_files(self, working_dir):
        """Listing a subdirectory should return its contents."""
        result = get_files_info(working_dir, "sub")
        assert "nested.py" in result

    def test_output_contains_file_size(self, working_dir):
        """Each entry should include a file_size field."""
        result = get_files_info(working_dir, ".")
        assert "file_size=" in result

    def test_output_contains_is_dir_flag(self, working_dir):
        """Each entry should include an is_dir field."""
        result = get_files_info(working_dir, ".")
        assert "is_dir=True" in result  # sub/ directory
        assert "is_dir=False" in result  # regular files

    def test_default_directory_is_working_dir(self, working_dir):
        """Calling without a directory argument should default to '.'."""
        result = get_files_info(working_dir)
        assert "hello.py" in result


class TestGetFilesInfoErrors:
    """Error-handling tests for invalid directory paths."""

    def test_path_outside_working_dir_returns_error(self, working_dir):
        """Absolute paths outside the working directory should be rejected."""
        result = get_files_info(working_dir, "/bin")
        assert "Error" in result
        assert "outside" in result

    def test_traversal_attack_returns_error(self, working_dir):
        """Parent-directory traversal should be rejected."""
        result = get_files_info(working_dir, "../")
        assert "Error" in result

    def test_nonexistent_directory_returns_error(self, working_dir):
        """A path that does not exist should return an error."""
        result = get_files_info(working_dir, "no_such_dir")
        assert "Error" in result

    def test_file_as_directory_returns_error(self, working_dir):
        """Passing a regular file instead of a directory should return an error."""
        result = get_files_info(working_dir, "notes.txt")
        assert "Error" in result
