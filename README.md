# DevOps Apprenticeship: Project Exercise

## System Requirements

The project uses poetry for Python to create an isolated environment and manage package dependencies. To prepare your system, ensure you have an official distribution of Python version 3.7+ and install poetry using one of the following commands (as instructed by the [poetry documentation](https://python-poetry.org/docs/#system-requirements)):

### Poetry installation (Bash)

```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
```

### Poetry installation (PowerShell)

```powershell
(Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -UseBasicParsing).Content | python
```

## Dependencies

The project uses a virtual environment to isolate package dependencies. To create the virtual environment and install required packages, run the following from your preferred shell:

```bash
$ poetry install
```

You'll also need to clone a new `.env` file from the `.env.template` to store local configuration options. This is a one-time operation on first setup:

```bash
$ cp .env.template .env  # (first time only)
```

The `.env` file is used by flask to set environment variables when running `flask run`. This enables things like development mode (which also enables features like hot reloading when you make a file change). There's also a [SECRET_KEY](https://flask.palletsprojects.com/en/1.1.x/config/#SECRET_KEY) variable which is used to encrypt the flask session cookie.

## Set up instructions for Trello application :
1)For the application, create your account in Trello and then create a board.
We will use the app to access the board using REST APIs
a) KEY :To begin the authentication process, you need an API key. Every Trello user is given an API key. You can retrieve your API key by logging into Trello and visiting https://trello.com/app-key/.
b) TOKEN : You will also need a token to access your board via API. You will be directed to a page to generate user specific token once API key has been generated.

## Other set up instructions for running the tests:
3) Add fake KEY and TOKEN to .env.test file instead of hardcoding in the the program. This file should be added to source control

4) Add the requests library to your list of poetry dependencies in
pyproject.toml by running poetry add requests

5) Add pytest to library in your list of poetry dependencies in pyproject.toml by running poetry add pytest
This needs to be run only once, if the entry is present in pyproject.toml and poetry.lock, it needn't be run again

6) Download chromedriver from following link and place the file choromedriver.exe in a test folder where all other test files will be placed. 
https://chromedriver.chromium.org/downloads

7) Add chromedriver.exe to .gitignore as we don't want to push these files to Github

## Executing tests
1) Running unit test:
a. Place the test file test_viewmodel.py in test folder of project app and execute following command:
poetry run pytest test_viewmodel.py

2) Running Integration tests
a. Mock the test and place test file test_trello_mock.py in test folder and run  poetry run pytest test_trello_mock.py
Based on current assertions in the test, this should pass

3) Testing end to end with Selenium
a. Place test file test_selenium.py in test folder and run poetry run test_selenium.py
Based on current assertions in the test, this should pass



## Running the App

Once the all dependencies have been installed, start the Flask app in development mode within the poetry environment by running:
```bash
$ poetry run flask run
```

You should see output similar to the following:
```bash
 * Serving Flask app "app" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with fsevents reloader
 * Debugger is active!
 * Debugger PIN: 226-556-590
```
Now visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app.


Docker commands
These are the commands to build the image and run docker
For Dev instance
```
docker build --target development --tag todo-app:dev .

without bind mount

docker run -p 5000:5000 --env-file .env todo-app

with bind mount

docker run --mount type=bind,src=C:/Users/Rajesh/Devops_project/DevOps-Course-Starter/todo_app,dst=/app/src/todo_app -p 5000:5000 --env-file .env  todo-app:dev

For Production instance

docker build --target production --tag todo-app:prod .

without bind mount

docker run -p 8000:8000 --env-file .env todo-app:prod

with bind mount

docker run --mount type=bind,src=C:/Users/Rajesh/Devops_project/DevOps-Course-Starter/todo_app,dst=/app/src/todo_app -p 8000:8000 --env-file .env  todo-app:prod
```
     
#########

Module 6 C4 Diagram
The diagram to be openend using : https://app.diagrams.net/
This app was used to create the diagrams

There are 3 separate tabs for Context, container and component diagram

#############
Exercise-7 commands
#docker build --target test --tag my-test-image .

#docker run my-test-image test/test_viewmodel.py
#docker run my-test-image test/test_trello_mock.py

#with parameters
#docker run  -e TOKEN -e KEY my-test-image test/test_selenium.py
#with env file
#docker run --env-file .env my-test-image test/test_selenium.py
# Testing commands for paths-ignore


########
Exercise-8
# Log into the Heroku API if you haven't already
$ heroku login

# Log into Heroku's registry (this can also be achieved with a docker login command)
$ heroku container:login

# Tag the image you built earlier for Docker Hub with the correct name for Heroku
<docker pull rajeshdewan/todoapp:production >
$ docker tag rajeshdewan/todoapp:production registry.heroku.com/todoappfordevops/web

# Push it to Heroku registry
$ docker push registry.heroku.com/todoappfordevops/web

# Release the app
heroku container:release web -a todoappfordevops
heroku open -a todoappfordevops
OR use the following link:
http://todoappfordevops.herokuapp.com/