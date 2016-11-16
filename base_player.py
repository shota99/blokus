from abc import ABC, abstractmethod


class BasePlayer(ABC):
    def __init__(self, trainable):
        self.trainable = trainable

    @abstractmethod
    def move(self, node):
        pass

    @abstractmethod
    def update(self, rewards):
        pass

    @abstractmethod
    def save(self, file_name):
        pass

    @abstractmethod
    def load(self, file_name):
        pass
