import pandas as pd
from glob import glob


def create_replay_characters_table(conn):
    for i, file in enumerate(glob('raw_csv/ReplayCharacters*.csv')):
        print("loading file %s."%file)
        df = pd.read_csv(file)
        df['file_index'] = i

        if i == 0:
            df.to_sql("characters", conn, index=False, index_label="ID", if_exists='replace', chunksize=10000)
        else:
            df.to_sql("characters", conn, index=False, index_label="ID", if_exists='append', chunksize=10000)
    return


def create_map_hero_table(conn):
    # this is an updated table, so we want to "latest" one only
    latest_file = sorted(glob('raw_csv/HeroIDAndMapID*.csv'))[-1]
    print("loading file %s."%latest_file)
    df = pd.read_csv(latest_file)
    df.to_sql("map_heros", conn, index=False, if_exists='replace', chunksize=100)

    return


def create_replays_table(conn):
    for i, file in enumerate(glob('raw_csv/Replays*.csv')):

        print("loading file %s."%file)
        df = pd.read_csv(file)
        df['file_index'] = i

        df = df.rename(columns={"GameMode(3=Quick Match 4=Hero League 5=Team League 6=Unranked Draft)": "GameMode"})

        if i == 0:
            df.to_sql("games", conn, index=False, index_label="ReplayID", if_exists='replace', chunksize=10000)
        else:
            df.to_sql("games", conn, index=False, index_label="ReplayID", if_exists='append', chunksize=10000)
    return

if __name__ == "__main__":
    import sqlite3
    with sqlite3.connect('heroes.db') as conn:
        conn.text_factory = str

        print("map hero table")
        create_map_hero_table(conn)

        print("replays table")
        create_replays_table(conn)

        print("replays character table")
        create_replay_characters_table(conn)

        print("Complete.")
