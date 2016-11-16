# from MCTS_player import MCTSPlayer

import random
from copy import deepcopy


class BlokusRandomPlayer:
    trainable = False

    @staticmethod
    def move(node, all_legal_actions):
        action = random.choice(tuple(node.legal_actions))
        all_legal_actions.update(action)
        next_node = deepcopy(all_legal_actions.blokus)
        return next_node


class BlokusMCTSPlayer(MCTSPlayer):
    def move(self, node, all_legal_actions=None):
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
        if all_legal_actions is not None:
            all_legal_actions.update(action)
            next_node = deepcopy(all_legal_actions.blokus)
        else:
            next_node = node.act(action)
        return next_node


class BlokusHeuristicPlayer:
    trainable = False

    @staticmethod
    def move(node, all_legal_actions=None):
        score = dict()
        for action in node.legal_actions:
            size_piece, num_corner, num_action, piece_blocking, edge_blocking = \
                all_legal_actions.get_heuristic_info(action)
            score[action] = 50 * size_piece + 1.3 * num_action + sum(piece_blocking[1:4]) - 0.5 * edge_blocking
        action = max(node.legal_actions, key=lambda action: score[action])
        size_piece, num_corner, num_action, piece_blocking, edge_blocking = \
            all_legal_actions.get_heuristic_info(action)
        print("piece size: {}, new corner: {}, new action: {}, blocking: {}, edge blocking: {}".format(
            size_piece, num_corner, num_action, piece_blocking, edge_blocking))
        if all_legal_actions is not None:
            all_legal_actions.update(action)
            next_node = deepcopy(all_legal_actions.blokus)
        else:
            next_node = node.act(action)
        return next_node
