state = {
   'board' :[4,4,4,4,4,4,4,4,4,4,4,4],
   'current_player': 0,
   'player_territory': (0,6)
}

action = 0
format_state(state, action)

def format_state(state, action):
    board = state['board']
    data = []
    for i,pit in enumerate(board):
        num = str(i)
        data[f'pit {num}'] = pit
    data['current_player'] = state['current_player']
    data['player_territory'] = state['player_territory'][1]
    data['action'] = action
    return [data]


# model

# train the value network using minimax

# train the policy network using mcts
# train the value network using mcts

# agent that uses a trained model to predict action
# agent that uses a trained model and mcts to predict action