import os
import shutil


class FileRepository:
    """
    Interface to interact with files using typical python standard lib operations.
    this is partly in order to make the code more testable.
    """

    def __init__(self):
        super().__init__()

    def create_dir(self, dir_path):
        os.mkdir(dir_path)

    def exists(self, path):
        return os.path.exists(path)

    def is_file(self, path):
        return os.path.isfile(path)

    def is_dir(self, path):
        return os.path.isdir(path)

    def basename(self, path):
        return os.path.basename(path)

    def join(self, *paths):
        return os.path.join(*paths)

    def copy(self, src, dest):
        return shutil.copy(src, dest)

    def relpath(self, path, start):
        return os.path.relpath(path, start)

    def walk(self, path):
        return os.walk(path)
