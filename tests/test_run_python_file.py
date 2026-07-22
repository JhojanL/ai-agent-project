"""Tests for functions.run_python_file."""

from functions.run_python_file import run_python_file


class TestRunPythonFileSuccess:
    """Happy-path tests for executing Python scripts."""

    def test_run_simple_script_returns_stdout(self, working_dir):
        """Running a valid Python script should capture its stdout."""
        result = run_python_file(working_dir, "hello.py")
        assert "hello world" in result

    def test_run_script_with_args_passes_arguments(self, working_dir):
        """Arguments should be forwarded to the executed script."""
        result = run_python_file(working_dir, "args_echo.py", ["foo", "bar"])
        assert "foo" in result
        assert "bar" in result

    def test_run_nested_script_returns_output(self, working_dir):
        """Scripts in subdirectories should be runnable via relative path."""
        result = run_python_file(working_dir, "sub/nested.py")
        assert "nested" in result

    def test_run_failing_script_returns_stderr(self, working_dir):
        """A script that raises an exception should return stderr output."""
        result = run_python_file(working_dir, "error_script.py")
        assert "RuntimeError" in result or "boom" in result


class TestRunPythonFileErrors:
    """Error-handling tests for invalid execution attempts."""

    def test_path_outside_working_dir_returns_error(self, working_dir):
        """Scripts outside the working directory should be rejected."""
        result = run_python_file(working_dir, "../main.py")
        assert "Error" in result
        assert "outside" in result

    def test_nonexistent_file_returns_error(self, working_dir):
        """Attempting to run a missing file should return an error."""
        result = run_python_file(working_dir, "nonexistent.py")
        assert "Error" in result

    def test_non_python_file_returns_error(self, working_dir):
        """Attempting to run a non-.py file should return an error."""
        result = run_python_file(working_dir, "notes.txt")
        assert "Error" in result
        assert "not a Python file" in result

    def test_directory_as_file_returns_error(self, working_dir):
        """Passing a directory instead of a file should return an error."""
        result = run_python_file(working_dir, "sub")
        assert "Error" in result
