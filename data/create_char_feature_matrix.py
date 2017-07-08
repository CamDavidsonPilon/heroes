from itertools import groupby
import pandas as pd
import sqlite3
from collections import namedtuple
import numpy as np
import random

N_GAMES = 5000000
CHARS_PER_GAME = 10
COLS = ["ReplayID", "win", "char", "hero_level", "mrr"]
Row = namedtuple("row", COLS)

FEATURE_COLS = [
 'mrr Abathur',
 'mrr Alarak',
 "mrr Anub'arak",
 'mrr Artanis',
 'mrr Arthas',
 'mrr Auriel',
 'mrr Azmodan',
 'mrr Brightwing',
 'mrr Cassia',
 'mrr Chen',
 'mrr Cho',
 'mrr Chromie',
 'mrr D.Va',
 'mrr Dehaka',
 'mrr Diablo',
 'mrr E.T.C.',
 'mrr Falstad',
 'mrr Gall',
 'mrr Gazlowe',
 'mrr Genji',
 'mrr Greymane',
 "mrr Gul'dan",
 'mrr Illidan',
 'mrr Jaina',
 'mrr Johanna',
 "mrr Kael'thas",
 'mrr Kerrigan',
 'mrr Kharazim',
 'mrr Leoric',
 'mrr Li Li',
 'mrr Li-Ming',
 'mrr Lt. Morales',
 'mrr Lunara',
 'mrr Lucio',
 'mrr Malfurion',
 'mrr Medivh',
 'mrr Muradin',
 'mrr Murky',
 'mrr Nazeebo',
 'mrr Nova',
 'mrr Probius',
 'mrr Ragnaros',
 'mrr Raynor',
 'mrr Rehgar',
 'mrr Rexxar',
 'mrr Samuro',
 'mrr Sgt. Hammer',
 'mrr Sonya',
 'mrr Stitches',
 'mrr Sylvanas',
 'mrr Tassadar',
 'mrr The Butcher',
 'mrr The Lost Vikings',
 'mrr Thrall',
 'mrr Tracer',
 'mrr Tychus',
 'mrr Tyrael',
 'mrr Tyrande',
 'mrr Uther',
 'mrr Valeera',
 'mrr Valla',
 'mrr Varian',
 'mrr Xul',
 'mrr Zagara',
 'mrr Zarya',
 'mrr Zeratul',
 "mrr Zul'jin",
 'hero_level Abathur',
 'hero_level Alarak',
 "hero_level Anub'arak",
 'hero_level Artanis',
 'hero_level Arthas',
 'hero_level Auriel',
 'hero_level Azmodan',
 'hero_level Brightwing',
 'hero_level Cassia',
 'hero_level Chen',
 'hero_level Cho',
 'hero_level Chromie',
 'hero_level D.Va',
 'hero_level Dehaka',
 'hero_level Diablo',
 'hero_level E.T.C.',
 'hero_level Falstad',
 'hero_level Gall',
 'hero_level Gazlowe',
 'hero_level Genji',
 'hero_level Greymane',
 "hero_level Gul'dan",
 'hero_level Illidan',
 'hero_level Jaina',
 'hero_level Johanna',
 "hero_level Kael'thas",
 'hero_level Kerrigan',
 'hero_level Kharazim',
 'hero_level Leoric',
 'hero_level Li Li',
 'hero_level Li-Ming',
 'hero_level Lt. Morales',
 'hero_level Lunara',
 'hero_level Lucio',
 'hero_level Malfurion',
 'hero_level Medivh',
 'hero_level Muradin',
 'hero_level Murky',
 'hero_level Nazeebo',
 'hero_level Nova',
 'hero_level Probius',
 'hero_level Ragnaros',
 'hero_level Raynor',
 'hero_level Rehgar',
 'hero_level Rexxar',
 'hero_level Samuro',
 'hero_level Sgt. Hammer',
 'hero_level Sonya',
 'hero_level Stitches',
 'hero_level Sylvanas',
 'hero_level Tassadar',
 'hero_level The Butcher',
 'hero_level The Lost Vikings',
 'hero_level Thrall',
 'hero_level Tracer',
 'hero_level Tychus',
 'hero_level Tyrael',
 'hero_level Tyrande',
 'hero_level Uther',
 'hero_level Valeera',
 'hero_level Valla',
 'hero_level Varian',
 'hero_level Xul',
 'hero_level Zagara',
 'hero_level Zarya',
 'hero_level Zeratul',
 "hero_level Zul'jin"
 ]


if __name__ == "__main__":

    with sqlite3.connect('heroes.db') as conn:

        with open("sql/character_outcomes.sql", 'r') as sql:
            conn.execute(sql.read())
            print "character_outcomes added to db (if doesn't exist)"

        SQL = """
        SELECT %s FROM character_outcomes
        WHERE game_mode = 4 or game_mode = 5 -- heroleague & teamleague
         and mrr is not NULL
         and mrr > 0
        LIMIT %s
        """ % (",".join(COLS), CHARS_PER_GAME * N_GAMES)
        winners = []
        losers = []

        for (game_id, win), rows in groupby(conn.execute(SQL), key=lambda r: (r[0], r[1])):
            rows = map(lambda _: Row(*_), rows)
            if win:
                winners.extend(rows)
            else:
                losers.extend(rows)

    winners = pd.DataFrame(winners)
    winners['mrr'] = np.log(winners['mrr']+1)
    winners['hero_level'] = np.log(winners['hero_level']+1)
    winners = winners.set_index(["ReplayID", "char"])[['mrr', 'hero_level']].unstack(1, fill_value=0)
    winners.columns = FEATURE_COLS

    losers = pd.DataFrame(losers)
    losers['mrr'] = np.log(losers['mrr']+1)
    losers['hero_level'] = np.log(losers['hero_level']+1)
    losers = losers.set_index(["ReplayID", "char"])[['mrr', 'hero_level']].unstack(1, fill_value=0)
    losers.columns = FEATURE_COLS

    n_games_realized = winners.shape[0]
    random_split = np.arange(0, n_games_realized)
    random.shuffle(random_split)
    half = n_games_realized / 2

    # negative_instances
    neg = losers - winners
    neg['outcome'] = 0

    # positive instances
    pos = winners - losers
    pos['outcome'] = 1

    df = pos.iloc[random_split[:half]].append(neg.iloc[random_split[half:]])

    with sqlite3.connect('heroes.db') as conn:
        df.to_sql("hl_game_matrix", conn, if_exists='replace')

    print "hl_game_matrix loaded to DB. %d rows included" % df.shape[0]
    # at this point, game map is not included.
