CREATE VIEW player_details AS
    SELECT p.id AS id, p.name AS name, grade, sex, u.name AS univ_name, u.id AS univ_id
    FROM players p
    JOIN universities u ON u.id = p.university_id;