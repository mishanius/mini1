from perfect_match.objects.BipartiteVertex import VertexQ


class RealVertexQ(VertexQ):

    def __init__(self, lable=None):
        super().__init__(lable)
        self.__neighboors = []

    def get_neighboors(self):
        return self.__neighboors

    def get_neighboor(self, index):
        return self.__neighboors[index]

    def set_neighboors(self, neighboors):
        self.__neighboors = neighboors

    def add_neighboor(self, vertex):
        self.__neighboors.append(vertex)

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, o: object) -> bool:
        return isinstance(o, RealVertexQ) and self.name == o.name

    def __copy__(self):
        cls = self.__class__
        result = cls.__new__(cls)
        result.__neighboors = self.__neighboors.copy()
        return result