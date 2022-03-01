from graph import Graph
from vertex import Vertex
from step import Step
from edge import Edge


class JKUMap(Graph):

    def __init__(self):
        super().__init__()

        self.notvisited = []
        self.matrix = []
        self.matrix_steps = []

        v_spar = self.insert_vertex("Spar")
        v_lit = self.insert_vertex("LIT")
        v_openlab = self.insert_vertex("Open Lab")
        v_khg = self.insert_vertex("KHG")
        v_parking = self.insert_vertex("Parking")
        v_bellacasa = self.insert_vertex("Bella Casa")
        v_sp1 = self.insert_vertex("SP1")
        v_sp3 = self.insert_vertex("SP3")
        v_lui = self.insert_vertex("LUI")
        v_teichwerk = self.insert_vertex("Teichwerk")
        v_library = self.insert_vertex("Library")
        v_chat = self.insert_vertex("Chat")
        v_bank = self.insert_vertex("Bank")
        v_porter = self.insert_vertex("Porter")
        v_castle = self.insert_vertex("Castle")
        v_papaya = self.insert_vertex("Papaya")
        v_JKH = self.insert_vertex("JKH")

        self.insert_edge(v_spar, v_lit, 50)
        self.insert_edge(v_spar, v_porter, 103)
        self.insert_edge(v_spar, v_khg, 165)
        self.insert_edge(v_khg, v_bank, 150)
        self.insert_edge(v_khg, v_parking, 190)
        self.insert_edge(v_parking, v_bellacasa, 145)
        self.insert_edge(v_parking, v_sp1, 240)
        self.insert_edge(v_sp1, v_sp3, 130)
        self.insert_edge(v_sp1, v_lui, 175)
        self.insert_edge(v_lui, v_teichwerk, 135)
        self.insert_edge(v_lui, v_library, 90)
        self.insert_edge(v_lui, v_chat, 240)
        self.insert_edge(v_library, v_chat, 160)
        self.insert_edge(v_chat, v_bank, 115)
        self.insert_edge(v_bank, v_porter, 100)
        self.insert_edge(v_porter, v_openlab, 70)
        self.insert_edge(v_porter, v_lit, 80)
        self.insert_edge(v_castle, v_papaya, 85)
        self.insert_edge(v_papaya, v_JKH, 80)

    def get_shortest_path_from_to(self, from_vertex: Vertex, to_vertex: Vertex):
        """
        This method determines the shortest path between two POIs "from_vertex" and "to_vertex".
        It returns the list of intermediate steps of the route that have been found
        using the dijkstra algorithm.

        :param from_vertex: Start vertex
        :param to_vertex:   Destination vertex
        :return:
           The path, with all intermediate steps, returned as an list. This list
           sequentially contains each vertex along the shortest path, together with
           the already covered distance (see example on the assignment sheet).
           Returns None if there is no path between the two given vertices.
        :raises ValueError: If from_vertex or to_vertex is None, or if from_vertex equals to_vertex
        """
        if from_vertex is None:
            raise ValueError
        if to_vertex is None:
            raise ValueError
        if from_vertex == to_vertex:
            raise ValueError

        matrix, p = self.helper_dijkstra(from_vertex)

        if to_vertex not in p:
            return None

        result = []
        end_vertex = to_vertex

        while end_vertex != p[end_vertex]:
            for small_list in matrix:
                if small_list[0] == end_vertex.name:
                    value = small_list[1]
                    break
            result.append(Step(end_vertex, value))
            end_vertex = p[end_vertex]

        result.append(Step(from_vertex, 0))
        result.reverse()

        return result

    def get_steps_for_shortest_paths_from(self, from_vertex: Vertex):
        """
        This method determines the amount of "steps" needed on the shortest paths
        from a given "from" vertex to all other vertices.
        The number of steps (or -1 if no path exists) to each vertex is returned
        as a dictionary, using the vertex name as key and number of steps as value.
        E.g., the "from" vertex has a step count of 0 to itself and 1 to all adjacent vertices.

        :param from_vertex: start vertex
        :return:
          A map containing the number of steps (or -1 if no path exists) on the
          shortest path to each vertex, using the vertex name as key and the number of steps as value.
        :raises ValueError: If from_vertex is None.
        """
        if from_vertex is None:
            raise ValueError

        result = {from_vertex.name: 0}

        for vertex in self.get_vertices():

            if vertex is not from_vertex:
                temp = self.get_shortest_path_from_to(from_vertex, vertex)
                if temp is None:
                    result.update({vertex.name: -1})
                else:
                    result.update({vertex.name: len(temp)-1})

        return result

    def get_shortest_distances_from(self, from_vertex: Vertex):
        """
        This method determines the shortest paths from a given "from" vertex to all other vertices.
        The shortest distance (or -1 if no path exists) to each vertex is returned
        as a dictionary, using the vertex name as key and the distance as value.

        :param from_vertex: Start vertex
        :return
           A dictionary containing the shortest distance (or -1 if no path exists) to each vertex,
           using the vertex name as key and the distance as value.
        :raises ValueError: If from_vertex is None.
        """

        if from_vertex is None:
            raise ValueError

        matrix = self._dijkstra(from_vertex, [], {}, {})
        dictionary = {}

        for small_list in matrix:
            dictionary[small_list[0]] = small_list[1]

        return dictionary

    def _dijkstra(self, cur: Vertex, visited_list, distances: dict, paths: dict):
        """
        This method is expected to be called with correctly initialized data structures and recursively calls itself.

        :param cur: Current vertex being processed
        :param visited_list: List which stores already visited vertices.
        :param distances: Dict (nVertices entries) which stores the min. distance to each vertex.
        :param paths: Dict (nVertices entries) which stores the shortest path to each vertex.

        """

        dijkstra = self.helper_dijkstra(cur)

        return dijkstra[0]

    def helper_dijkstra(self, cur: Vertex):

        adj_matrix = self.get_adjacency_matrix()
        self.matrix = []
        self.notvisited = []
        paths = {cur: cur}

        for vertex in self.vertices:
            self.matrix.append([vertex.name])
            self.notvisited.append(vertex.name)

        self.matrix[self.matrix.index([cur.name])].append(0)
        vertex_min_name = cur.name

        while len(self.notvisited) != 0:

            for i in range(self.num_vertices):
                if self.vertices[i].name == vertex_min_name:
                    cur = self.vertices[i]

            if cur is None:
                break

            self.notvisited.remove(cur.name)
            adj_vertices = self.get_adj_vertices(cur)

            for i in range(len(self.matrix)):
                for vertex in adj_vertices:
                    if self.matrix[i][0] == vertex.name:
                        if len(self.matrix[i]) == 1:
                            self.matrix[i].append(adj_matrix[cur.idx][i] + self.matrix[cur.idx][1])
                            paths.update({vertex: cur})
                        else:
                            if self.matrix[i][1] > adj_matrix[cur.idx][i] + self.matrix[cur.idx][1]:
                                self.matrix[i][1] = adj_matrix[cur.idx][i] + self.matrix[cur.idx][1]
                                paths.update({vertex: cur})
            cur = None

            vertex_min_name = self.get_min_vertex()[0]

        for small_list in self.matrix:
            for vertex in self.notvisited:
                if small_list[0] == vertex:
                    small_list.append(-1)

        print(paths)
        return [self.matrix, paths]

    def get_min_vertex(self):
        min_value = 999999
        min_vertex = None
        for small_list in self.matrix:
            if small_list[0] in self.notvisited and len(small_list) > 1:
                if small_list[1] < min_value:
                    min_value = small_list[1]
                    min_vertex = small_list[0]
        return [min_vertex, min_value]

    def get_adj_vertices(self, cur: Vertex):

        list_1 = []
        for i in range(self.num_vertices):
            if self.vertices[i].name == cur.name:
                index = cur.idx
        for x in range(self.num_edges):
            if self.edges[x].first_vertex.idx == index:
                list_1.append(self.edges[x].second_vertex)
            elif self.edges[x].second_vertex.idx == index:
                list_1.append(self.edges[x].first_vertex)

        return list_1


