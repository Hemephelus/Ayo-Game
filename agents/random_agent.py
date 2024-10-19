import random
randint = random.randint


def get_valid_actions_mct(state):
    board = state['board']
    territory = state['player_territory'][1]
    current_player = state['current_player']
    valid_actions = []
    for i,a in enumerate(board):
        if current_player == 0 and i < territory and a != 0:
                    valid_actions.append(i)
        if current_player == 1 and i >= territory and a != 0:
                    valid_actions.append(i)
    return valid_actions


def agent(state, arg=None):
        valid_actions = get_valid_actions_mct(state)
        return valid_actions[randint(0,len(valid_actions)-1)]