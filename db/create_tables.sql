DROP TABLE game_state_decisions;
DROP TABLE game_state_players;
DROP TABLE game_states;
DROP TABLE game_players;
DROP TABLE games;
DROP TABLE strategies;

CREATE TABLE strategies(
	id SERIAL NOT NULL PRIMARY KEY,
	short_description VARCHAR(200),
	long_description TEXT
);
-- CREATE TABLE players(
-- 	age INT,
-- 	first_name VARCHAR(255),
-- 	last_name VARCHAR(255),
-- 	email TEXT
-- );
CREATE TABLE games(
	id SERIAL NOT NULL PRIMARY KEY,
	game_name TEXT,
	deck INT[]
	-- created_at INTEGER NOT NULL DEFAULT NOW()
);
CREATE TABLE game_players(
	id SERIAL NOT NULL PRIMARY KEY,
	game_id SERIAL REFERENCES games(id),
	player_name TEXT,
	strategy_id INTEGER REFERENCES strategies(id),
	order_val INT
);
CREATE TABLE game_states(
	id SERIAL PRIMARY KEY,
	games SERIAL REFERENCES games(id),
	turn_number INT,
	card_value INT,
	player_index INT,
	tokens INT
);
CREATE TABLE game_state_players(
	id SERIAL NOT NULL PRIMARY KEY,
	game_state_id INTEGER REFERENCES game_states(id),
	game_player_id INTEGER REFERENCES game_players(id),
	tokens INT,
	cards INT[]
);
CREATE TABLE game_state_decisions(
	id SERIAL NOT NULL PRIMARY KEY,
	game_state_id INTEGER REFERENCES game_states(id),
	kekko BOOLEAN
);
--CREATE TABLE tournaments;
