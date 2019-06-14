from abc import ABC, abstractmethod


class IBipartiteGraph(ABC):
    @abstractmethod
    def __init__(self, d):
        self._d = d

    @property
    def d(self):
        return self._d

    @abstractmethod
    def vertices_p(self): pass