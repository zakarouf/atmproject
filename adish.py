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
        cursorA.execute("CREATE DATABASE medicals")
    except:
        pass

    cursorA.execute("USE medicals")  # uses database named 'medicals'

    try:
        # Creating a table in 'medicals' datable named 'Sales'
        cursorA.execute("CREATE TABLE Sales\
            (Sno INT NOT NULL,\
            Buyer CHAR(64),\
            Product CHAR(64),\
            Price DECIMAL(15,5),\
            PRIMARY KEY (Sno)\
            );")
    except:
        pass

# Inserting Data

def InsertData():
    Buyer = input  ("Buyer   : ")
    Product = input("Product : ")
    Price = input  ("Price   : ")

    cursorA.execute("SELECT * FROM Sales ORDER BY Sno DESC LIMIT 1")
    row = cursorA.fetchone()
    try:
        Sno = int(row[0]) + 1
    except TypeError:
        Sno = 1;

    string = "{A}, \"{B}\", \"{C}\", {D}".format(A=Sno, B=Buyer, C=Product, D=Price)

    cursorA.execute("INSERT INTO Sales(`Sno`, `Buyer`, `Product`, `Price`) VALUES\
        ({value})\
        ".format(value=string))

    print("\n[ DATA INSERT ]\n")

    db.commit()

# Showing Data

def showData(tab):
    cursorA.execute("SELECT * FROM {name}".format(name=tab))
    data_tmp = cursorA.fetchall()
    print(tabulate(data_tmp, headers=cursorA.column_names), '\n')

# Delete Data
def deleteData():
    Sno = input("Enter Sno")
    cursorA.execute("DELETE FROM Sales WHERE Sno={A}".format(A=Sno))
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
            showData("Sales")
        if op == '3':
            deleteData()
        if op == '0':
            quit = 1    # Exit the program


main_menu()



#Output
#Hello Adish