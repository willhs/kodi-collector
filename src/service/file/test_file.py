from typing import List

from src.service.file.abstract_file import FileService


class File:
    def __init__(self, path: str):
        self.path = path
        self.children: List[File] = []
        self.parent: File


def _create_root_media_dir() -> File:
    root = File('/')
    root.children.append(File('Movies'))
    root.children.append(File('TV Shows'))
    return root


class TestFileService(FileService):
    def __init__(self):
        super().__init__()

        self.media_root_dir = create_root_media_dir()

    def create_dir(self, dir_path):
        """
        creates a dir from the root file, depending on the path provided.
        if
        :param dir_path:
        :return:
        """
