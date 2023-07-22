import os
import argparse
from dotenv import load_dotenv

from src.repo.file_repo import FileRepository
from src.repo.media_repo import MediaRepository
from src.strategy.media_file_transformer import MediaFileTransformer


def collect_media(media_path):
    file_repo = FileRepository()
    transformer = MediaFileTransformer(
        file_repo=file_repo,
        media_repo=MediaRepository(file_repo)
    )

    transformer.transform_media_file_to_kodi_item(media_path)


if __name__ == "__main__":
    load_dotenv()

    parser = argparse.ArgumentParser(description='Process some files.')
    parser.add_argument('paths', nargs='+', help='the path(s) to the file(s) or directory(ies)')

    args = parser.parse_args()

    for path in args.paths:
        collect_media(path)
