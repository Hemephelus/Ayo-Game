import random
import copy
from json.encoder import INFINITY
import math
from ayo_game import play, is_illegal_move, assign_reward, print_game_play, end_game
from agents import random_agent as ra
from agents import random_agent

seed = 37
get_valid_actions_mct = random_agent.get_valid_actions_mct
randint = random.randint
random.seed(seed)
random_agent = ra.agent


class Node():
    def __init__(self,state,root_current_player, action=None,parent_node=None):
        self.parent_node = parent_node
        self.action = action
        self.legal_actions = []
        self.total_score = 0
        self.visit_count = 0
        self.expanded = False
        self.children = None
        self.state = state
        self.root_current_player = root_current_player

    def update_result(self, reward):
        self.total_score += reward
        self.visit_count += 1

    def printer(self):
        print('parent_node: ',self.parent_node)
        print('action: ',self.action)
        print('legal_actions: ',self.legal_actions)
        print('total_score: ',self.total_score)
        print('visit_count: ',self.visit_count)
        print('expanded: ',self.expanded)
        print('children: ',self.children)
        print('root_current_player: ',self.root_current_player)
        print('state: ',self.state)



def expand(node):
    state = node.state
    actions = get_valid_actions_mct(state)
    node.legal_actions = actions
    node.expanded = True
    root_current_player = node.root_current_player
    node.children = {}

    for action in actions:
        new_state, reward = play(state, action)
        node.children[action] = Node(new_state,root_current_player,action,node)
    return node



def resources_left( max_iterations, iterations):
    return max_iterations > iterations



def ucb(constant = 2, total_score = 0, number_of_parent_visits = 0, number_of_visits = 0):
    if number_of_visits == 0:
        return INFINITY
    avg_score = total_score / number_of_visits

    return (avg_score +(constant*math.sqrt(math.log(number_of_parent_visits)/number_of_visits)))



def select(node):
    actions = node.legal_actions

    if len(actions) == 0:
        return None

    best_score = -INFINITY
    for action in actions:
        child = node.children[action]
        total_score = child.total_score
        parent_visit_count = node.visit_count
        visit_count = child.visit_count
        score = ucb(2,total_score, parent_visit_count, visit_count )

        if score > best_score:
            best_score = score
            best_action = action

    return best_action
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

# function for the result of the simulation
def rollout(node):

    state = node.state

    player_1 = {
    'func': random_agent,
    'arg': {}
    }

    player_2 = {
    'func': random_agent,
    'arg': {}
    }

    if end_game(state):
            return 0

    reward, path = simulate_game(state, player_1, player_2)

    if reward[node.root_current_player] > 24:
        results = 1
    if reward[node.root_current_player] < 24:
        results = 0
    if reward[node.root_current_player] == 24:
        results = -1

    return  results


def best_child(node):
    actions = node.legal_actions
    highest_visit = -INFINITY
    for action in actions:
        child = node.children[action]
        visit_count = child.visit_count
        if visit_count > highest_visit:
            highest_visit = visit_count
            best_action = action
    return best_action



def back_propagation(node, result):
    node.update_result(result)
    parent_node =node.parent_node

    if parent_node == None:
        return

    back_propagation(parent_node, result)



def agent(state,arg):
    max_iterations = arg['max_iterations']
    root = Node(state,state['current_player'])
    expand(root)
    node = root
    i = 0

    while resources_left(max_iterations, i):
        i += 1
        while node.children:
            action = select(node)

            if action == None:
                break
            child = node.children[action]
            node = child
            # node.printer()

        if node.visit_count == 0:
            result = rollout(node)
            back_propagation(node, result)
            node = root
        else:
            expand(node)
            action = select(node)
            if action == None:
                break
            child = node.children[action]
            node = child
            result = rollout(node)
            back_propagation(node, result)
            node = root

    return best_child(root)

