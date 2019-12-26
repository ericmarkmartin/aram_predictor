from match_crawler import cass_setup, crawl_matches
from settings import RIOT_API_KEY, SEED_SUMMONER

from itertools import islice

import cassiopeia as cass
import pandas as pd


DF_COLUMNS = ["match_id"] + [
    "{}_{}".format(side, i) for side in ["blue", "red"] for i in range(1, 6)
]


def champions_from_match(match):
    return [
        participant.champion
        for team in match.teams
        for participant in team.participants
    ]


def row_from_match(match):
    return [match.id] + [champion.id for champion in champions_from_match(match)]


def df_from_matches(matches):
    return pd.DataFrame(
        (row_from_match(match) for match in matches), columns=DF_COLUMNS
    )


if __name__ == "__main__":
    cass_setup(RIOT_API_KEY, "NA")
    seed_summoner = cass.get_summoner(name=SEED_SUMMONER)
    poro_kings = islice(
        (
            match
            for match in crawl_matches(seed_summoner, 10)
            if match.mode == cass.GameMode.poro_king
        ),
        20,
    )
    df = df_from_matches(poro_kings)
    df.to_csv(path_or_buf="matches.csv")
