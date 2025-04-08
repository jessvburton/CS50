-- write a SQL query that lists the names of the songs that feature other artists
SELECT songs.name
FROM songs
JOIN artists ON songs.artist_id = artists.id
WHERE songs.name LIKE "%feat.%";