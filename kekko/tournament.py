class Tourney(object):

    def __init__(self, strategies):
        #FIXME: Need to update this to include player names, not just strategies
        self.strategies = strategies
        
        self.scores = dict([(s.__name__,0) for s in strategies])
        self.wins = dict([(s.__name__,0) for s in strategies])

        self.history = []

    def play_whole_tourney(self, games=100):
        
        wins = dict([(s.__name__,0) for s in self.strategies])

        for g in range(games):
            outcome = self.play_whole_game()#strategies)
            
            for w in outcome['winners']:
                wins[w] += 1

            self.history.append(outcome)

        print(wins)

    def play_whole_game(self, verbosity=0):
        strategies = copy.deepcopy(self.strategies)
        random.shuffle(strategies)

        strategy_names = [s.__name__ for s in strategies]

        #FIXME: Need to update this to include player names, not just strategies
        G = Game(strategies)
        # print json.dumps(G.game_state, indent=2)
        while 1:
            G.take_action(verbosity)
            # print json.dumps(G.game_state, indent=2)
            # print G.deck
            # print G.score_game()

            if G.final_score != None:
                break

        outcome = {
            'strategies' : strategy_names,
            'scores' : G.final_score,
            'winners' : [s for i, s in enumerate(strategy_names) if G.final_score[i]==min(G.final_score)]
        }

        self.last_game = G

        return outcome
