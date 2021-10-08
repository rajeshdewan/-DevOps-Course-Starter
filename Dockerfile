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



