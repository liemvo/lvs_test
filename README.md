# Simple Security System Application

## Config python virtual environment

### Create environment
    
    `python -m venv .venv`
### Active virtual env
    
    `source .venv/bin/activate`
### Deactive virtual env

    `deactivate`


## Install all dependencies

Need to config python virtual env and activate. 

Run command `pip install -r requirements.txt` to install all dependencies for project. 

## How to run application?

1. Use python 3.x or install and active virtual env
2. Install all dependencies
3. Invoke application
    `python main.py`



## How to run test coverage

### Run the unit tests with coverage

`coverage run --source=lvs -m unittest discover`

### Generate the coverage report

`coverage report`

#### In html format

`coverage html`


## AI Assistant was used during the development process of this test

An AI assistant was used during the development process of this security system application. Specifically, the assistant provided the following:

1. Guidance on structuring the project according to the user stories and functional requirements.
2. Code snippets for:
   - Capturing images using OpenCV and saving them with a timestamp.
   - Handling errors and logging them to a log file.
3. Unit testing suggestions and mock examples for capturing images and logging events.