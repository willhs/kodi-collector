import unittest
from parameterized import parameterized

from src.model.media_type import MediaType
from src.service.intelligence import classify_media_file, rename_movie_filename, rename_tv_show_filename


class IntelligenceTests(unittest.TestCase):
    @parameterized.expand([
        # single file
        "The.Insider.1999.1080p.BluRay.x265-RARBG.mkv",
        "The.Shining.1980.US.1080p.BluRay.H264.AAC-RARBG",
        "Big (1988)",
        "Charlie_Chaplin_The_Knockout.avi",
        "011836DVD Alpine Antics LT.avi",
        # in a dir
        "Up (2009) [1080p]/Up (2009) [1080p].avi",
        # movie collection
        "Star Wars Movie Collection (1977-2019)/Star Wars M01-M03 [Bluray] (1977-1983)/Star Wars M01 E04 A New Hope [BluRay] (1977 360p re-blurip).mp4"
    ])
    def test_classify_media_file_name_movies(self, filename):
        classification = classify_media_file(filename)
        self.assertEqual(MediaType.MOVIE, classification)

    @parameterized.expand([
        # single file
        "Silicon Valley S01E01.avi",
        # in full dir structure
        "Louis Theroux/S2-When Louis Met/WLM S02E04 - Max Clifford.avi",
        "Louis Theroux/S3/African Hunting Party.avi",
        "Fargo.1080p.WEB.H264-VIDEOHOLE/Season 4/Fargo.S04E01.1080p.WEB.H264-VIDEOHOLE.mkv",
        "The Simpsons/Season 1/The Simpsons S01E01.avi",
    ])
    def test_classify_media_file_name_tv_shows(self, filename):
        classification = classify_media_file(filename)
        self.assertEqual(MediaType.TV_SHOW, classification)

    @parameterized.expand([
        ("Up (2009) [1080p].mkv", "Up (2009).mkv"),
        ("Big (1988).avi", "Big (1988).avi"),
        ("The.Shining.1980.US.1080p.BluRay.H264.AAC-RARBG.mp4", "The Shining (1980).mp4"),
        ("Under_California_Stars.avi", "Under California Stars (1948).avi"),
        ("Charlie_Chaplin_The_Knockout.avi", "The Knockout (1914).avi"),
        ("011836DVD Alpine Antics LT.avi", "Alpine Antics (1936).avi"),
        ("04 Mission Impossible Ghost Protocol - Mystery 2011 Eng Ita Multi-Subs 720p [H264-mp4].mp4", "Mission Impossible Ghost Protocol (2011).mp4"),
        ("Cheech.and.Chong.Up.In.Smoke.1978.DVDRip.x264-HANDJOB.mvk", "Up in Smoke (1978).mkv")
    ])
    def test_rename_movie_filename(self, filename, expected_new_filename):
        new_filename = rename_movie_filename(filename)

        self.assertEqual(expected_new_filename, new_filename)

    @parameterized.expand([
        ("The Simpsons S01E01.avi", ["The Simpsons S01E01.avi", "The Simpsons (1989) S01E01.avi"]),
        ("Fargo.S04E01.1080p.WEB.H264-VIDEOHOLE.mkv", ["Fargo S04E01.mkv", "Fargo (2014) S04E01.mkv"]),
        ("Better Call Saul S05E01 Magic Man.mkv", ["Better Call Saul S05E01.mkv", "Better Call Saul (2015) S05E01.mkv"]),
        ("Inside No. 9 - S02 - E05 - Nana's Party.avi", ["Inside No. 9 S02E05.avi", "Inside No. 9 (2014) S02E05.avi"]),
        ("flash_gordon_ep01.avi", ["Flash Gordon (1954) S01E01.avi", "Flash Gordon S01E01 (1954).avi"]),
        ("Documentary.The.Power.Of.Nightmares.01.Baby.Its.Cold.Outside.avi", ["The Power Of Nightmares 01.avi", "The Power Of Nightmares (2004) 01.avi", "The Power Of Nightmares (2004) S01E01.avi", "Baby It's Cold Outside.avi", "Baby It's Cold Outside (2004).avi"]),
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
