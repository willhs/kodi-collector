import argparse
from dotenv import load_dotenv

from src.service.file_service import FileService
from src.repo.media_repo import MediaRepository
from src.strategy.media_file_collector import MediaFileCollector


def collect_media(media_path):
    file_service = FileService()
    collector = MediaFileCollector(
        file_service=file_service,
        media_repo=MediaRepository(file_service)
    )

    collector.collect_media_file(media_path)


if __name__ == "__main__":
    load_dotenv()

    parser = argparse.ArgumentParser(description='Process some files.')
    parser.add_argument('paths', nargs='+', help='the path(s) to the file(s) or directory(ies)')

    args = parser.parse_args()

    for path in args.paths:
        collect_media(path)
