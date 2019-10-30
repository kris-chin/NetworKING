"""
    Author: Krischin Layon (2019)

    db-updater.py

    The existance of the program counts as a type of data wrangling.

    The purpose of this program is to make it easier to update or add to the network_visualizer
    so you don't have to manually search and precisely edit a certain row, since these files are
    anticpiated to be really big.


"""
import sqlite3

import csv_db #program if you would like to convert the db to the csv

#runs and returns a query for a given nodeName
#cursor = sqlite3 cursor object
#nodeName = name of node to query for
def fetchNode(cursor, nodeName):
    cursor.execute('''
                SELECT *  FROM nodes
                WHERE name = ?;
                ''', (nodeName, )
                )
    
    #return the query results
    return cursor.fetchone()

#runs and returns a query of all edges of a given string
#cursor = sqlite3 cursor object
#nodeName = name of node to query for
def fetchEdgeNodes(cursor, nodeName):
    edgeNodes = []
    cursor.execute('''
                SELECT * FROM edges
                WHERE node1 = ?;
                ''', (nodeName, )
    )
    for edge in cursor.fetchall():
        edgeNodes.append(edge[1])

    cursor.execute('''
                SELECT * FROM edges
                WHERE node2 = ?;
                ''',(nodeName,)
    )
    for edge in cursor.fetchall():
        edgeNodes.append(edge[0])

    return edgeNodes

def addEdges(cursor,firstNodeName):
    while True:
        nodeName_2 = input("Type in a connection name. Press ENTER to Exit: ")
        if nodeName_2 == '':
            print("\nReturning...\n")
            break
        else:
            cursor.execute('''
                SELECT * FROM nodes
                WHERE name = ?;
            ''',(nodeName_2,)
            )
            if cursor.fetchone() == None:
                print("NOTE: \""+  nodeName_2 + "\" is not on the list.")
            cursor.execute('''
                    INSERT INTO edges (node1, node2)
                    VALUES (?,?);
                    ''', (firstNodeName,nodeName_2,)
                    )

def deleteEdges(cursor,firstNodeName):
    while True:
        nodeName_2 = input("Type in a connection name to delete. Press ENTER to Exit: ")
        if nodeName_2 == '':
            print("\nReturning...\n")
            break
        else:
            #TODO: test if inputted value exists
            cursor.execute('''
                    DELETE FROM edges
                    WHERE node1 = ? AND node2 = ?;
                    ''', (firstNodeName,nodeName_2,)
                    )

