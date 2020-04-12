### Strategies ###

def rand_strat_50(game_state):
    outcome = random.random() > .50
    return outcome

def rand_strat_90(game_state):
    outcome = random.random() < .90
    return outcome

def rand_strat_99(game_state):
    outcome = random.random() > .99
    return outcome

def always_say_kekko(game_state):
    return True

def manual_play(game_state):
    current_val = game_state['current_card']['val']
    current_tokens = game_state['current_card']['tokens']
    my_status = game_state['players'][game_state['current_card']['player_id']]
    my_tokens = my_status['tokens']
    my_cards = my_status['cards']
    my_cards.sort()

    print('-'*80)
    print('You are player', game_state['current_card']['player_id'])
    print('The current card is', current_val, 'and carries', current_tokens, 'tokens.')
    print('You have', my_tokens, 'tokens')
    if len(my_cards) == 0:
        print('You have no cards yet.')
    elif len(my_cards) == 1:
        print('Your only card is', my_cards[0])
    elif len(my_cards) == 2:
        print('Your cards are', my_cards[0], 'and', my_cards[1])
    else:
        print('Your cards are', ', '.join([str(c) for c in my_cards[:-1]]), 'and', my_cards[-1])
    print

    print("Your opponents have")
    num_players = len(game_state["players"])
    for i in range(num_players-1):
        index = (i + game_state['current_card']['player_id']+1) % num_players
        player = game_state["players"][index]
        if len(player["cards"]) > 0:
            print("    Player", index, "has", player["tokens"], "tokens and these cards:", ", ".join([str(c) for c in player["cards"]]))
        else:
            print("    Player", index, "has", player["tokens"], "tokens and no cards.")

    print("\nThere are %d cards left in the deck\n" % (game_state['cards_remaining'],))

    # print game_state

    i = raw_input('Press ENTER to say "kekko", or any other string to take the card.\n>>')
    return i == ''

def abe_1(game_state):
    # print game_state
    return game_state['current_card']['tokens'] / float(game_state['current_card']['val']) < .7

def jag_1(game_state):
    verbosity = 0
    if verbosity:
        print("*** Starting strategy jag_1 ********************")
        print(json.dumps(game_state, indent=2))
    # print("^^^^^^^^^^^^^^^^^^^^^^^")

    my_player_state = game_state["players"][game_state["current_card"]["player_id"]]

    #Take the card if it's less than 10 AND has at least two tokens.
    if (game_state["current_card"]["val"] < 10) and (game_state["current_card"]["tokens"] >= 2):
        choice = False

    else:
        #Otherwise, say kekko.
        choice = True

        #...unless the card makes a run.
        for card_value in my_player_state["cards"]:
            number_diff = card_value - game_state["current_card"]["val"]
            if (number_diff == 1) or (number_diff == -1):
                if verbosity:
                    print("Card makes a run!")
                choice = False
                break

        #...or the card's tokens >= the card's value - 5
        if choice:
            if game_state["current_card"]["tokens"] >= game_state["current_card"]["val"] - 5:
                if verbosity:
                    print("Card has enough tokens!")
                choice = False
            else:
                choice = True


    if verbosity:
        if( choice ):
            print("jag_1 says kekko")
        else:
            print("jag_1 takes the card")
        print("**********************************************")
        raw_input('Press ENTER to continue >>')

    return choice


def jag_2(game_state):
    verbosity = 0
    if verbosity:
        print("*** Starting strategy jag_2 ********************")
        print(json.dumps(game_state, indent=2))
    # print("^^^^^^^^^^^^^^^^^^^^^^^")

    my_player_state = game_state["players"][game_state["current_card"]["player_id"]]
    other_player_cards = []
    for i, player_state in enumerate(game_state["players"]):
        if i == game_state["current_card"]["player_id"]:
            continue
        other_player_cards = other_player_cards + player_state["cards"]

    #Start off with my_rating = number of tokens minus value of card
    my_rating = game_state["current_card"]["tokens"] - game_state["current_card"]["val"]

    #If the card is less than 10 AND has at least two tokens, add 5 to the rating
    if (game_state["current_card"]["val"] < 10) and (game_state["current_card"]["tokens"] >= 2):
        my_rating += 5

    #If the card makes a run, add 10 to the rating
    for card_value in my_player_state["cards"]:
        number_diff = card_value - game_state["current_card"]["val"]
        if (number_diff == 1) or (number_diff == -1):
            if verbosity:
                print("Card makes a run!")
            my_rating += 10

            for other_card_value in other_player_cards:
                other_number_diff = other_card_value - game_state["current_card"]["val"]
                if (other_number_diff == 1) or (other_number_diff == -1):
                    if verbosity:
                        print("Card makes a run for someone else, too!")
                    my_rating += 100

    if my_player_state["tokens"] < 6:
        my_rating += 12 - 2*my_player_state["tokens"]

    choice = my_rating < -8

    if verbosity:
        print("jag_2 rates this choice at %d" % (my_rating,))
        if( choice ):
            print("jag_2 says kekko")
        else:
            print("jag_2 takes the card")
        print("**********************************************")
        raw_input('Press ENTER to continue >>')

    return choice

def jag_3(game_state):
    verbosity = 0
    if verbosity:
        print("*** Starting strategy jag_3 ********************")
        print(json.dumps(game_state, indent=2))
    # print("^^^^^^^^^^^^^^^^^^^^^^^")

    my_player_state = game_state["players"][game_state["current_card"]["player_id"]]
    other_player_cards = []
    for i, player_state in enumerate(game_state["players"]):
        if i == game_state["current_card"]["player_id"]:
            continue
        other_player_cards = other_player_cards + player_state["cards"]

    #Start off with my_rating = number of tokens minus value of card
    my_rating = weights["intercept"]

    my_rating += game_state["current_card"]["tokens"]
    my_rating += weights["card_val"] * game_state["current_card"]["val"]

    #If the card is less than 10 AND has at least two tokens, add 5 to the rating
    # if (game_state["current_card"]["val"] < 10) and (game_state["current_card"]["tokens"] >= 2):
    #     my_rating += weights["card_val"]

    #If the card makes a run, add 10 to the rating
    for card_value in my_player_state["cards"]:
        number_diff = card_value - game_state["current_card"]["val"]
        if (number_diff == 1) or (number_diff == -1):
            if verbosity:
                print("Card makes a run!")
            my_rating += 10

            for other_card_value in other_player_cards:
                other_number_diff = other_card_value - game_state["current_card"]["val"]
                if (other_number_diff == 1) or (other_number_diff == -1):
                    if verbosity:
                        print("Card makes a run for someone else, too!")
                    my_rating += 100

    if my_player_state["tokens"] < 6:
        my_rating += 12 - 2*my_player_state["tokens"]

    choice = my_rating < -8

    if verbosity:
        print("jag_2 rates this choice at %d" % (my_rating,))
        if( choice ):
            print("jag_2 says kekko")
        else:
            print("jag_2 takes the card")
        print("**********************************************")
        raw_input('Press ENTER to continue >>')

    return choice

import cbg
