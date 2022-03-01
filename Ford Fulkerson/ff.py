# Ford-Fulkerson algorith in Python

class Graph:

    def __init__(self, graph):
        self.graph = graph  # original graph
        self.residual_graph = [[cell for cell in row] for row in graph]  # cloned graph
        self.latest_augmenting_path = [[0 for cell in row] for row in
                                       graph]  # empty graph with same dimension as graph
        self.current_flow = [[0 for cell in row] for row in graph]  # empty graph with same dimension as graph
        self.max_flow = 0

    def bfs_path(self, source, sink):

        visited_list = []
        queue = [[source]]

        if source == sink:
            return

        while queue:
            path = queue.pop(0)
            vertex = path[-1]
            if vertex not in visited_list:
                for i in range(len(self.residual_graph)):
                    new_path = list(path)
                    if self.residual_graph[vertex][i] != 0:
                        new_path.append(i)
                        queue.append(new_path)
                        if i == sink:
                            return new_path

            visited_list.append(vertex)
        return None

    def bottleneck(self, graph, path):
        minim = None
        for i in range(len(path)-1):
            if minim is None or graph[path[i]][path[i + 1]] < minim:
                minim = graph[path[i]][path[i + 1]]

        return minim

    def make_residual(self, graph, path):
        residual_graph = []
        for i in range(len(graph)):
            row = []
            for j in range(len(graph)):
                row.append(graph[i][j])
            residual_graph.append(row)

        min_flow = self.bottleneck(residual_graph,path)


        for i in range(len(path)-1):
            residual_graph[path[i]][path[i + 1]] -= min_flow
            residual_graph[path[i+1]][path[i]] += min_flow

        return residual_graph


    def ff_step(self, source, sink):
        """
        Perform a single flow augmenting iteration from source to sink
        Update the latest augmenting path, the residual graph and the current flow by the maximum possible amount according to your chosen path.
        The path must be chosen based on BFS.
        @param source the source's vertex id
        @param sink the sink's vertex id
        @return the amount by which the flow has increased.
        """
        self.latest_augmenting_path = [[0 for cell in row] for row in self.graph]  # empty graph with same dimension as graph

        path = self.bfs_path(source, sink)
        if path is None:
            return 0

        min_flow = self.bottleneck(self.residual_graph, path)
        self.residual_graph = self.make_residual(self.residual_graph,path)


        for i in range(len(path)-1):
            self.latest_augmenting_path[path[i]][path[i+1]] = self.latest_augmenting_path[path[i]][path[i+1]] + min_flow

        for i in range(len(path)-1):
            if  self.graph[path[i]][path[i+1]] > 0:
                self.current_flow[path[i]][path[i+1]] = self.current_flow[path[i]][path[i+1]] + min_flow
            elif self.graph[path[i ]][path[i+1]] == 0:
                self.current_flow[path[i + 1]][path[i]] = self.current_flow[path[i + 1]][path[i]] - min_flow

        self.max_flow = self.max_flow + min_flow

        return min_flow

    def ford_fulkerson(self, source, sink):
        """
        Execute the ford-fulkerson algorithm (i.e., repeated calls of ff_step())
        @param source the source's vertex id
        @param sink the sink's vertex id
        @return the max flow from source to sink
        """

        while self.ff_step(source,sink) !=0 :
            pass

        return self.max_flow

