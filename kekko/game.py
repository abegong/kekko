import random
import copy
import logging

from .strategies import rand_strat_50

"""
game_state : {
    current_card : {
        val : int,
        tokens : int,
        player_id : int,
    },
    players : [{
        cards : [],
        tokens : int,
    }],
    cards_remaining : int
}
"""

class Game(object):

    def __init__(self, num_players=5, strategies=None, db=None):
        logging.info("Game.__init__")

        self.db = db

        self.init_deck()
        self.init_players(num_players, strategies)
        self.init_game_state()

        self.history = []
        self.final_score = None


    def init_deck(self):
        logging.info("Game.init_deck")

        self.deck = list(range(2,36))
        random.shuffle(self.deck)
        self.deck = self.deck[:-6]

        if self.db:
            query = """INSERT INTO games (game_name, deck) VALUES ('hello', ARRAY[%s]) RETURNING id;""" % (
                ",".join([str(card) for card in self.deck])
            )
            result = self.db.execute(query)
            self._id = result.fetchone()[0]

    def init_players(self, num_players=5, strategies=None):
        if strategies:
            self.strategies = strategies
            self.num_players = self.strategies

        else:
            if num_players:
                self.num_players = num_players
                self.strategies = [rand_strat_50 for i in range(num_players)]
            else:
                raise ValueError("num_players and strategies cannot bot be None")
        
        if self.db:
            values_strings = ["(%d, 'NAME', NULL, %d )""" % (self._id, i) for i in range(self.num_players)]
            values_string = ",".join(values_strings)
            query = "INSERT INTO game_players (game_id, player_name, strategy_id, order_val) VALUES " + values_string + "RETURNING id;"

            result = self.db.execute(query)
            self._player_ids = [r[0] for r in result.fetchall()]


    def init_game_state(self):
        logging.info("Game.init_game_state")

        players = [{
            'name' : "Player "+str(i),#self.players[i]["name"],
            'cards' : [],
            'tokens' : 11,
        } for i in range(self.num_players)]

        current_card = {
            'val' : self.deck.pop(),
            'tokens' : 0,
            'player_id' : 0,
        }
        
        self.game_state = {
            'current_card' : current_card,
            'players' : players,
            'cards_remaining' : len(self.deck),
        }

        if self.db:
            query = """
            INSERT INTO game_states
                (game_id, cards_remaining, card_value, player_index, tokens) VALUES
                (%d, %d, %d, %d, %d)
            RETURNING id;""" % (
                self._id,
                self.game_state["cards_remaining"],
                self.game_state["current_card"]["val"],
                self.game_state["current_card"]["player_id"],
                self.game_state["current_card"]["tokens"],
            )

            result = self.db.execute(query)
            new_game_state_id = result.fetchall()[0][0]

            values_strings = ["(%d, %d, %d, ARRAY%s::INTEGER[] )""" % (
                new_game_state_id,
                self._player_ids[0],
                self.game_state["players"][i]["tokens"],
                str(self.game_state["players"][i]["cards"])
            ) for i in range(self.num_players)]
            values_string = ",".join(values_strings)
            query = """
            INSERT INTO game_state_players
                (game_state_id, game_player_id, tokens, cards) VALUES
                %s
            RETURNING id;""" % (values_string,)
            print(query)
            result = self.db.execute(query)

    def _resolve_action(self, kekko, current_player_id, verbosity=0):
        self.history.append({
            'game_state' : copy.deepcopy(self.game_state),
            'strategy' : self.strategies[current_player_id].__name__,
            'kekko' : kekko,
        })

        if kekko and self.game_state['players'][current_player_id]['tokens'] > 0:
            #Decrement personal tokens
            self.game_state['players'][current_player_id]['tokens'] -= 1

            if verbosity > 0:
                # print("Player %d playing strategy %s says kekko to the %d card. It now has %d tokens." % (
                #     self.game_state['current_card']['player_id'],
                #     "{:<15}".format(self.strategies[current_player_id].__name__),
                #     self.game_state['current_card']['val'],
                #     self.game_state['current_card']['tokens']+1,
                # ))
                print("Player %d says kekko to the %d card. It now has %d tokens." % (
                    self.game_state['current_card']['player_id'],
                    self.game_state['current_card']['val'],
                    self.game_state['current_card']['tokens']+1,
                ))

            #Update game state
            self.game_state['current_card'] = {
                'val' : self.game_state['current_card']['val'],
                'tokens' : self.game_state['current_card']['tokens']+1,
                'player_id' : (current_player_id+1) % self.num_players,
            }

        else:
            #Update personal cards and tokens
            self.game_state['players'][current_player_id]['tokens'] += self.game_state['current_card']['tokens']
            self.game_state['players'][current_player_id]['cards'].append(self.game_state['current_card']['val'])

            if verbosity > 0:
                # print("Player %d playing strategy %s takes the %d card and %d tokens." % (
                #     self.game_state['current_card']['player_id'],
                #     "{:<15}".format(self.strategies[current_player_id].__name__),
                #     self.game_state['current_card']['val'],
                #     self.game_state['current_card']['tokens'],
                # ))
                print("Player %d takes the %d card and %d tokens." % (
                    self.game_state['current_card']['player_id'],
                    self.game_state['current_card']['val'],
                    self.game_state['current_card']['tokens'],
                ))
            
            #Draw new card
            if len(self.deck) > 0 :
                self.game_state['current_card'] = {
                    'val' : self.deck.pop(),
                    'tokens' : 0,
                    'player_id' : current_player_id,
                }
                self.game_state['cards_remaining'] = len(self.deck)

            else :
                self.game_state['current_card'] = {}

    def take_action(self, verbosity=0):
        """Figure out the next action to take, then resolve it.

        It does not update any game state itself---all of that code is delegated to _resolve_action.
        This method is primraily useful when running in simulation mode, not client-server mode.
        """
        logging.info("Game.take_action")

        #If there is no current card,
        if self.game_state['current_card'] == {}:
            logging.info("No current card")
            #...set the final score for the game...
            self.final_score = self.score_game()

            #...and exit without taking any action
            return

        current_player_id = self.game_state['current_card']['player_id']
        kekko = self.strategies[current_player_id](self.game_state)

        self._resolve_action(kekko, current_player_id, verbosity)

        return self.get_game_state()

    def score_game(self):
        scores = []

        for p in self.game_state['players']:
            card_set = set(p['cards'])
            score = 0
            for c in card_set:
                if not c-1 in card_set:
                    score += c

            score -= p['tokens']

            scores.append(score)

        return scores

    def get_game_state(self):
        logging.info("Game.get_game_state")

        return self.game_state

    def get_history(self):
        logging.info("Game.get_history")

        return self.history