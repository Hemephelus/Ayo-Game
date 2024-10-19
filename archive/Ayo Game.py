
import copy
from json.encoder import INFINITY
from random import random



def four_left(game_state):
    ayo_board = game_state['ayo_board']
    i = 0
    p1 =[]
    p2 =[]
    total_p1 = 0
    total_p2 = 0

    for pot in ayo_board:

        if i < 6:
            total_p1 += pot

            if pot == 1:
                p1.append(i)

        else:
            total_p2 += pot
            
            if pot == 1:
                p2.append(i%6)

        i+=1

    if total_p1 == total_p2:
        p1 =sum(p1)
        p2 = sum(p2)

        if p1 == p2:
            p = (game_state['current_player']%2)+1
            game_state[f'player_{p}_points'] += 4

        elif p1 < p2:
            game_state['player_1_points'] += 4

        else:
            game_state['player_2_points'] += 4

    elif total_p1 > total_p2:
        game_state['player_1_points'] += 4

    else:
        game_state['player_2_points'] += 4

    game_state['ayo_board'] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    
    return game_state


def total_stones(game_state):
    ayo_board = game_state['ayo_board']
    starting_position = game_state['starting_position']
    return ayo_board[starting_position]



def session(game_state):
    ayo_board = game_state['ayo_board']
    starting_position = game_state['starting_position']
    stones = total_stones(game_state)
    
    for stone in range(stones):
        current_position = (stone + starting_position + 1) % 12
        ayo_board[current_position] += 1

        if ayo_board[current_position] == 4:

            if stone == stones-1 and current_position < 6 and game_state['current_player'] == 2:
                game_state['player_2_points'] += 4
                ayo_board[current_position] = 0 
                continue

            if stone == stones-1 and current_position >= 6 and game_state['current_player'] == 1:
                game_state['player_1_points'] += 4
                ayo_board[current_position] = 0
                continue
                    
            if current_position < 6:
                game_state['player_1_points'] += 4

            else:
                game_state['player_2_points'] += 4
            
            ayo_board[current_position] = 0

    if ayo_board[starting_position] >= 12:
        ayo_board[starting_position] = 1

    elif ayo_board[starting_position] >= 24:
        ayo_board[starting_position] = 2

    else:
        ayo_board[starting_position] = 0


    game_state['stones'] = sum(ayo_board)
    game_state['ayo_board'] = ayo_board
    game_state['starting_position'] = current_position

    return game_state

# [0, 9, 1, 9, 1, 11, 3, 7, 0, 6, 0, 7, 2, 10, 0, 6]

def play_game(game_state):
    game_state = session(game_state)
    stones = total_stones(game_state)

    while stones > 1:
        game_state = session(game_state)
        stones = total_stones(game_state)
    
    if sum(game_state['ayo_board']) <= 4:
        game_state = four_left(game_state)

    return game_state



def best_move(origin_game_state):
    all_game_state = []
    max_dept1 = 7
    max_dept2 = 7

    all_game_state.append(origin_game_state)
    
    if origin_game_state['current_player'] == 1:
        best_score = -INFINITY
        for child in range(6):
            temp_state =  copy.deepcopy(all_game_state[-1])
            temp_state['starting_position'] = child
            temp_state['path'].append(child)
            ayo_board = temp_state['ayo_board']

            if ayo_board[child] != 0:
                game_state = play_game(temp_state)
                all_game_state.append(game_state)
                score = minimax(game_state, False,all_game_state,2,max_dept1,-INFINITY,INFINITY)
                all_game_state.pop()

                if score > best_score:
                    best_score = score
                    move = child

    else:
        best_score = INFINITY
        for child in range(6,12):
            temp_state =  copy.deepcopy(all_game_state[-1])
            temp_state['starting_position'] = child
            temp_state['path'].append(child)
            ayo_board = temp_state['ayo_board']

            if ayo_board[child] != 0:
                game_state = play_game(temp_state)
                all_game_state.append(game_state)
                score = minimax(game_state, True,all_game_state,1,max_dept2,-INFINITY,INFINITY)
                all_game_state.pop()

                if score < best_score:
                    best_score = score
                    move = child
    print('best_score',best_score)
    return move



def minimax(game_state, is_maximizing,all_game_state,current_player,max_dept,alpha,beta ):
    max_dept -= 1
    ayo_board = game_state['ayo_board']
    game_state['current_player'] = current_player

    if(max_dept <= 0 or  sum(ayo_board) <= 4):
        return game_state['player_1_points']-game_state['player_2_points']
    
    if is_maximizing:
        best_score = -INFINITY

        for child in range(6):
            temp_state =  copy.deepcopy(all_game_state[-1])
            temp_state['starting_position'] = child
            temp_state['path'].append(child)
            ayo_board = temp_state['ayo_board']

            if ayo_board[child] != 0:
                game_state = play_game(temp_state)
                all_game_state.append(game_state)
                score = minimax(game_state, False,all_game_state,2,max_dept,alpha,beta)
                all_game_state.pop()
                best_score = max(score, best_score)              
                alpha = max(alpha,score)

                if beta <= alpha:
                    break

        return best_score

    else:
        best_score = INFINITY

        for child in range(6,12):
            temp_state =  copy.deepcopy(all_game_state[-1])
            temp_state['starting_position'] = child
            temp_state['path'].append(child)
            ayo_board = temp_state['ayo_board']

            if ayo_board[child] != 0:
                game_state = play_game(temp_state)
                all_game_state.append(game_state)
                score = minimax(game_state, True,all_game_state,1,max_dept,alpha,beta)
                all_game_state.pop()
                best_score = min(score, best_score)
                beta = min(beta,score)

                if beta <= alpha:
                    break

        return best_score



