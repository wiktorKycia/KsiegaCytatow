-- Zapytanie zwracające full joina id-ków użytkowników i autorów, posortowane
SELECT u.`id` as 'user_id', a.`id` as 'author_id' FROM `authors` a JOIN `users` u
ORDER BY u.`id`, a.`id`;

-- dołączenie null-a z prawej strony do poprzedniego zapytania
SELECT user_id, author_id, NULL as 'nickname_id' FROM (
    SELECT u.`id` as 'user_id', a.`id` as 'author_id' FROM `authors` a JOIN `users` u
) AS tbl
ORDER BY user_id, author_id;

-- wstawienie wierszy do tabeli
INSERT INTO usernicknamespreferences (user_id, author_id, nickname_id)
select *
from  (SELECT user_id, author_id, NULL as 'nickname_id' FROM (
        SELECT u.`id` as 'user_id', a.`id` as 'author_id' FROM `authors` a JOIN `users` u
    ) AS tbl
    ORDER BY user_id, author_id) alias