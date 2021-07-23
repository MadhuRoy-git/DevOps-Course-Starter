from flask import Flask, render_template, request, redirect, url_for, abort
import db_items as mongoDB
from viewmodel import ViewModel
from user import User
import pymongo
import certifi
import os
import requests
from flask_login import LoginManager, login_required, login_user, current_user
from oauthlib.oauth2 import WebApplicationClient
from loggly.handlers import HTTPSHandler 
from logging import Formatter
from logging import getLogger
   
secret_key = os.environ.get('SECRET_KEY', 'secret_key')
admin_user = os.environ.get('APP_ADMIN_USER_ID', 'MadhuRoy-git')
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
login_manager = LoginManager()
appClient = WebApplicationClient(client_id)

ROLE_READER = 'reader'
ROLE_WRITER = 'writer'

def create_app():
    app = Flask(__name__) 

    login_disabled = os.environ.get('LOGIN_DISABLED', 'False') == 'True'
    log_level = os.environ.get('LOG_LEVEL', 'INFO')
    loggly_token = os.environ.get('LOGGLY_TOKEN')
    app.config['LOGIN_DISABLED'] = login_disabled
    app.config['LOG_LEVEL'] = log_level
    app.config['LOGGLY_TOKEN'] = loggly_token
    app.logger.setLevel(app.config['LOG_LEVEL'])
    
    board_id = os.getenv('BOARD_ID')
    db_connectionstring = os.getenv('MONGO_CONNECTION_URL')

    if app.config['LOGGLY_TOKEN'] is not None:
        handler = HTTPSHandler(f'https://logs-01.loggly.com/inputs/{app.config["LOGGLY_TOKEN"]}/tag/todo-app')
        handler.setFormatter(Formatter("[%(asctime)s] %(levelname)s in %(module)s: %(message)s"))
        app.logger.addHandler(handler)
        getLogger('werkzeug').addHandler(HTTPSHandler(f'https://logs-01.loggly.com/inputs/{app.config["LOGGLY_TOKEN"]}/tag/todo-app-requests'))

    client = pymongo.MongoClient(
        db_connectionstring,
        tlsCAFile=certifi.where()
    )
    db = client.TodoListDB
    collection = db.todos

    @login_manager.unauthorized_handler 
    def unauthenticated():
        uri = appClient.prepare_request_uri("https://github.com/login/oauth/authorize")
        return redirect(uri)
        
    @login_manager.user_loader 
    def load_user(user_id):
        return User(user_id) 
        # return None

    @app.route('/login/callback', methods=['GET'])
    def login_callback():
        token_url, headers, body = appClient.prepare_token_request(
                                    'https://github.com/login/oauth/access_token',
                                    authorization_response=request.url,
                                    code=request.args.get('code')
                                )

        token_response = requests.post(
                        token_url,
                        headers=headers,
                        data=body,
                        auth=(client_id, client_secret),
                    )

        appClient.parse_request_body_response(token_response.text)

        userinfo_endpoint = 'https://api.github.com/user'
        uri, headers, body = appClient.add_token(userinfo_endpoint)
        user_response = requests.get(uri, headers=headers, data=body)

        login_user(User(user_response.json()['login']))  
        app.logger.info("User has logged in successfully")      
        return redirect(url_for('index'))
    
    def get_user_role():             
        if (app.config.get('LOGIN_DISABLED') or current_user.user_id == admin_user):                        
            return ROLE_WRITER
        else:            
            return ROLE_READER

    @app.route('/')
    @login_required
    def index():
        items = mongoDB.get_items(collection, board_id)
        user_role = get_user_role()
        item_view_model = ViewModel(items[0], items[1], items[2], user_role)
        return render_template('index.html', view_model=item_view_model)

    @app.route('/add', methods=['POST'])
    @login_required
    def add():
        app.logger.debug("User performing add")
        name = request.form.get('new_item_name')
        app.logger.info("Value of name is %s", name)
        description = request.form.get('new_item_description')
        
        user_role = get_user_role()
        if (user_role == ROLE_WRITER):
            mongoDB.create_item(collection, board_id, name, description)
            return redirect(url_for('index'))
        else:
            return abort(403)

    @app.route('/start/<item_id>', methods=['POST'])
    @login_required
    def start_item(item_id):
        app.logger.debug("User performing start")
        user_role = get_user_role()
        if (user_role == ROLE_WRITER):
            mongoDB.start_item(collection, board_id, item_id)
            return redirect(url_for('index'))
        else:
            return abort(403)
        
    @app.route('/complete/<item_id>', methods=['POST'])
    @login_required
    def complete_item(item_id):
        app.logger.debug("User performing complete")
        user_role = get_user_role()
        app.logger.info("Value of user_role is %s", user_role)
        if (user_role == ROLE_WRITER):
            mongoDB.complete_item(collection, board_id, item_id)
            return redirect(url_for('index'))
        else:
            return abort(403)

    @app.route('/undo/<item_id>', methods=['POST'])
    @login_required
    def undo_item(item_id):
        app.logger.debug("User performing undo")
        user_role = get_user_role()
        if (user_role == ROLE_WRITER):
            mongoDB.undo_item(collection, board_id, item_id)
            return redirect(url_for('index'))
        else:
            return abort(403)

    return app, collection

app, collection = create_app()
app.secret_key = secret_key
login_manager.init_app(app)
