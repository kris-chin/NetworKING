"""
    Author: Krischin Layon (2019)

    NOTE: you're basically done. don't spend any unecessary time on this that could be used for other tasks

    TODO: Add an option to specifiy the name of the csv file.
    TODO: Add google sheets compatibility.
    TODO: Live Update Matplotlib (just watch the network build as you type commands)
    TODO: way later, optimize this. i think its like n^3 or something lmao

    Main.py

    This program reads 'names.csv', which is stored in the same directory as this script, and draws a network graph.
    Uses csv, networkx, matplotlib.pyplot, matplotlib.ticker and mpld3

    CSV Format:
        FIRST ITEM = name of connection, SECOND ITEM = type of connection, THIRD ITEM = Estimate of the connection's health, ADDITIONAL ITEMS = EDGES
        If the First Item is [C], the following items are the classifications of each node.
"""

import networkx as nx
import matplotlib.pyplot as plt, mpld3
import matplotlib.ticker as plticker #used for determining even ticker distances
import csv

class Classification: #we're gonna have a small class dedicated to our classifications (i was using tuples at first but they arent mutable)
    def __init__(self,name,color,count):
        self.name = name
        self.color = color
        self.count = count
    

def GetLeaves(G):
    #G = networkx graph object

    # returns a list object of all nodes with one real edge.
   
    leaves = []

    #go through the graph's nodes
    for node in G.nodes():
        realEdgeCount = 0

        #go through it's edges
        for edge in G.edges(node):
            if G.edges[edge]['isGhostEdge'] == False:
                realEdgeCount +=1

        if realEdgeCount == 1:
            leaves.append(node)

    return leaves

def GetLowHealth(G, threshold):
    #G = networkx graph object
    #threshold = return nodes at this value and lower

    #returns a list object of all nodes at the health threshold and below.
    #(ignores 0 health nodes)

    lowHealth = []

    for node in G.nodes():
        if (0 < G.nodes[node]['health'] <= threshold):
            lowHealth.append(node)
    
    return lowHealth

def GetGhosts(G,threshold,countReal):
    #G = networkx graph object
    #threshold = only returns ghosts with an edge count above this value
    #countReal = boolean. if true, counts only edges to real nodes
    #returns a list of 2-tuples. the first part is the ghostnode. the second part is it's number of edges

    ghosts = []

    for node in G.nodes():
        if (G.nodes[node]['health'] == 0):

            if countReal == False: #if we can count ALL edges
                edgeCount = G.degree(node)
                
            else: #if we can only count edges to REAL nodes
                edgeCount = 0

                #if the other node in the edge has a health over 0, add to the edge count
                for edge in G.edges(node):
                    if G.nodes[edge[1]]['health'] > 0:
                        edgeCount +=1

            if edgeCount >= threshold:
                ghosts.append( (node,edgeCount) )
    
    return ghosts



def GetNotDefined(G):
    #G = networkx graphic object
    #returns a list object of all nodes without a classification\
    notDefined = []

    for node in G.nodes():
        if G.nodes[node]['type'] == "N/A":
            notDefined.append(node)

    return notDefined

def GetZeroEdges(G):
    #G = networkx graph object
    #returns a list object of all nodes with zero literal edges
    zeroEdges = []

    for node in G.nodes():
        if G.degree(node) == 0:
            zeroEdges.append(node)

    return zeroEdges


