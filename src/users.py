import re

class Users:
    def __init__(self):
        self.__users_list = {}

    # username is not hashed, password is
    def add_user(self, username, password):
        if username in self.__users_list:
            raise Exception('User already exists')
        if not re.fullmatch('[a-zA-Z0-9]*', password) or not re.fullmatch('[a-zA-Z0-9]*', username) or len(password) < 6 or len(username) < 3:
            raise Exception('Wrong format')

        self.__users_list[username] = hash(password)

    def get_user(self, username):
        return {
            "username": username
        }
    
    def show_password(self, username):
        return {
            "password": self.__users_list[username]
        }
    
    def user_exists(self, username: str) -> bool:
        return self.__users_list.__contains__(username)

    def authorize(self, username, password) -> bool:
        return username in self.__users_list and self.__users_list[username] == hash(password)