FROM python:3.13

WORKDIR /code

RUN pip install --upgrade pip && pip install pipenv 

ENV PIPENV_CUSTOM_VENV_NAME="book_api"

COPY ./Pipfile /code/Pipfile

COPY ./Pipfile.lock /code/Pipfile.lock

RUN pipenv install --dev