import os
from datetime import timedelta

from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt import JWT

from security import authentication, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

"""app = flask.Flask(__name__) = Creates the Flask application object, which contains data about the application 
and also methods (object functions) 
that tell the application to do certain actions. The last line, app.run(), is one such method."""
app = Flask(__name__)


#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Api_data.db' => Telling app.py where to find api_data.db file
#since we added postgres in Heroku we are adding os.evniron and provided get with 2 param (if 1st not found then use 2nd param)
# uri: unique URI for the task. String type.
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL','sqlite:///Api_data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'jose'
api = Api(app)

# Create table with out file "create_Table" SQLAclchemy will create table if not exist
@app.before_first_request
def create_tables():
    db.create_all()

# If we want to change the url to the authentication endpoint instead of default /auth
# app.config['JWT_AUTH_URL_RULE'] = '/login'

# the authentication endpoint (by default, /auth );
jwt = JWT(app, authentication, identity)

# config JWT Token Expiration within half an hour, instead of default 5 min
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)

# config JWT Authentication key name to be 'email' instead of default 'username'
# app.config['JWT_AUTH_USERNAME_KEY'] = 'email'

if __name__ == '__main__':
    @jwt.auth_response_handler
    def customized_response_handler(access_token, identity):
        return jsonify({'access_token': access_token.decode('utf-8'),
                        'user_id': identity.id
                        })

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')

# Whenever we run file (ex. python app.py) python creates especial name '__main__' for that file
# below condition is for if we run app.py then execute below but if we inherite app.py in user.py
    # and if we run user.py file then app.run should not run
if __name__ == '__main__':

    from database import db
    db.init_app(app)

    # app.run() — A method that runs the application server.
    # app.config["DEBUG"] = True — Starts the debugger. With this line, if your code is malformed, you’ll see an error when you visit your app. Otherwise you’ll only see a generic message such as Bad Gateway in the browser when there’s a problem with your code.
    app.run(port=5000, debug=True)
