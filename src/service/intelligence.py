import os.path
import string
import textwrap

from src.model.media_type import MediaType
from src.service.filename_cleaner import clean_filename
from src.service.gpt import ask_gpt_for_response


def classify_media_file(path) -> MediaType:
    gpt_system_prompt = textwrap.dedent("""
    You are a smart classifier of downloaded media files for Kodi media player which matches files with the www.themoviedb.org's movie or tv show classifications.
    Your task is to classify each given file (path) as either a tv show ("tv show") or a movie ("movie"). 
    Lean on your knowledge of media when possible.
    For example, a file like "The Matrix/The.Matrix.1999.1080p.BrRip.x264.mp4" should be classified as a "movie", while a file like "Game.of.Thrones.720p.HDTV.x264/Season 1/Game.of.Thrones.S01E01.720p.HDTV.x264.mp4".
    If in doubt given your knowledge of media: if it looks to be episodic, classify it as a tv show, otherwise if it is a singular work classify it as a movie.
    A documentary is considered a movie unless its episodic then its a tv show.
    """)
    # Given the filename, parent directory and your knowledge of media, please classify it as either a "tv show" or a "movie".

    messages = [
        {"role": "system", "content": f"{gpt_system_prompt}"},
        {"role": "user", "content": 'Madagascar.DVDRip.XviD-DoNE/Madagascar.DVDRip.XviD-DoNE.avi'},
        {"role": "assistant", "content": 'movie'},
        {"role": "user", "content": 'The_Simpsons/Season 1/The_Simpsons_S01E01.avi'},
        {"role": "assistant", "content": 'tv show'},
        {"role": "user", "content": '(1994) Baseball/Baseball_-_Inning 06_-_1991_-_Ken_Burns.mp4'},
        {"role": "assistant", "content": 'tv show'},
        {"role": "user", "content": 'Wallace and Gromit Film Collection/Wallace and Gromit in A Grand Day Out.avi'},
        {"role": "assistant", "content": 'movie'},
        {"role": "user", "content": f'{path}'},
    ]

    gpt_response = ask_gpt_for_response(
        messages=messages,
        max_response_tokens=3,
        # model="gpt-4",
    )

    if "tv show" in gpt_response.lower():
        return MediaType.TV_SHOW
    elif "movie" in gpt_response.lower():
        return MediaType.MOVIE
    else:
        raise Exception(f"GPT couldn't classify {path})")


def rename_movie_file(path) -> string:
    gpt_system_prompt = textwrap.dedent("""
        You are a smart filename parser for Kodi media player, specializing in movie files. 
        Your task is to clean up raw file paths into a preferred format: "Movie Name (Year)". 
        Rely on your extensive knowledge base to deduce the year of release. 
        If multiple movies exist with the same name, make your best educated guess to select the most probable one. 
        Prioritize adding the year, even if not 100% certain. Omit it rather than guess. 
        If you cannot determine the year, it's acceptable to leave it out.
        In all cases, ensure the title is as accurate and well-formatted as possible.
    """)

    # Here are good examples:
    # - "The Avengers (2012)"
    # - "Interstellar (2014)"
    # - "The Year of the Killer Bees!"

    # raw_path, file_extension = os.path.splitext(path)

    messages = [
        {"role": "system", "content": gpt_system_prompt},
        {"role": "user", "content": 'The_Kid.mp4'},
        {"role": "assistant", "content": 'The Kid (1921).mp4'},
        {"role": "user", "content": 'torrent/The.Incredibles.2.2018.HDRip.XviD.AC3-EVO.avi'},
        {"role": "assistant", "content": 'The Incredibles 2 (2018).avi'},
        {"role": "user", "content": f"{path}"}
    ]

    new_filename = ask_gpt_for_response(
        messages=messages,
        max_response_tokens=20,
        # model="gpt-4"
    )
    cleaned_new_filename = clean_filename(new_filename)

    return f"{cleaned_new_filename}"


def rename_tv_show_filename(path) -> string:
    gpt_system_prompt = textwrap.dedent("""
        You are a smart filename cleaner for Kodi media player, specializing in tv show files.
        Your task is take a file path and change into the preferred format: "TV Show Name (Year) SXXEYY" where XX is the season number and YY is the episode number.
        Rely on your extensive knowledge base to deduce the year of release. If multiple tv shows exist with the same name, make your best educated guess to select the most probable one. 
        The file path is provided as context.
        If you cannot make a good estimate of the year, it's acceptable to leave it out. 
        If the season is unspecified, assume it is season 1.
        In all cases, ensure the title is as accurate and well-formatted as possible.
    """)

    # Here are good examples:
    # - "filename: The Simpsons (1989) S01E01 - Simpsons Roasting on an Open Fire, parent directory: Season 1"
    # - "filename: Whose Line Is It Anyway (1998) S02E08, parent directory: Whose Line is Anyway Season 2"
    # - "filename: Beasly Boys S01E01, parent directory: Best of Beasly Boys"

    # raw_file_name = os.path.splitext(path)[0]

    messages = [
        {"role": "system", "content": gpt_system_prompt},
        {"role": "user", "content": "One-Punch.Man.S01.COMPLETE.JAPANESE.720p.HULU.WEBRip.x264-GalaxyTV[TGx]/One-Punch.Man.02.1080p.AnimeRG.[KoTuWa].avi"},
        {"role": "assistant", "content": "One Punch Man (2015) S01E02.avi"},
        {"role": "user", "content": "South.Park.The.Pandemic.Special.1080p/South.Park.S24E01.The.Pandemic.Special.1080p.AHDTV.x264-DARKFLiX.mkv"},
        {"role": "assistant", "content": "South Park (1997) S24E01.mkv"},
        {"role": "user", "content": f"{path}"}
    ]

    response = ask_gpt_for_response(messages, 20)

    # file_extension = os.path.splitext(name)[1]
    # return f"{response}{file_extension}"

    return f"{response}"
