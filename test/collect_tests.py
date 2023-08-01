import os
from unittest import TestCase
from unittest.mock import Mock

from parameterized import parameterized
from src.repo.media_repo import MediaRepository
from src.service.file.file_service import FileService
from src.strategy.media_file_collector import MediaFileCollector

MOVIES_PATH = "/movies"
TV_SHOWS_PATH = "/tv_shows"


class FileCollectionTests(TestCase):

    def setUp(self):
        self.mock_file_service = Mock(spec=FileService)

        self.media_repo = MediaRepository(file_service=self.mock_file_service)
        self.media_repo.movies_path = MOVIES_PATH
        self.media_repo.tv_shows_path = TV_SHOWS_PATH

        self.media_file_collector = MediaFileCollector(file_service=self.mock_file_service, media_repo=self.media_repo)

        self.mock_file_service.splitext = lambda x: os.path.splitext(x)
        self.mock_file_service.basename = lambda x: os.path.basename(x)
        self.mock_file_service.dirname = lambda x: os.path.dirname(x)
        self.mock_file_service.join = lambda *xs: os.path.join(*xs)

        self.mock_file_service.exists.return_value = False

    @parameterized.expand([
        (f"Up (2009) [1080p].mkv", f"{MOVIES_PATH}/Up (2009).mkv"),
        ("Big (1988).avi", f"{MOVIES_PATH}/Big (1988).avi"),
        ("The.Shining.1980.US.1080p.BluRay.H264.AAC-RARBG.mp4", f"{MOVIES_PATH}/The Shining (1980).mp4"),
        ('Charlie_Chaplin_The_Knockout.avi', f'{MOVIES_PATH}/The Knockout (1914).avi'),
        # ('The.Road.to.El.Dorado.2000.WS.DVDRip.XViD.iNT-EwDp/ewdp-rted.avi', f'{MOVIES_PATH}/The Road to El Dorado (2000).avi'),
    ])
    def test_collect_movie_file(self, original_movie_filename, expected_new_path):
        # arrange
        self.mock_file_service.is_file.return_value = True

        # only when the file service is asked if the original file exists, return True
        self.mock_file_service.exists = lambda x: x == original_movie_filename

        # act: The real function is not called and no actual file I/O is performed
        self.media_file_collector.collect_media_file(original_movie_filename)

        # assert: Check if copy was called with the right arguments
        self.mock_file_service.copy.assert_called_once_with(original_movie_filename, expected_new_path)

    @parameterized.expand([
        ("Silicon Valley S01E01.avi", [
            f"{TV_SHOWS_PATH}/Silicon Valley/Season 1/Silicon Valley S01E01.avi",
            f"{TV_SHOWS_PATH}/Silicon Valley (2014)/Season 1/Silicon Valley (2014) S01E01.avi"
        ]),
        ("Nathan for You S02E08 Yogurt Shop, Pizzeria.mp4", [
            f"{TV_SHOWS_PATH}/Nathan for You/Season 2/Nathan for You S02E08 Yogurt Shop, Pizzeria.mp4",
            f"{TV_SHOWS_PATH}/Nathan for You (2013)/Season 2/Nathan for You (2013) S02E08 Yogurt Shop, Pizzeria.mp4",
            f"{TV_SHOWS_PATH}/Nathan for You (2013)/Season 2/Nathan for You (2013) S02E08.mp4",
            f"{TV_SHOWS_PATH}/Nathan for You/Season 2/Nathan for You - Yogurt Shop, Pizzeria S02E08.mp4"
        ]),
    ])
    def test_collect_tv_show_file(self, original_tv_show_file, acceptable_new_tv_show_paths):
        # arrange
        self.mock_file_service.is_file.return_value = True
        self.mock_file_service.exists = lambda x: x == original_tv_show_file

        acceptable_new_tv_show_paths_full = list(map(
            lambda expected_path: self.mock_file_service.join(TV_SHOWS_PATH, expected_path),
            acceptable_new_tv_show_paths))

        # act
        self.media_file_collector.collect_media_file(original_tv_show_file)

        # assert whether the copy function was called with the right arguments
        # Get the args the mock copy method was called with
        copy_args = self.mock_file_service.copy.call_args_list

        self.assertEqual(1, len(copy_args))

        # Check that copy was called with the right src (first argument to copy)
        self.assertEqual(copy_args[0][0][0], original_tv_show_file)

        # Check that copy was called with an acceptable dst (second argument to copy)
        self.assertIn(copy_args[0][0][1], acceptable_new_tv_show_paths_full)

    @parameterized.expand([
        ("Season 1",
         [
             "Silicon Valley S01E01 (2014).avi",
             "Silicon Valley S01E02 (2014).avi"
         ],
         [
             f"{TV_SHOWS_PATH}/Silicon Valley (2014)/Season 1/Silicon Valley (2014) S01E01.avi",
             f"{TV_SHOWS_PATH}/Silicon Valley (2014)/Season 1/Silicon Valley (2014) S01E02.avi",
         ],
         ),
        ("Pixar greatest movies 1990 - 2015",
         [
             f"Up (2009).mkv",
             f"Inside Out (2015).mkv"
         ],
         [
             f"{MOVIES_PATH}/Up (2009).mkv",
             f"{MOVIES_PATH}/Inside Out (2015).mkv"
         ]
         ),
    ])
    def test_collect_directory_single_level(self, original_directory_name, files_in_dir, expected_new_paths):
        # arrange
        file_paths = list(map(lambda x: os.path.join(original_directory_name, x), files_in_dir))
        self.mock_file_service.is_file = lambda x: x in file_paths
        self.mock_file_service.exists = lambda x: x == original_directory_name or x in file_paths
        self.mock_file_service.list_dir = lambda x: files_in_dir

        # act
        self.media_file_collector.collect_media_file(original_directory_name)

        # assert
        for expected_new_path in expected_new_paths:
            self.assertTrue(self.mock_file_service.copy.called_with(expected_new_path))

    # @parameterized.expand([
    #     (
    #             {
    #                 "root": [
    #                     {
    #                         "Futurama (2006)": [
    #                             "Futurama S01E01.avi",
    #                             "Futurama S01E02.avi",
    #                             {
    #                                 "Season 2": [
    #                                     "Futurama S02E01.avi",
    #                                     "Futurama S02E02.avi"
    #                                 ]
    #                             }
    #                         ]
    #                     }
    #                 ]
    #             },
    #             [
    #                 f"{TV_SHOWS_PATH}/Futurama (2006)/Season 1/Futurama S01E01.avi",
    #                 f"{TV_SHOWS_PATH}/Futurama (2006)/Season 1/Futurama S01E02.avi",
    #                 f"{TV_SHOWS_PATH}/Futurama (2006)/Season 2/Futurama S02E01.avi",
    #                 f"{TV_SHOWS_PATH}/Futurama (2006)/Season 2/Futurama S02E02.avi",
    #             ]
    #     )
    # ])
    # def test_collect_directory_recursive(self, original_directory_structure, expected_new_paths):
    #     def setup_mock_files(mock_file_service, mock_file_service, nested_dict, root_path=""):
    #         for key, value in nested_dict.items():
    #             if isinstance(value, list):
    #                 for item in value:
    #                     if isinstance(item, dict):
    #                         setup_mock_files(mock_file_service, mock_file_service, item, os.path.join(root_path, key))
    #                     else:
    #                         file_path = os.path.join(root_path, key, item)
    #                         mock_file_service.create_file(file_path)
    #                         mock_file_service.exists.return_value = True
    #
    #     # arrange
    #     file_service = fake_filesystem.FakeFilesystem()
    #     self.file_service = fake_filesystem.FakeFilesystem()
    #     setup_mock_files(file_service, self.file_service, original_directory_structure)
    #
    #     # act
    #     self.media_file_collector.collect_media_file("root")
    #
    #     # assert
    #     for expected_new_path in expected_new_paths:
    #         assert self.file_service.exists(expected_new_path)
