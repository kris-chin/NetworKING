from flask import Flask, render_template, request, session, redirect
import model.Accessor, model.Graph, model.Graph_Meta, User
from flask_cors import CORS

app = Flask(__name__) #our app is a new Flask instance
CORS(app) #allows for cross-origin resource sharing (angular to flask)
app.secret_key = 'secret key' #used for sessions
database = "model/test_database.db"

#the @ symbol is a decorator in python
@app.route('/') #by decorating route() with ('/'), it binds any following functions with the '/' URL
def index():
    if 'user' in session: #if a user is logged in client-wise
        print("A user is logged into the session. Redirecting...")
        return redirect('/graph')
    else: #if no one is logged in
        return render_template('index.html', invalid = False)

@app.route('/graph', methods=['GET', 'POST'])
def graph():
    if request.method == 'POST': #called on log-in specifically.
        #print(request.json)
        #access the respective data based on the inputted userid
        username = request.json['user_or_email']
        password = request.json['pass']

        A = model.Accessor.Accessor(database)
        try:
            id = int(A.FindUserID(username,password))
        except:
            print("NO USER FOUND")
            return render_template('index.html', invalid = True)
        print("USER " + username + " FOUND. Loading...")

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

        #save session variables for the user and the graph, these are basically secure cookies
        session['user'] = user
        session['graph'] = G.json()

        return {'user': session['user'], 'graph': session['graph']}
    else:
        if 'user' in session: #if the user is already logged in on the client
            user = session['user']
            graph = session['graph']
        else: #if no user is logged in 
            user = {'userid': '-1', 'username' : 'dog'} #this is a json
            graph = {'classifications' : [], 'vertices': [], 'edges' : []}
        return render_template('graph.html', title='THE GANG', user=user, graph = graph)

@app.route('/graph/update', methods = ['POST'])
def Action():
    #get action button clicked
    action = request.form['action']
    print("Action: " + str(action))
    try:
        id = int(request.form['id'])
    except:
        id = None
    print("ID: " + str(id))

    #get the graph object for the current session
    g = model.Graph.dejson(session['graph'])

    if (action == 'Add Class'):
        input_name = request.form['classification_name']
        input_color = request.form['classification_color']
        input_id = model.Graph.HighestID(g.classifications) + 1

        if (input_name == '' or input_color ==''):
            print("Error: Incomplete input")
        else:
            g.AddClass(model.Graph.Classification(input_id, input_name, input_color))

    elif (action == 'Edit Class'):
        input_name = request.form['classification_name']
        input_color = request.form['classification_color']
        g.UpdateClassification(id, input_name, input_color)

    elif (action == 'Delete Class'):
        g.RemoveClassification(id)

    elif (action == 'Add Vertex'):
        input_name = request.form['vertex_name']
        input_type_id = request.form['vertex_type'] #STRING OF TYPE, NEEDS CONVERSION
        input_type = model.Graph.FindClassificationByID(g.classifications,int(input_type_id))
        
        input_health = request.form['vertex_health']
        #input_shape = request.form['vertex_shape']
        input_shape = 'o'
        input_notes = request.form['vertex_notes']

        input_id = model.Graph.HighestID(g.vertices) + 1

        if (input_name == '' or input_type == None):
            print("Error: Empty or Invalid Input for Adding Vertex")
        else:
            g.AddVertex(model.Graph.Vertex(input_id,input_name,input_type,input_health,input_shape,input_notes))

    elif (action == 'Edit Vertex'):
        input_name = request.form['vertex_name']
        input_type_id = request.form['vertex_type'] #STRING OF TYPE ID
        input_type = model.Graph.FindClassificationByID(g.classifications,int(input_type_id))
        input_health = request.form['vertex_health']
        #input_shape = request.form['vertex_shape'] 
        input_shape = 'o'
        input_notes = request.form['vertex_notes']
        
        g.UpdateVertex(id, input_name, input_type, input_health, input_shape, input_notes)

    elif (action == 'Add Neighbor'):
        input_neighbor_id = request.form['vertex_addNeighbor'] #ID OF NEIGHBOR
        input_neighbor = model.Graph.FindVertexByID(g.vertices, int(input_neighbor_id))
        #input_color
        #input_size
        #input_style

        input_id = model.Graph.HighestID(g.edges) + 1
        input_vertex = model.Graph.FindVertexByID(g.vertices, id)

        if (input_neighbor == None):
            print("Error: Neighbor is invalid")
        elif (input_neighbor in g.GetNeighbors(input_vertex) ):
            print("Error: Vertices are already neighbors")
        else:
            g.AddEdge(model.Graph.Edge(input_id, (input_vertex, input_neighbor)) )

    elif (action == 'Delete Vertex'):
        g.RemoveVertex(id)

    elif (action == 'Edit Edge'):
        #input_color = request.form['edge_color'] #this is a color value
        input_color = 'Black'
        input_size = request.form['edge_size']
        #input_style = request.form['edge_style']
        input_style = 'solid'

        g.UpdateEdge(id, input_color, input_size, input_style)

    elif (action == 'Delete Edge'):
        g.RemoveEdge(id)

    elif (action == 'Edit User Settings'):
        print("EUS")

    elif (action == 'Log Out'):
        #note: not secure, if id is modified then you can edit the values of other id's graphs
        A = model.Accessor.Accessor(database)
        A.SetAllData(g,int(session['user']['userid']))
        #print(session['user']['userid'])

        #pop session variables, logging the user out of the session
        session.pop('user', None)
        session.pop('graph', None)
        return redirect('/') #go back to regular
    else:
        print('INVALID ACTION: \"' + action + "\'")

    #update session values
    session['graph'] = g.json()
    
    return render_template('graph.html', title ='THE GANG 2', user = session['user'], graph = session['graph'])

@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    if request.method == 'GET':
        email = ""; username = ""; password = ""
        data = {'email':email , 'username': username, 'password':password}

        return render_template('signup.html', invalid = False, userdata = data)
    else:
        email = request.form['email']
        username = request.form['user']
        password = request.form['pass']

        data = {'email':email , 'username': username, 'password':password}

        if (username == "" or password == "" or email == ""):
            return render_template('signup.html', invalid = True, userdata = data)
        else:
            
            if (not (User.validEmail(email))): #if valid email
                print("Email is used")
                return render_template('signup.html', invalid = True, userdata = data)
            elif (not (User.validUser(username))): #if user 
                print("username is taken")
                return render_template('signup.html', invalid = True, userdata = data)
            elif (not (User.validPassword(password))):
                print("password is invalid")
                return render_template('signup.html', invalid = True, userdata = data)
            
            print("Valid.")

            #add to database
            A = model.Accessor.Accessor(database)
            A.AddUser(email,username,password)

            return render_template('success.html', userdata = data)

#this only runs if the file was run as a script
if __name__ == '__main__':
    #run() runs the application on the local devleopment server
    app.run()