def main():
    #initialize networkx graph
    G = nx.Graph()
    bgColor = 'white'
    fgColor = 'black' #system will automatically adjust the color if necessary

    #this is a list of Classification objects.
    classifications = []

    nodeColor_map = [] #list of colors for each node. appended on every addition of a new node.
    nodeSize_map = [] #list of node sizes. appended on every addition of a new node

    edgeColor_map = [] #list of colors for each edge. items are appended after all edges are established
    edgeWidth_map = [] #same but with width 

    hideZeroHealth = False #hide the 0-health connections
    hideLabels = False

    maxNodeSize = 300 #networkx default: 300.
    minNodeSize = 3
    edgeWidth = 0.5
    zeroHealthColor = '#32cd32'

    expBase = 2 #the base value for the exponential sizing. the larger the value (2+), the smaller weaker connections are
    maxHealthValue = 7 #the highest possible value for "connection health"
    
    healthCounts = []
    for i in range(maxHealthValue+1): healthCounts.append(0)

    #read csv file
    with open('cl-names.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader: #row is a list object with each item correlating to each item in the row that the reader reads

            if (row[0] == "[C]"): #start a file with [C] to specifiy it's classifications
                for i in range(1, len(row), 2): #go through the remaining items
                    #the program will append 2-Tuples for every two items. the first item is the name of the classification, the second is the color of the node, the third value is the count of that classification
                    classifications.append(Classification(row[i],row[i+1],0) )
                #print(classifications)
                continue

            if (row[0] != '#'): #any row with the first item # is a comment! :)
            
                nodeIndex = None

                #procedures for if the node already exists and was added from an edge
                if row[0] in G: #if the item was added from an edge.
                    nodeIndex = list(G).index(row[0]) #search the node list for the index of the already existing node
                    nodeColor_map.pop(nodeIndex) #remove the corresponding color based off of the given node index
                    nodeSize_map.pop(nodeIndex) #remove the corresponding size based on the given node index

                else:
                    nodeIndex = len(G)#sets the nodeIndex to the length of G (aka, the end of the list)
            
                #apply colors based on connection classification
                for x in classifications: #x = every 2-Tuple in the classifications list
                    if row[1] == x.name: #if the classification value in the row matches the classification in the list
                        if (int(row[2]) != 0): x.count+=1
                        nodeColor_map.insert(nodeIndex, x.color) #add a new value to the color map based on the respective color
                        break #continue
                    elif x.name == "Other": #if they reached the end and no classifcation fits. apply the "other" colors
                        if (int(row[2]) != 0): x.count+=1
                        x.count+=1
                        nodeColor_map.insert(nodeIndex, x.color) 
            
                #apply settings based on connection health
                if (int(row[2]) == 0):
                    computedSize = maxNodeSize
                    nodeShape = 'x'
                else:
                    computedSize = minNodeSize + ( (maxNodeSize-minNodeSize) * ( (expBase**int(row[2])) / expBase**maxHealthValue) )
                    nodeShape = 'o'
                
                nodeSize_map.insert(nodeIndex,computedSize) #set the node's size based off of it's health value
                #print(computedSize)
                #add the actual node
                G.add_node(row[0], type=row[1], health=int(row[2]), shape=nodeShape) #add a new node based off of the first item. the second item is the type, third item is connection health
                
                #increase the count of health (if not 0)
                if (int(row[2]) != 0): healthCounts[int(row[2])] += 1
                
                #adds edges to nodes based off of additional items
                for i in range(3, len(row)):
                    if row[i] not in G:
                        nodeColor_map.append('black') #black nodes will represent nodes not inserted in the csv
                        nodeSize_map.append(maxNodeSize) #no-size nodes represent nodes not inserted in the csv  
                        G.add_node(row[i],type="N/A",health=0,shape='x') #add the node anyways. it will be updated later
     
                    G.add_edge(row[0], row[i], isGhostEdge = False) #add edge and assume it's not a ghost edge unless proven otherwise

    #add edge details to edge map
    for e in G.edges():
        #add edge color based on the connection health
        if ( (G.nodes[e[0]]['health'] == 0) or (G.nodes[e[1]]['health'] == 0) ): #if either edge's health is 0
            if (hideZeroHealth == True):
                edgeColor_map.append(zeroHealthColor)
                edgeWidth_map.append(0)
            else:
                edgeColor_map.append(zeroHealthColor)
                edgeWidth_map.append(edgeWidth/3)

            #update edge to be ghost edge
            G.edges[e]['isGhostEdge'] = True

        else:
            edgeColor_map.append(fgColor)
            edgeWidth_map.append(edgeWidth)
        

    #get the positions of the computed nodes
    pos = nx.spring_layout(G)
    
    #extra information
    print("Number of nodes: " + str(G.number_of_nodes()) )
    print("Number of edges: " + str(G.number_of_edges()) )

    print("Count of each health value: " + str(healthCounts))

    groupCounts = []
    for x in classifications: groupCounts.append(x.count)
    print("Count of each group: " + str(groupCounts))

#---------------------------DRAWING (maybe split this into another py later)-------------------------------------
    #set up figure
    fig = plt.figure()
    ax = plt.axes((0,0,1,1))
    
    #drawing the nodes by shape
    nodeShapes = set( (node[1]['shape'] for node in G.nodes(data=True) ) ) #make a set for every shape that appears between each node
    
    for shape in nodeShapes: #go through each node in each shape set (2 sets)
        #make individual lists/maps for each shape and draw from those
        shape_nodeList = []
        shape_nodeSize_map = []
        shape_nodeColor_map = []
        shape_labels = dict() #labels rewuires a dict instead of a list
        #filter the nodes by shape
        for shape_node in filter(lambda x: x[1]['shape'] == shape,G.nodes(data=True)): 
            shape_nodeIndex = list(G).index(shape_node[0]) #get the index of the filered node in the OG list
            shape_nodeList.append(shape_node[0])
            shape_nodeSize_map.append(nodeSize_map[shape_nodeIndex])
            shape_nodeColor_map.append(nodeColor_map[shape_nodeIndex])
            shape_labels[shape_node[0]] = shape_node[0] #update dictionary with node name

        #drawing for 0 health connections
        if shape == 'x': 
            if (hideZeroHealth == True):
                shape_alpha = 0
            else:
                shape_alpha = 0.25
        else:
            shape_alpha = 1

        #label toggle
        if (hideLabels == True):
            label_alpha = 0
        else:
            label_alpha = shape_alpha

        #draw the actual nodes
        nodes = nx.draw_networkx_nodes(G, pos, ax=ax, node_shape=shape, nodelist = shape_nodeList,
        node_size=shape_nodeSize_map, node_color=shape_nodeColor_map,edgecolors=fgColor,alpha=shape_alpha)

        #draw the graph's labels
        nx.draw_networkx_labels(G, pos, ax=ax, labels=shape_labels, alpha=label_alpha, font_size=8,font_color=fgColor,font_weight='bold')

    #draw the graph's edges by style (dash or dot)
    nx.draw_networkx_edges(G, pos, ax=ax, width=edgeWidth_map, edge_color=edgeColor_map)

    #legend
    legend_colors = [] #we append to an empty list of non-plotted points for specific use with the legend
    for x in classifications:
        legend_colors.append(plt.scatter(None,None,c=x.color,label=x.name))
    plt.legend(handles=legend_colors)

    #other stuff
    fig.set_facecolor(bgColor)

    #button_labelToggle = plt.Button(ax,"Toggle Labels")
    #def button_labelToggle_onClick(input):
    #    print(input)
    #button_labelToggle.on_clicked(button_labelToggle_onClick)

    print("Leaves: ")
    print(GetLeaves(G))
    print("Nodes with health 2 or lower: ")
    print(GetLowHealth(G,2))
    print("Nodes with 0 edges: ")
    print(GetZeroEdges(G))
    print("Undefined Nodes: ")
    print(GetNotDefined(G))
    print("Ghosts with more than 1 real edge:")
    print (sorted(GetGhosts(G,1,True),key=lambda x: x[1],reverse=True)) #sorts the list by the 2nd element in the tuple in reverse.
    #that way we can see who we have to most edges to

    #draw histogram of node health
    fig2 = plt.figure()
    ax2 = plt.axes()

    #set up x values of bar chart
    bar_xValues = []
    for i in range(maxHealthValue+1): bar_xValues.append(i)

    plt.bar(bar_xValues,healthCounts,color="blue")
    plt.ylabel("Count")
    ax2.yaxis.set_major_locator(plticker.MultipleLocator(base=2))
    plt.xlabel("Health Value")

    plt.title("Count of Health Values")

    #draw pie chart of types
    fig3 = plt.figure()

    #set up labels of the pie chart
    pie_groupNames = []
    pie_groupColors = []
    for i in classifications:
        pie_groupNames.append(i.name)
        pie_groupColors.append(i.color)

    plt.pie(groupCounts,labels=pie_groupNames,colors=pie_groupColors,autopct='%1.1f%%',shadow=True)

    plt.title("Distribution of Categories")

    plt.show()
    #print(mpld3.fig_to_html(fig))
    #mpld3.show()


main()