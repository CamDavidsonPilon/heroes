CREATE TABLE if not exists character_outcomes AS
SELECT
      c.ReplayID,
      "Is Winner" as "win",
      m1."Name" as "char",
      m1."Group" as "group",
      m1."SubGroup" as "sub_group",
      m2."Name" as "map_name",
      c."Hero Level" as "hero_level",
      c."MMR Before" as "mrr",
      "Timestamp (UTC)" as timestamp_utc,
      "GameMode" as "game_mode"
FROM characters c
JOIN map_heros m1 ON c."HeroID" = m1."ID"
JOIN games g ON g."ReplayID" = c."ReplayID"
JOIN map_heros m2 ON g."MapID" = m2.ID
ORDER BY g.ReplayID, "Is Winner";
