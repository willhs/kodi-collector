def clean_filename(filename):
    # replace : with -
    filename = filename\
        .replace(":", " -")\
        .replace("/", "-")

    return filename
