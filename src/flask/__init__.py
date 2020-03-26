from flask import Flask, request, session, jsonify
import model.Accessor, model.Graph, model.Graph_Meta, User
from flask_cors import CORS

app = Flask(__name__) #our app is a new Flask instance
database = "model/test_database.db"

SECRET_KEY = "secret key" #used for sessions
CORS(app, supports_credentials=True)#allows for cross-origin resource sharing (angular to flask)

@app.route('/login', methods=['POST'])
def login():
    #returns 'success=true' if this is a valid login
    #when a client recieves this success value, the client will set a cookie signifying that the user is properly logged in
    username = request.json['user_or_email']
    password = request.json['pass']

    A = model.Accessor.Accessor(database)
    try:
        print("USER " + username + " FOUND.")
        id = int(A.FindUserID(username,password))
        #obviously not secure
        return {'success': True, 'user_validated': username, 'pass_validated': password}
    except:
        print("NO USER FOUND")
        return {'success': False}

@app.route('/graph', methods=['POST'])
def graph():

    #access the respective data based on the inputted userid
    username = request.json['user_validated']
    password = request.json['pass_validated']

    A = model.Accessor.Accessor(database)
    try:
        id = int(A.FindUserID(username,password))
    except:
        return {'success': False}

    #create respective lists of objects from db data
    classifications = []
    for row in A.GetClassificationsData(id):
        classifications.append(model.Graph.Classification(row[0], row[2], row[3]))
    vertices = []
    for row in A.GetVerticesData(id):
        #get the respective classification based on the data in row[3]
        c = model.Graph.FindClassificationByID(classifications,row[4])
        vertices.append(model.Graph.Vertex(row[0], row[2], c, row[5], row[6], row[7]))
    edges = []
    for row in A.GetEdgesData(id):
        v1 = model.Graph.FindVertexByID(vertices, row[3])
        v2 = model.Graph.FindVertexByID(vertices, row[5])
        edges.append(model.Graph.Edge(row[0], (v1, v2), row[6], row[7], row[8]))

    #create Graph from db data
    G = model.Graph.Graph(vertices,edges,classifications)
    user = {'userid': id, 'username' : username}

    response = {'success': True, 'user': user, 'graph': G.json()}

    return response

@app.route('/graph/update', methods = ['POST'])
def Update():
    #updates the database with the request's graph object
    try:
        id = int(request.json['user']['userid'])
    except:
        id = None
    print("ID: " + str(id))

    #get the response graph object
    g = model.Graph.dejson(request.json['graph'])
    A = model.Accessor.Accessor(database)
    
    #update the database based on the inputted graph object
    #THE FOLLOWING LINE IS NOT SECURE!!!
    result = A.SetAllData(g,id)

    if (result == True):
        print('Successfully updated DB')
        return {'success': True}
    else:
        print('Failed to update DB')
        return {'success': False}

@app.route('/signup', methods = ['POST'])
def signup():
        email = request.json['email']
        username = request.json['user']
        password = request.json['pass']

        if (username == "" or password == "" or email == ""):
            response = {'success': False}
            return response
        else:
            if (not (User.validEmail(email))): #if valid email
                print("Email is used")
                response = {'success': False}
                return response
            elif (not (User.validUser(username))): #if user 
                print("username is taken")
                response = {'success': False}
                return response
            elif (not (User.validPassword(password))):
                print("password is invalid")
                response = {'success': False}
                return response
            print("Valid.")

            #add to database
            A = model.Accessor.Accessor(database)
            A.AddUser(email,username,password)

            response = {'success': True, 'user_validated': username, 'pass_validated': password}

            return response
            

#this only runs if the file was run as a script
if __name__ == '__main__':
    #run() runs the application on the local devleopment server
    app.run()