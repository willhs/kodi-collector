import os.path
import string
import textwrap

from src.model.media_type import MediaType
from src.service.filename_cleaner import clean_filename
from src.service.gpt import ask_gpt_for_response


def classify_media_file_name(filename, parent_directory) -> MediaType:
    gpt_system_prompt = textwrap.dedent("""
    You are a smart classifier of downloaded media files for Kodi media player which matches files with the www.themoviedb.org's movie / tv show classifications.
    Your task is to classify each given filename (with its parent directory name as context) as either a tv show ("tv show") or a movie ("movie"). 
    Lean on your knowledge of media when possible as the file and parent directory naming can be inconsistent.
    If in doubt given your knowledge of media: if it looks to be episodic, classify it as a tv show, otherwise if it is a singular work classify it as a movie.
    A documentary is considered a movie unless its episodic then its a tv show.

    For example, a filename like "The.Matrix.1999.1080p.BrRip.x264.mp4" with parent directory "The Matrix" should be classified as a "movie", while a filename like "Game.of.Thrones.S01E01.720p.HDTV.x264.mp4" in parent directory "Season 1" should be classified as a "tv show".

    Given the filename, parent directory and your knowledge of media, please classify it as either a "tv show" or a "movie".
    """)

    messages = [
        {"role": "system", "content": f"{gpt_system_prompt}"},
        {"role": "user", "content": 'filename: Madagascar.DVDRip.XviD-DoNE.avi, parent directory: Madagascar'},
        {"role": "assistant", "content": 'movie'},
        {"role": "user", "content": 'filename: The_Simpsons_S01E01.avi, parent directory: Season 1'},
        {"role": "assistant", "content": 'tv show'},
        {"role": "user", "content": 'filename: Baseball - Inning 06_-_1991_-_Ken Burns.mp4, parent directory: (1994) Baseball'},
        {"role": "assistant", "content": 'tv show'},
        {"role": "user", "content": 'filename: Wallace and Gromit in A Grand Day Out.avi, parent directory: Wallace and Gromit Film Collection'},
        {"role": "assistant", "content": 'movie'},
        {"role": "user", "content": f'filename: {filename}, parent directory: {parent_directory}'},
    ]

    gpt_response = ask_gpt_for_response(
        # model="gpt-4",
        messages=messages,
        max_response_tokens=3
    )

    if "tv show" in gpt_response.lower():
        return MediaType.TV_SHOW
    elif "movie" in gpt_response.lower():
        return MediaType.MOVIE
    else:
        raise Exception(f"GPT couldn't classify {filename} ({gpt_response})")


def rename_movie_filename(filename, parent_directory) -> string:
    gpt_system_prompt = textwrap.dedent("""
        You are a smart filename parser for Kodi media player, specializing in movie files. 
        Your task is to clean up raw filenames (with parent directory for context) into a preferred format: "Movie Name (Year)". 
        Rely on your extensive knowledge base to deduce the year of release. 
        If multiple movies exist with the same name, make your best educated guess to select the most probable one. 
        Prioritize adding the year, even if not 100% certain. Omit it rather than guess. 
        If you cannot determine the year, it's acceptable to leave it out.

        Here are good examples:
        - "The Avengers (2012)"
        - "Interstellar (2014)"
        - "The Year of the Killer Bees!"

        In all cases, ensure the title is as accurate and well-formatted as possible.
    """)

    raw_file_name, file_extension = os.path.splitext(filename)

    messages = [
        {"role": "system", "content": gpt_system_prompt},
        {"role": "user", "content": 'filename: The_Kid, parent directory: Charlie_Chaplin'},
        {"role": "assistant", "content": 'The Kid (1921)'},
        {"role": "user", "content": 'filename: The.Incredibles.2.2018.HDRip.XviD.AC3-EVO, parent directory: torrent'},
        {"role": "assistant", "content": 'The Incredibles 2 (2018)'},
        {"role": "user", "content": f"filename: {raw_file_name}, parent directory: {parent_directory}"}
    ]

    new_name = ask_gpt_for_response(messages, 20)
    cleaned_new_name = clean_filename(new_name)

    return f"{cleaned_new_name}{file_extension}"


def rename_tv_show_filename(name, parent_directory) -> string:
    gpt_system_prompt = textwrap.dedent("""
        You are a smart filename cleaner for Kodi media player, specializing in tv show files. 
        Your task is to clean up raw filenames into a preferred format: "TV Show Name (Year) SXXEYY" where XX is the season number and YY is the episode number.
        Rely on your extensive knowledge base to deduce the year of release. If multiple tv shows exist with the same name, make your best educated guess to select the most probable one. 
        The filename and parent directory are provided as context.
        If you cannot make a good estimate of the year, it's acceptable to leave it out. 
        If the season is unspecified, assume it is season 1.
        
        Here are good examples:
        - "filename: The Simpsons (1989) S01E01 - Simpsons Roasting on an Open Fire, parent directory: Season 1"
        - "filename: Whose Line Is It Anyway (1998) S02E08, parent directory: Whose Line is Anyway Season 2"
        - "filename: Beasly Boys S01E01, parent directory: Best of Beasly Boys"

        In all cases, ensure the title is as accurate and well-formatted as possible.
    """)

    raw_file_name = os.path.splitext(name)[0]

    messages = [
        {"role": "system", "content": gpt_system_prompt},
        {"role": "user", "content": "filename: One-Punch.Man.02.1080p.AnimeRG.[KoTuWa].mkv, parent directory: One-Punch.Man.S02.COMPLETE.JAPANESE.720p.HULU.WEBRip.x264-GalaxyTV[TGx]"},
        {"role": "assistant", "content": "One Punch Man (2015) S01E02"},
        {"role": "user", "content": "filename: South.Park.S24E01.The.Pandemic.Special.1080p.AHDTV.x264-DARKFLiX.mkv, parent directory: South.Park.The.Pandemic.Special.1080p"},
        {"role": "assistant", "content": "South Park (1997) S24E01"},
        {"role": "user", "content": f"filename: {raw_file_name}, parnet directory: {parent_directory}"}
    ]

    response = ask_gpt_for_response(messages, 20)

    file_extension = os.path.splitext(name)[1]
    return f"{response}{file_extension}"
