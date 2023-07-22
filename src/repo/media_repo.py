import os


import logging

from src.repo.file_repo import FileRepository

logger = logging.getLogger(__name__)


class MediaRepository:
    def __init__(self, file_service: FileRepository):
        self.file_service = file_service
        self.movies_path = os.getenv('MOVIE_LIBRARY_PATH')
        self.tv_shows_path = os.getenv('TV_SHOW_LIBRARY_PATH')

    def add_video_to_movies(self, original_media_path: str, video_name: str):
        new_path = self.file_service.join(self.movies_path, video_name)

        if self.does_movie_exist(new_path):
            print(f"Skipping: {video_name} already exists in movies dir")
            return

        print(f'Writing to {new_path}')
        self.file_service.copy(original_media_path, new_path)

    def add_tv_show_dir_to_tv_shows(self, original_media_path: str, tv_show_dir: str):
        new_path = self.file_service.join(self.tv_shows_path, tv_show_dir)

        if self.does_tv_show_exist(new_path):
            print(f"Skipping: {tv_show_dir} already exists in tv shows dir")
            return

        self.file_service.copy(original_media_path, new_path)

    def does_movie_exist(self, movie_file_name: str):
        # check if a file/directory already exists
        path = self.file_service.join(self.movies_path, movie_file_name)
        return self.file_service.exists(path)

    def does_tv_show_exist(self, tv_show_dir_name: str):
        path = self.file_service.join(self.tv_shows_path, tv_show_dir_name)
        return self.file_service.exists(path)