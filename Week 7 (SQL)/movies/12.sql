SELECT title
FROM movies
JOIN stars ON movies.id = stars.movie_id
JOIN people ON stars.person_id = people.id
WHERE people.name in ('Bradley Cooper','Jennifer Lawrence')
GROUP BY movies.id,movies.title
HAVING COUNT(DISTINCT people.name) = 2;
