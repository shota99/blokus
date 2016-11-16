import numpy as np
import random
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib import colors
from scipy import ndimage
from itertools import product, chain

from copy import deepcopy
from base_state import BaseState

pieces = np.array([
    [[0, 0]],  # 0
    [[0, 0], [0, -1]],  # 1
    [[0, 0], [0, 1], [0, -1]],  # 2
    [[0, 0], [0, 1], [1, 0]],  # 3
    [[0, 0], [0, 1], [0, -1], [0, -2]],  # 4
    [[0, 0], [0, 1], [0, -1], [-1, -1]],  # 5
    [[0, 0], [0, 1], [0, -1], [1, 0]],  # 6
    [[0, 0], [1, 0], [0, -1], [1, -1]],  # 7
    [[0, 0], [-1, 0], [0, -1], [1, -1]],  # 8
    [[0, 0], [0, 1], [0, 2], [0, -1], [0, -2]],  # 9
    [[0, 0], [0, 1], [0, 2], [0, -1], [-1, -1]],  # 10
    [[0, 0], [0, 1], [0, 2], [-1, 0], [-1, -1]],  # 11
    [[0, 0], [0, 1], [0, -1], [-1, 0], [-1, -1]],  # 12
    [[0, 0], [0, 1], [0, -1], [-1, 1], [-1, -1]],  # 13
    [[0, 0], [0, 1], [0, -1], [0, -2], [1, 0]],  # 14
    [[0, 0], [0, 1], [0, -1], [-1, -1], [1, -1]],  # 15
    [[0, 0], [0, 1], [0, 2], [1, 0], [2, 0]],  # 16
    [[0, 0], [0, 1], [-1, 1], [1, 0], [1, -1]],  # 17
    [[0, 0], [-1, 0], [-1, 1], [1, 0], [1, -1]],  # 18
    [[0, 0], [-1, 0], [-1, 1], [1, 0], [0, -1]],  # 19
    [[0, 0], [-1, 0], [0, 1], [1, 0], [0, -1]]  # 20
])
patterns = [
    [0, 0, 0, 0, 0, 0, 0, 0],  # 0
    [0, 1, 0, 1, 0, 1, 0, 1],  # 1
    [0, 1, 0, 1, 0, 1, 0, 1],  # 2
    [0, 1, 2, 3, 1, 2, 3, 0],  # 3
    [0, 1, 0, 1, 0, 1, 0, 1],  # 4
    [0, 1, 2, 3, 4, 5, 6, 7],  # 5
    [0, 1, 2, 3, 2, 3, 0, 1],  # 6
    [0, 0, 0, 0, 0, 0, 0, 0],  # 7
    [0, 1, 0, 1, 4, 5, 4, 5],  # 8
    [0, 1, 0, 1, 0, 1, 0, 1],  # 9
    [0, 1, 2, 3, 4, 5, 6, 7],  # 10
    [0, 1, 2, 3, 4, 5, 6, 7],  # 11
    [0, 1, 2, 3, 4, 5, 6, 7],  # 12
    [0, 1, 2, 3, 2, 3, 0, 1],  # 13
    [0, 1, 2, 3, 4, 5, 6, 7],  # 14
    [0, 1, 2, 3, 0, 1, 2, 3],  # 15
    [0, 1, 2, 3, 1, 2, 3, 0],  # 16
    [0, 1, 2, 3, 1, 2, 3, 0],  # 17
    [0, 1, 0, 1, 4, 5, 4, 5],  # 18
    [0, 1, 2, 3, 4, 5, 6, 7],  # 19
    [0, 0, 0, 0, 0, 0, 0, 0],  # 20
]
uni_patterns = [set(pattern) for pattern in patterns]
sizes = [1, 2, 3, 3, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]

rotate_func = [lambda i, j: (i, j),
               lambda i, j: (-j, i),
               lambda i, j: (-i, -j),
               lambda i, j: (j, -i),
               lambda i, j: (-i, j),
               lambda i, j: (-j, -i),
               lambda i, j: (i, -j),
               lambda i, j: (j, i)]


def rotate(piece_type, pattern):
    return np.array([rotate_func[pattern](i, j) for (i, j) in pieces[piece_type]], dtype=np.int8)


def get_blocks(piece_type, pattern, location):
    x, y = location
    return rotate(piece_type, pattern) + [x, y]


struct4 = ndimage.generate_binary_structure(2, 1)
struct8 = ndimage.generate_binary_structure(2, 2)


