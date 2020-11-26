# DevOps Apprenticeship: Project Exercise

## Initial Setup

A file called .env has been created with the environment variables below. This .env file is used by flask to set environment variables. This enables things like development mode (which also enables features like hot reloading when you make a file change). Populate the following variables inside the .env file with your Trello App API details/credentials:

```bash
FLASK_APP=app
FLASK_ENV=development

apiKey=# your trello api key
apiToken=# your trello api token
boardId=# your board id

TODO_LIST_ID=# your 'todo' list id
DOING_LIST_ID=# your 'doing' list id
DONE_LIST_ID=# your 'done' list id
```
Note that .env has been added to the gitignore file so that these secrets will not be commited to git. Now, our app is ready to be run.

### Running the App
```bash
$ poetry run python -m pytest
```

To build a docker image (in Development mode) and start the application in Development mode , run the following:
```bash
$ docker build --target development --tag todo-app:dev .
$ docker run -d -p 5000:5000 --env-file ./.env todo-app:dev 
```

To build a docker image (in Production mode) and start the application in Development mode , run the following:
```bash
$ docker build --target production --tag todo-app:prod .
$ docker run -d -p 5000:5000 --env-file ./.env todo-app:prod 
```

We can run the application in a VM using Vagrant within the poetry environment by running:
```bash
$ vagrant up --provision
```

You should see output similar to the following:
```bash
 * Serving Flask app "app" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://0.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with fsevents reloader
 * Debugger is active!
 * Debugger PIN: 226-556-590
```
Now visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app.

### Tests
There are 3 types of tests that have been added - Unit Tests , Integration Tests and EndToEnd Tests.
They can be run by the following command : python -m pytest
For the end to end tests , install the latest version of Firefox browser and geckodriver.