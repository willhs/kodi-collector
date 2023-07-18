import unittest

from parameterized import parameterized

from src.model.media import Media
from src.service.ai_service import classify_media_file_name, rename_movie_filename, rename_tv_show_filename


class MediaFileHandlerTests(unittest.TestCase):
    @parameterized.expand([
        ("Up (2009) [1080p]", Media.MOVIE),
        ("The.Insider.1999.1080p.BluRay.x265-RARBG", Media.MOVIE),
        ("Fargo.S04E01.1080p.WEB.H264-VIDEOHOLE", Media.TV_SHOW),
        ("Mr Robot Season 3 1080p skunktastic", Media.TV_SHOW),
        ("The Simpsons S01E01.avi", Media.TV_SHOW),
        ("Big (1988)", Media.MOVIE),
        ("The.Shining.1980.US.1080p.BluRay.H264.AAC-RARBG", Media.MOVIE),
        ("Under_California_Stars.avi", Media.MOVIE),
        ("The Wire Season 1", Media.TV_SHOW),
        ("Charlie_Chaplin_The_Knockout.avi", Media.MOVIE)
    ])
    def test_classify_media_file_name(self, filename, expected_classification):
        classification = classify_media_file_name(filename)

        self.assertEqual(expected_classification, classification)

    @parameterized.expand([
        ("Up (2009) [1080p].mkv", "Up (2009).mkv"),
        ("Big (1988).avi", "Big (1988).avi"),
        ("The.Shining.1980.US.1080p.BluRay.H264.AAC-RARBG.mp4", "The Shining (1980).mp4"),
        ("Under_California_Stars.avi", "Under California Stars (1948).avi"),
        ("Charlie_Chaplin_The_Knockout.avi", "The Knockout (1914).avi"),
    ])
    def test_rename_movie_filename(self, filename, expected_new_filename):
        new_filename = rename_movie_filename(filename)

        self.assertEqual(expected_new_filename, new_filename)

    @parameterized.expand([
        ("The Simpsons S01E01.avi", ["The Simpsons S01E01.avi", "The Simpsons (1989) S01E01.avi"]),
        ("Fargo.S04E01.1080p.WEB.H264-VIDEOHOLE.mkv", ["Fargo S04E01.mkv", "Fargo (2014) S04E01.mkv"]),
        ("Better Call Saul S05E01 Magic Man.mkv", ["Better Call Saul S05E01.mkv", "Better Call Saul (2015) S05E01.mkv"]),
        ("Inside No. 9 - S02 - E05 - Nana's Party.avi", ["Inside No. 9 S02E05.avi", "Inside No. 9 (2014) S02E05.avi"]),
    ])
    def test_rename_tv_show_filename(self, filename, expected_new_filenames):
        new_filename = rename_tv_show_filename(filename)

        self.assertTrue(new_filename in expected_new_filenames,
                        f"Expected {new_filename} to be one of {expected_new_filenames}")


    # @parameterized.expand([
    #     ("Mr Robot Season 3 1080p skunktastic", "Mr. Robot (2015) Season 3"),
    #     ("The Wire Season 1", "The Wire Season 1 (2002)"),
    # ])
    # def test_rename_media_directory(self, directory, expected_new_directory):
    #     new_directory = rename_media_directory(directory)
    #
    #     self.assertEqual(expected_new_directory, new_directory)


if __name__ == '__main__':
    unittest.main()
