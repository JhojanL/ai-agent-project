# AI Coding Agent

A command-line AI agent that interprets natural language prompts and autonomously executes local file-system operations — reading, writing, listing, and running Python files — through an iterative tool-calling loop powered by an LLM.

## Motivation

This project implements a **ReAct-style agentic loop** where a language model decides which tools to invoke, the system executes them locally, and the results are fed back to the model until the task is complete. It demonstrates the core pattern behind modern AI coding assistants: separating *reasoning* (the LLM) from *action* (sandboxed local functions).

### Key Concepts

- **Tool-use / Function-calling** — the LLM receives JSON schemas describing available tools and returns structured calls instead of free-form text.
- **Agentic loop** — the conversation continues in a loop (up to a configurable iteration limit) until the model produces a final text response with no further tool calls.
- **Sandboxed execution** — all file operations are restricted to a configurable working directory, preventing path-traversal attacks.

> [!WARNING]
> **Security Disclaimer:** This repository serves as an experimental reference implementation and proof-of-concept (PoC) designed strictly for educational purposes.
> 
> The integrated toolset grants the language model the capability to execute Python scripts locally via subprocesses. Because the current environment does not employ virtualization or containerized isolation (such as Docker), the agent operates directly on the host operating system. Consequently, untrusted inputs, unexpected model evaluations, or prompt injection vulnerabilities could result in unintended file system mutations or code execution.
> 
> **This implementation is not intended for production environments, nor should it be executed on systems with access to sensitive directories, private networks, or privileged API keys.**

## Quick Start

### Prerequisites

- **Python** ≥ 3.14
- **[uv](https://docs.astral.sh/uv/)** — fast Python package manager

### Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/<your-username>/ai-agent-project.git
   cd ai-agent-project
   ```

2. **Install dependencies**

   ```bash
   uv sync
   ```

3. **Create an `.env` file** in the project root with your API key:

   ```env
   OPENROUTER_API_KEY='your-openrouter-key'
   ```

   > The `.env` file is already included in `.gitignore` and will not be committed.

4. **Run a quick command**

   ```bash
   uv run main.py "what files are in the root?"
   ```

## Usage

```bash
uv run main.py "<prompt>" [--verbose]
```

### CLI Flags

| Flag        | Description                                        |
| ----------- | -------------------------------------------------- |
| `--verbose` | Prints token usage, function calls, and results    |

### Examples

```bash
# List files in the working directory
uv run main.py "what files are in the root?"

# Read a file
uv run main.py "get the contents of lorem.txt" --verbose

# Run the test suite
uv run main.py "run tests.py" --verbose

# Create a new file
uv run main.py "create a new README.md file with the contents '# calculator'"
```

## How It Works

1. **The user provides a natural language prompt** via the CLI.
2. **The LLM receives the prompt** along with JSON schemas for the four available tools.
3. **The model returns one or more tool calls** — each specifying a function name and arguments.
4. **`call_function` dispatches each call** — it resolves the function name from a registry, injects the sandboxed `working_directory`, and executes the function.
5. **The tool result is appended to the conversation** as a `tool` message, and the loop continues.
6. **When the model has enough context**, it returns a final text response and the loop terminates.

```
User Prompt ──▶ LLM ──▶ Tool Call(s) ──▶ Local Execution ──▶ Result ──▶ LLM ──▶ ... ──▶ Final Response
```

## Project Structure

```
ai-agent-project/
├── main.py              # Entry point — CLI parsing and agent loop
├── call_function.py     # Function registry and dynamic dispatch
├── prompts.py           # System prompt engineering
├── config.py            # Runtime constants (iteration limit, char cap, working dir)
├── functions/           # Tool implementations (one per file)
│   ├── get_files_info.py    # List directory contents with metadata
│   ├── get_file_content.py  # Read file contents (with truncation)
│   ├── run_python_file.py   # Execute a Python script in a subprocess
│   └── write_file.py        # Write or overwrite a file
├── calculator/          # Sample project the agent operates on
│   ├── main.py
│   ├── tests.py
│   ├── lorem.txt
│   └── pkg/
│       ├── calculator.py
│       └── render.py
├── tests/               # Pytest test suite
│   ├── conftest.py          # Shared fixtures (tmp working dir)
│   ├── test_get_file_content.py
│   ├── test_get_files_info.py
│   ├── test_run_python_file.py
│   └── test_write_file.py
└── test_*.py            # Legacy manual test scripts
```

## Available Tools

| Tool               | Description                                                     |
| ------------------ | --------------------------------------------------------------- |
| `get_files_info`   | Lists files in a directory with size and type metadata           |
| `get_file_content` | Reads a file's contents (truncated at 10 000 characters)        |
| `run_python_file`  | Executes a Python file with optional CLI arguments (30s timeout) |
| `write_file`       | Writes text content to a file, creating parent directories       |

All tools enforce path validation — any path that resolves outside the configured working directory is rejected.

## Configuration

Runtime constants are centralized in `config.py`:

| Constant      | Default          | Purpose                                         |
| ------------- | ---------------- | ----------------------------------------------- |
| `WORKING_DIR` | `./calculator`   | Sandboxed directory for all file operations      |
| `MAX_CHARS`   | `10000`          | Character limit when reading file contents       |
| `MAX_ITERS`   | `20`             | Maximum agent loop iterations before termination |

## Dependencies

| Package        | Version | Purpose                               |
| -------------- | ------- | ------------------------------------- |
| `openai`       | 2.44.0  | OpenAI-compatible API client          |
| `python-dotenv`| 1.1.0   | Load environment variables from `.env`|

## Contributing

Contributions are welcome! To contribute to this project:

1. **Fork and Clone** the repository.
2. **Create a Feature Branch**: `git checkout -b feature/my-new-feature`
3. **Run Tests**: Ensure all unit tests pass before submitting changes:
   ```bash
   uv run python -m pytest tests/ -v
   ```
4. **Check Formatting & Linting**: Run `ruff` to ensure code quality:
   ```bash
   uvx ruff format --check .
   uvx ruff check .
   ```
5. **Submit a Pull Request**: Push your branch and open a PR against `main`.

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.
