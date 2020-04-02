from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required, current_identity
from security import authenticate, identity # implemented in security.py

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
items = []

class Test(Resource):
    """
    test harness. return whatever name passed
    """
    def get(self, name):
        return {'test':name}

class Item(Resource):
    """
    Main Item Class
    Flask-RESTful does not need jsonify for returns
    """
    # Move parser within item instead of function by function
    parser = reqparse.RequestParser() #reqparser can also be used for form fields, also
    parser.add_argument('price',
        type=float,
        required=True,
        help='This field cannot be left blank'
    )
    #@jwt_required()
    def get(self, name):
        item = next(filter(lambda x: x['name'] == name, items), None) #next() returns only the first item from filter(lambda)
        # return {'item': item}, 200 if item is not None else 404
        return {'item': item}, 200 if item else 404 #shortened version

    #@jwt_required()
    def post(self, name):
        if next(filter(lambda x: x['name'] == name, items), None) is not None:
            return {'message': "An item with name '{}' already exists".format(name)}, 400

        data = Item.parser.parse_args()

        item = {
            'name' : name,
            'price' : data['price']
            }
        items.append(item)
        return item, 201

    #@jwt_required()   
    def delete(self, name):
        """
        Overwrite items list with a new list that has had 'name' removed
        """
        global items 
        items = list(filter(lambda x: x['name'] != name, items))
        return {'message':'Item Deleted'}

    #@jwt_required()
    def put(self, name):
        """
        Itempotent. Can create or update an item.
        """
        data = Item.parser.parse_args()

        item = next(filter(lambda x: x['name'] == name, items), None)
        if item is None:
            item = {'name':name,'price': data['price']}
            items.append(item)
        else:
            item.update(data)
        return item 


class ItemList(Resource):
    #@jwt_required()
    def get(self):
        return {'items': items}

# Adding resources:
# api.add_resource(xxx) replaces @app.route('xxx') under Student:get   
# Raw API Tester
api.add_resource(Test,'/test/<string:name>') 
# Application API targets
api.add_resource(Item,'/item/<string:name>') # e.g. http://localhost/item/mittens
api.add_resource(ItemList, '/items')

# Debug
app.run(port=5000, debug=True)
# Regular
#app.run(port=5000)




