# DevOps Apprenticeship: Project Exercise

## Getting started

The project uses a virtual environment to isolate package dependencies. To create the virtual environment and install required packages, run the following from a bash shell terminal:

### On macOS and Linux
```bash
$ source setup.sh
```
### On Windows (Using Git Bash)
```bash
$ source setup.sh --windows
```

Once the setup script has completed and all packages have been installed, start the Flask app by running:
```bash
$ flask run
```

You should see output similar to the following:
```bash
 * Serving Flask app "app" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with fsevents reloader
 * Debugger is active!
 * Debugger PIN: 226-556-590
```
Now visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app.

### Notes

A Trello Account has been setup.
The `.env` file is used by flask to set environment variables when running `flask run`. This enables things like developement mode (which also enables features like hot reloading when you make a file change).
* There's also a [SECRET_KEY](https://flask.palletsprojects.com/en/1.1.x/config/#SECRET_KEY) variable which is used to encrypt the flask session cookie.
* The .env file has the API Key and Token that have been created for the Trello Account.
* The .env file also has the boardId for the board on the Trello Account
* The list ids for "To Do" and "Done" are hard-coded in the trello_item.py. They are retrieved by a Get call to the Trello API.

When running `setup.sh`, the `.env.template` file will be copied to `.env` if the latter does not exist.

### Tests
There are 3 types of tests that have been added - Unit Tests , Integration Tests and EndToEnd Tests.
They can be run by the following command : python -m pytest
For the end to end tests , install the latest version of Firefox browser and geckodriver.