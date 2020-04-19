import pytest
import os
import random
import json

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



    # game_state = G.take_action()
    # print(json.dumps(game_state, indent=2))
    
    # game_state = G.take_action()
    # print(json.dumps(game_state, indent=2))
    
    # game_state = G.take_action()
    # print(json.dumps(game_state, indent=2))