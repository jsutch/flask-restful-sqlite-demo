import sqlite3

# create the connection object
connection = sqlite3.connect('data.db')

# create a cursor object
cursor = connection.cursor()

# define the schema
#create_table = "CREATE TABLE users (id int, username text, password text)"

# create the table
#cursor.execute(create_table)

# create a user
user = (1,'bob','asdf')
chuck = (2,'chuck','asdf')
annie = (3,'annie','asdf')
newusers = [
    (10,'tom','asdf'),
    (11,'tim','asdf'),
    (12,'terry','asdf')
]

# insert the user into the table
insert_query = '''INSERT INTO users VALUES (?, ?, ?)'''
#cursor.execute(insert_query, annie)
#cursor.executemany(insert_query,newusers)
select_query = "SELECT * FROM users"
#ret = cursor.execute(select_query)
#print(ret.fetchall())
for row in cursor.execute(select_query):
    print(row)

connection.commit()
connection.close()
