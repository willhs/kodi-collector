import os
import argparse
from dotenv import load_dotenv

from src.strategy.torrent_file_mover import process_torrent


def main(path):
    process_torrent(path)


if __name__ == "__main__":
    load_dotenv()

    parser = argparse.ArgumentParser(description='Process a torrent file.')
    parser.add_argument('path', type=str, help='the path to the torrent file or directory')

    args = parser.parse_args()

    main(args.path)
