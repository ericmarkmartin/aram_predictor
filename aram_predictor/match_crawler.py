from settings import RIOT_API_KEY, SEED_SUMMONER

from itertools import islice

import cassiopeia as cass


def cass_setup(key, region):
    cass.set_riot_api_key(key)
    cass.set_default_region(region)


def crawl_matches(seed_summoner, matches_per_summoner):
    matches = set()
    visited = set()
    to_visit = {seed_summoner.id}

    while len(to_visit) > 0:
        summoner_id = to_visit.pop()
        summoner = cass.get_summoner(id=str(summoner_id))
        match_history = islice(summoner.match_history, matches_per_summoner)

        visited.add(summoner_id)
        for match in match_history:
            to_visit.update(
                participant.summoner.id for participant in match.participants
            )

            if match not in matches:
                matches.add(match)
                yield match

        to_visit -= visited


if __name__ == "__main__":
    cass_setup(RIOT_API_KEY, "NA")
    seed_summoner = cass.get_summoner(name=SEED_SUMMONER)
    for match in islice(crawl_matches(seed_summoner, 5), 25):
        print(match.id)
