import sqlite3
from flask import Flask, request
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

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
    parser = reqparse.RequestParser() #reqparser can also be used for form fields, also
    parser.add_argument('price',
        type=float,
        required=True,
        help='This field cannot be left blank'
    )

    #@jwt_required()
    def get(self, name):
        """
        Accept external requests for items
        """
        item = self.find_by_name(name)
        if item:
            return item
        return {'message':'Item not found'}, 404

    @classmethod
    def find_by_name(cls, name):
        """
        An internal method to do database lookups
        """
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = '''SELECT * FROM items WHERE name =?'''
        result = cursor.execute(query, (name, ))
        row = result.fetchone()
        connection.close()

        if row:
            return {'item':{'name': row[0], 'price':row[1]}}


    #@jwt_required()
    def post(self, name):
        """
        Add a new item into the database
        """
        # if self.find_by_name(name): # two ways to call
        if Item.find_by_name(name):
            return {'message': "An item with name '{}' already exists".format(name)}, 404

        # prepare data
        data = Item.parser.parse_args()
        item = {'name': name, 'price': data['price']}

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = '''INSERT INTO items VALUES (?,?)'''
        cursor.execute(query, (item['name'], item['price']))

        connection.commit()
        connection.close()

        return item, 201

    #@jwt_required()   
    def delete(self, name):
        """
        Overwrite items list with a new list that has had 'name' removed
        """
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        global items 
        items = list(filter(lambda x: x['name'] != name, items))
        return {'message':'Item Deleted'}

    #@jwt_required()
    def put(self, name):
        """
        Itempotent. Can create or update an item.
        """
        data = Item.parser.parse_args()

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

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
        """
        Return a list of all items
        """
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = '''SELECT * FROM items'''
        result = cursor.execute(query)

        items = []
        for row in result:
            items.append({'name':row[0], 'price':row[1]})
        
        connection.close()

        return {'items':{ items }}, 200
