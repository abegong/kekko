import random

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

    def __init__(self, num_players=5, strategies=None):
        if strategies:
            self.strategies = strategies
            self.num_players = self.strategies
        else:
            if num_players:
                self.num_players = num_players
                self.strategies = [rand_strat_50 for i in range(num_players)]
            else:
                raise ValueError("num_players and strategies cannot bot be None")



        # self.strategies = [p["strategy"] for p in players]

        self.init_deck()
        
        self.init_game_state()

        self.history = []
        self.final_score = None


    def init_deck(self):
        self.deck = list(range(3,36))
        random.shuffle(self.deck)
        self.deck = self.deck[:-9]

    def init_game_state(self):
        

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

    def take_action(self, verbosity=0):
        #If there is no current card,
        if self.game_state['current_card'] == {}:
            #...set the final score for the game...
            self.final_score = self.score_game()

            #...and exit without taking any action
            return

        current_player_id = self.game_state['current_card']['player_id']

        kekko = self.players[current_player_id]["strategy"](self.game_state)
        self.history.append({
            'game_state' : copy.deepcopy(self.game_state),
            'strategy' : self.players[current_player_id]["strategy"].__name__,
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
                'player_id' : (current_player_id+1) % len(self.players),
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
        return self.game_state