from src.model.media_type import MediaType
from src.repo.file_repo import FileRepository
from src.repo.media_repo import MediaRepository
from src.service.intelligence import classify_media_file_name, rename_movie_filename, rename_tv_show_filename

import logging
logger = logging.getLogger(__name__)


class MediaFileTransformer:
    """
    Transforms a media file into a Kodi item.

    A media file is either:
    - a movie file
    - a tv show file
    - a directory containing one or more of the above

    Ideally this class can transform a raw dir tree of downloaded media
    into a new dir tree of media ready to be added to Kodi.
    """

    def __init__(self,
                 file_repo: FileRepository,
                 media_repo: MediaRepository):
        self.file = file_repo
        self.media_repo = media_repo

    def transform_media_file_to_kodi_item(self, media_path: str):
        print(f"Processing {media_path}")
        # is_file = self.file.is_file(media_path)

        # if not is_file:
        #     logging.error("Not a file")
        #     return

        try:
            # media_classification = classify_media_file_name(self.file.basename(media_path))
            media_classification = MediaType.MOVIE
        except Exception:
            logger.error(f"Unable to classify media file {media_path}")
            return

        print(f"Classified as {media_classification}")

        new_media_filename = rename_movie_filename(media_path) \
            if media_classification == MediaType.MOVIE \
            else rename_tv_show_filename(media_path)

        print(f"Cleaned name: {new_media_filename}")

        # copy to new file to movies or tv shows directory depending on the classification
        if media_classification == MediaType.MOVIE:
            self.media_repo.add_video_to_movies(media_path, new_media_filename)
        elif media_classification == MediaType.TV_SHOW:
            self.media_repo.add_tv_show_dir_to_tv_shows(media_path, new_media_filename)

    def get_dir_structure(self, root_dir):
        dir_structure = {}

        for dirpath, dirnames, filenames in self.file.walk(root_dir):
            current_dir = self.file.relpath(dirpath, root_dir)
            dir_structure[current_dir] = filenames

        return dir_structure

    def make_new_dir_structure(self, old_dir_structure):
        # Placeholder function to create new directory structure
        # TODO: Implement directory structure logic
        return old_dir_structure
