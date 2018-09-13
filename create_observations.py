from itertools import groupby, tee, filterfalse
import pandas as pd
import sqlite3
from collections import namedtuple
import numpy as np
import random
import statistics as stats
from collections import Counter


N_GAMES = 200_000
CHARS_PER_GAME = 10
COLS = ["ReplayID", "win", "char", "hero_level", "mrr", "map_name"]
Row = namedtuple("row", COLS)


def partition(pred, iterable):
    'Use a predicate to partition entries into false entries and true entries'
    # partition(is_odd, range(10)) --> 0 2 4 6 8   and  1 3 5 7 9
    t1, t2 = tee(iterable)
    return filterfalse(pred, t1), filter(pred, t2)

def allied_hero_col(hero):
    return "allied_char_%s" % hero.replace("'", '')

def opposing_hero_col(hero):
    return "opposing_char_%s" % hero.replace("'", '')

if __name__ == "__main__":


    with sqlite3.connect('data/heroes.db') as conn:

        SQL = """
        SELECT %s FROM character_outcomes
        WHERE (game_mode = 4 OR game_mode = 5) -- heroleague & teamleague
         and (mrr is not NULL)
         and (mrr > 0)
         and (
            map_name ='Hanamura' or map_name = 'Braxis Holdout' or map_name = 'Cursed Hollow' or map_name = 'Infernal Shrines' or map_name = 'Sky Temple' or map_name = 'Towers of Doom'
         )
         and timestamp_utc < '7/25/2018'
         and timestamp_utc > '7/10/2018'
        --LIMIT %s
        """ % (",".join(COLS), CHARS_PER_GAME * N_GAMES)
        print(SQL)
        games = []
        for i, (game_id, rows) in enumerate(groupby(conn.execute(SQL), key=lambda r: r[0])):

            rows = list(map(lambda _: Row(*_), rows))

            team1, team2 = partition(lambda r: r.win, rows)
            team1, team2 = list(team1), list(team2)

            if not (len(team1) == len(team2) == 5):
                print("missing data from some game.")
                continue

            # each team is a row.

            observation1 = {}

            # add if team1 won
            observation1['outcome'] = team1[0].win

            # add average mrr and hero_level
            observation1['allied_avg_mrr'] = stats.mean(r.mrr for r in team1)
            observation1['allied_avg_hero_level'] = stats.mean(r.hero_level for r in team1)
            observation1['opp_avg_hero_level'] = stats.mean(r.hero_level for r in team2)
            observation1['opp_avg_mrr'] = stats.mean(r.mrr for r in team2)

            observation1['map_%s' % team1[0].map_name] = 1

            for player in team1:
                observation1[allied_hero_col(player.char)] = 1

            # add opposing team
            for player in team2:
                observation1[opposing_hero_col(player.char)] = 1

            games.append(observation1)


            # other team
            observation2 = {}

            # add if team1 won
            observation2['outcome'] = team2[0].win

            # add average mrr and hero_level
            observation2['allied_avg_mrr'] = stats.mean(r.mrr for r in team2)
            observation2['allied_avg_hero_level'] = stats.mean(r.hero_level for r in team2)
            observation2['opp_avg_hero_level'] = stats.mean(r.hero_level for r in team1)
            observation2['opp_avg_mrr'] = stats.mean(r.mrr for r in team1)

            observation2['map_%s' % team1[0].map_name] = 1


            for player in team2:
                observation2[allied_hero_col(player.char)] = 1

            # add opposing team
            for player in team1:
                observation2[opposing_hero_col(player.char)] = 1

            games.append(observation2)

            if i % 1000 == 0:
                print(i)

        games = pd.DataFrame(games).fillna(0)
        games.to_csv("obs_matrix_newer_dataset.csv", index=False)
