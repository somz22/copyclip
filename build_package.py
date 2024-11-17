import os
import shutil
import subprocess
from copyclip import __version__

def clean_build_dirs():
    """Clean up build directories"""
    dirs_to_clean = ['build', 'dist', 'copyclip.egg-info']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"Cleaned {dir_name}/")

def run_checks():
    """Run pre-build checks"""
    # Check version matches
    with open('setup.py', 'r') as f:
        setup_content = f.read()
        if f'version="{__version__}"' not in setup_content:
            raise ValueError("Version mismatch between setup.py and __init__.py")
    
    # Verify README exists
    if not os.path.exists('README.md'):
        raise FileNotFoundError("README.md is required but missing")

def build_package():
    """Build the package distributions"""
    try:
        # Check if build package is installed
        try:
            import build
        except ImportError:
            print("'build' package not found. Installing...")
            subprocess.check_call(['pip3', 'install', 'build'])
            
        subprocess.check_call(['python3', '-m', 'build'])
        print("\nBuild successful! Created distributions:")
        for file in os.listdir('dist'):
            print(f"- dist/{file}")
    except subprocess.CalledProcessError as e:
        print(f"Build failed: {e}")
        return False
    return True

def main():
    print(f"Building CopyClip v{__version__}")
    print("\n1. Cleaning build directories...")
    clean_build_dirs()
    
    print("\n2. Running pre-build checks...")
    try:
        run_checks()
    except Exception as e:
        print(f"Pre-build checks failed: {e}")
        return
    
    print("\n3. Building package...")
    if build_package():
        print("\nBuild completed successfully!")
        print("\nTo publish to PyPI Test:")
        print("twine upload --repository-url https://test.pypi.org/legacy/ dist/*")
        print("\nTo publish to PyPI:")
        print("twine upload dist/*")

if __name__ == "__main__":
    main() 