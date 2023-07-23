import os
import unittest
from unittest.mock import Mock
from parameterized import parameterized

from src.repo.media_repo import MediaRepository
from src.strategy.media_file_collector import MediaFileCollector


class FileCollectionTests(unittest.TestCase):

    # before each
    def setUp(self):
        self.file_service = Mock()
        self.file_service.exists.return_value = False
        self.file_service.copy = Mock()
        self.file_service.basename = lambda x: x
        self.file_service.join = os.path.join

        self.media_repo = MediaRepository(file_service=self.file_service)
        self.media_file_collector = MediaFileCollector(file_service=self.file_service, media_repo=self.media_repo)

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
    def test_collect_movie_file(self, original_movie_filename, expected_movie_filename):
        # arrange
        expected_new_path = os.path.join(self.movies_path, expected_movie_filename)

        # act
        self.media_file_collector.collect_media_file(original_movie_filename)

        # assert
        self.file_service.copy.assert_called_once_with(original_movie_filename, expected_new_path)

    @parameterized.expand([
        ("The Simpsons S01E01.avi", [
            "The Simpsons/Season 1/The Simpsons S01E01.avi",
            "The Simpsons (1989)/Season 1/The Simpsons (1989) S01E01.avi"
         ]),
        ("Nathan for You S01E01 Yogurt Shop, Pizzeria.mp4", [
            "Nathan for You/Season 1/Nathan for You S01E01 Yogurt Shop, Pizzeria.mp4",
            "Nathan for You (2013)/Season 1/Nathan for You (2013) S01E01 Yogurt Shop, Pizzeria.mp4",
            "Nathan for You (2013)/Season 1/Nathan for You (2013) S01E01.mp4",
            "Nathan for You/Season 1/Nathan for You - Yogurt Shop, Pizzeria S01E01.mp4"
        ]),
    ])
    def test_collect_tv_show_file(self, original_tv_show_file, expected_new_tv_show_paths):
        # arrange
        expected_full_paths = list(map(
            lambda expected_path: os.path.join(self.tv_shows_path, expected_path),
            expected_new_tv_show_paths))

        # act
        self.media_file_collector.collect_media_file(original_tv_show_file)

        # assert
        actual_args = self.file_service.copy.call_args[0][1]
        self.assertIn(actual_args, expected_full_paths)

    # def test_collect_tv_show_directory(self, original_directory_name, destination_media_dir, expected_new_directory_name):
    #     pass

    # def test_collect_tv_show_season_directory(self, original_directory_name, destination_media_dir, expected_new_directory_name):
        # pass