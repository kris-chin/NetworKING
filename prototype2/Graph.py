class Classification:
    def __init__(self, name, color):
        self.name = name #STRING
        self.color = color #STRING

class Vertex:
    def __init__(self, name, type, health, shape, notes):
        self.name = name #STRING
        self.type = type #CLASSIFICATION OBJECT
        self.health = health #INT
        self.shape = shape #CHAR
        self.notes = notes #STRING
    
    #Updates the vertex by just replacing it's data with another vertex's
    #If you're just changing one value, you pass in a Vertex with only one different value
    def Update(self, newVertex):
        self.name = newVertex.name
        self.type = newVertex.type
        self.health = newVertex.health
        self.shape = newVertex.shape
        self.notes = newVertex.notes

class Edge:
    def __init__(self, vertex1, vertex2, color, size, style):
        self.vertices = (vertex1,vertex2) #2-TUPLE OF VERTEX OBJECTS
        self.color = color #STRING
        self.size = size #INT, THICKNESS
        self.style = style #STRING, STYLING
    
    #Same as Vertex.Update()
    def Update(self, newEdge):
        self.vertices = newEdge.vertices
        self.color = newEdge.color
        self.size = newEdge.size
        self.style = newEdge.style

class Graph:
    def __init__(self, vertices, edges):
        self.vertices = vertices #LIST OF VERTEX OBJECTS
        self.edges = edges #LIST OF EDGE OBJECTS
    def AddEdge(self, edge): self.edges.append(edge)
    def AddVertex(self, vertex): self.vertices.append(vertex)

    def GetVertex(self, vertex_name):
        for vertex in self.vertices:
            if vertex.name == vertex_name:
                return vertex
        #if you're here, there is no vertex of the given name
        return None