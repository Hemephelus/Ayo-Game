import copy
from json.encoder import INFINITY
from ayo_game import play, assign_reward, end_game


def agent(state, arg):
    max_dept = arg['max_dept']
    reward = [0,0,0]
    all_game_state = []
    all_game_state.append((state, reward))

    if state['current_player'] == 0:
        best_score = -INFINITY
        for action in range(state['player_territory'][1]):
            temp_state, reward =  copy.deepcopy(all_game_state[-1])
            game_state, new_reward = play(temp_state, action)
            reward = assign_reward(reward, new_reward)
            all_game_state.append((game_state, reward))
            score = minimax(game_state, False, all_game_state, reward, max_dept, -INFINITY, INFINITY)
            all_game_state.pop()

            if score > best_score:
                best_score = score
                move = action

    else:
        best_score = INFINITY
        for action in range(state['player_territory'][1],12):
            temp_state, reward =  copy.deepcopy(all_game_state[-1])
            game_state, new_reward = play(temp_state, action)
            reward = assign_reward(reward, new_reward)
            all_game_state.append((game_state, reward))
            score = minimax(game_state, True,all_game_state,reward,max_dept,-INFINITY,INFINITY)
            all_game_state.pop()

            if score < best_score:
                best_score = score
                move = action
    return move



def minimax(game_state, is_maximizing,all_game_state,reward,max_dept,alpha,beta ):
    max_dept -= 1

    if(max_dept <= 0 or  end_game(game_state)):
        return reward[0]-reward[1]

    if is_maximizing:
        best_score = -INFINITY

        for action in range(game_state['player_territory'][1]):
            temp_state, reward =  copy.deepcopy(all_game_state[-1])
            game_state, new_reward = play(temp_state, action)
            reward = assign_reward(reward, new_reward)
            all_game_state.append((game_state, reward))
            score = minimax(game_state, False,all_game_state,reward,max_dept,alpha,beta)
            all_game_state.pop()
            best_score = max(score, best_score)
            alpha = max(alpha,score)

            if beta <= alpha:
                break

        return best_score

    else:
        best_score = INFINITY

        for action in range(game_state['player_territory'][1],12):
            temp_state, reward =  copy.deepcopy(all_game_state[-1])
            game_state, new_reward = play(temp_state, action)
            reward = assign_reward(reward, new_reward)
            all_game_state.append((game_state, reward))
            score = minimax(game_state, True,all_game_state,reward,max_dept,alpha,beta)
            all_game_state.pop()
            best_score = min(score, best_score)
            beta = min(beta,score)

            if beta <= alpha:
                break

        return best_score
