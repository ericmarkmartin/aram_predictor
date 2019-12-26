import os
from itertools import islice

from dotenv import load_dotenv

load_dotenv()

RIOT_API_KEY = os.getenv("RIOT_API_KEY")
SEED_SUMMONER = os.getenv("SEED_SUMMONER")
