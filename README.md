# CopyClip

A command-line tool that helps you copy multiple code files from a directory to your clipboard. Perfect for sharing code snippets, preparing documentation, and especially useful when working with Large Language Models (LLMs).

## Features

- Copy multiple files to clipboard with a single command
- Smart file filtering with gitignore support
- Hidden files/directories handling
- LLM-friendly output formatting with relative paths
- Verification of clipboard operations
- Fallback to file output if clipboard fails

## Why CopyClip + LLMs?

CopyClip is designed to enhance your workflow with AI coding assistants like ChatGPT, Claude, or GitHub Copilot by:
- Easily sharing entire codebases or specific directories for context
- Maintaining proper file structure and formatting
- Streamlining code reviews and discussions
- Enabling quick context switching in AI conversations
- Preserving folder structure through relative path headers

Each file is concatenated with its relative path as a header, helping AI assistants understand your project's structure:

````

--- File: src/models/user.py ---
class User:
    def __init__(self):
        pass

--- File: src/utils/helpers.py ---
def format_date():
    return "2024-01-01"

--- File: src/main.py ---
from models.user import User
from utils.helpers import format_date
````

This structured format helps AI assistants:
- Understand file relationships and imports
- Provide more contextual code suggestions
- Better grasp your project architecture
- Generate more accurate responses about your codebase

## Installation

````

pip install copyclip
````

## Usage

Basic usage:
````

copyclip /path/to/directory
````

Advanced options:
````

# Ignore specific patterns
copyclip /path/to/directory --ignore "*.js" "*.pyc" "node_modules/*"

# Respect .gitignore patterns
copyclip /path/to/directory --gitignore

# Include hidden files
copyclip /path/to/directory --include-hidden

# Print output to console
copyclip /path/to/directory --print
````

## Arguments

| Argument | Description |
|----------|-------------|
| `path` | Root path of the directory to process |
| `--ignore` | List of regex patterns to ignore files (e.g., *.js, .env, index*) |
| `--gitignore` | Also respect .gitignore patterns |
| `--include-hidden` | Include hidden files and directories (starting with .) |
| `--print` | Print the concatenated output to console |

## Example Output

When you run CopyClip on a project, it generates a formatted output like this:

````

--- File: src/main.py ---
def main():
    print("Hello, World!")

--- File: tests/test_main.py ---
def test_main():
    assert True

--- File: utils/helpers.py ---
def helper_function():
    return "I'm helping!"
````

This format ensures that:
- File paths are clearly visible
- Code structure is preserved
- AI assistants can understand the project hierarchy
- Code relationships are maintained

## Requirements

- Python 3.6+
- pyperclip

## License

MIT License