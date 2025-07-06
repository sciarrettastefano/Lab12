import copy

import networkx as nx
from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._nodes = []
        self._idMapRetailers = {}
        self._bestPath = []
        self._bestScore = 0


    def buildGraph(self, nation, year):
        self._graph.clear()
        self._nodes = self.getAllNodes(nation)
        for ret in self.getAllNodes(nation):
            self._idMapRetailers[ret.Retailer_code] = ret
        if len(self._nodes) == 0:
            print("No nodes found")
            return
        self._graph.add_nodes_from(self._nodes)
        edges = self.getAllEdges(nation, year, self._idMapRetailers)
        for e in edges:
            self._graph.add_edge(e[0], e[1], weight=e[2])
        return self._graph


    def getBestPath(self, N):
        self._bestPath = []
        self._bestScore = 0
        parziale = []
        self._ricorsione(parziale, N)
        return self._bestPath, self._bestScore


    def _ricorsione(self, parziale, N):
        #condizione terminale
        if len(parziale) == N+1:
            score = self.getScore(parziale)
            if score > self._bestScore:
                self._bestScore = score
                self._bestPath = copy.deepcopy(parziale)
            return
        #ricorsione
        if len(parziale) == N:
            if self._graph.has_edge(parziale[-1], parziale[0]):
                parziale.append(parziale[0])
                self._ricorsione(parziale, N)
                parziale.pop()
            else:
                return
        if len(parziale) == 0:
            for n in list(self._graph.nodes()):
                parziale.append(n)
                self._ricorsione(parziale, N)
                parziale.pop()
        else:
            for n in list(self._graph.neighbors(parziale[-1])):
                if n not in parziale:
                    parziale.append(n)
                    self._ricorsione(parziale, N)
                    parziale.pop()


    def getScore(self, parziale):
        score = 0
        for i in range(len(parziale)-1): # itera n volte per n archi
            score += self._graph[parziale[i]][parziale[i+1]]['weight']
        return score


    def calcolaVolumi(self):
        volumi = []
        for node in self._graph.nodes():
            volume = 0
            vicini = list(nx.neighbors(self._graph, node))
            for vicino in vicini:
                volume += self._graph[node][vicino]['weight']
            volumi.append((node, volume))
        volumi.sort(key=lambda x: x[1], reverse=True)
        return volumi


    def getGraphDetails(self):
        return self._graph.number_of_nodes(), self._graph.number_of_edges()

    def getAllNations(self):
        return DAO.getAllNations()

    def getAllYears(self):
        return DAO.getAllYears()

    def getAllNodes(self, nation):
        return DAO.getAllNodes(nation)

    def getAllEdges(self, nation, year, idMapRetailer):
        return DAO.getAllEdges(nation, year, idMapRetailer)


