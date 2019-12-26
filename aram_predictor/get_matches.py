from settings import RIOT_API_KEY, SEED_SUMMONER

from itertools import islice

import cassiopeia as cass


def cass_setup(key, region):
    cass.set_riot_api_key(key)
    cass.set_default_region(region)


def get_n_matches(summoner, n, m):
    return list(
        islice(
            (
                match
                for match in islice(summoner.match_history, m)
                if match.mode == cass.GameMode.aram
            ),
            n,
        )
    )


def next_players_from_match_history(match_history):
    return [paticipant for match in match_history for paticipant in match.participants]


def collect_n_matches(seed_summoner, n):
    matches = set()
    visited = set()
    to_visit = {seed_summoner.id}

    while len(matches) < n and len(to_visit) > 0:
        print("Have {} matches".format(len(matches)))
        summoner_id = to_visit.pop()
        summoner = cass.get_summoner(id=str(summoner_id))
        match_history = get_n_matches(summoner, 10, 100)
        matches.update(match_history)
        to_visit.update(
            participant.summoner.id
            for participant in next_players_from_match_history(match_history)
        )
        visited.add(summoner_id)
        to_visit -= visited

    return list(matches)


if __name__ == "__main__":
    cass_setup(RIOT_API_KEY, "NA")
    seed_summoner = cass.get_summoner(name=SEED_SUMMONER)
    matches = collect_n_matches(seed_summoner, 100)
    print("Collected {} matches:".format(len(matches)))
    for match in matches:
        print(match.id)
