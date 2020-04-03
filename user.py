import sqlite3
from flask_restful import Resource, reqparse


class User:
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = '''SELECT * FROM users WHERE username=?'''
        result = cursor.execute(query, (username,)) # parameters must be in the form of a tuple
        row = result.fetchone()
        if row:
            # user = cls(row[0]. row[1], row[2])
            user = cls(*row) # simplifies the above
        else:
            user = None 
        connection.close()
        return user

    @classmethod
    def find_by_id(cls, _id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = '''SELECT * FROM users WHERE id=?'''
        result = cursor.execute(query, (_id,)) # parameters must be in the form of a tuple
        row = result.fetchone()
        if row:
            # user = cls(row[0]. row[1], row[2])
            user = cls(*row) # simplifies the above
        else:
            user = None 
        connection.close()
        return user

class UserRegister(Resource):
    # Move parser within item instead of function by function
    parser = reqparse.RequestParser() #reqparser can also be used for form fields, also
    parser.add_argument('username',
        type=str,
        required=True,
        help='username cannot be left blank'
    )
    parser.add_argument('password',
        type=str,
        required=True,
        help='password cannot be left blank'
    )
    def post(self):
        data = UserRegister.parser.parse_args()

        if User.find_by_username(data['username']):
            return {'message':'Username already exists'}, 404
        # create user
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = '''INSERT INTO users VALUES(NULL, ?, ?)'''
        cursor.execute(query, (data['username'], data['password']))

        connection.commit()
        connection.close()
        
        return {'message':'User created successfully'}, 201
            

