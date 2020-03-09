from flask import Flask, render_template, request
import model.Accessor, model.Graph, model.Graph_Meta, User

app = Flask(__name__) #our app is a new Flask instance

#the @ symbol is a decorator in python
@app.route('/') #by decorating route() with ('/'), it binds any following functions with the '/' URL

def index(): #for example, '/' is bound to hello_world
    return render_template('index.html', invalid = False)

@app.route('/graph', methods=['GET', 'POST'])
def graph():
    if request.method == 'POST':
        
        #access the respective data based on the inputted userid
        username = request.form['user']
        password = request.form['pass']

        A = model.Accessor.Accessor("model/test_database.db")
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
        return render_template('graph.html', title ='THE GANG 2', user=user, graph = G.json())
    else:
        user = {'userid': '-1', 'username' : 'dog'} #this is a json
        graph = {'classifications' : [], 'vertices': [], 'edges' : []}
        return render_template('graph.html', title='THE GANG', user=user, graph = graph)

@app.route('/graph/update', methods = ['POST'])
def update():
    print("TODO: calling this method updates the graph with the new graph")

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
            A = model.Accessor.Accessor("model/test_database.db")
            A.AddUser(email,username,password)

            return render_template('success.html', userdata = data)

#this only runs if the file was run as a script
if __name__ == '__main__':
    #run() runs the application on the local devleopment server
    app.run()