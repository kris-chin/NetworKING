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
                (id INTEGER NOT NULL PRIMARY KEY,
                userid INTEGER,
                name TEXT,
                classification TEXT,
                health INTEGER,
                shape TEXT,
                notes TEXT
                )
            ''')
        #Create "edges" table
        self.c.execute('''
            CREATE TABLE IF NOT EXISTS edges
                (id INTEGER NOT NULL PRIMARY KEY,
                userid INTEGER,
                vertex1 TEXT,
                vertex2 TEXT,
                color TEXT,
                size INTEGER,
                style TEXT)
            ''')
        #Create "classifications" table
        self.c.execute('''
            CREATE TABLE IF NOT EXISTS classifications
                (id INTEGER NOT NULL PRIMARY KEY,
                userid INTEGER,
                name TEXT,
                color TEXT,
                count INTEGER)
            ''')
        
        #Create "usersettings" table
        self.c.execute('''
            CREATE TABLE IF NOT EXISTS usersettings
                (id INTEGER NOT NULL PRIMARY KEY,
                userid INTEGER,
                username TEXT,
                darkmode BIT)
            '''
        ) 
        #check for missing columns in usersettings and add them
        try:
            self.c.execute('''
                SELECT username FROM usersettings
                '''
            )
        except sqlite3.Error:
            #sqlite3 can only execute 1 statement at a time, i'll have to fix this so it doesn't look so ugly
            self.c.execute('''
                ALTER TABLE usersettings
                RENAME TO usersettings_temp
                '''
            ) 
            self.c.execute('''
                CREATE TABLE usersettings
                    (id INTEGER NOT NULL PRIMARY KEY,
                        userid INTEGER,
                        username TEXT,
                        darkmode BIT)
                '''
            )
            self.c.execute('''
                INSERT INTO usersettings (userid, darkmode) SELECT userid, darkmode FROM usersettings_temp
            '''
            )
            self.c.execute('''
                DROP TABLE usersettings_temp
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
                    INSERT INTO classifications (userid, name, color, count)
                    VALUES (?, ?, ?, ?)
                    ''', (userid, cl.name, cl.color, cl.count, )
                )
        self.conn.commit()

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
                    SET vertex1 = ?, vertex2 = ?, color = ?, size = ?, style = ?
                    WHERE (id = ? AND userid = ?)
                    ''', (edge.vertices[0].name, edge.vertices[1].name, edge.color, edge.size, edge.style, edge.id, userid,  )
                )

            else:
                #if edges doesn't exist in table
                self.c.execute('''
                    INSERT INTO edges (userid, vertex1, vertex2, color, size, style)
                    VALUES (?, ?, ?, ?, ?, ?)
                    ''', (userid, edge.vertices[0].name, edge.vertices[1].name, edge.color, edge.size, edge.style)
                )
        self.conn.commit()

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
                    SET name = ?, classification = ?, health = ?, shape = ?, notes = ?
                    WHERE (id = ? AND userid = ?)
                    ''', (v.name, v.type.name, v.health, v.shape, v.notes, v.id, userid, )
                )

            else:
                #if vertex doesn't exist in table
                self.c.execute('''
                    INSERT INTO nodes (userid, name, classification, health, shape, notes)
                    VALUES (?, ?, ?, ?, ?, ?)
                    ''', (userid, v.name, v.type.name, v.health, v.shape, v.notes, )
                )
        self.conn.commit()

    def GetUserData(self,userid):
        #Returns a list of Row data for User Settings (Needs cleaning)
        #Get all of the Settings that have the same userid as the provided userid
        self.c.execute('''
            SELECT *  FROM usersettings
            WHERE userid = ?;
            ''', (userid, )
            )

        #return the query results
        return self.c.fetchall()

    def SetUserData(self,json_settings_file,userid):
        with open(json_settings_file) as file:
            data = json.load(file)
            print("file loaded")
            #Check if user exists
            self.c.execute('''
                SELECT * FROM usersettings
                WHERE (userid = ?)
                ''', (userid, )
            )

            if self.c.fetchone() != None:
                self.c.execute('''
                    UPDATE usersettings
                    SET username = ?, darkmode = ?
                    WHERE (userid = ?)
                    ''', (data['username'], (data['darkmode'] == "True"), userid, )
                )
            else: #if user doesn't even exist
                self.c.execute('''
                    INSERT INTO usersettings (userid, username, darkmode)
                    VALUES (?, ?, ?)
                    ''', (userid, data['username'], (data['darkmode'] == "True"),  )
                )
        self.conn.commit()

    def SetAllData(self,graph,userid,settings_file):
        self.SetClassificationsData(graph,userid)
        self.SetEdgesData(graph,userid)
        self.SetVerticesData(graph,userid)
        self.SetUserData(graph,userid,settings_file)