import numpy as np
from play import Player
import util
import matplotlib.pyplot as plt

"""
State:
integer tuple
Investment and corresponding idx
    Port1 : 0
    Port2 : 1
    Port3 : 2
    Shipyard1 : 3
    Shipyard2 : 4
    Shipyard3 : 5
    Ship1 : 6
    Ship2 : 7
    Ship3 : 8
    Ship1 position : 9
    Ship2 position : 10
    Ship3 position : 11
    money difference to 1st player : 12
    money difference to 2nd player : 13
    money difference to 3rd player : 14
    Round number : 15

Values:
    Ships : num of seats left
    Other investments : 0 == unavailable; 1 == available
    Ship position : current position
    
Action:
Action idx : 9
Values:
    Port1 : 0
    Port2 : 1
    Port3 : 2
    Shipyard1 : 3
    Shipyard2 : 4
    Shipyard3 : 5
    Ship1 : 6
    Ship2 : 7
    Ship3 : 8
    Skip : 9
"""


class QlearningAgent(Player):
    def __init__(self, name, money, color, game):
        super().__init__(name, money, color, game)
        self.qtable = util.Qtable()
        self.factor = 0
        self.alpha = 0.02
        self.gamma = 0.9
        self.tValue = 0
        self.seed = None
        self.verbose = False
        self.epsilon = .95
        self.eps_step = 0.01
        self.action_val_dic = {"Port1" : 0, "Port2" : 1, "Port3" : 2,
                               "Shipyard1" : 3, "Shipyard2" : 4, "Shipyard3" : 5,
                               "Ship1" : 6, "Ship2" : 7, "Ship3" : 8,
                               "Skip" : 9}
        self.delta_q_values = []  # To track delta Q values
        
    def set_verbose(self, verbose):
        self.verbose = verbose

    def saveQtable(self, filepath):
        self.qtable.save(filepath)

    def loadQtable(self, filepath):
        self.qtable.load(filepath)

    def set_seed(self, Myseed):
        self.seed = Myseed

    def set_factor(self, factor):
        self.factor = factor

    def get_qvalue(self, s_a_pair):
        return self.qtable[tuple(s_a_pair)]

    def update_Qtable(self, newQ, state, action):
        s_a_pair = tuple(state + [self.convertAction(action)])
        oldQ = self.get_qvalue(s_a_pair)
        deltaQ = newQ - oldQ

        # Update Q-table
        self.qtable[s_a_pair] = newQ

        # Track delta Q value for plotting
        self.delta_q_values.append(deltaQ)
    
    def plot_delta_q(self):
        # Plot delta Q values to see if Q-values converge over time
        plt.figure(figsize=(10, 6))
        x = range(len(self.delta_q_values)//100)
        y = [sum(self.delta_q_values[i-50:i+50])/100 for i in range(len(self.delta_q_values))]
        plt.scatter([num * 100 for num in x], y[50:-49:100], label='Delta Q Over Time',
                    s=2)
        plt.xlabel('Update Steps')
        plt.ylabel('Delta Q')
        plt.title('Average Delta Q Over 100 steps (Convergence Plot)')
        plt.legend()
        plt.grid(True)
        plt.show()

    def convertAction(self, action):
        return self.action_val_dic[action.name]

    def get_action(self):
        action_ls = []
        money = self.get_money()
        for action in self.game.action_ls:
            if action.get_availability() and action.get_cost() <= money:
                action_ls.append(action)
        return action_ls

    def get_probability(self, num_dice, target_value, larger=True):
        count = [[0, 1, 1, 1, 1, 1, 1], [0, 0, 1, 2, 3, 4, 5, 6, 5, 4, 3, 2, 1],[0, 0, 0, 1, 3, 6, 10, 15, 21, 25,
                                                                                     27, 27, 25, 21, 15, 10, 6, 3, 1]]
        if target_value > len(count[num_dice]):
            return 0
        if target_value < 0:
            return 1
        if larger:
            return sum(count[num_dice][target_value:])/sum(count[num_dice])
        else:
            return sum(count[num_dice][:target_value]) / sum(count[num_dice])

    def my_turn(self, current_epoch):
        # compute action with maximum Qvalue
        action, currentQ, currentState = self.eps_greedy()
        # compute Reward
        # R = self.computeReward(action)
        R = 0 - action.get_cost()
        # take the action
        self.money -= action.get_cost()
        action.invest(self)
        if self.verbose:
            print("{agent_name} invested in {investment_name}".format(
                agent_name=self.name, investment_name=action.name))
        # observe nextState and compute maximum Qvalue of nextState
        _, nextQ, _ = self.computeMax()

        alpha_tmp = self.alpha * (1 - current_epoch/30000)
        # update Qtable
        newQ = (1 - self.alpha) * currentQ + \
            self.alpha * (R + self.gamma * nextQ)
        # newQ = (1 - alpha_tmp) * currentQ + \
        #     alpha_tmp * (R + self.gamma * nextQ)
        self.update_Qtable(newQ, currentState, action)

    def get_state(self):
        state = []
        investment_ls = self.game.action_ls[:-1]
        # investment availability
        for investment in investment_ls:
            investor_num = len(investment.get_investors())
            slot_left = investment.get_length() - investor_num
            state.append(slot_left)

        # ship position
        for ship in self.game.ship_ls:
            state.append(ship.get_position())

        # money difference
        money_ls = sorted([player.get_money()
                          for player in self.game.player_ls])
        for money in money_ls:
            difference = self.get_money()-money
            state.append(difference)

        # round number
        state.append(self.game.round_num)
        return state

    def eps_greedy(self):
        eps_prob = np.random.rand()
        if eps_prob < self.epsilon:
            state = self.get_state()
            action_ls = self.get_action()
            action = util.randomChoice(action_ls)
            action_val = self.convertAction(action)
            s_a_pair = state + [action_val]
            qvalue = self.get_qvalue(s_a_pair)
            self.epsilon -= self.eps_step
            return action, qvalue, state
        else:
            self.epsilon -= self.eps_step
            return self.computeMax()

    def computeMax(self):

        # compute the maximum Qvalue based current state and available actions
        state = self.get_state()
        action_ls = self.get_action()
        qMax = float('-inf')
        candidate = []
        actionMax = None
        for action in action_ls:
            action_val = self.convertAction(action)
            s_a_pair = state + [action_val]
            qvalue = self.get_qvalue(s_a_pair) + self.computeReward(action)
            if qvalue == qMax:
                candidate.append(action)
            if qvalue > qMax:
                qMax = qvalue
                actionMax = action
                candidate = [action]
        # break tie randomly
        if len(candidate) != 0:
            actionMax = util.randomChoice(candidate, self.seed)
        return actionMax, qMax, state

    def computeReward(self, action):
        ship_pos_ls = [self.game.ship_ls[0].get_position(
        ), self.game.ship_ls[1].get_position(), self.game.ship_ls[2].get_position()]
        ship_pos_ls_sort = sorted(ship_pos_ls)
        ship_pos_max = ship_pos_ls_sort[2]
        ship_pos_mid = ship_pos_ls_sort[1]
        ship_pos_min = ship_pos_ls_sort[0]

        if action.get_type() == "ship":
            payback = action.get_payback()/(len(action.get_investors())+1)
            reward = self.factor*payback * \
                (self.get_probability((3-self.game.current_round), 11-action.get_position()))


        elif action.get_type() == "port":
            payback = action.get_payback()
            if (action.name == "Port1"):
                reward =  self.factor*payback * \
                    (self.get_probability((3-self.game.current_round), 11-ship_pos_max))
            elif (action.name == "Port2"):
                reward = self.factor*payback * \
                    (self.get_probability((3-self.game.current_round), 11-ship_pos_mid))
            else:
                reward = self.factor*payback * \
                    (self.get_probability((3-self.game.current_round), 11-ship_pos_min))


        elif action.get_type() == "shipyard":
            payback = action.get_payback()
            if action.name == "Shipyard1":
                reward = self.factor*payback * \
                    (self.get_probability((3-self.game.current_round), 11-ship_pos_min, False))
            elif action.name == "Shipyard2":
                reward = self.factor*payback * \
                    (self.get_probability((3-self.game.current_round), 11-ship_pos_mid, False))
            else:
                reward =  self.factor*payback * \
                    (self.get_probability((3-self.game.current_round), 11-ship_pos_max, False))

        else:
            reward = 0

        return reward
