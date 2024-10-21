import multiprocessing
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
# from tensorflow.keras import callbacks
 

import copy
import random
from json.encoder import INFINITY
import pandas as pd
import math
from ayo_game import play, is_illegal_move, assign_reward, print_game_play, end_game
from agents import random_agent as ra
from agents import minimax_agent as ma
from agents import mcts_agent as mctsa
seed = 37

randint = random.randint
random.seed(seed)
value_model_file = 'latest_value_model.keras'
policy_model_file = 'latest_policy_model.keras'
# checkpoint_filepath = 'latest.keras'
# checkpoint_filepath = 'multi.keras'

minimax_agent = ma.agent


def format_state(state):
    x = []
    x.extend(state['board'])
    x.append(state['current_player'])
    x.append(state['player_territory'][1])

    return x


def custom_train_test_split(data, test_size=0.2, shuffle=True, random_state=None):
    """
    Custom function to split data into training and test sets.

    Parameters:
    - X: Input features (numpy array or list)
    - y: Target labels (numpy array or list)
    - test_size: Proportion of the data to include in the test split (default 0.2)
    - shuffle: Whether to shuffle the data before splitting (default True)
    - random_state: Seed for the random number generator (optional, for reproducibility)

    Returns:
    - X_train, X_test, y_train, y_test: Split training and testing data
    """
    X = np.array([d[0] for d in data])
    y = np.array([d[1] for d in data])

    # Set random seed if provided (to ensure reproducibility)
    if random_state is not None:
        np.random.seed(random_state)

    # Get the number of samples
    num_samples = len(X)

    # Shuffle the data if requested
    if shuffle:
        indices = np.random.permutation(num_samples)
        X = X[indices]
        y = y[indices]

    # Compute the split index
    split_index = int(num_samples * (1 - test_size))

    # Split the data into training and testing sets
    X_train, X_test = X[:split_index], X[split_index:]
    y_train, y_test = y[:split_index], y[split_index:]

    return X_train, X_test, y_train, y_test


def remove_duplicates(arr):
    # Convert the list of lists to a NumPy array
    np_arr = np.array(arr, dtype=object)
    
    # Create a set to keep track of unique first elements (list of numbers)
    seen = set()
    unique_arr = []

    for item in np_arr:
        # Convert the list of numbers (first element) to a tuple so it can be added to a set
        num_tuple = tuple(item[0])
        if num_tuple not in seen:
            unique_arr.append(item)
            seen.add(num_tuple)
    
    return np.array(unique_arr, dtype=object)


class PolicyModel:
    def __init__(self):
        self.num_actions=12
        self.X_shape=14
        self.model = Sequential([
            Dense(64, input_dim=self.X_shape, activation='relu'),  # First hidden layer
            Dense(32, activation='relu'),  # Second hidden layer
            Dense(self.num_actions, activation='softmax')  # Output layer for 12 possible actions
        ])

        # Compile the model
        self.model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'], )

    def train(self, training_examples):
                # Train the model (Assume more training data is available)
        # For example purposes, we'll use the same sample data multiple times
        X_train, X_test, y_train, y_test = custom_train_test_split(training_examples, test_size=0.3, shuffle=True, random_state=None)

        # Convert target (y) to categorical (for classification)
        num_actions = self.num_actions # Assuming 12 possible actions (0 to 11)
        y_train = tf.keras.utils.to_categorical(y_train, num_classes=num_actions)
        y_test = tf.keras.utils.to_categorical(y_test, num_classes=num_actions)

        callbacks = [EarlyStopping(patience=20, monitor='loss', verbose=0),
             ReduceLROnPlateau(monitor='val_accuracy',factor=0.01, min_Ir=0.00001, verbose=0),
             ModelCheckpoint('latest_policy_model.keras', verbose=0, save_best_only=True, save_weights_only=False)]

        # Train the model (Assume more training data is available)
        # For example purposes, we'll use the same sample data multiple times
        self.model.fit(X_train, y_train, epochs=200, batch_size=64,  callbacks=callbacks, validation_data=(X_test,y_test))


    def predict(self,data):
        data = np.array(data)
        prediction = self.model.predict(data, verbose=None)
        return prediction[0]
    

