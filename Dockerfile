FROM python:3.8.4-buster as base
ENV POETRY_HOME=/poetry
ENV PATH=${POETRY_HOME}/bin:${PATH}
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
EXPOSE 5000
WORKDIR /DevOps-Course-Starter
COPY . /DevOps-Course-Starter

# local development stage
FROM base as development
RUN poetry config virtualenvs.create false --local
RUN poetry install
ENTRYPOINT poetry run flask run -h 0.0.0.0 -p 5000

# production build stage
FROM base as production
ENV FLASK_ENV=production
ENV PORT=33507
RUN poetry config virtualenvs.create false --local
RUN poetry install
RUN poetry add gunicorn
ENTRYPOINT ["sh", "./scripts/entrypoint.sh"]

# testing stage FROM base as test
FROM base as test
RUN poetry config virtualenvs.create false --local
RUN poetry install
# Install Chrome
RUN curl -sSL https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -o chrome.deb \
    && apt-get update \
    && apt-get -f install ./chrome.deb -y \
    && rm ./chrome.deb
# Install Chromium WebDriver
RUN LATEST=`curl -sSL https://chromedriver.storage.googleapis.com/LATEST_RELEASE` \
    && echo "Installing chromium webdriver version ${LATEST}" \
    && curl -sSL https://chromedriver.storage.googleapis.com/${LATEST}/chromedriver_linux64.zip -o chromedriver_linux64.zip \
    && apt-get install unzip -y \
    && unzip ./chromedriver_linux64.zip
ENV PYTHONPATH=.
ENTRYPOINT ["poetry", "run", "pytest"]