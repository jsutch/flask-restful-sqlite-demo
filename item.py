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
    TABLE_NAME = 'items'
    # parser
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

        data = Item.parser.parse_args()
        item = {'name':name,'price': data['price']}
        try:
            self.insert(item)
        except:
            return {'message':'An error occurred'}, 500

        return item, 201

    @classmethod
    def insert(cls, item):

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = '''INSERT INTO items VALUES (?,?)'''
        cursor.execute(query, (item['name'], item['price']))

        connection.commit()
        connection.close()

    @classmethod
    def update(cls, item):
        """
        Update an item in the datastore
        """
    
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        #query = '''UPDATE {table} SET price=? WHERE name=?'''.format(cls.TABLE_NAME)
        query = '''UPDATE items SET price=? WHERE name=?'''
        cursor.execute(query, (item['price'], item['name']))

        connection.commit()
        connection.close()


    #@jwt_required()   
    def delete(self, name):
        """
        Overwrite items list with a new list that has had 'name' removed
        """
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = '''DELETE FROM items WHERE name =?'''
        cursor.execute(query, (name,))

        connection.commit()
        connection.close()

        return {'message':'Item Deleted'}

    #@jwt_required()
    def put(self, name):
        """
        Itempotent. Can create or update an item.
        """
        data = Item.parser.parse_args()
        item = self.find_by_name(name)
        updated_item = {'name':name,'price': data['price']}

        if item is None:
            try:
                Item.insert(updated_item)
            except:
                return {'message':'An error occurred adding the item'}, 500    
        else:
            try:
                Item.update(updated_item)
            except:
                return {'message':'An error occurred updating the item'}, 500 
        return updated_item 


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

        return {'items': items }, 200
