from abc import ABC, abstractmethod


class FileService(ABC):
    @abstractmethod
    def create_dir(self, dir_path):
        pass

    @abstractmethod
    def is_file(self, path):
        pass

    @abstractmethod
    def is_dir(self, path):
        pass

    @abstractmethod
    def basename(self, path):
        pass

    @abstractmethod
    def join(self, *paths):
        pass

    @abstractmethod
    def copy(self, src, dest):
        pass

    @abstractmethod
    def relpath(self, path, start):
        pass

    @abstractmethod
    def walk(self, path):
        pass
