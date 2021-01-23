#SMS PROECT
import sys
import mysql.connector as ms
import random
from tabulate import tabulate

config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'raise_on_warnings': True
}

messagefolder = "message/"
db = ms.connect(**config)
cursorA = db.cursor(buffered=True)


def showTableDetails(cursor, columns, tableName):
    cursor.execute("SELECT {col} FROM {tab};".format(col=columns, tab=tableName))
    data = cursor.fetchall()
    print(tabulate(data, headers=cursor.column_names))

def getOrsetTotalMesageSet(getOrset, num, Slno):
    global cursorA, db
    r = ""
    if getOrset == "get":
        cursorA.execute("SELECT TotalMessages FROM Contacts ORDER BY Slno DESC LIMIT 1;")
        row = cursorA.fetchone()
        r = int(row[0]) + 1
        return r

    elif getOrset == "set":
        cursorA.execute("UPDATE Contacts SET TotalMessages={N} WHERE Slno={S};".format(N = num, S = Slno))
        db.commit()
        return 0

    return r

# Add Contact
def addContact(Name, Number):
    global cursorA, db
    cursorA.execute("SELECT * FROM Contacts ORDER BY Slno DESC LIMIT 1;")
    row = cursorA.fetchone()
    Sno = 1
    try:
        Sno = int(row[0]) + 1
    except TypeError:
        Sno = 1;

    string = "{A}, \"{B}\", \"{C}\"".format(A=Sno, B=Name, C=Number)

    cursorA.execute("INSERT INTO Contacts(`Slno`, `Name`, `PhNumber`) VALUES\
        ({value});\
        ".format(value=string))

    db.commit()

    getOrsetTotalMesageSet("set", 0, Sno)

    print("[ CONTACT ADDED ]")

# Delete Data
def deleteContact():
    global cursorA, db
    Slno = input("Enter Slno")
    cursorA.execute("DELETE FROM Sales WHERE Sno={A};".format(A=Slno))
    getOrsetTotalMesageSet("set", 0, Slno)
    db.commit()

def editContact(Slno):
    global cursorA, db
    op = input("Change (N)ame / (C)ontact Number: \n==> ")
    if op == 'N':
        new_name = input("New Name\n==> ")
        cursorA.execute("UPDATE Contacts SET `Name`='{N}' WHERE Slno={S};".format(N = new_name, S = Slno))
        db.commit()

    elif op == 'C':
        new_num = int(input("New Contact Number\n==> "))
        cursorA.execute("UPDATE Contacts SET `PhNumber`={N} WHERE Slno={S};".format(N = new_num, S = Slno))
        db.commit()

def viewMessage(Slno):
    global cursorA
    msgnum = 0

    cursorA.execute("SELECT TotalMessages FROM Contacts ORDER BY Slno DESC LIMIT 1;")
    msgnum = input("Input Message Number (Max : {})\n==> ".format(int(cursorA.fetchone())[0]))

    print("Message Number: ", msgnum)
    with open(messagefolder + str(h) + "_" + str(getOrsetTotalMesageSet("get",0, h)+1), "w") as file:
        print(file.writelines())


def composeMessage():
    cursorA.execute('SELECT Slno, Name, PhNumber From Contacts;')
    showTableDetails(cursorA, "Slno, Name, PhNumber", "Contacts")

    h=int(input('Enter the Slno of the Reciever \n==> '))
    cursorA.execute('SELECT PhNumber FROM Contacts WHERE Slno={};'.format(h))

    print("Write Message \n(Press Ctrl+d To Send)")

    with open(messagefolder + str(h) + "_" + str(getOrsetTotalMesageSet("get",0, h)+1), "w") as file:
        data = sys.stdin.readlines()
        file.writelines(data)
        getOrsetTotalMesageSet("set", (getOrsetTotalMesageSet("get",0, h)+1), h)

    print("MESSAGE SENT [{}]".format((getOrsetTotalMesageSet("get",0, h))))


def option():
    global cursorA
    print("Select Option ")
    quit = 0
    while quit == 0:
        opt = input('1. View Contacts \n2. Compose Message \n3. View inbox \n4. View recent message \n5. Add Contact\n6. Delete Contact\n7. Edit Contact\n0. Exit\n==> ')
        if opt == '1':
            print(20*'-')
            showTableDetails(cursorA, "`Name`, `PhNumber`", "Contacts")
            a=input ('Press enter to continue \n==> ')

        elif opt == '2':
            print(20*'-')
            composeMessage()

        elif opt == '3':
            g=random.randrange(0,15)
            print(20*'-')
            print('You have',g,'Unread messages')
            print(20*'-')

        elif opt == '4':
            slno = int(input("Enter Slno.\n==> "))
            viewMessage(slno)
            print(20*'-')

        elif opt == '5':
            print(20*'-')
            Name = input("Enter Name \n==> ")
            Num = input("Enter Number \n==> ")
            addContact(Name, Num)
            print(20*'-')

        elif opt == '6':
            deleteContact()

        elif opt == '7':
            showTableDetails(cursorA, "Slno, Name, PhNumber", "Contacts")
            editContact(input("Enter Slno\n==> "))

        elif opt == '0':
            quit = 1

        


def initialize_new_database(cursor, database):
    cursor.execute(
        "CREATE TABLE Contacts (Slno INT NOT NULL, Name CHAR(64), PhNumber CHAR(12), TotalMessages INT ,PRIMARY KEY (Slno))")

    database.commit()

    cursor.execute(
        "INSERT INTO Contacts (`Slno`,`Name`,`PhNumber`) VALUES"
        "(1, \"Akhil\" ,\"9633457812\"),"
        "(2, \"Aromal\",\"9657816349\"),"
        "(3, \"Sharan\",\"9876145986\"),"
        "(4, \"Chris\" ,\"9534876879\"),"
        "(5, \"Amal\"  ,\"9657813469\"),"
        "(6, \"Adsish\",\"9756481249\"),"
        "(7, \"Suraj\" ,\"9123478562\"),"
        "(8, \"Mridhun\",\"7356984512\"),"
        "(9, \"Anandhu\",\"7356941248\"),"
        "(10,\"Rahul\" ,\"7356214893\"),"
        "(11,\"Shuu\"  ,\"7356512158\"),"
        "(12,\"Suresh\",\"7356982136\")")
    database.commit()
    for i in range(1, 13):
        getOrsetTotalMesageSet("set", 0, i)

def create_new_database(cursor, db_name):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(db_name))
    except ms.Error as err:
        print("Failed creating database: {error}".format(error=err))
        exit(1)

def check_database_exist(db_name):
    global cursorA, db
    try:
        cursorA.execute("USE {}".format(db_name))
        return True

    except ms.Error as err:
        
        if err.errno == ms.errorcode.ER_BAD_DB_ERROR:
            print("Database {} does not exists.".format(db_name))
            query = input("Do You want To Create a New Database? (Y/n) : ")

            if query == 'Y':
                create_new_database(cursorA, db_name)
                
                print("Database {} created successfully.".format(db_name))
                cursorA.execute("USE {}".format(db_name))
                initialize_new_database(cursorA, db)
                return True
            else:
                print("Exiting")
                exit(0)

        else:
            print(err)
            exit(1)

#__main__
if __name__ == '__main__':
    databaseName = "akhil"

    if check_database_exist(databaseName) == True:
        a=input ('Press enter to continue \n==> ')
        if a==""or a==' ':
            option()
