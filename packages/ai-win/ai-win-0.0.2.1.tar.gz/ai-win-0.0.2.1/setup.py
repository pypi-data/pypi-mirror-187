from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.2.1'
DESCRIPTION = 'Helpful in creating logics of any AI.'
LONG_DESCRIPTION = 'A package that will help your program recognize your commands and respond respectively. You can train it according to you.'

# Setting up
setup(
    name="ai-win",
    version=VERSION,
    author="Aditya Pratap Singh",
    author_email="pypi.aditya@outlook.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['pyttsx3', 'SpeechRecognition', 'wikipedia'],
    keywords=['logics', 'recogize', 'speech recognition', 'open apps', 'speak', 'ai', 'python ai', 'aditya pratap singh'],
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "License :: OSI Approved :: IBM Public License",
        "License :: OSI Approved :: MIT License",
        "License :: OSI Approved :: Python Software Foundation License",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
    ]
)