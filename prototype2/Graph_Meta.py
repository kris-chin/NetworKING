import Graph

#Both the Analytics and Statistics objects point to a graph object where they will do all of their calculations

class Analytics:
    def __init__(self, graph):
        self.graph = graph
    def GetLeaves(self):
        LeafList = []
        for Node in self.graph.GetVertices():
            if len(self.graph.GetNeighbors(Node)) == 1:
                LeafList.append(Node)
        return LeafList

    def GetZeroEdges(self):
        ZeroList = []
        for Node in self.graph.GetVertices():
            if len(self.graph.GetNeighbors(Node)) == 0:
                ZeroList.append(Node)
        return ZeroList

    def GetLowHealth(self, threshold):
        LowHealth = []
        for Node in self.graph.GetVertices():
            if Node.health < threshold:
                LowHealth.append(Node)
        return LowHealth

    #def GetNotDefined(self):
    #    print("TODO")

    def GetGhosts(self):
        GhostList = []
        for Node in self.graph.GetVertices():
            if Node.health == 0: #if node is ghost
                NodeNeighbors = self.graph.GetNeighbors(Node)
                if len(NodeNeighbors) > 0: #if the ghost actually has connections,
                    for Neighbor in NodeNeighbors:
                        if Neighbor.health > 0: #if the ghost is connected to another node that has health
                            GhostList.append(Node)
                            break
        return GhostList

    def GetHighestDegree(self):
        HighestDegreeNode = None
        HighestDegree = 0
        for Node in self.graph.GetVertices():
            NodeDegree = len(self.graph.GetNeighbors(Node))
            if NodeDegree > HighestDegree:
                HighestDegree = NodeDegree
                HighestDegreeNode = Node

        return HighestDegreeNode

class Statistics:
    def __init__(self, graph):
        self.graph = graph

    def GetClassCounts(self, Class):
        counts = dict()
        for Class in self.graph.GetClassifcations():
            counts[Class.name] = Class.counts
        return counts

    def GetHealthCounts(self):
        counts = dict()
        for Node in self.graph.GetVertices():
            if Node.health in counts:
                counts[Node.health] += 1
            else:
                counts[Node.health] = 1
        return counts