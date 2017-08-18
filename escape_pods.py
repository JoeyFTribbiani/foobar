'''
I have learned a little bit more knowledge from graph theory to
solve this problem. This problem can be shaped into a max-flow
problem. Here I use Dinic algorithm to implement Ford–Fulkerson
method. The time complexity of this solution is O(E*V^2) where E
is the #edges (#non-zero elements in path + #entrances + #exits),
and V is the #vertice (len(path)+2, since I need to add a source
and a sink).
'''
import collections
import sys


class Edge(object):
    target = None
    revindex = None
    flow = None
    capacity = None

    def __init__(self, target, revindex, flow, capacity):
        self.target = target
        self.revindex = revindex
        self.flow = flow
        self.capacity = capacity


class Graph(object):
    def __init__(self, matrix):
        self.__level = collections.defaultdict(lambda: -1)
        self.__adj = collections.defaultdict(list)
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                if matrix[i][j] != 0:
                    self.__adj[i] += Edge(j, len(self.__adj[j]), 0, matrix[i][j]),
                    self.__adj[j] += Edge(i, len(self.__adj[i]) - 1, 0, 0),

    # search augmenting paths and build level graph
    def bfs(self, source, sink):
        self.__level.clear()
        self.__level[source] = 0
        queue = collections.deque([source])
        while queue:
            u = queue.popleft()
            for e in self.__adj[u]:
                if self.__level[e.target] < 0 and e.flow < e.capacity:
                    self.__level[e.target] = self.__level[u] + 1
                    queue += e.target,
        return self.__level[sink] >= 0

    # calculate flow
    def sendFlow(self, u, sink, flow, start):
        if u == sink:
            return flow
        while start[u] < len(self.__adj[u]):
            e = self.__adj[u][start[u]]
            if self.__level[e.target] == self.__level[u] + 1 and e.flow < e.capacity:
                tmpFlow = self.sendFlow(e.target, sink, min(flow, e.capacity - e.flow), start)
                if tmpFlow > 0:
                    e.flow += tmpFlow
                    self.__adj[e.target][e.revindex].flow -= tmpFlow
                    return tmpFlow
            start[u] += 1
        return 0

    def DinicMaxflow(self, source, sink):
        if source == sink:
            return -1

        total = 0
        while self.bfs(source, sink):
            start = collections.defaultdict(int)
            while True:
                # check whether more flows can be sent
                s = self.sendFlow(source, sink, sys.maxsize, start)
                if s:
                    total += s
                else:
                    break
        return total


def answer(entrances, exits, path):
    # preprocess the graph (add a consolidated source and a consolidated sink)
    path = [[0] * (len(path))] + path + [[0] * (len(path))]
    for p in path:
        p[:] = [0] + p + [0]
    for i in entrances:
        path[0][i + 1] = sys.maxsize
    for i in exits:
        path[i + 1][len(path) - 1] = sys.maxsize

    # build the graph
    g = Graph(path)

    return g.DinicMaxflow(0, len(path) - 1)