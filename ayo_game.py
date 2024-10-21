import copy

def end_game(state):
    return sum(state['board']) == 0

def assign_reward(reward, new_reward):
    return [reward[0] + new_reward[0], reward[1] + new_reward[1], new_reward[2]]


def terminate_loop(state):
    state['board'] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    reward = (0,0,0)

    return (state, reward)


def print_game_play(state, reward, new_starting_position):
    print('new_starting_position: ', new_starting_position)
    print('state: ', state)
    print('reward: ', reward)
    print('--------------------')


def four_left(state, reward):
    state['board'] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    if reward[2] == 0:
        return  (4,0,0)

    if reward[2] == 1:
        return  (0,4,1)


def get_valid_actions(arr):
    new_arr = []
    for i,a in enumerate(arr):
        if a != 0:
            new_arr.append(i)
    return new_arr



def is_valid_actions(state):

    if state['current_player'] == 0:
          val = state['board'][0:state['player_territory'][1]]
          return sum(val)

    if state['current_player'] == 1:
          val = state['board'][state['player_territory'][1]:12]
          return sum(val)


def get_reward(stones_in_pit, board, position, stone, current_player, player_territory):
    board[position] = 0
    if stone == stones_in_pit-1 and position < player_territory[1] and current_player == 1:
        return (0,4,1)

    if stone == stones_in_pit-1 and position >= player_territory[1] and current_player == 0:
        return  (4,0,0)

    if position < player_territory[1]:
        return  (4,0,0)
        # return (0,4,1)

    else:
        return (0,4,1)


def is_illegal_move(state, action):
    board = state['board']
    current_player = state['current_player']
    player_territory = state['player_territory']
    stones_in_pit = board[action]

    # is pit empty
    if stones_in_pit == 0:
        # print('pit is empty')
        return True

    # is pit not in player one's territory
    if current_player == 0 and action >= player_territory[1]:
        # print("pit is not in player 1's territory")
        return True

    # is pit not in player two's territory
    if current_player == 1 and action <  player_territory[1]:
        # print("pit is not in player 2's territory")
        return True

    return False


def session(state, starting_position,latest_winner ):
    new_state = copy.deepcopy(state)

    board = new_state['board']
    current_player = new_state['current_player']
    player_territory = new_state['player_territory']
    stones_in_pit = board[starting_position]
    board[starting_position] = 0
    reward = [0,0,latest_winner]


    for stone in range(stones_in_pit):
        future_position = (stone + starting_position + 1) % 12
        board[future_position] += 1

        if board[future_position] == 4:
             new_reward = get_reward(stones_in_pit, board, future_position, stone, current_player, player_territory)
             reward = assign_reward(reward, new_reward)

    return (new_state, reward, future_position)


def play(state, action, show=False):
    reward = [0,0,0]
    max_rez = 50
    rez = 0
    # print(is_illegal_move(state, action))
    if is_illegal_move(state, action):
        new_state = {
        'board' : [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        'current_player': state['current_player'],
        'player_territory': (0,6)}
        r = new_state['current_player']
        reward = [r*400,((r+1)%2)*400,0]
        return (new_state, reward)

    state, new_reward, new_starting_position = session(state, action, reward[2])
    reward = assign_reward(reward, new_reward)
    if show:
        print_game_play(state, reward, new_starting_position)

    board = state['board']
    stones_in_pit = board[new_starting_position]

    while stones_in_pit > 1:
        state, new_reward, new_starting_position = session(state,new_starting_position,reward[2])
        reward = assign_reward(reward, new_reward)
        if show:
            print_game_play(state, reward, new_starting_position)

        board = state['board']
        stones_in_pit = board[new_starting_position]

        if rez > max_rez:
            state, reward = terminate_loop(state)
            return (state, reward)

        rez += 1


    state['current_player'] = +(not state['current_player'])

    if sum(state['board']) <= 4:
        new_reward = four_left(state, reward)
        reward = assign_reward(reward, new_reward)

    if not is_valid_actions(state):
        state['current_player'] = +(not state['current_player'])

    return (state, reward)