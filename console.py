import numpy as np


class Console:
    def __init__(self, players, root):
        self.players = players
        self.num_players = len(players)
        self.root = root
        # record the trainable flags
        self._trainable_dict = dict()
        for player in self.players:
            self._trainable_dict[player] = player.trainable

    def __call__(self, n=100):
        for _ in range(n):
            # run one episode
            rewards = self._play_once()
            # update
            for player in self.players:
                if player.trainable:
                    player.update(rewards=rewards)

    def _play_once(self):
        node = self.root
        while not node.is_terminal:
            player = node.current_player
            node = self.players[player].move(node)
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
        while not node.is_terminal:
            # node.display()
            player = node.current_player
            node = self.players[player].move(node)
        rewards = node.rewards
        node.display()
        print("result: {0}, winner: {1} ".format(rewards, np.argmax(rewards)))

    @untrainable_mode
    def test(self, n=100):
        # play n times
        rewards = np.zeros(self.num_players, dtype=np.float)
        for _ in range(n):
            rewards += self._play_once()
        average_rewards = rewards / n
        print("result: {0}, winner: {1} ".format(average_rewards, np.argmax(rewards)))
        return average_rewards
