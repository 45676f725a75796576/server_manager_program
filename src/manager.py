
from users import Users
from programs import ProgramsPool

import os

from flask import Flask
from flask import request, jsonify, abort

import wget

import secrets

class Manager:
    def __init__(self):
        self.users = Users()
        self.programsPool = ProgramsPool()
        self.loggedUsers = {}

    def create_new_user(self,username: str, password: str):
        if self.users.__users_list.__contains__(username):
            raise Exception('User already exist')
        self.users.add_user(username, password)
        self.programsPool.create_dir(hash(username))

    def download_program(self, username, alias: str, download_url: str):
        username = hash(username)
        url = self.programsPool.get_env_path(username)
        wget.download(download_url, (url + '/' + alias))

app = Flask(__name__)

manager = Manager()

def build_tree(path):
    tree = {}
    try:
        items = os.listdir(path)
    except Exception:
        return tree

    for item in items:
        full = os.path.join(path, item)
        if os.path.isdir(full):
            tree[item] = build_tree(full)
        else:
            tree[item] = None
    return tree

# to access server at first you have to authorize
@app.route('/authorize', methods=['GET'])
def authorize():
    data = request.get_json(silent=True)
    try:
        username = data["username"]
        password = data["password"]
    except Exception as e:
        abort(400, description=f"Invalid data: {e}")
    if manager.users.authorize(username, password):
        manager.loggedUsers[username] = secrets.token_hex(16)
        return { "username": manager.loggedUsers[username] }
    
# to see your working directory
@app.route('/directory', methods=['GET'])
def get_directory():
    token = request.args.get("token")
    if not token:
        abort(400, "Missing user token")

    for lu in manager.loggedUsers.keys:
        if manager.loggedUsers[lu] == token:
            user = lu

    user_path = os.path.join(manager.programsPool.get_env_path(hash(user)), user)

    if not os.path.exists(user_path):
        abort(404, "User directory not found")

    return jsonify(build_tree(user_path))


# everytime you know, that you are done with work, please logout,
# token you got can be stolen and used on this server
@app.route('/logout', methods=['GET'])
def logout():
    token = request.args.get("token")
    if not token:
        abort(400, "Missing user token")
    for lu in manager.loggedUsers.keys:
        if manager.loggedUsers[lu] == token:
            manager.loggedUsers.pop[lu]
        