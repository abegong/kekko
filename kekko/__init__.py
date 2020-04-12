from .game import Game

### Train a bot to play games ###
if __name__ == "__main__":
    rows = []
    for i in range(1000):
        print(datetime.datetime.now(), i)
        T = Tourney([
            jag_2,
            cbg.cbg,
            # jag_1,
            # cbg.cbg,
            abe_1,
            rand_strat_90,
        ])
        outcome = T.play_whole_game(verbosity=0)
        # print outcome

        my_player_id = outcome["strategies"].index("jag_2")
        new_row = {
            'best_score' : min(outcome["scores"]),
            'my_score' : outcome["scores"][my_player_id],
            'my_player_id' : my_player_id,
            'winning_strategy' : outcome["winners"],
            'did_i_win' : outcome["winners"] == ["jag_2"],
        }
        rows.append(new_row)

    my_df = pd.DataFrame(rows)
    print(my_df)


    print(my_df.did_i_win.value_counts())
    print(my_df.winning_strategy.map(str).value_counts())
