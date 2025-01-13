FROM python:3.13

# for postgres and redis
RUN apt update && apt install -y postgresql redis-tools

WORKDIR /code

RUN pip install --upgrade pip && pip install pipenv 
ENV PIPENV_CUSTOM_VENV_NAME="bookhive"
COPY ./Pipfile /code/Pipfile
COPY ./Pipfile.lock /code/Pipfile.lock

RUN pipenv install --dev