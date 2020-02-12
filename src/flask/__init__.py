from flask import Flask, render_template, request
import model.Accessor, model.Graph, model.Graph_Meta

app = Flask(__name__) #our app is a new Flask instance

#the @ symbol is a decorator in python
@app.route('/') #by decorating route() with ('/'), it binds any following functions with the '/' URL

def hello_world(): #for example, '/' is bound to hello_world
    #the tutorials say to do all of this in an HTML template and not literally just returning a string of HTML code, but hey.
    return '<a href="http://google.com/"> Click this to go to google </a>'

@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        
        #access the respective data based on the inputted userid
        id = int(request.form['userid'])
        A = model.Accessor.Accessor("model/test_database.db")
        username = A.GetUserData(id)[0][2]

        #create respective lists of objects from db data
        classifications = []
        for row in A.GetClassificationsData(id):
            classifications.append(model.Graph.Classification(row[0], row[2], row[3]))
        vertices = []
        for row in A.GetVerticesData(id):
            #get the respective classification based on the data in row[3]
            c = model.Graph.FindClassification(classifications,row[3])
            vertices.append(model.Graph.Vertex(row[0], row[2], c, row[4], row[5], row[6]))
        edges = []
        for row in A.GetEdgesData(id):
            v1 = model.Graph.FindVertex(vertices, row[2])
            v2 = model.Graph.FindVertex(vertices, row[3])
            edges.append(model.Graph.Edge(row[0], (v1, v2), row[4], row[5], row[6]))

        #create Graph from db data
        G = model.Graph.Graph(vertices,edges,classifications)

        user = {'userid': id, 'username' : username}
        return render_template('index.html', title ='THE GANG 2', user=user, graph = G.json())
    else:
        user = {'userid': '-1', 'username' : 'dog'} #this is a json
        graph = {'classifications' : [], 'vertices': [], 'edges' : []}
        return render_template('index.html', title='THE GANG', user=user, graph = graph)

#this only runs if the file was run as a script
if __name__ == '__main__':
    #run() runs the application on the local devleopment server
    app.run()