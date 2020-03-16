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
    def AddVertex(self, vertex): self.vertices.append(vertex)
    def AddClass(self, classification): self.classifications.append(classification)
    
    def GetVertices(self):
        return self.vertices
        
    def UpdateVertex(self, id, input_name, input_type, input_health, input_shape, input_notes):
        v = FindVertexByID(self.vertices, id)
        if (v != None):
            v.name = input_name
            v.type = input_type
            v.health = input_health
            v.shape = input_shape
            v.notes = input_notes

    def RemoveVertex(self, id):
        v = FindVertexByID(self.vertices, id)
        if (v != None):
            #first, remove all edges connected to this vertex
            e = FindEdgeByVertexID(self.edges,id)
            while (e != None):
                self.RemoveEdge(e.id)
                e = FindEdgeByVertexID(self.edges,id)
            #then, delete the vertex itself
            self.vertices.remove(v)
            del v
    
    def GetEdges(self):
        return self.edges

    def UpdateEdge(self, id, input_color, input_size, input_style ):
        e = FindEdgeByID(self.edges, id)
        if (e != None):
            e.color = input_color
            e.size = input_size
            e.style = input_style

    def RemoveEdge(self,id):
        e = FindEdgeByID(self.edges, id)
        if (e != None):
            self.edges.remove(e)
            del e

    def GetClassifications(self):
        return self.classifications
    
    def UpdateClassification(self, id, input_name, input_color):
        #updates a given classification with a new classification
        c = FindClassificationByID(self.classifications, id)
        if (c != None):
            c.name = input_name
            c.color = input_color

    def RemoveClassification(self, id):
        c = FindClassificationByID(self.classifications, id)
        if (c != None):
            #first, remove all vertices associated with this class
            for v in self.vertices:
                #TODO:fix why this only deletes only odd numbers
                print([vert.id for vert in self.vertices])
                if (v.type.id == c.id):
                    #print(v.name)
                    self.RemoveVertex(v.id)
            #then, delete the class
            self.classifications.remove(c)
            del c
            
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
    classifications = []
    for c in json_input['classifications']:
        try: classifications.append(Classification(int(c['id']), c['name'], c['color']))
        except: print("ignoring dejsonification of invalid class")
    vertices = []
    for v in json_input['vertices']:
        try: vertices.append(Vertex(int(v['id']), v['name'], FindClassification(classifications,v['type']), int(v['health']), v['shape'], v['notes']))
        except: print("ignoring dejsonification of invalid vertex")
    edges = []
    for e in json_input['edges']:
        try: edges.append(Edge(int(e['id']), (FindVertex(vertices,e['vertex1']), FindVertex(vertices,e['vertex2'])), e['color'], int(e['size']), e['style']))
        except: print("ignore dejsonification of invalid edge")
    return Graph(vertices,edges,classifications)

def FindClassification(classificationlist, stringinput): #goes through classification list to find respective classification
    for c in classificationlist:
        if c.name == stringinput:
            #print("Found '" + stringinput + "'")
            return c
    print("Couldn't find '" + stringinput + "'")
    return None

def FindClassificationByID(classificationlist, ID): #goes through classification list to find respective classification
    for c in classificationlist:
        if c.id == ID:
            #print("Found '" + stringinput + "'")
            return c
    print("Couldn't find '" + str(ID) + "'")
    return None

def FindVertex(vertexlist, stringinput): #goes through vertex list and returns vertex if matching
    for v in vertexlist:
            if v.name == stringinput:
                #print("Found '" + stringinput + "'")
                return v
    print("Couldn't find '" + stringinput + "'")
    return None

def FindVertexByID(vertexlist, ID): #goes through vertex list and returns vertex if matching
    for v in vertexlist:
            if v.id == ID:
                #print("Found '" + stringinput + "'")
                return v
    print("Couldn't find '" + str(ID) + "'")
    return None

def FindEdgeByVertexID(edgelist, vertex_id):
    for e in edgelist:
        if (e.vertices[0].id == vertex_id or e.vertices[1].id == vertex_id):
            return e
    print("Couldn't find any edges containing vertex id: \'" + str(vertex_id) + "\'")
    return None

def FindEdgeByID(edgelist, ID):
    for e in edgelist:
            if e.id == ID:
                #print("Found '" + stringinput + "'")
                return e
    print("Couldn't find '" + str(ID) + "'")
    return None

def HighestID(list):
    #returns the highest id in a list (list must contain objects containing id values)
    highestValue = 0
    for item in list:
        try:
            if (item.id > highestValue):
                highestValue = item.id
        except:
            print("ERROR: Input list in HighestID() doesn't use objects with id values")
            highestValue = None
    return highestValue
