import random
import investment


class Game():
    '''
    instantiate the players, ships, ports, and shipyards, and outputfile
    '''

    def __init__(self, verbose):
        """

        Args:
            game_num (int): times the game will be executed
        """
        ship1 = investment.ship("Ship1", [2, 3, 4], 30)
        ship2 = investment.ship("Ship2", [3, 4, 5], 40)
        ship3 = investment.ship("Ship3", [1, 2, 3], 20)
        ship4 = investment.ship("Ship4", [1, 2, 3], 20)
        ship5 = investment.ship("Ship5", [1, 2, 3], 20)
        ship6 = investment.ship("Ship6", [1, 2, 3], 20)
        ship7 = investment.ship("Ship7", [1, 2, 3], 20)
        ship8 = investment.ship("Ship8", [1, 2, 3], 20)
        ship9 = investment.ship("Ship9", [1, 2, 3], 20)

        port1 = investment.port("Port1", 4, 6)
        port2 = investment.port("Port2", 3, 8)
        port3 = investment.port("Port3", 2, 15)
        port4 = investment.port("Port4", 2, 15)
        port5 = investment.port("Port5", 2, 15)
        port6 = investment.port("Port6", 2, 15)
        port7 = investment.port("Port7", 2, 15)
        port8 = investment.port("Port8", 2, 15)
        port9 = investment.port("Port9", 2, 15)

        shipyard1 = investment.shipyard("Shipyard1", 4, 6)
        shipyard2 = investment.shipyard("Shipyard2", 3, 8)
        shipyard3 = investment.shipyard("Shipyard3", 2, 15)
        shipyard4 = investment.shipyard("Shipyard4", 2, 15)
        shipyard5 = investment.shipyard("Shipyard5", 2, 15)
        shipyard6 = investment.shipyard("Shipyard6", 2, 15)
        shipyard7 = investment.shipyard("Shipyard7", 2, 15)
        shipyard8 = investment.shipyard("Shipyard8", 2, 15)
        shipyard9 = investment.shipyard("Shipyard9", 2, 15)

        self.player_ls = []
        self.ship_ls = []
        self.port_ls = []
        self.shipyard_ls = []
        self.round_num = 10
        self.verbose = verbose
        self.current_round = 1
        # instantiate skip in game
        self.skip = investment.skip()

        # put players, ships, ports, and shipyards into lists

        self.ship_ls = [ship1, ship2, ship3, ship4,
                        ship5, ship6, ship7, ship8, ship9]
        self.port_ls = [port1, port2, port3, port4,
                        port5, port6, port7, port8, port9]
        self.shipyard_ls = [shipyard1, shipyard2, shipyard3, shipyard4,
                            shipyard5, shipyard6, shipyard7, shipyard8, shipyard9]
        self.action_ls = [port1, port2, port3, port4, port5, port6, port7, port8, port9, shipyard1, shipyard2, shipyard3, shipyard4, shipyard5, shipyard6, shipyard7, shipyard8, shipyard9,
                          ship1, ship2, ship3, ship4, ship5, ship6, ship7, ship8, ship9, self.skip]

    def add_player(self, player_ls):
        self.player_ls = player_ls

    def players_move(self):
        """
        All players take their turns
        """
        for player in self.player_ls:
            player.my_turn()
            if self.verbose:
                print("{} has current money: {}\n".format(
                    player.name, player.money))

        return

    def ships_move(self):
        """
        Roll dices for each ship and move
        """
        for ship in self.ship_ls:
            dice_num = random.randint(1, 6)
            ship.move(dice_num)
            if self.verbose:
                print("{}'s current position {}".format(
                    ship.name, ship.get_position()))

        return

    def check_balance(self):
        """
        Calculate balance for each player after the game ends
        """
        # count how many ships have reached the port
        ship_to_port_ls = []
        ship_sink_ls = []
        for ship in self.ship_ls:
            if ship.get_position() > 30:
                ship_to_port_ls.append(ship)
            else:
                ship_sink_ls.append(ship)

        for idx, ship in enumerate(ship_to_port_ls):
            for investor in ship.get_investors():
                ave_profit = ship.get_payback()/len(ship.get_investors())
                investor.profit(ave_profit)

            port = self.port_ls[idx]
            if len(port.get_investors()) == 0:
                continue
            port.get_investors()[0].profit(port.get_payback())

        for idx, ship in enumerate(ship_sink_ls):
            shipyard = self.shipyard_ls[idx]
            if len(shipyard.get_investors()) == 0:
                continue
            shipyard.get_investors()[0].profit(shipyard.get_payback())

    def get_state(self):
        pass

    def start(self):
        while self.current_round <= self.round_num:
            if self.verbose:
                print("\nThis is round", (self.current_round))
            self.players_move()
            self.ships_move()
            self.current_round += 1
        self.check_balance()
        ship1 = investment.ship("Ship1", [2,3,4], 30)
        ship2 = investment.ship("Ship2", [3,4,5], 40)
        ship3 = investment.ship("Ship3", [1,2,3], 20)
        ship4 = investment.ship("Ship4", [1,2,3], 20)
        ship5 = investment.ship("Ship5", [1,2,3], 20)
        ship6 = investment.ship("Ship6", [1,2,3], 20)
        ship7 = investment.ship("Ship7", [1,2,3], 20)
        ship8 = investment.ship("Ship8", [1,2,3], 20)
        ship9 = investment.ship("Ship9", [1,2,3], 20)
        
    
        port1 = investment.port("Port1", 4, 6)
        port2 = investment.port("Port2", 3, 8)
        port3 = investment.port("Port3", 2, 15)
        port4 = investment.port("Port4", 2, 15)
        port5 = investment.port("Port5", 2, 15)
        port6 = investment.port("Port6", 2, 15)
        port7 = investment.port("Port7", 2, 15)
        port8 = investment.port("Port8", 2, 15)
        port9 = investment.port("Port9", 2, 15)

        shipyard1 = investment.shipyard("Shipyard1", 4, 6)
        shipyard2 = investment.shipyard("Shipyard2", 3, 8)
        shipyard3 = investment.shipyard("Shipyard3", 2, 15)
        shipyard4 = investment.shipyard("Shipyard4", 2, 15)
        shipyard5 = investment.shipyard("Shipyard5", 2, 15)
        shipyard6 = investment.shipyard("Shipyard6", 2, 15)
        shipyard7 = investment.shipyard("Shipyard7", 2, 15)
        shipyard8 = investment.shipyard("Shipyard8", 2, 15)
        shipyard9 = investment.shipyard("Shipyard9", 2, 15)

        
        # put players, ships, ports, and shipyards into lists
        
        self.ship_ls = [ship1, ship2, ship3, ship4, ship5, ship6, ship7, ship8, ship9]
        self.port_ls = [port1, port2, port3, port4, port5, port6, port7, port8, port9]
        self.shipyard_ls = [shipyard1, shipyard2, shipyard3, shipyard4, shipyard5, shipyard6, shipyard7, shipyard8, shipyard9]
        self.action_ls = [port1, port2, port3, port4, port5, port6, port7, port8, port9
                          , shipyard1, shipyard2, shipyard3, shipyard4, shipyard5, shipyard6, shipyard7, shipyard8, shipyard9,
                            ship1, ship2, ship3, ship4, ship5, ship6, ship7, ship8, ship9, self.skip]
