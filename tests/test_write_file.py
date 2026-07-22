"""Tests for functions.write_file."""

import os

from functions.write_file import write_file


class TestWriteFileSuccess:
    """Happy-path tests for writing file contents."""

    def test_write_new_file_creates_it(self, working_dir):
        """Writing to a new file path should create the file."""
        result = write_file(working_dir, "new_file.txt", "hello world")
        assert "Successfully wrote" in result

        created = os.path.join(working_dir, "new_file.txt")
        assert os.path.isfile(created)
        with open(created, encoding="utf-8") as f:
            assert f.read() == "hello world"

    def test_write_existing_file_overwrites_content(self, working_dir):
        """Writing to an existing file should overwrite its content."""
        result = write_file(working_dir, "notes.txt", "overwritten content")
        assert "Successfully wrote" in result

        with open(os.path.join(working_dir, "notes.txt"), encoding="utf-8") as f:
            assert f.read() == "overwritten content"

    def test_write_creates_missing_parent_directories(self, working_dir):
        """Writing to a deeply nested path should auto-create parent dirs."""
        result = write_file(working_dir, "a/b/c/deep.txt", "deep content")
        assert "Successfully wrote" in result

        created = os.path.join(working_dir, "a", "b", "c", "deep.txt")
        assert os.path.isfile(created)

    def test_result_includes_character_count(self, working_dir):
        """The success message should report the number of characters written."""
        content = "twelve chars"
        result = write_file(working_dir, "counted.txt", content)
        assert str(len(content)) in result


class TestWriteFileErrors:
    """Error-handling tests for invalid write operations."""

    def test_path_outside_working_dir_returns_error(self, working_dir):
        """Paths outside the working directory should be rejected."""
        result = write_file(working_dir, "/tmp/escape.txt", "bad")
        assert "Error" in result
        assert "outside" in result

    def test_traversal_attack_returns_error(self, working_dir):
        """Parent-directory traversal should be rejected."""
        result = write_file(working_dir, "../../escape.txt", "bad")
        assert "Error" in result

    def test_write_to_directory_returns_error(self, working_dir):
        """Writing to a path that is already a directory should fail."""
        result = write_file(working_dir, "sub", "bad")
        assert "Error" in result
        assert "directory" in result
