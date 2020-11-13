FROM python:3.8.4-buster as base
RUN pip install poetry
EXPOSE 5000
WORKDIR /DevOps-Course-Starter
COPY . /DevOps-Course-Starter/
RUN poetry install
ENTRYPOINT poetry run flask run -h 127.0.0.1 -p 5000