# Author : Snehashish Laksar
# Date   : 13-04-2022
# This file is a command line application

# Importing necessary modules
import json
import os
from pathlib import Path
from prettytable import PrettyTable
from getpass import getpass as gp

global current_user
current_user = ""

if not os.path.exists("path.json"):
    with open('path.json', 'w') as file:
        json.dump({
            'path':''
        }, file)
    raise Exception("edit path.json")
    
with open("path.json", "r") as file:
    path3 = json.load(file)['path']

path2 = os.path.join(path3, "data")
path = path2 + "/data.json"

if not os.path.exists(path2):
    os.mkdir(path2)
    with open(path, 'w') as file:
        json.dump({}, file)
    
def fecthAllData():
    data  = None
    with open(path, "r") as file:
        data = json.load(file)

    return data

def checkUserExists(username):
    data  = fecthAllData()
    usernames = data.keys()

    if username in usernames:
        return True
    return False


def addUser(username, password):
    data = fecthAllData()

    if checkUserExists(username) == False:
        with open(path, "w") as fp:
            data[username] = {"data": {}, "password":password}
            json.dump(data, fp, indent=4)
            return 200
    elif checkUserExists(username):
        raise KeyError("User Already Exists")

def fetchUserSpecefic(username):
    data = fecthAllData()

    if checkUserExists(username):
        return data[username]
    else:
        raise KeyError("User Does not Exist")

def checkSiteExists(username, sitename):
    data = fecthAllData()

    if checkUserExists(username):
        for i in data[username]["data"]:
            if i.lower()  == sitename.lower():
                return True
            else:
                return False

    else:
        raise KeyError("User does not exist")


def fetchUserPassword(username, sitename):
    data = fecthAllData()

    if checkUserExists(username):
        result = None
        try:
            result = checkSiteExists(username, sitename)
            if result:
                for i in data[username]["data"]:
                    if sitename in i or i in sitename:
                        print(data[username]["data"][i])
                        return data[username]["data"][i]

                    else:
                        return "Not Found"

            else:
                raise Exception("Site Does not exist")

        except KeyError:
            return {"error":404}

def addPassword(username, pw, email, name, sitename):
    data = fecthAllData()

    if checkUserExists(username):
        print("User tick")
        if not checkSiteExists(username, sitename):
            values = {
                "sitename":sitename,
                "sitepassword":pw,
                "siteusername":name
            }
            data[username]["data"][sitename] = {}
            data[username]["data"][sitename][email] = values

            with open(path, "w") as fp:
                json.dump(data, fp, indent =4) 
            
            
        else:
            values = {
                "sitename":sitename,
                "sitepassword":pw,
                "siteusername":name
            }
            data[username]["data"][sitename][email] = values

            with open(path, "w") as fp:
                json.dump(data, fp, indent =4) 
            

    
    else:   
        raise KeyError("User does not exist")

def checkSitesWithThisEmail(username,email):
    data = fecthAllData()
    result = []
    if checkUserExists(username):

        for i in data[username]["data"]:
            dicts = data[username]['data'][i]
            for j in dicts:
                if j == email:
                    result.append({
                        "email":email,
                        "sitename":dicts[j]["sitename"],
                        "siteusername":dicts[j]["siteusername"],
                        "sitepassword":dicts[j]["sitepassword"]
                        
                    })  


        table  = PrettyTable(["Email", "Name of Site", "username used", "password"])
        for i in result:
            table.add_row([i["email"], i["sitename"], i["siteusername"], i["sitepassword"]])

        return table
    else:
        raise Exception("User does not exist")

def delteSite(username, sitename):
    data = fecthAllData()[username]
    for i in data["data"]:
        if i == sitename:
            del data["data"][i]
            break

    with open(path, "w") as fp:
        json.dump(data, fp,)

def askToCreateUser():
    
    while True:

        print("-----------SETTING UP NEW USER-----------------")
        username = input("set the master username: ")
        password = gp("enter the master password for the account: ")

        if checkUserExists(username):
            print("Sorry username already taken.Please Try Again")

        else:
            addUser(username, password)
            current_user = username
            break


def askForNewPassword():

    print("------ADDING NEW PASSWORD---------")
    username = current_user

    if username == "":
        pass
    else:
        while True:
            sitename = input("enter the site's name: ")
            email  = input("enter the email you used to sign up: ")
            siteusername = input("enter the username that you created for the site: ")
            password = gp("enter the password you used for this site: ")

            if "" in (sitename, email, siteusername, password):
                print("please do not give empty values")

            else:
                addPassword(username, password, email, siteusername, sitename)
                print("Password successfully aded to the database")
                break


def login(user):
    
    print("------------LOGIN AUTHORIZATION----------------")
    while True:
        if user == "":
            username = input("Please enter your username: ")
            password = gp("Please enter your password: ")

            data = fecthAllData()
            if data[username]["password"] == password:
                global current_user
                current_user = username
                break
            else:
                print("Incorrect credentials Please try again!")


def getAllUserData():
    
    if current_user == "":
        login()
    username = current_user

    data = fecthAllData()
    table = PrettyTable(["Username", "Site", "Email", "Username Used", "Password"])

    for i in data[username]["data"]:
        site = i
        for j in data[username]["data"][i]:
            email = j
            name = data[username]["data"][i][j]["siteusername"]
            password = data[username]["data"][i][j]["sitepassword"]

            table.add_row([username,site, email, name, password ])

    print(table)


def getUserPassword():
    
    
    if current_user == "":
        login()

    username = current_user
    data = fetchUserSpecefic(username)["data"]
    sitename = input("Enter the site whose password you are looking for: ")

    table = PrettyTable([ "Site", "Email", "Username Used", "Password"])
    for i in data:
        if i.lower() == sitename.lower():
            site = i
            for j in data[i]:
                email = j
                name = data[i][j]["siteusername"]
                password = data[i][j]["sitepassword"]

                table.add_row([site, email, name, password])

    print(table)


def getRegisteredSitesWithThisEmail():
    username = current_user
    email = input("enter the email adress: ")

    result = checkSitesWithThisEmail(username, email)

    print(result)



def main():
    
    def help():
        print("""
    Commands:
    -> Type ALL to get all the data related to a user
    -> Type VIEW SITE to get a password for a site
    -> Type EMAIL to see all the passwords linked to an email account
    -> Type ADD to add a new password
    -> type help to see all commands again
    -> type exit to exit the application
    """)

    functions = {
        "ALL":getAllUserData,
        "VIEW SITE":getUserPassword,
        "EMAIL":getRegisteredSitesWithThisEmail,
        "ADD":askForNewPassword,
        "help":help,
    }

    data = fecthAllData()
    if data == {}:
        askToCreateUser()
    if current_user == "":
        login(current_user)

    help()
    while True:
        inp = input(f"[{current_user}@passwordManager]:~$ ")

        for i in functions:
            if i == inp:
                functions[i]()

main()
