import sqlite3 as sql
import os
from pathlib import Path


path = os.path.join(Path(__file__).parent, "data")

def startup():

    if not os.path.exists(path + "/authdata.db"):
        with open(path + "/authdata.db", 'w') as file:
            pass

    if not os.path.exists(path + "/userdata.db"):
        with open(path + "/userdata.db", 'w') as file:
            pass

authconn = sql.connect(path + "/authdata.db", check_same_thread=False)
dataconn = sql.connect(path + "/userdata.db", check_same_thread=False)
authcursor = authconn.cursor()
datacursor = dataconn.cursor()


def init_auth_table():
    query = """
    CREATE TABLE IF NOT EXISTS AUTHDATA(
        username VARCHAR,
        password VARCHAR
    );
    """
    authcursor.execute(query)
    authconn.commit()

def listAllAuthData():
    query = """SELECT * FROM AUTHDATA"""

    authcursor.execute(query)
    ans = authcursor.fetchall()
    return ans

def addUser(username, password):
    query = f"""INSERT INTO AUTHDATA(username, password) VALUES(?, ?)"""
    authcursor.execute(query, (username, password))
    authconn.commit()

    query = """CREATE TABLE IF NOT EXISTS {}(sitename VARCHAR, email VARCHAR, password VARCHAR, username VARCHAR);""".format(username)
    datacursor.execute(query)
    dataconn.commit()

    return listAllAuthData()

def selectiveUsername(username):
    query = """SELECT * FROM AUTHDATA WHERE username =:username """
    authcursor.execute(query, {'username':username})
    return authcursor.fetchall()

def fetchAllUserdata(username):
    datacursor.execute('''SELECT * FROM {}'''.format(username))
    return datacursor.fetchall()

def fetchUserDataSite(username, sitename):
    datacursor.execute('''SELECT * FROM {} WHERE sitename = {}'''.format(username, sitename))
    return datacursor.fetchall()

def addSite(username, sitename, email, password, site_username):
    query = f"INSERT INTO {username}(sitename, email, password, username) VALUES(?,?,?,?)"
    datacursor.execute(query, (sitename, email, password, site_username))
    dataconn.commit()

    return fetchAllUserdata(username)

def correct_login(username, password):
    
    if selectiveUsername(username) != []:
        if selectiveUsername(username)[0][0] == username and selectiveUsername(username)[0][0] == password:
            
            return username, password

        else:
            return "error"
    else:
        pass
    
def convertUserDataToJson(username):
    data = fetchAllUserdata(username)
    ans = []
    for i in data:
        ans.append({
            'sitename':i[0],
            'email':i[1],
            'password':i[2],
            'username':i[3],
        })
    return ans

def deletesite(username, site):
    query = f"DELETE FROM {username} WHERE sitename =:site"
    datacursor.execute(query, {'site': site})
    dataconn.commit()

def deleteUser(username):
    query = f"DELETE FROM AUTHDATA WHERE username =:username"
    authcursor.execute(query, {'username' : username})
    authconn.commit()

    query = f"DROP TABLE {username}"
    datacursor.execute(query)
    dataconn.commit()

    
startup()
init_auth_table()
