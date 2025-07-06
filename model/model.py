import networkx as nx
from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._nodes = []
        self._idMapRetailers = {}

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


