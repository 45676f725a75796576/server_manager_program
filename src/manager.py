
from users import Users
from programs import ProgramsPool

class Manager:
    def __init__(self):
        users = Users()
        programsPool = ProgramsPool()

    def create_new_user(self,username: str, password: str):
        if self.users.__users_list.__contains__(username):
            raise Exception('User already exist')
        self.users.add_user(username, password)
        self.programsPool.create_dir(hash(username))

    def download_program(self, identity, url: str, alias: str):
        identity = hash(identity)
        pass