from src.model.media_type import MediaType
from src.service.file.file_service import FileService
from src.repo.media_repo import MediaRepository
from src.service.intelligence import rename_movie_file, rename_tv_show_filename, classify_media_file

import logging

logger = logging.getLogger(__name__)

video_file_extensions = [".mkv", ".avi", ".mp4", ".m4v", ".mpg", ".ogg", ".wmv", ".mov", ".flv", ".webm", ".vob"]


class MediaFileCollector:
    """
    collects a media file into a Kodi item.

    A media file is either:
    - a movie file
    - a tv show file
    - a directory containing one or more of the above

    Ideally this class can collect a raw dir tree of downloaded media
    into a new dir tree of media ready to be added to Kodi.
    """

    def __init__(self,
                 file_service: FileService,
                 media_repo: MediaRepository):
        self.file_service = file_service
        self.media_repo = media_repo

    def collect_media_file(self, media_path: str):
        if not self.file_service.exists(media_path):
            raise Exception(f"Path {media_path} does not exist")

        print(f"Processing:\t{media_path}")
        is_file = self.file_service.is_file(media_path)

        if not is_file:
            return self.collect_media_directory(media_path)

        if not self.is_video_file(media_path):
            logging.error(f"Path {media_path} is not a video file")
            return

        # basename = self.file_service.basename(media_path)
        # parent_dir = self.file_service.basename(self.file_service.dirname(media_path))

        try:
            media_classification = classify_media_file(media_path)
        except Exception as e:
            logger.error(f"Unable to classify media file {media_path} because of\n{str(e)}")
            return

        print(f"Classified as\t{media_classification.name}")

        new_media_filename = rename_movie_file(media_path) \
            if media_classification == MediaType.MOVIE \
            else rename_tv_show_filename(media_path)

        print(f"Cleaned:\t{new_media_filename}")

        # copy to new file to movies or tv shows directory depending on the classification
        if media_classification == MediaType.MOVIE:
            self.media_repo.add_video_to_movies(media_path, new_media_filename)
        elif media_classification == MediaType.TV_SHOW:
            try:
                self.media_repo.add_video_to_tv_shows(media_path, new_media_filename)
            except Exception as e:
                logger.error(f"Unable to add video to tv shows: {e}")

    def collect_media_directory(self, media_path):
        """
        collect all media files in the directory, recursively
        """
        print(f"Processing directory: {media_path}")

        for file in self.file_service.list_dir(media_path):
            path = self.file_service.join(media_path, file)
            self.collect_media_file(path)

    def is_video_file(self, filename):
        """
        Check if a file is a video file
        """
        _, file_extension = self.file_service.splitext(filename)
        return file_extension in video_file_extensions
