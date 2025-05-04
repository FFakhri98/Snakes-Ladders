import random


def determining_turns(name_of_players):
    """
    determines turns of players with dice.
    """
    determining_turns_output = list()
    while len(name_of_players) > 0:
        for player in name_of_players:
            if random.randint(1, 6) == 6:
                determining_turns_output.append(player)
                name_of_players.remove(player)
    return determining_turns_output
