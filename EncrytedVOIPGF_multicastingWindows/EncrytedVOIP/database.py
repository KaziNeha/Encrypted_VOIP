# LOGS Database:

import sqlite3

class database:
    def __init__(self):
        try:
            self.conn = sqlite3.connect('GoSecure.db')
            print("Database connected")
        except:
            print ("Error")
        try:
            self.conn.execute("""CREATE TABLE Logs  
            ( Sr_no INTEGER PRIMARY KEY AUTOINCREMENT ,
            ID INT ,
            TIME VARCHAR(20),
             secs VARCHAR(20))
            """)
            print ("Created table for Logs")

            self.conn.execute("""CREATE TABLE directory  
                        ( Sr_no INTEGER PRIMARY KEY AUTOINCREMENT ,
                        ID INT UNIQUE,
                        IP_add VARCHAR(20) )
                        """)
            print ("Table created for Directories")
        except Exception as e:
            print(e)

    def insertIntoLogs(self, id, tim, sec):
        try:
            self.conn.execute("INSERT INTO LOGS(ID, TIME, secs) VALUES (?,?,? )", (id, tim, sec))
            self.conn.commit()
            print ("RECORDS INSERTED")
        except Exception as e:
            print(e)



    def getDataFromLogs(self):

        try:
            res = self.conn.execute("SELECT * FROM LOGS")
            for i in res:
                print(i)

        except Exception as e:
            print(e)


    def insertIntoDirectory(self, id, ip):
        try:
            self.conn.execute("INSERT INTO directory(ID, IP_add) VALUES (?,? )", (id, ip))
            self.conn.commit()
            print ("RECORDS INSERTED")
        except Exception as e:
            print(e)

    def getRecieverIP(self, id):
        try:
            res = self.conn.execute('''SELECT IP_add FROM directory WHERE ID = ?''', (id,))
            for i in res:
                ipr = i[0]
                print(ipr)
            return ipr
            print("Done")
        except Exception as e:
            print(e)

    def updateUserIP(self,ip,id):
        try:
            self.conn.execute("UPDATE directory SET IP_add = ? WHERE ID = ? ", (ip,id))
        except Exception as e:
            print(e)



    def connectionclose(self):
        self.conn.close()

if __name__ == '__main__':
    db = database()
    db.insertIntoDirectory(101, '192.168.1.101')
    db.insertIntoDirectory(103, '192.168.1.103')

    db.insertIntoLogs(9819,'21:00', '1:00')
    db.getDataFromLogs()
    db.getRecieverIP(9819)
    db.getRecieverIP(9820)
    db.connectionclose()