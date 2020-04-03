from werkzeug.security import safe_str_cmp
from user import User # implemented in user.py

# authenticate a user
def authenticate(username,password):
    user = User.find_by_username(username) # default mapping to None if no user is found
    if user and safe_str_cmp(user.password, password): # safe_str_cmp safer than passwd == mypasswd for
        return user

def identity(payload):
    """
    Unique to Flask JWT. The payload is the contents of the JWT
    """
    user_id = payload['identity']
    return User.find_by_id(user_id)

