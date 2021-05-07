from flask import Flask, render_template, request, redirect, url_for
import db_items as mongoDB
from viewmodel import ViewModel
from user import User
import pymongo
import certifi
import os
import requests
from flask_login import LoginManager, login_required, login_user
from oauthlib.oauth2 import WebApplicationClient
   
secret_key = os.environ.get('SECRET_KEY', 'secret_key')
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
login_manager = LoginManager()
appClient = WebApplicationClient(client_id)

def create_app():
    app = Flask(__name__) 

    login_disabled = os.environ.get('LOGIN_DISABLED', 'False') == 'True'
    app.config['LOGIN_DISABLED'] = login_disabled
    
    board_id = os.getenv('BOARD_ID')
    db_connectionstring = os.getenv('MONGO_CONNECTION_URL')
    

    client = pymongo.MongoClient(
        db_connectionstring,
        tlsCAFile=certifi.where()
    )
    db = client.TodoListDB
    collection = db.todos

    print(login_disabled, flush=True)

    @login_manager.unauthorized_handler 
    def unauthenticated():
        print("Inside unauthenticated", flush=True)
        uri = appClient.prepare_request_uri("https://github.com/login/oauth/authorize")
        return redirect(uri)
        
    @login_manager.user_loader 
    def load_user(user_id):
        print("Inside load_user : " + user_id, flush=True)
        return User(user_id) 
        # return None

    @app.route('/login/callback', methods=['GET'])
    def login_callback():
        print("Inside login_callback", flush=True)
        token_response = requests.post('https://github.com/login/oauth/access_token', data={
                'client_id': client_id,
                'client_secret': client_secret,
                'code': request.args.get('code')
            }, headers={'Accept': 'application/json'})

        appClient.parse_request_body_response(token_response.text)

        user_response = requests.get('https://api.github.com/user', headers={
            'Accept': 'application/json', 
            'Authorization': f"token {token_response.json()['access_token']}"
            })

        login_user(User(user_response.json()['login']))        
        return redirect(url_for('index'))
    
    @app.route('/')
    @login_required
    def index():
        print("Inside index", flush=True)
        items = mongoDB.get_items(collection, board_id)
        item_view_model = ViewModel(items[0], items[1], items[2])
        return render_template('index.html', view_model=item_view_model)

    @app.route('/add', methods=['POST'])
    @login_required
    def add():
        name = request.form.get('new_item_name')
        description = request.form.get('new_item_description')
        mongoDB.create_item(collection, board_id, name, description)
        return redirect(url_for('index'))

    @app.route('/start/<item_id>', methods=['POST'])
    @login_required
    def start_item(item_id):
        mongoDB.start_item(collection, board_id, item_id)
        return redirect(url_for('index'))

    @app.route('/complete/<item_id>', methods=['POST'])
    @login_required
    def complete_item(item_id):
        mongoDB.complete_item(collection, board_id, item_id)
        return redirect(url_for('index'))

    @app.route('/undo/<item_id>', methods=['POST'])
    @login_required
    def undo_item(item_id):
        mongoDB.undo_item(collection, board_id, item_id)
        return redirect(url_for('index'))

    return app, collection

app, collection = create_app()
app.secret_key = secret_key
login_manager.init_app(app)
