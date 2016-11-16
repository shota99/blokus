from blokus.player import Player
from blokus.utils import encodeFourCode
from Blokus import *


def _change_action_coding(action):
    piece, pattern, (x, y) = action
    return encodeFourCode(x, y, "abcdefghijklmnopqrstu"[piece], int("60247135"[pattern]))


class CPlayerB34(Player):
    def __init__(self):
        super().__init__()

        self.count = 0
        self.logs = []
        self.board = None
        self.all_legal_actions = None
        self.node = None

    def log(self, player, move):
        self.logs.append((player, move))

    def move(self, board, pieces):
        if self.count == 0:
            self._initial(board)
        else:
            self._update(board)
        if self.node.legal_actions:
            # action = random.choice(tuple(self.node.legal_actions))
            score = dict()
            for action in self.node.legal_actions:
                size_piece, num_corner, num_action, piece_blocking, edge_blocking = \
                    self.all_legal_actions.get_heuristic_info(action)
                score[action] = 50 * size_piece + 1.3 * num_action + sum(piece_blocking[1:4]) - 0.5 * edge_blocking
            action = max(self.node.legal_actions, key=lambda action: score[action])
            self.all_legal_actions.update(action)
            hand = _change_action_coding(action)
        else:
            hand = 'pass'
        self.count += 1
        return hand

    def _initial(self, board):
        init_pieces_sets = [set(), set(), set(), set()]
        for player in [1, 2, 3]:
            node = Blokus(current_player=player)
            piece_size = np.sum(board == (player + 1))
            for action in node.legal_actions:
                if sizes[action[0]] == piece_size:
                    row, col = get_blocks(*action).transpose()
                    if np.all(board[row, col] == (player + 1)):
                        init_pieces_sets[player].add(action)
                        break
        self.board = board
        self.all_legal_actions = LegalAction(Blokus(init_pieces_sets, 0))
        self.node = self.all_legal_actions.blokus

    class FoundPiece(Exception):
        pass

    def _update(self, new_board):
        diff = self.board != new_board
        for player in [1, 2, 3]:
            new_piece = np.array(np.where(np.logical_and(
                new_board == (player + 1), diff))).transpose()
            piece_size = len(new_piece)
            used = [piece_args[0] for piece_args in self.node.pieces_sets[player]]
            remained_pieces = set(range(21)) - set(used)
            try:
                for piece in (piece for piece in remained_pieces if sizes[piece] == piece_size):
                    for pattern in uni_patterns[piece]:
                        abs_blocks = rotate(piece, pattern)
                        for center in new_piece:
                            blocks = abs_blocks + center
                            row, col = blocks.transpose()
                            if np.all(blocks >= 0) and np.all(blocks < 20) and \
                                    np.all(new_board[row, col] == (player + 1)):
                                piece_arg = (piece, pattern, tuple(center))
                                self.all_legal_actions.blokus.current_player = player
                                self.all_legal_actions.update_graph(piece_arg)
                                raise self.FoundPiece
            except self.FoundPiece:
                pass

        self.all_legal_actions.blokus.current_player = 0
        self.all_legal_actions.blokus.legal = self.all_legal_actions.get_legal_actions()
        # self.node.display()
        self.board = new_board
