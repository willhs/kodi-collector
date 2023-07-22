import os
import unittest
from unittest.mock import Mock
from parameterized import parameterized
from src.strategy.media_file_transformer import MediaFileTransformer


class FileStructureTests(unittest.TestCase):

    # before each
    def setUp(self):
        self.file_service = Mock()
        self.media_repo = Mock()
        self.media_file_transformer = MediaFileTransformer(file_repo=self.file_service, media_repo=self.media_repo)

        self.movies_path = "/movies"
        self.tv_shows_path = "/tvshows"

        self.media_repo.movies_path = self.movies_path
        self.media_repo.tv_shows_path = self.tv_shows_path

    @parameterized.expand([
        ("Up (2009) [1080p].mkv", "Up (2009).mkv"),
        ("Big (1988).avi", "Big (1988).avi"),
        ("The.Shining.1980.US.1080p.BluRay.H264.AAC-RARBG.mp4", "The Shining (1980).mp4"),
        ('Charlie_Chaplin_The_Knockout.avi', 'The Knockout (1914).avi'),
    ])
    def test_transform_movie_file(self, original_movie_filename, expected_movie_filename):
        # arrange
        self.file_service.basename = lambda x: x
        # expected_new_path = os.path.join(self.movies_path, expected_movie_filename)

        # act
        self.media_file_transformer.transform_media_file_to_kodi_item(original_movie_filename)

        # assert
        self.media_repo.add_video_to_movies.assert_called_once_with(original_movie_filename, expected_movie_filename)

    # def test_transform_move_dir(self, original_dir, destination_media_dir):
        #

    # def test_transform_tv_show_directory(self, original_directory_name, destination_media_dir, expected_new_directory_name):
    #     pass

    # def test_transform_tv_show_season_directory(self, original_directory_name, destination_media_dir, expected_new_directory_name):
        # pass