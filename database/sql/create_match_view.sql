CREATE VIEW result_details AS 
  SELECT match_results.id AS id,
         w.name AS winner_name, wu.name AS winner_univ_name,
         l.name AS loser_name, lu.name AS loser_univ_name,
         winner_game_count, loser_game_count,
         winner_game1_score, winner_game2_score, winner_game3_score,
         loser_game1_score, loser_game2_score, loser_game3_score,
         meta.name AS match_name, meta.sex AS sex,
         w.id AS winner_id, l.id AS loser_id,
         wu.id AS winner_univ_id, lu.id AS loser_univ_id,
         meta.id AS match_meta_id
  FROM match_results
  JOIN players w ON w.id = winner_id
  JOIN players l ON l.id = loser_id
  JOIN universities wu ON wu.id = w.university_id
  JOIN universities lu ON lu.id = l.university_id
  JOIN match_metas meta ON meta.id = match_meta_id;