class ValueModel:
    def __init__(self):
        self.X_shape= 14
        self.model = Sequential([
            Dense(64, input_dim=self.X_shape, activation='relu'),  # First hidden layer
            Dense(32, activation='relu'),  # Second hidden layer
            Dense(1)  # Output layer for 12 possible actions
        ])

        # Compile the model
        self.model.compile(optimizer='adam', loss='mean_squared_error', metrics=['accuracy'])

    def train(self, training_examples):
        # Train the model (Assume more training data is available)
        # For example purposes, we'll use the same sample data multiple times
        X_train, X_test, y_train, y_test = custom_train_test_split(training_examples, test_size=0.3, shuffle=True, random_state=None)

        callbacks = [EarlyStopping(patience=20, monitor='loss', verbose=0),
             ReduceLROnPlateau(monitor='val_accuracy',factor=0.01, min_Ir=0.00001, verbose=0),
             ModelCheckpoint('latest_value_model.keras', verbose=0, save_best_only=True, save_weights_only=False)]

        self.model.fit(X_train, y_train, epochs=200, batch_size=64,  callbacks=callbacks, validation_data=(X_test,y_test))


    def predict(self,data):
        # Predict action for a new data point
        data = np.array(data)
        prediction = self.model.predict(data, verbose=None)
        return prediction[0][0]



value_model = ValueModel()
policy_model = PolicyModel()


def get_valid_actions_mct(state):
    board = state['board']
    territory = state['player_territory'][1]
    current_player = state['current_player']
    valid_actions = []
    for i,a in enumerate(board):
        if current_player == 0 and i < territory and a != 0:
                valid_actions.append(1)
                continue
        if current_player == 1 and i >= territory and a != 0:
                valid_actions.append(1)
                continue
        valid_actions.append(0)
    return valid_actions


class Node():
    def __init__(self,state,prior,parent_node=None):
        self.parent_node = parent_node
        self.prior = prior
        self.total_score = 0
        self.visit_count = 0
        self.expanded = False
        self.children = {}
        self.state = state

    def update_result(self, reward):
        self.total_score += reward
        self.visit_count += 1

    def printer(self):
        print('parent_node: ',self.parent_node)
        print('total_score: ',self.total_score)
        print('visit_count: ',self.visit_count)
        print('expanded: ',self.expanded)
        print('children: ',self.children)
        print('state: ',self.state)



def expand(node, action_probs):
    """
    We expand a node and keep track of the prior policy probability given by neural network
    """
    state = node.state
    for action, prob in enumerate(action_probs):
        if prob != 0:
            new_state, _ = play(state, action)
            node.children[action] = Node(state=new_state,prior=prob,parent_node=node)

    node.expanded = True



def resources_left( max_iterations, iterations):
    return max_iterations > iterations


def ucb_score(parent, child):
    """
    The score for an action that would transition between the parent and child.
    """
    prior_score = child.prior * math.sqrt(parent.visit_count) / (child.visit_count + 1)
    if child.visit_count > 0:
        # The value of the child is from the perspective of the opposing player
        value_score = child.total_score / child.visit_count
    else:
        value_score = np.inf
    return value_score + prior_score



def select(node):
    """
    Select the child with the highest UCB score.
    """
    best_score = -np.inf
    best_action = -1
    best_child = None

    for action, child in node.children.items():
        score = ucb_score(node, child)
        if score > best_score:
            best_score = score
            best_action = action
            best_child = child

    return best_action, best_child


def generate_action(state,agent_1, agent_2):
   if state['current_player'] == 0:
      func = agent_1['func']
      arg = agent_1['arg']
      return func(state, arg)

   if state['current_player'] == 1:
      func = agent_2['func']
      arg = agent_2['arg']
      return func(state, arg)



def simulate_game(state,  agent_1, agent_2,show=False):
    state = copy.deepcopy(state)
    reward = [0,0,0]
    path = []

    while True:
        action = generate_action(state, agent_1, agent_2)

        if is_illegal_move(state, action):
            continue

        state, new_reward = play(state, action)
        reward = assign_reward(reward, new_reward)
        if show:
            print_game_play(state, reward, action)

        if end_game(state):
            break
        path.append(action)

    return  (reward, path)



def best_child(node):
    actions = node.action_prob
    highest_visit = -INFINITY
    for action in actions:
        child = node.children[action]
        visit_count = child.visit_count
        if visit_count > highest_visit:
            highest_visit = visit_count
            best_action = action
    return best_action



def back_propagation(node, result):
    act_result = result * ((-1)**node.state['current_player'])
    node.update_result(act_result)

    parent_node = node.parent_node

    if parent_node == None:
        return

    back_propagation(parent_node, result)



