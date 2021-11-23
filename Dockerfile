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
#ENTRYPOINT ["poetry","run","gunicorn","--bind","0.0.0.0:8000","todo_app.app:create_app()"]
CMD poetry run gunicorn "todo_app.app:create_app()" --bind 0.0.0.0:$PORT

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
COPY .env.test ./

ENTRYPOINT ["poetry", "run", "pytest"]

