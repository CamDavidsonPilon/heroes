import pandas as pd


def create_replay_characters_table(conn):
    df = pd.read_csv("raw_csv/ReplayCharacters.csv")
    df.to_sql("characters", conn, index=False, index_label="ID", if_exists='replace', chunksize=100000)
    return


def create_map_hero_table(conn):
    df = pd.read_csv("raw_csv/HeroIDAndMapID.csv")
    df.to_sql("map_heros", conn, index=False, if_exists='replace', chunksize=100000)
    return


def create_replays_table(conn):
    df = pd.read_csv("raw_csv/Replays.csv")
    df = df.rename(columns={"GameMode(3=Quick Match 4=Hero League 5=Team League 6=Unranked Draft)": "GameMode"})
    df.to_sql("games", conn, index=False, index_label="ReplayID", if_exists='replace', chunksize=100000)
    return

if __name__ == "__main__":
    import sqlite3
    with sqlite3.connect('heroes.db') as conn:
        conn.text_factory = str

        print "map hero table"
        create_map_hero_table(conn)

        print "replays table"
        create_replays_table(conn)

        print "replays character table"
        create_replay_characters_table(conn)

        print "Complete."
