import re

import logging

logger = logging.getLogger(__name__)


def make_path_for_movie(movies_library_dir, video_name, file_service):
    return file_service.join(movies_library_dir, video_name)


def make_path_for_tv_show(tv_shows_library_dir, video_name, file_service):
    try:
        # Create a regular expression pattern that matches formats like:
        # "The Simpsons S01E01.avi", "Fargo.S04E01.1080p.WEB.H264-VIDEOHOLE.mkv",
        # "Better Call Saul S05E01 Magic Man.mkv", "Inside No. 9 - S02 - E05 - Nana's Party.avi"
        pattern = re.compile(r"(.+?)[\s\.]-?\s*S(\d+)[\s\.Ee-]+(\d+)")

        # Use the pattern to match the video_name
        match = pattern.match(video_name)

        if match:
            # If a match is found, the tv show name is the first group in the match
            tv_show_name = match.group(1)

            # The season number is the second group in the match
            season_number = int(match.group(2))
        else:
            logger.warning(f"Unable to parse season number from video name: {video_name}. Assuming Season 1.")
            tv_show_name = video_name
            season_number = 1

        return file_service.join(tv_shows_library_dir, tv_show_name, f"Season {season_number}", video_name)

    except Exception as e:
        logger.error(f"Error when trying to parse tv show name and season number from {video_name}")
        logger.error(f"Error: {e}")
        return
