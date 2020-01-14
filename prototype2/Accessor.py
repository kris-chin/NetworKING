import sqlite3

class SQLITE:
    def ConnectCursor(self,database): #returns a tuple of a SQLITE connection and it's cursor
        conn = sqlite3.connect(database)
        return (conn,conn.cursor)
    

#The Accessor Object access the DB for Graph Information for a user id.
#It returns the collected information in the form of our Python Objects that we created.
class Accessor:

    def __init__(self, type_of_access, database):

        #connect to database with a given connection. c is cursor.
        connection = type_of_access.ConnectCursor(database)
        self.conn = connection[0]
        self.c = connection[1]

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
                (userid INTEGER,
                node1 TEXT,
                node2 TEXT,
                color TEXT,
                size INTEGER,
                style TEXT)
            ''')
        #Create "classifications" table
        self.c.execute('''
            CREATE TABLE IF NOT EXISTS classifications
                (userid INTEGER,
                name TEXT,
                color TEXT,
                count INTEGER)
            ''')
        #Create "usersettings" table
        self.c.execute('''
            CREATE TABLE IF NOT EXISTS usersettings
                (userid INTEGER,
                darkmode BIT)
        ''')

    def GetClassificationsData(self,userid):
        print("TODO")

    def SetClassificationsData(self,userid):
        print("TODO")

    def GetEdgesData(self,userid):
        print("TODO")

    def SetEdgesData(self,userid):
        print("TODO")

    def GetVerticesData(self,userid):
        print("TODO")

    def SetVerticesData(self,userid):
        print("TODO")