import os.path
import string
import textwrap

from src.model.media import Media
from src.repo.gpt_repo import ask_gpt_for_response


def classify_media_file_name(raw_file_name) -> Media:
    gpt_system_prompt = textwrap.dedent("""
        You are a parser for filenames of downloaded media, either tv shows or movies. 
        Please classify the file given the filename as either a tv show ("tv show") or movie ("movie") based on your knowledge of media.
    """)

    messages = [
        {"role": "system", "content": gpt_system_prompt},
        {"role": "user", "content": 'Hercules_Against_the_Moonmen.avi'},
        {"role": "assistant", "content": 'movie'},
        {"role": "user", "content": 'The_Simpsons_S01E01.avi'},
        {"role": "assistant", "content": 'tv show'},
        {"role": "user", "content": f'{raw_file_name}'},
    ]

    gpt_response = ask_gpt_for_response(
        messages=messages,
        max_response_tokens=3
    )

    if "tv show" in gpt_response.lower():
        return Media.TV_SHOW
    elif "movie" in gpt_response.lower():
        return Media.MOVIE
    else:
        raise Exception(f"Unable to classify media file {raw_file_name}")


def rename_movie_filename(name) -> string:
    gpt_system_prompt = textwrap.dedent("""
        You are a smart filename parser for Kodi media player, specializing in movie files. 
        Your task is to clean up raw filenames into a preferred format: "Movie Name (Year)". 
        Rely on your extensive knowledge base to deduce the year of release. 
        If multiple movies exist with the same name, make your best educated guess to select the most probable one. 
        If you cannot determine the year, it's acceptable to leave it out. Here are good examples:

        - "The Avengers (2012)"
        - "Interstellar (2014)"

        Prioritize adding the year, even if not 100% certain. Omit it rather than guess. 
        In all cases, ensure the title is as accurate and well-formatted as possible.
    """)

    raw_file_name = os.path.splitext(name)[0]

    messages = [
        {"role": "system", "content": gpt_system_prompt},
        {"role": "user", "content": 'The_Kid'},
        {"role": "assistant", "content": 'The Kid (1921)'},
        {"role": "user", "content": 'The.Incredibles.2.2018.HDRip.XviD.AC3-EVO'},
        {"role": "assistant", "content": 'The Incredibles 2 (2018)'},
        {"role": "user", "content": f"{raw_file_name}"}
    ]

    response = ask_gpt_for_response(messages, 20)

    file_extension = os.path.splitext(name)[1]
    return f"{response}{file_extension}"


def rename_tv_show_filename(name) -> string:
    gpt_system_prompt = textwrap.dedent("""
        You are a smart filename parser for Kodi media player, specializing in tv show files. Your task is to clean up raw filenames into a preferred format: "TV Show Name (Year) SXXEYY". 
        Rely on your extensive knowledge base to deduce the year of release. If multiple tv shows exist with the same name, make your best educated guess to select the most probable one. 
        If you cannot determine the year, it's acceptable to leave it out. Here are good examples:

        - "The Simpsons (1989) S01E01"
        - "Whose Line Is It Anyway (1998) S02E08"

        Prioritize adding the year, even if not 100% certain. Omit it rather than guess. In all cases, ensure the title is as accurate and well-formatted as possible.
    """)

    raw_file_name = os.path.splitext(name)[0]

    messages = [
        {"role": "system", "content": gpt_system_prompt},
        {"role": "user", "content": 'The_Kid'},
        {"role": "assistant", "content": 'The Kid (1921)'},
        {"role": "user", "content": 'The.Incredibles.2.2018.HDRip.XviD.AC3-EVO'},
        {"role": "assistant", "content": 'The Incredibles 2 (2018)'},
        {"role": "user", "content": f"{raw_file_name}"}
    ]

    response = ask_gpt_for_response(messages, 20)

    file_extension = os.path.splitext(name)[1]
    return f"{response}{file_extension}"