def main():
    filename = 'cl-names.db'

    #initalize sqlite3
    conn = sqlite3.connect(filename)
    c = conn.cursor() #cursors are what allow for SQL commands.

    #create tables if they do not exist in given database
    c.execute('''
    CREATE TABLE IF NOT EXISTS nodes
        (id INTEGER NOT NULL PRIMARY KEY,
        name TEXT,
        classification TEXT,
        health INTEGER
        )
    ''')
    c.execute('''
    CREATE TABLE IF NOT EXISTS edges
        (node1 TEXT,
        node2 TEXT)
    ''')
    c.execute('''
    CREATE TABLE IF NOT EXISTS classifications
        (name TEXT,
        color TEXT)
    ''')

    while True:
        #intro message
        print("Network Visualizer Database Manager!\n\n1 - Nodes + Edges\n2 - Classifications\n")
        userInput = input("Press ENTER to quit: ")

        #-------------------------nodes----------------------------------------
        if userInput == '1':
            nodeName = input("\nType in node name. If it doesn't exist, a new node will be added.\nPress ENTER to go back: ")
            if nodeName == '':
                print('')
                continue
            else:
                print('')
                
                nodeQuery = fetchNode(c,nodeName)

                #if the node does not exist (empty query), make a new row
                if nodeQuery == None:
                    print("\"" + nodeName + "\" does not exist. Beginning the Node Creation Process...")
                    nodeClassification = input("\nType in the node classification.\nPress ENTER to cancel: ")
                    if nodeClassification == '': continue
                    else:
                        nodeHealth = input("\nType in the node health.\nPress ENTER to cancel: ")
                        if nodeHealth == '': continue
                        else:
                            print("")
                            #we have all of our information
                            #. create a new row.
                            c.execute('''
                                INSERT INTO nodes (name, classification, health)
                                VALUES (?,?,?);
                                ''', (nodeName,nodeClassification,nodeHealth,)
                                )

                            conn.commit()
                            nodeQuery = fetchNode(c,nodeName)
                
                #print the details of the node
                print("----------------------------")
                print("Name: " + str(nodeQuery[1]))
                print("Classification: " + str(nodeQuery[2]))
                print("Health: " + str(nodeQuery[3]))
                
                edgeQuery = fetchEdgeNodes(c,nodeName)

                print("\nHas connections to: ")
                for edgeNode in edgeQuery: print(" -" + str(edgeNode))

                print("----------------------------")

                print("\n0 - Add Edges\n1 - Delete Edges\n3 - Modify Node\n4 - Delete Node\n")
                userInput = input("Press Enter to Exit: ")
                if userInput == '':
                    print("\nReturning...\n")
                    continue #go back to the beginning
                #add edge
                elif userInput == '0':
                    addEdges(c,nodeName) #looping prompt
                    conn.commit()
                    continue

                #delete edge
                elif userInput == '1':
                    deleteEdges(c,nodeName)
                    conn.commit()
                    continue

                #modify node
                elif userInput == '3':
                    newNodeName = input("Type in new node name. Leave blank to leave unchanged: ")
                    if newNodeName == '':
                        newNodeName = nodeName
                    newClassification = input("Type in new classification. Leave blank to leave unchanged: ")
                    if newClassification == '':
                        newClassification = str(nodeQuery[2])
                    newHealth = input("Type in a new health value. Leave blank to leave unchanged: ")
                    if newHealth == '':
                        newHealth = str(nodeQuery[3])

                    #step one: modify the node in the node table
                    c.execute('''
                        UPDATE nodes
                        SET
                            name = ?,
                            classification = ?,
                            health = ?
                        WHERE
                            name = ?;
                    ''',(newNodeName,newClassification,newHealth,nodeName,)
                    )
                    
                    #step two: rename the instances of the node on the edges table
                    c.execute('''
                        UPDATE edges
                        SET
                            node1 = ?
                        WHERE
                            node1 = ?
                    ''',(newNodeName,nodeName,)
                    )
                    c.execute('''
                        UPDATE edges
                        SET
                            node2 = ?
                        WHERE
                            node2 = ?
                    ''',(newNodeName,nodeName,)
                    )
                    
                    conn.commit()

                    print("New Name: \"" + newNodeName + "\". New Classification: \"" + newClassification + "\". New Health: " + newHealth)
                    continue

                #delete node
                elif userInput == '4':
                    print("Are you sure you want to delete \"" + nodeName + "\"? (y/n)")
                    userInput = input("Press Enter to go back: ")
                    if userInput == 'y':
                        
                        #step 1: delete the node from the node table

                        c.execute('''
                            DELETE FROM nodes
                            WHERE name = ?;
                            ''', (nodeName,)
                        )

                        #step 2: delete the edges that contain the node
                        c.execute('''
                            DELETE FROM edges
                            WHERE node1 = ? OR node2 = ?;
                            ''', (nodeName,nodeName,)
                        )

                        conn.commit()

                        print ("\"" + nodeName + "\" has been deleted. Returning...")

                        continue
                    elif userInput == 'n':
                        print("\nReturning...\n")
                        continue
                    elif userInput == '':
                        continue
                    else:
                        print("\nInvalid Input.\n")
                        continue

                else:
                    print("\nInvalid Input.\n")
                    continue
                
        #-------------------------classifications----------------------------------------- 
        elif userInput == '2':
            print("----------------------------")
            print("Classifications: ")

            c.execute('''
                SELECT *
                FROM classifications;
            ''')
            classificationsQuery = c.fetchall()
            for classification in classificationsQuery:
                print("\"" + str(classification[0]) + "\". Color: " + str(classification[1]))

            print("----------------------------")
            
            print("\nType in a classification name. If it doesn't exist, a new classification will be made.")
            classificationName = input("Or press ENTER to go back: ")
            
            if classificationName == '':
                print("\nReturning...\n")
                continue

            else:
                c.execute('''
                    SELECT *
                    FROM classifications
                    WHERE name = ?;
                ''', (classificationName, )
                )
                classQuery = c.fetchone()
                
                #creating a new classification
                if classQuery == None:
                    print("\"" + classificationName + "\" does not exist.")
                    classificationColor = input("Enter classification color, or press ENTER to go back: ")
                    if classificationColor == '':
                        continue
                    else:
                        c.execute('''
                            INSERT INTO classifications (name, color)
                            VALUES (?,?);
                        ''', (classificationName,classificationColor,)
                        )
                        print("\"" + classificationName + "\". Color: " + classificationColor + " created.")
                        conn.commit()
                        continue
                #targeting an existing classification
                else:
                    userInput = input("\n1 - Modify classification\n2 - Delete Classification\nPress ENTER to go back: ")
                    #modify classification
                    if userInput == '1':
                        newClassName = input("Type in new class name. Leave blank to leave unchanged: ")
                        if newClassName == '':
                            newClassName = classificationName
                        newColor = input("Type in new color. Leave blank to leave unchanged: ")
                        if newColor == '':
                            newColor = str(classQuery[1])

                        c.execute('''
                            UPDATE classifications
                            SET
                                name = ?,
                                color = ?,
                            WHERE
                                name = ?;
                        ''',(newClassName,newColor,classificationName,)
                        )
                        
                        conn.commit()

                        print("New Name: \"" + newClassName + "\". New Color: " + newColor)
                        continue
                    #delete classification
                    elif userInput == '2':
                        print("Are you sure you want to delete \"" + classificationName + "\"? (y/n)")
                        userInput = input("Press ENTER to go back: ")
                        if userInput == 'y':
                            
                            c.execute('''
                                DELETE FROM classifications
                                WHERE name = ?;
                            ''', (classificationName,)
                            )
                            conn.commit()

                            print("\"" + classificationName + "\" deleted.")

                            continue
                        elif userInput == 'n':
                            print("Returning...")
                            continue
                        elif userInput == '':
                            print("Returning...")
                            continue
                        else:
                            print("Invalid Input.")
                            continue
                    elif userInput == '':
                        print("Returning...")
                        continue
                    else:
                        print("Invalid Input.")
                        continue

        #---------------------------exit-----------------------------
        elif userInput == '':
            conn.close()
            userInput = input("Would you like to export a csv file of this database? (enter: y/n): ")
            if userInput == 'n':
                print("Bye!")
            else: 
                csv_db.Convert(filename,True)
            break
        
        else:
            print("\nInvalid Input.\n")

main()
