CREATE TABLE universities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE players (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL,
    grade INTEGER NOT NULL,
    sex VARCHAR(8) CHECK(sex IN ('男子', '女子')) NOT NULL,
    university_id INTEGER NOT NULL,
    FOREIGN KEY (university_id) REFERENCES universities(id)
);

CREATE TABLE match_metas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL,
    sex VARCHAR(8) CHECK(sex IN ('男子', '女子')) NOT NULL
);

CREATE TABLE match_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    winner_game_count INTEGER NOT NULL,
    loser_game_count INTEGER NOT NULL,
    winner_game1_score INTEGER NOT NULL,
    winner_game2_score INTEGER NOT NULL,
    winner_game3_score INTEGER,
    loser_game1_score INTEGER NOT NULL,
    loser_game2_score INTEGER NOT NULL,
    loser_game3_score INTEGER,
    winner_id INTEGER NOT NULL,
    loser_id INTEGER NOT NULL,
    match_meta_id INTEGER NOT NULL,
    FOREIGN KEY (winner_id) REFERENCES players(id),
    FOREIGN KEY (loser_id) REFERENCES players(id),
    FOREIGN KEY (match_meta_id) REFERENCES match_metas(id)
);

