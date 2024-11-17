import os
import re
import argparse
import pyperclip
from copyclip import __version__

def gather_files(root_path, ignore_patterns, use_gitignore=False, include_hidden=False):
    """Recursively gathers files from the root_path, excluding files that match any ignore pattern."""
    files_to_process = []
    
    # Convert root_path to absolute path
    root_path = os.path.abspath(os.path.expanduser(root_path))
    print(f"Scanning directory: {root_path}")  # Debug print
    
    # Add gitignore patterns if requested
    if use_gitignore:
        gitignore_path = os.path.join(root_path, '.gitignore')
        if os.path.exists(gitignore_path):
            with open(gitignore_path, 'r') as f:
                gitignore_patterns = [
                    line.strip() 
                    for line in f.readlines() 
                    if line.strip() and not line.startswith('#')
                ]
                ignore_patterns.extend(gitignore_patterns)
                print(f"Added {len(gitignore_patterns)} patterns from .gitignore")  # Debug print
    
    # Escape the patterns to treat them as literal strings with wildcards
    escaped_patterns = [re.escape(pattern).replace('\\*', '.*') for pattern in ignore_patterns]
    
    try:
        for dirpath, dirnames, filenames in os.walk(root_path):
            # Skip hidden directories unless explicitly included
            if not include_hidden:
                dirnames[:] = [d for d in dirnames if not d.startswith('.')]
            
            for filename in filenames:
                # Skip hidden files unless explicitly included
                if not include_hidden and filename.startswith('.'):
                    continue
                    
                file_path = os.path.join(dirpath, filename)
                try:
                    relative_path = os.path.relpath(file_path, root_path)
                    
                    # Check if file matches any ignore pattern
                    if not any(re.search(pattern, relative_path) for pattern in escaped_patterns):
                        # Verify file is readable before adding
                        with open(file_path, 'r', encoding='utf-8') as f:
                            f.read(1)  # Try to read first byte
                        files_to_process.append(file_path)
                except (IOError, UnicodeDecodeError) as e:
                    print(f"Skipping {file_path}: {e}")
                    continue
                
    except Exception as e:
        print(f"Error while scanning directory: {e}")
    
    print(f"Found {len(files_to_process)} files to process")  # Debug print
    return files_to_process

def concatenate_files(files, root_path):
    """Concatenates file contents with metadata."""
    final_output = []
    total_size = 0
    processed_files = 0  # Counter for successfully processed files
    
    for file_path in files:
        try:
            relative_path = os.path.relpath(file_path, root_path)
            final_output.append(f"--- File: {relative_path} ---\n")
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                final_output.append(content)
                total_size += len(content)
                processed_files += 1
            
            final_output.append("\n\n")
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
    
    print(f"Successfully processed {processed_files} out of {len(files)} files")
    print(f"Total content size: {total_size} bytes")
    return ''.join(final_output)

def copy_to_clipboard(text):
    """Copy text to clipboard using pyperclip."""
    try:
        pyperclip.copy(text)
        
        # Verify the copy worked
        clipboard_content = pyperclip.paste()
        if clipboard_content == text:
            return True
        else:
            print("Clipboard verification failed - content mismatch")
            return False
    except Exception as e:
        print(f"Error copying to clipboard: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(
        description="""
CopyClip - A command-line tool that helps you copy multiple code files from a directory to your clipboard.
Perfect for sharing code snippets, preparing documentation, and especially useful when working with Large Language Models (LLMs).

Example Usage:
  Basic:
    copyclip /path/to/directory
  
  With ignore patterns:
    copyclip /path/to/directory --ignore "*.js" "*.pyc" "node_modules/*"
  
  With gitignore support:
    copyclip /path/to/directory --gitignore
  
  Include hidden files:
    copyclip /path/to/directory --include-hidden
  
  Print to console:
    copyclip /path/to/directory --print
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "path",
        help="Root path of the directory to process"
    )
    parser.add_argument(
        "--ignore",
        nargs="*",
        default=[],
        help="List of regex patterns to ignore files (e.g., *.js, .env, index*)"
    )
    parser.add_argument(
        "--gitignore",
        action="store_true",
        help="Respect .gitignore patterns when scanning files"
    )
    parser.add_argument(
        "--include-hidden",
        action="store_true",
        help="Include hidden files and directories (starting with .)"
    )
    parser.add_argument(
        "--print",
        action="store_true",
        help="Print the concatenated output to console instead of copying to clipboard"
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"CopyClip {__version__}",
        help="Show program's version number and exit"
    )
    
    args = parser.parse_args()
    root_path = os.path.abspath(os.path.expanduser(args.path))
    
    if not os.path.exists(root_path):
        print(f"Error: The path {root_path} does not exist.")
        return
    
    files = gather_files(root_path, args.ignore, args.gitignore, args.include_hidden)
    if not files:
        print("No files found to process.")
        return
    
    final_output = concatenate_files(files, root_path)
    
    # Print output if requested
    if args.print:
        print("\n=== BEGIN OUTPUT ===\n")
        print(final_output)
        print("\n=== END OUTPUT ===\n")
    
    # Try to copy to clipboard
    if copy_to_clipboard(final_output):
        print(f"Successfully copied content of {len(files)} files to clipboard.")
    else:
        print("Failed to copy to clipboard. Saving to file instead...")
        output_file = "code_output.txt"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(final_output)
        print(f"Content saved to {output_file}")

if __name__ == "__main__":
    main()
