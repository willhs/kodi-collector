import os
import shutil

from dotenv import load_dotenv

from src.model.media import Media
from src.service.ai_service import classify_media_file, rename_movie_filename

home_dir = os.path.expanduser('~')
# torrent_downloads_dir = os.path.join(home_dir, "Downloads", "torrent")
script_dir = os.path.dirname(os.path.realpath(__file__))

# Build the path to the directory or file you want
examples_dir = os.path.join(script_dir, 'res', 'example')

torrent_downloads_dir = examples_dir
# test_downloaded_file = os.path.join(torrent_downloads_dir, "Woman_in_Brown.avi")
# test_downloaded_file = os.path.join(torrent_downloads_dir, ".avi")

videos_dir = os.path.join(home_dir, "videos")
movies_dir = os.path.join(videos_dir, "movies")
tv_shows_dir = os.path.join(videos_dir, "tvshows")


def get_dir_structure(root_dir):
    dir_structure = {}

    for dirpath, dirnames, filenames in os.walk(root_dir):
        current_dir = os.path.relpath(dirpath, root_dir)
        dir_structure[current_dir] = filenames

    return dir_structure


def make_new_dir_structure(old_dir_structure):
    # Placeholder function to create new directory structure
    # TODO: Implement directory structure logic
    return old_dir_structure


def process_torrent(torrent_path):
    print(f"Processing {torrent_path}")
    is_file = os.path.isfile(torrent_path)

    if not is_file:
        print("Not a file or directory")
        return

    media_classification = classify_media_file(os.path.basename(torrent_path))
    print(f"Classified as {media_classification}")

    new_media_filename = rename_movie_filename(torrent_path) \
        if media_classification == Media.MOVIE \
        else rename_tv_show_filename(torrent_path)

    # copy to new file to movies or tv shows directory depending on the classification
    new_directory = movies_dir if media_classification == Media.MOVIE else tv_shows_dir
    new_file_path = os.path.join(new_directory, new_media_filename)
    shutil.copy(torrent_path, new_file_path)

# Driver code
def main():
    # get the first file in the test directory
    test_downloaded_file = os.path.join(torrent_downloads_dir, os.listdir(torrent_downloads_dir)[0])
    process_torrent(test_downloaded_file)


if __name__ == "__main__":
    load_dotenv()
    main()
