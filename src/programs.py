import tempfile
import subprocess
import shutil
import os

class ProgramsPool:
    def __init__(self):
        self.__isolated_dirs = {}

    def create_dir(self, identity):
        if self.__isolated_dirs.__contains__(identity):
            raise Exception('Directory already exists')
        
        self.__isolated_dirs[identity] = tempfile.mkdtemp(prefix=(identity+'_env_'))

    def run_isolated(self, command, identity):
        result = subprocess.run(
            command,
            cwd=self.__isolated_dirs[identity],
            capture_output=True,
            text=True
        )
        
        return {
            "exit_code": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr
        }