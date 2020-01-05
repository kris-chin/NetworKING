import Graph

#Both the Analytics and Statistics objects point to a graph object where they will do all of their calculations

class Analytics:
    def __init__(self, graph):
        self.graph = graph
    def GetLeaves(self):
        print("TODO")
    def GetZeroEdges(self):
        print("TODO")
    def GetLowHealth(self):
        print("TODO")
    def GetNotDefined(self):
        print("TODO")
    def GetGhosts(self):
        print("TODO")
    def GetHighestDegree(self):
        print("TODO")

class Statistics:
    def __init__(self, graph):
        self.graph = graph
    def GetClassCounts(self):
        print("TODO")
    def GetHealthCounts(self):
        print("TODO")
    def GetNodeCounts(self):
        print("TODO")