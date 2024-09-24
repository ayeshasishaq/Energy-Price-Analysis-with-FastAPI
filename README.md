# IN3110 Energy-Price-Analysis-with-FastAPI

## Introduction to Assignment 5: Energy Price Analysis and Visualization with FastAPI
This assignment focuses on utilizing Python's data analysis using FastAPI and Altair to build a dynamic webpage. The webpage´s functionality revolves around retrieving, processing, and graphically presenting data on electricity prices in Norway. The tasks completed are 5.1 to 5.6, excluding task 5.4.

## Installation
Ensure Python 3.8 or above is installed. To install the in3110_instapy package, use pip in your project's root directory:

    python3 -m pip install .


## Required dependencies
Following dependencies are needed to run the program:

    python3 -m pip install altair==4.*
    python3 -m pip install altair-viewer
    python3 -m pip install beautifulsoup4
    python3 -m pip install "fastapi[all]"
    python3 -m pip install pandas
    python3 -m pip install pytest
    python3 -m pip install requests
    python3 -m pip install requests-cache
    python3 -m pip install uvicorn

## Displaying the graphic visualization and the webpage
Run Strompris.py as follow for visualization:

    python strompris.py

To display the webpage run the FastAPI app:

    python app.py 

Access the webpage with: http://127.0.0.1:5000/ in an open web browser.

## Sphinx documentation
After installing sphinx using this command: 

    python -m pip install sphinx

Create a directory inside your project to hold your docs:

    mkdir docs

Thereby Run sphinx-quickstart:

    sphinx-quickstart

In result various sphinx files are installed in the directory. With these necessary files information about the project can be
written neatly and as detailed.

Then the documentation will be transformed from the index.rst file to an index.html file.


# Energy-Price-Analysis-with-FastAPI
