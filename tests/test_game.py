import pytest
import os
import random
import json
import sqlalchemy as sa

import kekko

def test_game_init():
    random.seed(1)

    G = kekko.Game()
    game_state = G.get_game_state()
    # print(json.dumps(game_state, indent=2))

    assert game_state.keys() == set(["current_card", "players", "cards_remaining"])
    assert game_state["cards_remaining"]==27

    assert len(game_state["players"])==5
    for p in game_state["players"]:
        assert p.keys() == set(["name", "cards", "tokens"])
        assert p["cards"] == []
        assert p["tokens"] == 11


    G = kekko.Game(num_players=2)
    game_state = G.get_game_state()
    # print(json.dumps(game_state, indent=2))

    assert game_state.keys() == set(["current_card", "players", "cards_remaining"])
    assert game_state["cards_remaining"]==27
    
    assert len(game_state["players"])==2
    for p in game_state["players"]:
        assert p.keys() == set(["name", "cards", "tokens"])
        assert p["cards"] == []
        assert p["tokens"] == 11

def test_take_action():
    random.seed(1)

    G = kekko.Game()
    game_state = G.get_game_state()

    game_state = G.take_action()
    print(json.dumps(game_state, indent=2))
    print(json.dumps(game_state["current_card"], indent=2))
    # print(json.dumps(G.get_history(), indent=2))

    for i in range(20):
        game_state = G.take_action()
        print(json.dumps(game_state["current_card"], indent=2))

    # The game must eventually end
    while True:
        game_state = G.take_action()
        if game_state == None:
            break


def test_db():
    random.seed(1)

    # engine = sa.create_engine('sqlite:///:memory:', echo=True)
    engine = sa.create_engine('postgresql://postgres@localhost/kekko')#, echo=True)

    # Clear out the DB
    with open("db/create_tables.sql") as f_:
        create_tables_query = f_.read()
        engine.execute(create_tables_query)
    assert engine.execute("SELECT COUNT(*) FROM games;").fetchone()[0] == 0


    G = kekko.Game(db=engine)
    assert engine.execute("SELECT COUNT(*) FROM games;").fetchone()[0] == 1
    

    # assert engine.execute("SELECT COUNT(*) FROM game_states;").fetchone()[0] == 0
    # game_state = G.take_action()
    # assert engine.execute("SELECT COUNT(*) FROM game_states;").fetchone()[0] == 1


    # # The game must eventually end
    # while True:
    #     game_state = G.take_action()
    #     if game_state == None:
    #         break