class Blokus(BaseState):
    init_pieces_sets = [set(), set(), set(), set()]
    init_player = 0
    num_players = 4

    def __init__(self, pieces_sets=init_pieces_sets, current_player=init_player):
        self.pieces_sets = pieces_sets
        self.current_player = current_player
        self.legal = self.get_legal()

    def get_board(self):
        board = np.zeros(shape=(20, 20), dtype=np.int8)
        for player in range(4):
            for piece_args in self.pieces_sets[player]:
                for (x, y) in get_blocks(*piece_args):
                    board[x][y] = player + 1
        return board

    def display(self):
        board = self.get_board().astype(str)
        for i in range(20):
            print(" ".join(board[i]).translate(str.maketrans('01234', '.RBGY')))
        print('')

    def color_plot(self):
        board = self.get_board()
        img = board
        fig, ax = plt.subplots(figsize=(5, 5))
        cmap = colors.ListedColormap(['white', 'red', 'blue', 'green', 'yellow'])
        major_ticks = np.arange(-0.5, 20, 5)
        minor_ticks = np.arange(-0.5, 20, 1)
        ax.set_xticks(major_ticks)
        ax.set_xticks(minor_ticks, minor=True)
        ax.set_yticks(major_ticks)
        ax.set_yticks(minor_ticks, minor=True)
        ax.grid(which='both')
        ax.grid(which='minor', alpha=0.5)
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        bounds = [0, 1, 2, 3, 4, 5]
        norm = colors.BoundaryNorm(bounds, cmap.N)
        ax.imshow(img, cmap=cmap, norm=norm, interpolation='nearest')
        plt.show()

    def allowed_and_corner_position(self):
        board = self.get_board()
        # allowed position, 20x20 boolean array
        unoccupied = (board == 0)
        own = (board == (self.current_player + 1))
        adjacent4 = ndimage.binary_dilation(own, structure=struct4)
        allowed = np.logical_and(np.logical_not(adjacent4), unoccupied)
        # list of corner positions of shape [x,y]
        if self.pieces_sets[self.current_player]:
            adjacent8 = ndimage.binary_dilation(own, structure=struct8)
            corner = np.argwhere(np.logical_and(allowed, adjacent8))
        else:
            corner = [[[19, 0], [0, 0], [0, 19], [19, 19]][self.current_player]]
        return allowed, corner

    # @profile
    def get_legal(self, allowed=None, corner=None):
        if corner is None:
            allowed, corner = self.allowed_and_corner_position()
        # get remained pieces
        used = [piece_args[0] for piece_args in self.pieces_sets[self.current_player]]
        remained_pieces = set(range(21)) - set(used)
        # get legal actions
        legal = []
        for remained_piece in remained_pieces:
            for pattern in uni_patterns[remained_piece]:
                abs_blocks = rotate(remained_piece, pattern)
                for (x, y) in corner:
                    for (i, j) in abs_blocks:
                        blocks = abs_blocks + [x - i, y - j]
                        if np.all(blocks >= 0) and np.all(blocks < 20):
                            row, col = blocks.transpose()
                            if np.all(allowed[row, col]):
                                piece_args = (remained_piece, pattern, (x - i, y - j))
                                legal.append(piece_args)
        return set(legal)

    @property
    def legal_actions(self):
        return self.legal

    @property
    def next_player(self):
        return [1, 2, 3, 0][self.current_player]

    def act(self, action):
        new_pieces_sets = deepcopy(self.pieces_sets)
        new_pieces_sets[self.current_player].add(action)
        new_board = Blokus(new_pieces_sets, self.next_player)
        for _ in range(3):
            if new_board.legal_actions:
                return new_board
            else:
                new_board = Blokus(new_pieces_sets, new_board.next_player)
        return new_board

    @property
    def is_terminal(self):
        return len(self.legal_actions) == 0

    @property
    def rewards(self):
        board = self.get_board()
        used = np.array([(board == i + 1).sum() for i in range(4)])
        return used - 89

    def __hash__(self):
        immutable = tuple([frozenset(pieces) for pieces in self.pieces_sets])
        return hash(immutable)


