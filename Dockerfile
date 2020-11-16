FROM python:3.8.4-buster as base
RUN pip install poetry
EXPOSE 5000
WORKDIR /DevOps-Course-Starter
COPY . /DevOps-Course-Starter/
RUN poetry install
FROM base as development
ENTRYPOINT poetry run flask run -h 0.0.0.0 -p 5000
FROM base as production
ENV FLASK_ENV=production
ENTRYPOINT poetry run gunicorn "app:create_app()" --bind 0.0.0.0:5000