def play_ayo():
    origin_game_state = {
        'ayo_board': [4,4,4,4,4,4,4,4,4,4,4,4],
        'starting_position': 0,
        'player_1_points': 0,
        'player_2_points': 0,              
        'current_player': 1,    
        'path': [] ,
        'stones': 48,
    }

    print('\n')
    player = 1
    player = int(input('What player are you? (1 or 2): '))
    print('\n')
    origin = 0

    if player == 1:
        origin = 0
    else:
        origin = 6
   
    print(origin_game_state['ayo_board'])
    print(origin_game_state['player_1_points'],origin_game_state['player_2_points'])
    print("Path: ", origin_game_state['path'])
  
    while  sum(origin_game_state['ayo_board']) > 4:

        if origin_game_state['player_1_points'] == origin_game_state['player_2_points']:
            print('They are in a Tie')
        elif origin_game_state['player_1_points'] > origin_game_state['player_2_points']:
            print('Player 1 is winning')
        elif origin_game_state['player_1_points'] < origin_game_state['player_2_points']:
            print('Player 2 is winning')

        if player == 1:
            # human plays
            print('\n\n')
            position = int(input('What position will you play? ')) + origin
            # position = best_move(origin_game_state)
            if origin_game_state['ayo_board'][position] == 0:
                print('Sorry you cannot play from this position. Try another spot')
                continue
            print('Human\'s move: ', position)
            origin_game_state['path'].append(position)
            origin_game_state['starting_position'] = position
            origin_game_state = play_game(origin_game_state)
            origin_game_state['current_player'] = ((origin_game_state['current_player'])%2)+1
            player = 2
            
        else:
            # ai plays
            print('\n\n')
            position = best_move(origin_game_state)
            if origin_game_state['ayo_board'][position] == 0:
                print('Sorry you cannot play from this position. Try another spot')
                continue
            print("AI's move: ",position)
            origin_game_state['path'].append(position)
            origin_game_state['starting_position'] = position
            origin_game_state = play_game(origin_game_state)
            origin_game_state['current_player'] = ((origin_game_state['current_player'])%2)+1
            player = 1

        print(origin_game_state['ayo_board'])
        print(origin_game_state['player_1_points'],origin_game_state['player_2_points'])
        print("Path: ", origin_game_state['path'])

    if origin_game_state['player_1_points'] > origin_game_state['player_2_points']:
        print('Player 1 Wins')
    elif origin_game_state['player_1_points'] < origin_game_state['player_2_points']:
        print('Player 2 Wins')
    else:
        print('Tie')

        

    print('\n\n\n')
    print(origin_game_state)

play_ayo()


#  11 = [0, 6, 5, 11, 1, 6, 0, 6, 3, 6, 2, 6, 0, 8, 1, 9, 0, 10]
#  10 = [0, 6, 5, 10, 2, 10, 2, 7, 0, 8, 2, 6, 0, 6, 0, 6, 2, 6]
#  9 = [0, 6, 5, 10, 2, 8, 4, 6, 0, 8, 0, 6, 1, 6, 2, 7, 0, 9, 1, 10, 0, 7, 2, 8, 3]
#  8 = [0, 6, 1, 7, 1, 10, 0, 7, 0, 8, 1, 6, 4, 6, 3, 9, 5, 8, 0, 7, 1, 6, 2, 7, 4, 9]
#  7 = [0, 6, 5, 10, 2, 10, 2, 7, 0, 8, 2, 6, 0, 6, 0, 6, 2, 6]
#  6 = [0, 6, 5, 10, 2, 8, 2, 10, 1, 7, 0, 6, 0, 7, 2, 6, 3, 8, 4, 6, 5]
#  5 = [0, 6, 3, 11, 3, 10, 2, 7, 1, 6, 4, 9]
#  4 = [0, 9, 1, 6, 0, 10, 0, 7, 0, 7]
#  3 = [3, 10, 5, 8, 1, 8, 3, 6, 1, 6, 2, 7, 4] -> 20 28
#  2 = [0, 7, 3, 6, 0, 6, 2, 7, 3, 6, 4, 6] -> 12 20 #could not compute
#  1 = [0, 7, 2, 6, 3, 6, 0, 7, 0, 6, 1, 7, 2, 10, 0, 11] -> 20 28