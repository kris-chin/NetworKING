class Classification:
    def __init__(self, id, name, color):
        self.id = id #INT
        self.name = name #STRING
        self.color = color #STRING
        self.count = 0 #INT
    def __str__(self):
        return self.name
    def IncrementCount(self):
        self.count += 1
    def GetName(self):
        return self.name

    #returns the json representation of the classification object
    def json(self):
        return {
            'id' : self.id,
            'name' : self.GetName(),
            'color' : self.color,
            'count' : self.count
        }

class Vertex:
    def __init__(self, id, name, type, health, shape = 'o', notes = 'None'):
        self.id = id #INT
        self.name = name #STRING

        self.type = type #CLASSIFICATION OBJECT
        self.type.IncrementCount() #increase classifcation count

        self.health = health #INT
        self.shape = shape #CHAR
        self.notes = notes #STRING
    
    def __str__(self):
        return self.name
    
    #Updates the vertex by just replacing it's data with another vertex's
    #If you're just changing one value, you pass in a Vertex with only one different value
    def Update(self, newVertex):
        self.name = newVertex.name
        self.type = newVertex.type
        self.health = newVertex.health
        self.shape = newVertex.shape
        self.notes = newVertex.notes

    def PrintDetails(self):
        print("Name: '" + self.name + "'")
        print("Type: '" + str(self.type) + "'")
        print("Health: " + str(self.health))
        print("Shape: '" + self.shape + "'")
        if self.notes != "None":
            print("Notes: " + self.notes)
        
    def GetName(self):
        return self.name

    #returns the json representation of the vertex object
    def json(self):
        return {
            'id' : self.id,
            'name' : self.GetName(),
            'type' : self.type.GetName(),
            'health' : self.health,
            'shape' : self.shape,
            'notes' : self.notes
        }

class Edge:
    def __init__(self, id, vertices, color = "Black", size = 1, style = 'solid'):
        self.id = id #INT
        self.vertices = vertices #2-TUPLE OF VERTEX OBJECTS
        self.color = color #STRING
        self.size = size #INT, THICKNESS
        self.style = style #STRING, STYLING

    def __getitem__(self, key): #used for accessing either Vertex1 or Vertex2
        return self.vertices[key]

    def __str__(self):
        return "(" + str(self.vertices[0]) + ", " + str(self.vertices[1]) + ")"
    
    #Same as Vertex.Update()
    def Update(self, newEdge):
        self.vertices = newEdge.vertices
        self.color = newEdge.color
        self.size = newEdge.size
        self.style = newEdge.style

    #Returns the names of the vertices as the edge's name
    def GetName(self):
        return "(" + self.vertices[0].name + ", " + self.vertices[1].name + ")"

    #Returns the json representation of the Edge
    def json(self):
        return {
            'id' : self.id,
            'name' : self.GetName(),
            'vertex1' : self.vertices[0].GetName(),
            'vertex2' : self.vertices[1].GetName(),
            'color' : self.color,
            'size' : self.size,
            'style' : self.style
        }

class Graph:
    def __init__(self, vertices, edges, classifications):
        self.vertices = vertices #LIST OF VERTEX OBJECTS
        self.edges = edges #LIST OF EDGE OBJECTS
        self.classifications = classifications #LIST OF CLASSIFICATION OBJECTS

    def __str__(self):
        vertex_strings = list(str(Vertex) for Vertex in self.vertices)
        edge_strings = list(str(Edge) for Edge in self.edges)
        return "Vertices: " + str(vertex_strings) + "\nEdges: " + str(edge_strings)

    def AddEdge(self, edge): self.edges.append(edge)
    def AddVertex(self, vertex): self.vertices.aappend(vertex)

    #Returns the Vertex Object of matching name string
    def GetVertex(self, vertex_name):
        for vertex in self.vertices:
            if vertex.name == vertex_name:
                return vertex
        #if you're here, there is no vertex of the given name
        return None

    def GetVertices(self):
        return self.vertices
    def GetEdges(self):
        return self.edges
    def GetClassifications(self):
        return self.classifications
            
    #Returns a list of all neighboring Vertices
    def GetNeighbors(self,vertex):
        NeighborList = []

        for Edge in self.edges:
            if (Edge[0] == vertex):
                if (Edge[1] not in NeighborList): #if the other node is not already in the list
                    NeighborList.append(Edge[1]) #append it
            elif (Edge[1] == vertex):
                if (Edge[0] not in NeighborList): #if the other node is not already in the list
                    NeighborList.append(Edge[0]) #append it
        
        return NeighborList

    #Returns the JSON representation of the graph
    def json(self):
        return {'classifications' : [c.json() for c in self.classifications], 'vertices' : [v.json() for v in self.vertices], 'edges' : [e.json() for e in self.edges] }

############################################################

def dejson(json_input):
    classifications = [Classification(int(c['id']), c['name'], c['color']) for c in json_input['classifications'] ]
    vertices = [Vertex(int(v['id']), v['name'], FindClassification(classifications,v['type']), int(v['health']), v['shape'], v['notes']) for v in json_input['vertices'] ]
    edges = [Edge(int(e['id']), (FindVertex(vertices,e['vertex1']), FindVertex(vertices,e['vertex2'])), e['color'], int(e['size']), e['style']) for e in json_input['edges'] ]

    return Graph(vertices,edges,classifications)

def FindClassification(classificationlist, stringinput): #goes through classification list to find respective classification
    for c in classificationlist:
        if c.name == stringinput:
            #print("Found '" + stringinput + "'")
            return c
    print("Couldn't find '" + stringinput + "'")
    return None

def FindVertex(vertexlist, stringinput): #goes through vertex list and returns vertex if matching
    for v in vertexlist:
            if v.name == stringinput:
                #print("Found '" + stringinput + "'")
                return v
    print("Couldn't find '" + stringinput + "'")
    return None