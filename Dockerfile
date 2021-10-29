FROM python:3.9.7-buster as base


RUN mkdir -p /app/src
WORKDIR /app/src
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
ENV PATH=$PATH:/root/.poetry/bin 
ENV FLASK_APP=todo_app/app

COPY poetry.lock poetry.toml pyproject.toml ./ 

RUN poetry install --no-dev
COPY todo_app ./todo_app

EXPOSE 5000

FROM base as production
EXPOSE 8000

ENV FLASK_ENV=production
ENTRYPOINT ["poetry","run","gunicorn","--bind","0.0.0.0:8000","todo_app.app:create_app()"]

FROM base as development

ENTRYPOINT ["poetry","run","flask","run","--host","0.0.0.0"] 

FROM base as test

RUN poetry install
RUN apt-get update -qqy && apt-get install -qqy wget gnupg unzip
# Install Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub |apt-key add - \
 && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
 && apt-get update -qqy \
 && apt-get -qqy install google-chrome-stable \
 && rm /etc/apt/sources.list.d/google-chrome.list \
 && rm -rf /var/lib/apt/lists/* /var/cache/apt/*

# Install Chrome WebDriver
RUN CHROME_MAJOR_VERSION=$(google-chrome --version | sed -E "s/.* ([0-9]+)(\.[0-9]+){3}.*/\1/") \
 && CHROME_DRIVER_VERSION=$(wget --no-verbose -O - "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_${CHROME_MAJOR_VERSION}") \
 && echo "Using chromedriver version: "$CHROME_DRIVER_VERSION \
 && wget --no-verbose -O /tmp/chromedriver_linux64.zip https://chromedriver.storage.googleapis.com/$CHROME_DRIVER_VERSION/chromedriver_linux64.zip \
 && unzip /tmp/chromedriver_linux64.zip -d /usr/bin \
 && rm /tmp/chromedriver_linux64.zip \
 && chmod 755 /usr/bin/chromedriver \
 && cp /usr/bin/chromedriver .

COPY test ./test
#COPY /usr/bin/chromedriver ./test

ENTRYPOINT ["poetry", "run", "pytest"]

#docker build --target test --tag my-test-image .

#docker run my-test-image test/test_viewmodel.py
#docker run my-test-image test/test_trello_mock.py

#with parameters
#docker run  -e TOKEN=fd05c8b40c8e6ee957943ab385a64dd617b5a7857546628024797e4619071a47  -e KEY=223a298a35a8501137490e59595d2ac3  my-test-image test/test_selenium.py 
#docker run  -e TOKEN -e KEY my-test-image test/test_selenium.py
#with env file
#docker run --env-file .env my-test-image test/test_selenium.py      


# These are the commands to build the image and run docker
#For Dev instance
#docker build --target development --tag todo-app:dev .

#without bind mount
#docker run -p 5000:5000 --env-file .env todo-app

#with bind mount
#docker run --mount type=bind,src=C:/Users/Rajesh/Devops_project/DevOps-Course-Starter/todo_app,dst=/app/src/todo_app -p 5000:5000 --env-file .env  todo-app:dev

#For Production instance
#docker build --target production --tag todo-app:prod .

#without bind mount
#docker run -p 8000:8000 --env-file .env todo-app:prod

#with bind mount
#docker run --mount type=bind,src=C:/Users/Rajesh/Devops_project/DevOps-Course-Starter/todo_app,dst=/app/src/todo_app -p 8000:8000 --env-file .env  todo-app:prod



