import argparse

from dotenv import load_dotenv

from src.service.file.file_service import FileService
from src.repo.media_repo import MediaRepository
from src.strategy.media_file_collector import MediaFileCollector


def start():
    load_dotenv()

    parser = argparse.ArgumentParser(description='Process some files.')
    parser.add_argument('paths', nargs='+', help='the path(s) to the file(s) or directory(ies)')

    args = parser.parse_args()
    collect_media(*args.paths)


def collect_media(*media_paths):
    print(f"Collecting media files: {media_paths}")
    for path in media_paths:
        collect_media_path(path)


def collect_media_path(media_path):
    print(f"Collecting media file: {media_path}")
    file_service = FileService()
    collector = MediaFileCollector(
        file_service=file_service,
        media_repo=MediaRepository(file_service)
    )

    collector.collect_media_file(media_path)
