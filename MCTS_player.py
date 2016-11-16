import random

from base_player import BasePlayer

import numpy as np
import networkx as nx

from collections import deque
import pickle


class MCTSPlayer(BasePlayer):
    def __init__(self, num_players, tree_policy,
                 trainable=True, new_nodes_per_episode=1):
        self.num_players = num_players
        self.tree_policy = tree_policy

        self.new_nodes_per_episode = new_nodes_per_episode

        self.graph = nx.DiGraph()
        self._num_new_nodes = 0
        self._replay_buffer = deque()
        super().__init__(trainable)

    def move(self, node):
        if self.trainable:
            if node not in self.graph:
                action = self.do_simulation(node)
            elif self.graph.node[node]['untried_actions']:
                action = self.do_expansion(node)
            else:
                action = self.do_selection(node)
        else:
            if node not in self.graph:
                action = self.do_simulation(node)
            else:
                action = self.do_selection(node)
        next_node = node.act(action)
        return next_node

    def do_selection(self, node):
        action = self.tree_policy(self.graph, node)
        if self.trainable:
            self._replay_buffer.append((node, action))
        return action

    def do_expansion(self, node):
        action = random.choice(tuple(self.graph.node[node]['untried_actions']))
        if self.trainable:
            self.graph.node[node]['untried_actions'].remove(action)
            self.graph.add_edge(node, action,
                                plays=0,
                                rewards=np.zeros(self.num_players, dtype=np.float))
            self._replay_buffer.append((node, action))
        return action

    def do_simulation(self, node):
        action = random.choice(tuple(node.legal_actions))
        if self.trainable and self._num_new_nodes <= self.new_nodes_per_episode:
            self.graph.add_node(node,
                                plays=0,
                                rewards=np.zeros(self.num_players, dtype=np.float),
                                untried_actions=node.legal_actions)
            self.graph.add_edge(node, action,
                                plays=0,
                                rewards=np.zeros(self.num_players, dtype=np.float))
            self._num_new_nodes += 1
            self._replay_buffer.append((node, action))
        return action

    def update(self, rewards):
        if self.trainable:
            for node, action in self._replay_buffer:
                # N_s
                n = self.graph.node[node]['plays']
                self.graph.node[node]['rewards'] = \
                    n / (n + 1) * self.graph.node[node]['rewards'] + \
                    1 / (n + 1) * rewards
                self.graph.node[node]['plays'] += 1
                # N_s,a
                n = self.graph[node][action]['plays']
                self.graph[node][action]['rewards'] = \
                    n / (n + 1) * self.graph[node][action]['rewards'] + \
                    1 / (n + 1) * rewards
                self.graph[node][action]['plays'] += 1
            self._num_new_nodes = 0
            self._replay_buffer.clear()

    def save(self, file_name):
        with open(file_name+'.pickle', "wb") as file:
            pickle.dump(self.graph, file)

    def load(self, file_name):
        with open(file_name+'.pickle', "rb") as file:
            self.graph = pickle.load(file)
        print("loaded MCTS player from {0}, total node {1}".format(file_name, self.graph.number_of_nodes()))


class PriorMCTSPlayer(MCTSPlayer):
    def __init__(self, num_players, tree_policy, prior_model,
                 trainable=True, new_nodes_per_episode=1):
        self.prior_model = prior_model
        super().__init__(num_players, tree_policy, trainable, new_nodes_per_episode)

    def move(self, node):
        pass
