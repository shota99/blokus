from Blokus_console import BlokusConsole
from Blokus_player import BlokusMCTSPlayer, BlokusRandomPlayer, BlokusHeuristicPlayer
from Blokus import Blokus
from tree_policies import UCT1, Best, Secure, Robust

root = Blokus()
num_players = Blokus.num_players

playerR = BlokusRandomPlayer()
playerH = BlokusHeuristicPlayer()
player0 = BlokusMCTSPlayer(num_players=num_players, tree_policy=UCT1(), trainable=True, new_nodes_per_episode=10)
player1 = BlokusMCTSPlayer(num_players=num_players, tree_policy=UCT1(), trainable=True, new_nodes_per_episode=10)
player2 = BlokusMCTSPlayer(num_players=num_players, tree_policy=UCT1(), trainable=True, new_nodes_per_episode=10)
player3 = BlokusMCTSPlayer(num_players=num_players, tree_policy=UCT1(), trainable=True, new_nodes_per_episode=10)

# player0.load("Blokus_MCTS_player0")
# player1.load("Blokus_MCTS_player1")
# player2.load("Blokus_MCTS_player2")
# player3.load("Blokus_MCTS_player3")

player_list = [playerR, playerH, playerR, playerH]

console = BlokusConsole(players=player_list, root=root)

for i in range(1):
    # console(n=1)
    console.show()
    # console.test(n=10)

# player0.save("Blokus_MCTS_player0")
# player1.save("Blokus_MCTS_player1")
# player2.save("Blokus_MCTS_player2")
# player3.save("Blokus_MCTS_player3")
