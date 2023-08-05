from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.7'
DESCRIPTION = 'hi my package do many thing and made by liveofcode'
LONG_DESCRIPTION = 'hi this package do this chatbot, input to file Translatortext it have Speak engine ,Listen engine,write like print password maker and do math and search on google and search website'

# Setting up
setup(
    name="pyliveofcode",
    version=VERSION,
    author="liveofcode",
    author_email="liveallgamegamer@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=["pyttsx3","SpeechRecognition","googletrans","nltk","scikit-learn","playsound"],
    keywords=['arithmetic', 'math', 'mathematics', 'python tutorial', 'avi upadhyay'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)