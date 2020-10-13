import mysql.connector as ms
import sys

config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'raise_on_warnings': True
}

db = ms.connect(**config)
cursorA = db.cursor(buffered=True)
cursorB = db.cursor(buffered=True)

query = (
    "SELECT AcctID, Holder, Balance, ACTIVE FROM ACCOUNTS AS ac")


def SysAdmin():
    log = input("PassWord >> ")
    if log == "password":
        cursorA.execute(query)

    while(True):
        op = input("\n1. Show All Accounts\n2. Add An New Account\n>> ")
        if op == '1':
            data = cursorB.fetchall()
            print(tabulate(data, headers=cursorB.column_name))


def start_menu():
    while (True):
        print("Choose a option\n", 50*"*")
        print("\n1. Login As SysAdmin\n2. Login As Account Holder\n3. Exit >> ", end='')
        op = input()

        if op == '1':
            SysAdmin()
        elif op == '2':
            # AcctLogin()
        else:
            print("Exiting")
            db.close()
            exit(0)


def create_new_database(cursor, db_name):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(db_name))
    except ms.Error as err:
        print("Failed creating database: {error}".format(error=err))
        exit(1)


def check_database_exist(db_name):
    try:
        cursor.execute("USE {}".format(db_name))
        return True

    except ms.Error as err:
        print("Database {} does not exists.".format(db_name))

        if err.errno == ms.errorcode.ER_BAD_DB_ERROR:
            query = input("Do You want To Create a New Database? (Y/n) : ")

            if query == 'Y':
                create_new_database(cursor, db_name)
                print("Database {} created successfully.".format(db_name))
                db.database = db_name
                return True
            else:
                print("Exiting")
                exit(0)

        else:
            print(err)
            exit(1)


def main():
    database_name = "atm"  # Name of the database to be connected
    if check_database_exist(database_name) == True:
        print("Connected To " + database_name)
        start_menu()


main()
db.close()
