
from users import Users
from programs import ProgramsPool

from flask import Flask
from flask import request

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

@app.route('/authorize', methods=['GET'])
def authorize():
    data = request.get_json(silent=True)
    try:
        username = data["username"]
        password = data["password"]
    except Exception as e:
        abort(400, description=f"Invalid data: {e}")
        