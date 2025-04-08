-- write a SQL query to list the names of all people who starred in a movie in which Kevin Bacon also starred
-- Be sure to only select the Kevin Bacon born in 1958
SELECT DISTINCT(people.name)
FROM people
JOIN stars ON people.id = stars.person_id
JOIN movies ON stars.movie_id = movies.id
WHERE movies.title IN
(SELECT DISTINCT(movies.title) FROM people
JOIN stars ON people.id = stars.person_id
JOIN movies ON stars.movie_id = movies.id
WHERE people.name IS "Kevin Bacon" AND people.birth = '1958')
AND people.name IS NOT "Kevin Bacon";