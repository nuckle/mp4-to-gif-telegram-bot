from os import getenv

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
TG_TOKEN = getenv("TG_TOKEN")
FOLDER = getenv("FOLDER") or 'media/'
GIF_PARAMS = [
    "-vf",
    "fps=14,scale=320:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse",
]
