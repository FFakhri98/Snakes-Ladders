from random import randint


def game(
    players=[1, 2, 3],
    snakes_ladders={1: 20, 13: 2, 15: 33, 56: 26, 63: 84, 99: 1},
):

    players_status = {i: "out" for i in players}
    players_location = {i: 0 for i in players}

    while list(players_status.values()).count("won") != len(players):

        for player in players:
            dice = randint(1, 6)

            if players_status[player] == "won":
                continue

            elif dice == 6 and players_status[player] == "out":
                players_status[player] = "in"

            elif dice == 6 and players_status[player] == "in":

                while dice == 6 and players_status[player] == "in":

                    players_location[player] += dice

                    if players_location[player] in snakes_ladders.keys():
                        players_location[player] = snakes_ladders[
                            players_location[player]
                        ]

                    elif players_location[player] == 100:
                        players_status[player] = "won"

                    dice = randint(1, 6)

            elif dice != 6 and players_status[player] == "in":
                players_location[player] += dice

                if players_location[player] in snakes_ladders.keys():
                    players_location[player] = snakes_ladders[players_location[player]]

                elif players_location[player] == 100:
                    players_status[player] = "won"
