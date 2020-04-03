from flask import Flask
from flask_restful import Api, reqparse
from flask_jwt import JWT, current_identity
# our libraries
from security import authenticate, identity # implemented in security.py
from user import UserRegister
from item import Item, Itemlist

# instantiate app
app = Flask(__name__)
# add secret key for auth
app.secret_key = 'hummingbird'
# instantiate API
api = Api(app)

# JWT additions
# creates a new endpoint of /auth
jwt = JWT(app, authenticate, identity)

# datastore
# items = []




# Adding resources:
# api.add_resource(xxx) replaces @app.route('xxx') under Student:get   
# Raw API Tester
api.add_resource(Test,'/test/<string:name>') 
# Application API targets
api.add_resource(Item,'/item/<string:name>') # e.g. http://localhost/item/mittens
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister,'/register')

# Debug
app.run(port=5000, debug=True)
# Regular
#app.run(port=5000)




