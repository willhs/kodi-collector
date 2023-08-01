import os

from pyfakefs.fake_filesystem_unittest import Patcher

from src.service.file.file_service import FileService


class MockFileService(FileService):
    def __init__(self):
        self.patcher = Patcher(additional_skip_names=['/etc/ssl/certs', '/usr/local/etc/openssl@1.1/certs',
                                                      '/Users/will/projects/kodi-collector/venv/lib/python3.8/site-packages/certifi/'],
                               modules_to_reload=[os, open])
        self.patcher.setUp()
        self.fs = self.patcher.fs  # This is the fake file system

    def create_dir(self, dir_path):
        self.fs.create_dir(dir_path)

    def exists(self, path):
        return self.fs.exists(path)

    def is_file(self, path):
        return self.fs.isfile(path)

    def is_dir(self, path):
        return self.fs.isdir(path)

    def basename(self, path):
        return os.path.basename(path)

    def join(self, *paths):
        return os.path.join(*paths)

    def copy(self, src, dest):
        if not self.exists(src):
            raise FileNotFoundError(f"No such file or directory: '{src}'")
        content = self.fs.get_object(src).contents
        self.fs.create_file(dest, contents=content)

    def relpath(self, path, start):
        return os.path.relpath(path, start)

    def walk(self, path):
        return os.walk(path)

    def list_dir(self, path):
        return self.fs.listdir(path)

    def splitext(self, path):
        return os.path.splitext(path)

    def create_file(self, original_tv_show_file):
        return self.fs.create_file(original_tv_show_file)

    def tearDown(self):
        self.patcher.tearDown()