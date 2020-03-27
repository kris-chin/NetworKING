import sqlite3, json
#The Accessor Object access the DB for Graph Information for a user id.
#It returns the collected information in the form of our Python Objects that we created.
class Accessor:

    def __init__(self, database):

        #connect to database with a given connection. c is cursor.
        self.conn = sqlite3.connect(database)
        self.c = self.conn.cursor()

        #create tables if they do not exist in given database

        #Create "nodes" table
        self.c.execute('''
            CREATE TABLE IF NOT EXISTS nodes
                (id INTEGER NOT NULL,
                userid INTEGER,
                name TEXT,
                classification TEXT,
                classification_id INTEGER,
                health INTEGER,
                shape TEXT,
                notes TEXT
                )
            ''')
        #Create "edges" table
        self.c.execute('''
            CREATE TABLE IF NOT EXISTS edges
                (id INTEGER NOT NULL,
                userid INTEGER,
                vertex1 TEXT,
                vertex1_id INTEGER,
                vertex2 TEXT,
                vertex2_id INTEGER,
                color TEXT,
                size INTEGER,
                style TEXT)
            ''')
        #Create "classifications" table
        self.c.execute('''
            CREATE TABLE IF NOT EXISTS classifications
                (id INTEGER NOT NULL,
                userid INTEGER,
                name TEXT,
                color TEXT,
                count INTEGER)
            ''')
        #Create a "userbase" table (be careful!!!)
        self.c.execute('''
            CREATE TABLE IF NOT EXISTS userbase
            (id INTEGER NOT NULL,
            userid INTEGER,
            email TEXT,
            username TEXT,
            password TEXT,
            settingsfile TEXT
            )
            '''
        )
        try:
            self.c.execute('''
                SELECT settingsfile from userbase
            ''')
        except (sqlite3.Error): #used for debug. modify the below table individually to your liking
            print("UPDATING")
            #sqlite3 can only execute 1 statement at a time, i'll have to fix this so it doesn't look so ugly
            self.c.execute('''
                INSERT INTO userbase (userid) SELECT userid FROM usersettings
            '''
            )
            self.c.execute('''
                DROP TABLE usersettings
            '''
            )
        self.conn.commit()
    def GetClassificationsData(self,userid):
        #Returns a list of Row Data for Classifications (Needs cleaning)
        #Get all of the Classifications that have the same userid as the provided userid
        self.c.execute('''
            SELECT *  FROM classifications
            WHERE userid = ?;
            ''', (userid, )
        )

        #return the query results
        return self.c.fetchall()

    def SetClassificationsData(self,graph,userid):
        #update the classifcation data for the given userid based on the inputted graph object
        for cl in graph.classifications:
            #Check if classification exists
            self.c.execute('''
                SELECT * FROM classifications
                WHERE (userid = ? AND id = ?);
                ''', (userid, cl.id, )
            )

            if self.c.fetchone() != None: 
                #if classification exists in table
                self.c.execute('''
                    UPDATE classifications
                    SET name = ?, color = ?, count = ?
                    WHERE (id = ? AND userid = ?);
                    ''', (cl.name, cl.color, cl.count, cl.id, userid,  )
                )

            else:
                #if classification doesn't exist in table
                self.c.execute('''
                    INSERT INTO classifications (id, userid, name, color, count)
                    VALUES (?, ?, ?, ?, ?)
                    ''', (cl.id, userid, cl.name, cl.color, cl.count, )
                )
        self.conn.commit()
        return True

    def GetEdgesData(self,userid):
        #Returns a list of Row data for Edges (Needs cleaning)
        #Get all of the Edges that have the same userid as the provided userid
        self.c.execute('''
            SELECT *  FROM edges
            WHERE userid = ?;
            ''', (userid, )
            )

        #return the query results
        return self.c.fetchall()

    def SetEdgesData(self,graph,userid):
        #update the edges data for the given userid based on the inputted graph object
        for edge in graph.edges:
            #Check if edge exists
            self.c.execute('''
                SELECT * FROM edges
                WHERE (userid = ? AND id = ?)
                ''', (userid, edge.id, )
            )

            if self.c.fetchone() != None: 
                #if edge exists in table
                self.c.execute('''
                    UPDATE edges
                    SET vertex1 = ?, vertex1_id = ?, vertex2 = ?, vertex2_id = ?, color = ?, size = ?, style = ?
                    WHERE (id = ? AND userid = ?)
                    ''', (edge.vertices[0].name, edge.vertices[0].id, edge.vertices[1].name, edge.vertices[1].id, edge.color, edge.size, edge.style, edge.id, userid,  )
                )

            else:
                #if edges doesn't exist in table
                self.c.execute('''
                    INSERT INTO edges (id, userid, vertex1, vertex1_id, vertex2, vertex2_id, color, size, style)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (edge.id, userid, edge.vertices[0].name, edge.vertices[0].id, edge.vertices[1].name,  edge.vertices[1].id, edge.color, edge.size, edge.style)
                )
        self.conn.commit()
        return True

    def GetVerticesData(self,userid):
        #Returns a list of Row data for Vertices (Needs cleaning)
        #Get all of the Nodes that have the same userid as the provided userid
        self.c.execute('''
            SELECT *  FROM nodes
            WHERE userid = ?;
            ''', (userid, )
            )

        #return the query results
        return self.c.fetchall()


    def SetVerticesData(self,graph,userid):
        #update the vertices data for the given userid based on the inputted graph object
        for v in graph.vertices:
            #Check if vertex exists
            self.c.execute('''
                SELECT * FROM nodes
                WHERE (userid = ? AND id = ?)
                ''', (userid, v.id, )
            )

            if self.c.fetchone() != None: 
                #if vertex exists in table
                self.c.execute('''
                    UPDATE nodes
                    SET name = ?, classification = ?, classification_id = ?, health = ?, shape = ?, notes = ?
                    WHERE (id = ? AND userid = ?)
                    ''', (v.name, v.type.name, v.type.id, v.health, v.shape, v.notes, v.id, userid, )
                )

            else:
                #if vertex doesn't exist in table
                self.c.execute('''
                    INSERT INTO nodes (id, userid, name, classification, classification_id, health, shape, notes)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (v.id, userid, v.name, v.type.name, v.type.id, v.health, v.shape, v.notes, )
                )
        self.conn.commit()
        return True

    def GetUserData(self,userid):
        #Returns a list of Row data for User Settings (Needs cleaning)
        #Get all of the Settings that have the same userid as the provided userid
        self.c.execute('''
            SELECT settingsfile  FROM userbase
            WHERE userid = ?;
            ''', (userid, )
            )

        #return the query results
        return self.c.fetchall()

    def AddUser(self,email,username,password):
        #Adds a user to the userbase
        newID = self.GenerateUserID()

        self.c.execute('''
        INSERT INTO userbase (userid, email, username, password )
        VALUES (?, ?, ?, ?)
        ''', (newID, email, username, password, )
        )
        self.conn.commit()

    def SetUserSettings(self,json_settings_file,userid):
        #with open(json_settings_file) as file:
            #data = json.load(file)
            #print("file loaded")
            #Check if user exists
        self.c.execute('''
            SELECT * FROM userbase
            WHERE (userid = ?)
            ''', (userid, )
        )

        if self.c.fetchone() != None:
            self.c.execute('''
                UPDATE usersbase
                SET usersettings
                WHERE (userid = ?)
                ''', (json_settings_file, userid, )
            )
        else: #if user doesn't even exist
            print("user n/a")
            #we can't update settings, since the user doesn't exist. we need the user to sign in
        self.conn.commit()
        return True

    #finds a userid using a provided username and pass (extremely unsecure. remember to change)
    def FindUserID(self,user,password):
        self.c.execute('''
            SELECT userid FROM userbase
            WHERE (username = ? AND password = ?)
        ''', (user,password, ) )
        ids = self.c.fetchall()
        print("ids: " + str(ids))
        if ids != None:
            if (len(ids) == 1):
                return ids[0][0]
            else:
                print("There is a duplicate entry of either username or password in the database")
                return None
        else:
            return None

    def SetAllData(self,graph,userid):
        #returns true if successfully set database data
        classificationCheck = self.SetClassificationsData(graph,userid)
        edgeCheck = self.SetEdgesData(graph,userid)
        vertexCheck = self.SetVerticesData(graph,userid)
        #self.SetUserData(graph,userid,settings_file)
        if (classificationCheck == True and edgeCheck == True and vertexCheck == True):
            return True
        else:
            return False

    def GenerateUserID(self):
        self.c.execute('''
            SELECT max(userid) FROM userbase;
        ''')
        highestValue = self.c.fetchone()[0]
        if highestValue != None:
            #print("highestValue:" + str(highestValue))
            return highestValue + 1
        else:
            return None