def mcts(state,max_iterations):
    root = Node(state,state['current_player'])
    data = [format_state(root.state)]
    action_probs = policy_model.predict(data)
    valid_actions = np.array(get_valid_actions_mct(state))
    action_probs = action_probs *valid_actions
    action_probs /= np.sum(action_probs)
    expand(root, action_probs)
    i = 0    
    
    while resources_left(max_iterations, i):
        node = root
        while len(node.children) > 0:
            _, child = select(node)
            if child == None:
                break
            node = child


        data = [format_state(node.state)]
        if node.visit_count != 0:
            action_probs = policy_model.predict(data)
            valid_actions = np.array(get_valid_actions_mct(node.state))
            action_probs = action_probs * valid_actions
            action_probs /= np.sum(action_probs)
            expand(node, action_probs)
    
        result = value_model.predict(data)
        # print(result,data)
        back_propagation(node, result)
        i += 1

    return root

def select_action(node, temperature):
        """
        Select action according to the visit count distribution and the temperature.
        """
        visit_counts = np.array([child.visit_count for child in node.children.values()])
        actions = [action for action in node.children.keys()]
        if temperature == 0:
            action = actions[np.argmax(visit_counts)]
        elif temperature == float("inf"):
            action = np.random.choice(actions)
        else:
            # See paper appendix Data Generation
            visit_count_distribution = visit_counts ** (1 / temperature)
            visit_count_distribution = visit_count_distribution / sum(visit_count_distribution)
            action = np.random.choice(actions, p=visit_count_distribution)

        return action

def agent(state, arg):
    max_iterations = arg['max_iterations']
    temperature = arg['temperature']
    root = mcts(state, max_iterations)
    return select_action(root, temperature)



def execute_episode(state,  agent_1, agent_2,show=False):
    state = copy.deepcopy(state)
    reward = [0,0,0]
    path = []
    train_example_policy = []
    train_example_value = []

    while True:
        action = generate_action(state, agent_1, agent_2)
        
        if is_illegal_move(state, action):
            continue

        train_example_policy.append([format_state(state), action])
        state, new_reward = play(state, action)
        reward = assign_reward(reward, new_reward)

        if show:
            print_game_play(state, reward, action)

        if end_game(state):
            diff = reward[0] - reward[1]

            if diff < 0:
                value = -1
            elif diff > 0:
                value = 1
            else:
                value = 0

            for hist_state, action in train_example_policy:
                player_value = value * ((-1) ** (hist_state[12]))
                train_example_value.append([hist_state, player_value])
                
            break
        path.append(action)

    return  train_example_value, train_example_policy, path


def generate_training_data(num_of_eps):
    value_data = []
    policy_data = []

    state = {
   'board' :[4,4,4,4,4,4,4,4,4,4,4,4],
   'current_player': 0,
   'player_territory': (0,6)
    }
    
    agent_1 = {
    'func': agent,
    'arg': {
        'max_iterations': 100,
        'temperature': 1,
    },
    'name': 'mcts_agent',
    'elo': 1200
    }

    agent_2 = {
    'func': agent,
    'arg': {
        'max_iterations': 100,
        'temperature': 1,
    },
    'name': 'mcts_agent',
    'elo': 1200
    }

    for i in range(num_of_eps):
        state['current_player'] = i%2
        state_value_data, state_policy_data, path = execute_episode(state,  agent_1, agent_2)
        value_data.extend(state_value_data)
        policy_data.extend(state_policy_data)
        # print(reward)
        
    return remove_duplicates(value_data), remove_duplicates(policy_data)




def test_play(num_of_eps):
    value_data = []
    policy_data = []

    state = {
   'board' :[4,4,4,4,4,4,4,4,4,4,4,4],
   'current_player': 0,
   'player_territory': (0,6)
    }
    
    agent_1 = {
    'func': agent,
    'arg': {
        'max_iterations': 100,
        'temperature': 0,
    },
    'name': 'mcts_agent',
    'elo': 1200
    }

    agent_2 = {
    'func': minimax_agent,
    'arg': {
        'max_dept': 3,
    },
    'name': 'minimax_agent',
    'elo': 1200
    }

    for i in range(num_of_eps):
        state['current_player'] = i%2
        state_value_data, state_policy_data, path = execute_episode(state,  agent_1, agent_2,True)
        print('state_value_data: ', state_value_data)
        print('state_policy_data: ', state_policy_data)
        print('path: ', path)
        value_data.extend(state_value_data)
        policy_data.extend(state_policy_data)
        
    return remove_duplicates(value_data), remove_duplicates(policy_data)



# num = 100
# for _ in range(num):
#     value_data, policy_data = generate_training_data(100)
#     value_model.train(value_data)
#     policy_model.train(policy_data)
#     test_play(1)




if __name__ == '__main__':
    pool = multiprocessing.Pool()
    results = pool.map(generate_training_data, [1,2,3,4,5,6,7,8,9,10])
    # value_data, policy_data = generate_training_data(100)
    # value_model.train(value_data)
    # policy_model.train(policy_data)
    # test_play(1)
    print(results)