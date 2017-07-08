SELECT 
  hl.*,
 (name = "Battlefield of Eternity") as "Battlefield of Eternity",
 (name = "Blackheart's Bay") as "Blackheart's Bay",
 (name = "Cursed Hollow") as "Cursed Hollow",
 (name = "Dragon Shire") as "Dragon Shire",
 (name = "Garden of Terror") as "Garden of Terror",
 (name = "Haunted Mines") as "Haunted Mines",
 (name = "Infernal Shrines") as "Infernal Shrines",
 (name = "Sky Temple") as "Sky Temple",
 (name = "Tomb of the Spider Queen") as "Tomb of the Spider Queen",
 (name = "Towers of Doom") as "Towers of Doom",
 (name = "Braxis Holdout") as "Braxis Holdout",
 (name = "Warhead Junction") as "Warhead Junction",
 (name = "Braxis Outpost") as "Braxis Outpost",
 (name = "Hanamura") as "Hanamura"
FROM hl_game_matrix hl 
JOIN games g 
 on g.ReplayID = hl.ReplayID
JOIN map_heros m
 on g.mapID = m.ID
ORDER BY RANDOM();