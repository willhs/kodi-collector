# Kodi media collector
Use this program to collect media to your kodi media library.

## Set up
Install dependencies in your python environment
```
pip install -r requirements.txt
```

Copy .env.example to .env
```
cp .env.example .env
```

Add your kodi media library path for movies & tv show
```
MOVIE_LIBRARY_PATH=/Volumes/Video city/Movies
TV_SHOW_LIBRARY_PATH=/Volumes/Video city/TV Shows
GPT_API_KEY=your_gpt_api_key
```

Add kodi-collector to your path
```
export PATH=$PATH:/path/to/kodi-collector/script
```

## Usage
```
kodi-collector.sh <media-path>
```

The media-path can be any number of paths to media files or directories containing media files.

## What does it do?
1. Cleans media file names e.g. `The.Big.Bang.Theory.S01E01.720p.HDTV.x264-CTU.mkv` -> `The Big Bang Theory S01E01.mkv`
2. Classifies your media as either movie or tv show
3. Moves your media to the correct kodi library path
