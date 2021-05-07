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
RUN poetry add oauthlib flask-login
ENTRYPOINT poetry run flask run -h 0.0.0.0 -p 5000

# production build stage
FROM base as production
ENV FLASK_ENV=production
ENV PORT=5000
RUN poetry config virtualenvs.create false --local
RUN poetry install
RUN poetry add oauthlib flask-login
RUN poetry add gunicorn
ENTRYPOINT ["sh", "./scripts/entrypoint.sh"]

# testing stage FROM base as test
FROM base as test
RUN poetry config virtualenvs.create false --local
RUN poetry install

RUN apt-get update && apt-get install wget gnupg unzip -y
# Install Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
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
  && rm -rf /opt/selenium/chromedriver \
  && unzip /tmp/chromedriver_linux64.zip -d /opt/selenium \
  && rm /tmp/chromedriver_linux64.zip \
  && mv /opt/selenium/chromedriver /opt/selenium/chromedriver-$CHROME_DRIVER_VERSION \
  && chmod 755 /opt/selenium/chromedriver-$CHROME_DRIVER_VERSION \
  && ln -fs /opt/selenium/chromedriver-$CHROME_DRIVER_VERSION /usr/bin/chromedriver

ENV PYTHONPATH=.
ENTRYPOINT ["poetry", "run", "pytest"]