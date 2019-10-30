"""
    Author: Krischin Layon (2019)

    csv_db.py

    This is a quick formatter script that reads our formatted CSVs and instantly puts them into the db
    
    The purpose of this script is so we don't have to be manually inputting values of a large CSV for awhile.
    There is also an option to convert a DB back to a CSV.
"""

import csv
import sqlite3
import os

def Convert(fileName,sameName):
    #filename = string. name of file
    #sameName = bool. if true, uses skips the step of specifying the other file's name
    #          -ex. if true and inputing a db, skips specifying the csv and just uses the same string for a csv
    
    if fileName.lower().endswith('.csv'):
        if os.path.exists(fileName) == False:
            print("File does not exist.")
        else: 
            print("CSV file detected.")
            if sameName == False:
                dbName = input("Enter the name of the database to write to: ")
            else:
                dbName = fileName.replace('.csv','.db')
            if os.path.exists(dbName):
                if dbName.lower().endswith('.db'):
                    with open(fileName, newline='') as csvfile:
                        reader = csv.reader(csvfile)
                        with sqlite3.connect(dbName) as conn:
                            c = conn.cursor()

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

                            #go through each row 
                            for row in reader:
                                if row[0] == "[C]": #if classification
                                    #go through every classification in the row and add it
                                    print("Classification Detected...")
                                    for i in range(1,len(row),2):

                                        #check if exists
                                        c.execute('''
                                            SELECT * FROM classifications
                                            WHERE name = ?;
                                            ''', (row[i],)
                                            )
                                        if c.fetchone() == None:
                                            #add
                                            c.execute('''
                                                INSERT INTO classifications (name, color)
                                                VALUES (?,?);
                                                ''', (row[i], row[i+1],)
                                                )
                                            print(" -Imported: \"" + row[i] + "\" Color: " + row[i+1])
                                        else:
                                            print(" -\"" + row[i] + "\" is already in the database. Ignoring...")

                                elif row[0] == "#": #if comment
                                    print("Comment detected. Ignoring...")

                                else: #if actual entry
                                    print("Entry Detected...")

                                    #check if exists 
                                    c.execute('''
                                        SELECT * FROM nodes
                                        WHERE name = ?;
                                        ''', (row[0],)
                                        )
                                    
                                    if c.fetchone() == None:
                                        #add
                                        c.execute('''
                                            INSERT INTO nodes (name, classification, health)
                                            VALUES (?,?,?);
                                            ''', (row[0],row[1],row[2],)
                                            )

                                        print(" -Imported: \"" + row[0] + "\", Classification: " + row[1] + ", Health: " + row[2])
                                        print("  -EDGES: ", end="")
                                    else:
                                        print(" -\"" + row[0] + "\" is already in the database. Checking for new edges..." )
                                        print("  -NEW EDGES: ", end="")
                                    #import edges
                                    for i in range(3,len(row)):
                                        #check if exists
                                        c.execute('''
                                            SELECT * FROM edges
                                            WHERE node1 = ? AND node2 = ?;
                                            ''', (row[0],row[i],)
                                            )
                                        if c.fetchone() == None:
                                            #add
                                            c.execute('''
                                                INSERT INTO edges (node1,node2)
                                                VALUES (?,?);
                                                ''', (row[0],row[i],)
                                                )
                                            print(row[i], end=", ")
                                    print("")
                                        
                            print("\nImport Complete.\n")
                            conn.commit()
                        conn.close()

                else:
                    print("Invalid Input.")
            else:
                print("Database doesn't exist.")

    #-------------------------------------------------------------
    #DB TO CSV
    elif fileName.lower().endswith('.db'):
        if os.path.exists(fileName) == False:
            print("File does not exist.")
        else:
            print("Database detected.")
            if sameName == False:
                csvName = input("Enter the name of the CSV. (Overwrites existing CSVs): ")
            else:
                csvName = fileName.replace(".db",".csv")
            if csvName.lower().endswith('.csv'):
                with sqlite3.connect(fileName) as conn:
                    c = conn.cursor()
                    with open("TEMPDATA","w+",newline="") as csvfileTemp:
                        writer = csv.writer(csvfileTemp)
                        
                        #write the first set of rows for classifications
                        c.execute('''
                        SELECT * from classifications
                        ''')
                        for dbClass in c.fetchall():
                            writer.writerow(['[C]', dbClass[0], dbClass[1]])

                        #write the next set of rows for nodes and their edges
                        c.execute('''
                        SELECT * from nodes
                        ''')
                        for dbNode in c.fetchall():
                            fullRow = [dbNode[1],dbNode[2],dbNode[3]] #have a list of just the node details for now
                            c.execute('''
                            SELECT * from edges
                            WHERE node1 = ?;
                            ''',(dbNode[1],)
                            )
                            for dbNodeEdge in c.fetchall():
                                fullRow.append(dbNodeEdge[1]) #append to the fullRow list for every edge
                            writer.writerow(fullRow)
                        
                    if os.path.exists(csvName):
                        os.remove(csvName) #delete the old file
                    os.rename("TEMPDATA", csvName) #rename the temporary data to this file

                conn.close()
                print("Written to \"" + csvName + "\".\n")

            else:
                print("Invalid Input.")
    else:
        print("Invalid Input.")
'''
while True:
    filename = input("Enter the name of the file to convert. (Press ENTER to exit):")
    if filename == '':
        print("Goodbye!")
        break
    else:
        Convert(filename,False)
'''