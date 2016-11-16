from console import Console
from Blokus import LegalAction

from copy import deepcopy
import numpy as np


class BlokusConsole(Console):
    def _play_once(self):
        node = deepcopy(self.root)
        all_legal_actions = LegalAction(node)
        while not node.is_terminal:
            player = node.current_player
            node = self.players[player].move(node, all_legal_actions)
        rewards = node.rewards
        return rewards

    def untrainable_mode(func):
        def wrapper(self, *args, **kwargs):
            # set all players to untrainable temporarily
            for player in self.players:
                player.trainable = False
            # call the function
            result = func(self, *args, **kwargs)
            # change back the trainable flag
            for player in self.players:
                player.trainable = self._trainable_dict[player]
            return result
        return wrapper

    @untrainable_mode
    def show(self):
        node = self.root
        all_legal_actions = LegalAction(node)
        while not node.is_terminal:
            node.color_plot()
            print("player: {0}, #actions: {1}".format(node.current_player, len(node.legal_actions)))
            player = node.current_player
            node = self.players[player].move(node, all_legal_actions)
        rewards = node.rewards
        node.color_plot()
        print("result: {0}, winner: {1} ".format(rewards, np.argmax(rewards)))
