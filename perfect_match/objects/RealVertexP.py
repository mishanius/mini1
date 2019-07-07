from perfect_match.objects.BipartiteVertex import VertexP


class RealVertexP(VertexP):

    def __init__(self, lable=None):
        super().__init__(lable)
        self.__neighboors = []

    def __copy__(self):
        cls = self.__class__
        result = cls.__new__(cls)
        result.__neighboors = self.__neighboors.copy()
        return result

    def get_neighboors(self):
        return self.__neighboors

    def get_neighboor(self, index):
        return self.__neighboors[index]

    def remove_neighbore(self, neigbore):
        self.__neighboors.remove(neigbore)

    def set_neighboors(self, neighboors):
        self.__neighboors = neighboors

    def add_neighboor(self, vertex):
        # if not vertex in self.__neighboors:
        self.__neighboors.append(vertex)



    def __hash__(self):
        return hash(self.name)

    def __eq__(self, o: object) -> bool:
        return isinstance(o, RealVertexP) and self.name == o.name

    def __repr__(self):
        return self.__str__()