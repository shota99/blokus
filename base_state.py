from abc import ABC, abstractmethod, abstractproperty


class BaseState(ABC):
    """
    The abstract base class for any game.
    Usually the information that uniquely determine the state of the
    game is necessary, such as pieces on the board (a list of sets),
    etc.
    required property:
    is_terminal: if the game is terminal
    current_player: the player who is about to make the move.
    """

    @abstractproperty
    def legal_actions(self):
        """
        :return: the set of all legal actions by the current player
        """

    @abstractproperty
    def rewards(self):
        """
        :return: the list of rewards to every player
        """

    @abstractmethod
    def act(self, action):
        """
        :param action: action info
        :return: the next state by taking this action
        """

    def display(self):
        """
        display the information in a user-friendly way.
        :return:
        """
        raise NotImplementedError("Display function not implemented.")

    @abstractmethod
    def __hash__(self):
        """
        define the hash function based on the state_info
        """

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()
