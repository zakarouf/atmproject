import mysql.connector as ms
from tabulate import tabulate  #  showing data in tables

config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'raise_on_warnings': True
}

db = ms.connect(**config)

cursorA = db.cursor(buffered=True)

def sql_init():
    try:
        cursorA.execute("CREATE DATABASE library")
    except:
        pass

    cursorA.execute("USE library")  # uses database named 'library'

    try:
        # Creating a table in 'library' datable named 'Lenders'
        cursorA.execute("CREATE TABLE Lenders\
            (Slno INT NOT NULL,\
            Name CHAR(64),\
            LenderID INT NOT NULL,\
            Book CHAR(64),\
            DateT DATETIME,\
            PRIMARY KEY (Slno)\
            );")
    except:
        pass


# Showing Data
def showData(tab):
    cursorA.execute("SELECT * FROM {name}".format(name=tab))
    data_tmp = cursorA.fetchall()
    print(tabulate(data_tmp, headers=cursorA.column_names), '\n')

# Delete Data
def deleteData():
    Slno = input("Enter Slno")
    cursorA.execute("DELETE FROM Lenders WHERE Slno={A}".format(A=Slno))
    db.commit()

# Inserting Data
def InsertData():
    Name = input  ("Lender Name   : ")
    Book = input    ("Book          : ")
    LenderID = input("LenderID      : ")

    cursorA.execute("SELECT * FROM Lenders ORDER BY Slno DESC LIMIT 1")
    row = cursorA.fetchone()
    try:
        Slno = int(row[0]) + 1
    except TypeError:
        Slno = 1;

    string = "{A}, \"{B}\", {D} , \"{C}\", NOW()".format(A=Slno, B=Name, C=Book, D=LenderID)

    cursorA.execute("INSERT INTO Lenders (`Slno`, `Name`, `LenderID`, `Book`, DateT) VALUES\
        ({value})\
        ".format(value=string))

    print("\n[ DATA INSERT ]\n")

    db.commit()

def main_menu():
    sql_init()
    quit = 0
    while quit == 0:
        print("Option:\n\
            1. Insert Data\n\
            2. Show Data\n\
            3. Delete Data\n\
            0. Quit\n\
            ")
        op = input()
        if op == '1':
            InsertData()
        if op == '2':
            showData("Lenders")
        if op == '3':
            deleteData()
        if op == '0':
            quit = 1    # Exit the program


main_menu()