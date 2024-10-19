# # # delcaring a dictionary
# # originalDict = {1: "Lahore", 2: "Islamabad", 3: "Karachi"}

# # print("Original Dictionary:", originalDict)

# # # creating a shallow copy using function
# # shallowCopy = dict(originalDict)
# # print("Shallow copy: ", shallowCopy)

# # # adding an element to the shallow copy
# # shallowCopy[1] = "Quetta"

# # # printing the shallow copy after adding an element
# # print("Shallow copy after appending an element: ", shallowCopy)

# # # printing the original dictionary to show no changes took place
# # print("Original dictionary remains the same: ", originalDict)

# # delcaring a dictionary
# originalDict = {1: "A", 2: "B", 3: ["a", "b"]}

# # declaring a new, empty dictionary
# shallowCopy = {}

# print("Original Dictionary:", originalDict)

# # creating a shallow copy using for loop
# for key, value in originalDict.items():
#   shallowCopy[key] = value

# print("Shallow copy: ", shallowCopy)

# # adding an element to the shallow copy
# shallowCopy[4] = "D"

# # printing the shallow copy after adding an element
# print("Shallow copy after adding an element: ", shallowCopy)

# # printing the original dictionary to show no changes took place
# print("Original dictionary remains the same: ", originalDict)

# # however, making a change in the 3rd value of the shallow copy
# # which is a list, will result in the original dictionary being changed
# shallowCopy[3].append("hello")

# print("Shallow Copy after changing list element:", shallowCopy)
# print("Original Dictionary also changes: ", originalDict)




#     # print(game_state)
#     # while stones != 0:
#     #     game_state = play_game(game_state)
#     #     game_state['dept'] += 1
#     #     if game_state['current_player'] == 1:
#     #         game_state['current_player'] = 2
#     #         game_state['starting_position'] = 7
#     #     else:
#     #         game_state['current_player'] = 1
#     #         game_state['starting_position'] = 1

#     #     ayo_board = game_state['ayo_board']
#     #     starting_position = game_state['starting_position']
#     #     stones = ayo_board[starting_position]
#     #     print(game_state)

# # for i in range(6,12):
# # starting_position = 10
# # previous_position = starting_position.copy()

# #   for stone in range(stones):
origin_game_state = {
        'ayo_board': [4,4,4,4,4,4,4,4,4,4,4,4],
        'starting_position': 1,
        'player_1_points': 0,
        'player_2_points': 0,               
        'current_player': 1,     
        'path': [] ,
        'stones': 48,
    }


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

def play_game(game_state):
    game_state = session(game_state)
    stones = total_stones(game_state)

    while stones > 1:
        game_state = session(game_state)
        stones = total_stones(game_state)

    return game_state

s = play_game(origin_game_state)
print(s)


'''
old Ayo logic
'''



# def session(game_state):
#     ayo_board = game_state['ayo_board']
#     starting_position = game_state['starting_position']
#     player_1_points = game_state['player_1_points']
#     player_2_points = game_state['player_2_points']
#     session_number = game_state['session_number']
#     session_number += 1
#     stones = ayo_board[starting_position]

#     for stone in range(stones):
#         current_position = (stone + starting_position + 1) % 12
#         ayo_board[current_position] += 1

#         if ayo_board[current_position] == 4:

#             if stone == stones-1 and current_position < 6 and game_state['current_player'] == 2:
#                 player_2_points += 4
#                 ayo_board[current_position] = 0 
#                 continue

#             if stone == stones-1 and current_position >= 6 and game_state['current_player'] == 1:
#                 player_1_points += 4
#                 ayo_board[current_position] = 0
#                 continue
                    

#             if current_position < 6:
#                 player_1_points += 4

#             else:
#                 player_2_points += 4
            
#             ayo_board[current_position] = 0

#     if ayo_board[starting_position] >= 12:
#         ayo_board[starting_position] = 1

#     elif ayo_board[starting_position] >= 24:
#         ayo_board[starting_position] = 2

#     else:
#         ayo_board[starting_position] = 0

#     game_state = {
#         'ayo_board': ayo_board,
#         'starting_position': current_position,
#         'player_1_points': player_1_points,
#         'player_2_points': player_2_points,
#         'session_number': session_number,
#         'current_player': game_state['current_player'],
#         'dept': game_state['dept'],
#         'path': game_state['path'],
#         'stones': sum(ayo_board),
#     }

#     return game_state



# def play_game(game_state):
#     game_state = session(game_state)
#     ayo_board = game_state['ayo_board']
#     starting_position = game_state['starting_position']
#     stones = ayo_board[starting_position]

#     while stones > 1:
#         game_state = session(game_state)
#         ayo_board = game_state['ayo_board']
#         starting_position = game_state['starting_position']
#         stones = ayo_board[starting_position]
   
#     return game_state