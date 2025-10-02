-- SELECT people.name
-- FROM movies
-- JOIN stars s1 ON movies.id = stars.movie_id
-- JOIN people ON stars.person_id = people.id
-- WHERE people.name = 'Kevin Bacon' AND people.birth = 1958

-- SELECT DISTINCT people.name
-- FROM movies


SELECT people.name
FROM people
JOIN stars ON people.id = stars.person_id
WHERE stars.movie_id IN (
    SELECT stars.movie_id
    FROM people
    JOIN stars ON people.id = stars.person_id
    WHERE people.name = 'Kevin Bacon' AND people.birth = 1958
)
AND people.name != 'Kevin Bacon';
