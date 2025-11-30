
from users import Users
from programs import ProgramsPool

import os

from flask import Flask
from flask import request, jsonify, abort

import wget

class Manager:
    def __init__(self):
        self.users = Users()
        self.programsPool = ProgramsPool()

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

@app.route('/authorize', methods=['GET'])
def authorize():
    data = request.get_json(silent=True)
    try:
        username = data["username"]
        password = data["password"]
    except Exception as e:
        abort(400, description=f"Invalid data: {e}")
    if manager.users.authorize(username, password):
        return { "username": username }
@app.route('/directory', methods=['GET'])
def get_directory():
    username = request.args.get("username")
    if not username:
        abort(400, "Missing username")

    user_path = os.path.join(manager.programsPool.get_env_path(hash(username)), username)

    if not os.path.exists(user_path):
        abort(404, "User directory not found")

    return jsonify(build_tree(user_path))
        