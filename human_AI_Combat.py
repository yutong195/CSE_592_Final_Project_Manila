import game
import agents
import play
import argparse
# import dqn


def main(args):
    g = game.Game(True, 0)
    player2 = play.Player("Player2", 30, None, g)
    if args.mode == 'Q_learning':
        player1 = agents.QlearningAgent("Player1", 30, None, g)
        player1.set_verbose(True)
        player3 = agents.QlearningAgent("Player3", 30, None, g)
        player3.set_verbose(True)
        player1.loadQtable("qtable_" + args.behavior1 + ".json")
        player3.loadQtable("qtable_" + args.behavior2 + ".json")
    if args.mode == 'DQN':
        player2 = dqn.DQNAgent("Player2", 30, None, g)
        player3 = dqn.DQNAgent("Player3", 30, None, g)
        player2.loadWeights("dqn_" + args.behavior1 + ".pth")
        player3.loadWeights("dqn_" + args.behavior2 + ".pth")
        player2.set_verbose(True)
        player3.set_verbose(True)
    player_ls = [player1, player2, player3]
    g.add_player(player_ls)
    g.start()
    print("Player1's final money:", int(player_ls[0].money))
    print("Player2's final money:", int(player_ls[1].money))
    print("Player3's final money:", int(player_ls[2].money))


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description='Allow human to play with AI in the Manila')
    parser.add_argument('--mode', default='Q_learning', type=str,
                        help='What method you want to use (Q_learning, DQN)')
    parser.add_argument('--behavior1', default='normal', type=str,
                        help='Mode of the agents (normal, conservative, aggressive)')
    parser.add_argument('--behavior2', default='normal', type=str,
                        help='Mode of the agents (normal, conservative, aggressive)')
    args = parser.parse_args()
    print(args)
    main(args)
