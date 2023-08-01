#!/usr/bin/env python3

import os

from src.program import collect_media_path

torrent_name = os.getenv('TR_TORRENT_NAME')
torrent_dir = os.getenv('TR_TORRENT_DIR')

collect_media_path(torrent_dir)
