from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="copyclip",
    version="0.1.2",
    author="Somil Jain",
    author_email="somiljain9999@gmail.com",
    description="A CLI tool to copy code files from a directory to the clipboard",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/somz22/copyclip",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "pyperclip>=1.8.0",
    ],
    entry_points={
        "console_scripts": [
            "copyclip=copyclip.main:main",
        ],
    },
)
