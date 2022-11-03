from abc import ABC, abstractmethod
import copy


class FOSG(ABC):

    @staticmethod
    @abstractmethod
    def get_initial_state():
        pass


class State(ABC):
    @abstractmethod
    def is_terminal(self):
        pass

    @abstractmethod
    def get_possible_actions(self):
        pass

    @abstractmethod
    def get_possible_joint_actions(self):
        pass

    @abstractmethod
    def apply_actions(self, actions):
        pass

    @abstractmethod
    def get_private_information(self, player: int):
        pass

    @abstractmethod
    def get_public_information(self):
        pass

    def get_player_information(self, player: int):
        return self.get_private_information(player) + self.get_public_information()

    @abstractmethod
    def can_play(self, player: int):
        pass

    @abstractmethod
    def get_state_string(self):
        pass

    def get_child(self, actions):
        child = copy.deepcopy(self)
        child.apply_actions(actions)
        return child

    @abstractmethod
    def get_value(self):
        pass