class LegalAction:
    def __init__(self, blokus):
        self.blokus = deepcopy(blokus)
        self.graphs = [nx.Graph(), nx.Graph(), nx.Graph(), nx.Graph()]
        for _ in range(4):
            self.blokus.current_player = (self.blokus.current_player + 1) % 4
            self.graphs[self.blokus.current_player].add_nodes_from(product(range(20), range(20)), bipartite=1)
            legal_actions = self.blokus.get_legal()
            self.graphs[self.blokus.current_player].add_nodes_from(legal_actions, bipartite=0)
            for legal_action in legal_actions:
                edges = [(legal_action, tuple(block)) for block in get_blocks(*legal_action)]
                self.graphs[self.blokus.current_player].add_edges_from(edges)

    def _get_action_info(self, action):
        # get block set
        block_arr = get_blocks(*action)
        block_set = set([tuple(block) for block in block_arr])
        # get edge set
        adjacent4 = set(chain.from_iterable([((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1))
                                             for x, y in block_set]))
        edge_set = set([(x, y) for x, y in (adjacent4 - block_set)
                        if 0 <= x < 20 and 0 <= y < 20])
        # get corner set
        _, old_corner = self.blokus.allowed_and_corner_position()
        self.blokus.pieces_sets[self.blokus.current_player].add(action)
        allowed, new_corner = self.blokus.allowed_and_corner_position()
        corner_set = set(map(tuple, new_corner)) - set(map(tuple, old_corner))
        # get legal actions
        legal_actions = self.blokus.get_legal(allowed=allowed, corner=corner_set)
        self.blokus.pieces_sets[self.blokus.current_player].remove(action)  # for no side effect
        # return block set, edge set, legal actions
        return block_set, edge_set, corner_set, legal_actions

    # @profile
    def update_graph(self, action):
        block_set, edge_set, _, legal_actions = self._get_action_info(action)
        self.blokus.pieces_sets[self.blokus.current_player].add(action)
        # for all players remove all actions whose
        # required blocks overlays with current action blocks
        for i in range(4):
            for block in block_set:
                self.graphs[i].remove_nodes_from(self.graphs[i].neighbors(block))
        # for current player remove all actions whose
        # type of piece are the same
        node_set = set(n for n, data in self.graphs[self.blokus.current_player].nodes(data=True)
                       if data['bipartite'] == 0 and n[0] == action[0])
        self.graphs[self.blokus.current_player].remove_nodes_from(node_set)
        # for current player remove all actions whose
        # required blocks contact current action blocks
        for block in edge_set:
            node_lst = self.graphs[self.blokus.current_player].neighbors(block)
            self.graphs[self.blokus.current_player].remove_nodes_from(node_lst)
        # for current player try new corners created by current action
        # add all LA actions in the graphs
        self.graphs[self.blokus.current_player].add_nodes_from(legal_actions, bipartite=0)
        for legal_action in legal_actions:
            edges = [(legal_action, tuple(block)) for block in get_blocks(*legal_action)]
            self.graphs[self.blokus.current_player].add_edges_from(edges)

    def update_player(self):
        self.blokus.current_player = self.blokus.next_player
        legal = self.get_legal_actions()
        for _ in range(3):
            if legal:
                break
            self.blokus.current_player = self.blokus.next_player
            legal = self.get_legal_actions()
        self.blokus.legal = legal

    def update(self, action):
        self.update_graph(action)
        self.update_player()

    def get_heuristic_info(self, action):
        block_set, edge_set, corner_set, legal_actions = self._get_action_info(action)
        # the size of this piece
        size_piece = len(block_set)
        # the number of new corner made
        num_corner = len(corner_set)
        # the number of new legal actions
        num_action = len(legal_actions)
        # how many legal actions of oneself and next 3 players
        # this action would block because of piece occupying
        piece_blocking = [0, 0, 0, 0]
        for i in range(4):
            player = (self.blokus.current_player + i) % 4
            for block in block_set:
                piece_blocking[i] += len(self.graphs[player].neighbors(block))
        # how many legal actions of oneself
        # this action would block because of edge block occupying
        edge_blocking = 0
        for block in edge_set:
            edge_blocking += len(self.graphs[self.blokus.current_player].neighbors(block))
        return size_piece, num_corner, num_action, piece_blocking, edge_blocking

    def get_legal_actions(self):
        legal_actions = set(n for n, data in self.graphs[self.blokus.current_player].nodes(data=True)
                            if data['bipartite'] == 0)
        return legal_actions


pieces_sets = [
    {(18, 1, (1, 1)), (17, 1, (4, 4)), (19, 6, (7, 7))},
    {(18, 0, (1, 18)), (17, 0, (4, 15))},
    {(16, 1, (19, 17)), (17, 3, (15, 15))},
    {(17, 0, (18, 1)), (11, 6, (16, 5))}
]

"""
# game = Blokus(pieces_sets=pieces_sets, current_player=1)
game = Blokus()
la = LegalAction(game)
game.display()

node = game
num = 1
while not node.is_terminal:
    #node.color_plot()
    print("player: {0}, #actions: {1}".format(node.current_player, len(node.legal_actions)))        
    num *= len(node.legal_actions)
    if node.current_player == 3:
        print("_______________________")
    # node.display()
    action = random.choice(tuple(node.legal_actions))
    print(la.get_heuristic_info(action))
    la.update(action)
    node = la.blokus
node.color_plot()
print(node.rewards, np.argmax(node.rewards))
print("{0:.2E}".format(num))
#"""
