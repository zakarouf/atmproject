import mysql.connector as ms
from tabulate import tabulate

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
    "SELECT AcctID, Holder, Balance, ACTIVE FROM accounts AS ac")

def selectone_where(pkey, column_name):
    global cursorA
    cursorA.execute("SELECT AcctID, Holder, Balance FROM accounts WHERE {col}={val}".format(col=column_name, val=pkey))
    print(tabulate(cursorA.fetchall(), headers=cursorA.column_names))

def add_trans_record(acctid, amount, ttype, remark, balance):
    global cursorB
    dbname = "acct"+str(acctid)
    print()
    try:
        cursorB.execute("INSERT INTO {} VALUES (NOW(), %s, %s, %s, %s)".format(dbname), (remark, amount, ttype, balance))
        db.commit()

    except ms.Error as err:
        if err.errno == ms.errorcode.ER_BAD_TABLE_ERROR:
            cursorA.execute("CREATE TABLE `{}`("
            "`DateT` DATETIME,"
            "`Remark` CHAR(64),"
            "`Amount` DECIMAL(15,5),"
            "`Type` CHAR(4),"
            "`Balance` DECIMAL(15,5))".format(dbname))
            db.commit()
            cursorB.execute("INSERT INTO {} VALUES (NOW(), %s, %s, %s, %s)".format(dbname), (remark, amount, ttype, balance))
            db.commit()
        else:
            print("----------\nERROR\n-----------")




def AccountLog():
    global cursorA, cursorB, db

    acctid = int(input("Account Holder ID : "))
    passw = input("Password : ")
    print("Logging In... ", end='')

    cursorA.execute("SELECT * FROM accounts WHERE AcctID={}".format(acctid))
    data = cursorA.fetchone()
    if data[3] == True:
        if passw == data[4]:
            print("Successful")
            while True:

                cursorA.execute("SELECT * FROM accounts WHERE AcctID={}".format(acctid))
                data = cursorA.fetchone()
                print("\nNow Logged In As {name} (ID.{num})".format(name=data[1], num=data[0]))
                print("Balance: ", data[2])

                op = input("\n1. Withdraw\n2. Deposit\n3. Show Transaction History\n4. Change Password\n0. Go Back\n\n>> ")
                if op == '1':
                    amount = int(input("Enter Amount: "))
                    rem = input("Remarks: ")
                    if amount<data[2]:
                        cursorA.execute("UPDATE accounts SET Balance={amt} WHERE AcctID={aid}".format(amt=data[2]-abs(amount), aid=acctid)) 
                    else:
                        print("Insufficient Fund")
                    db.commit()
                    add_trans_record(acctid, abs(amount), "Dr.", rem, data[2]-abs(amount))

                elif op == '2':
                    amount = int(input("Enter Amount: "))
                    rem = input("Remarks: ")

                    cursorA.execute("UPDATE accounts SET Balance={amt} WHERE AcctID={aid}".format(amt=data[2]+abs(amount), aid=acctid)) 
                    db.commit()
                    add_trans_record(acctid, abs(amount), "Cr.", rem, data[2]+abs(amount))

                elif op == '3':
                    try:
                        db_name = "acct"+str(acctid)
                        print("Show Transaction History for {name} (ID.{aid})\n".format(name=data[1], aid=data[0]))
                        cursorB.execute("SELECT * FROM {}".format(db_name))
                        data_tmp = cursorB.fetchall()
                        print(tabulate(data_tmp, headers=cursorB.column_names))
                         

                    except ms.Error as err:
                        if err.errno == ms.errorcode.ER_BAD_TABLE_ERROR:
                            print("No Transaction Recorded Yet")


                elif op == '4':
                    oldpass = input("Enter Old Password: ")
                    newpass = input("Enter New Password: ")
                    if oldpass == data[4]:
                        cursorA.execute("UPDATE accounts SET pass={passw} WHERE AcctID={aid}".format(passw=newpass, aid=acctid))
                    else:
                        print("Wrong Old Password")

                    db.commit()

                elif op == '0':
                    return 0
                cursorA.execute("SELECT * FROM accounts WHERE AcctID={}".format(acctid))
                
                
        else:
            print("\nError: Password Is Wrong")
    else:
        print("Error: Account is Deactivated")
        return -1


def ManAccount():
    global cursorA, db
    mode=""
    while True:
        acctID = input("Select Account Id: ")
        selectone_where(acctID, "AcctID")
        op = input("\n1. Deactivate Account\n2. Activate Account\n3. Delete Account(Permanant)\n0. Go Back\n\n>> ")
        if op == '1':
            mode="Deactivated"
            q = ("Deactivate This Account (Y/n) >> ")
            if q == 'Y':
                cursorA.execute("UPDATE accounts SET ACTIVE=0 WHERE AcctID={}".format(acctID))     
            else:
                mode="Not " + mode

        elif op == '2':
            mode="Activated"
            q = ("Activate This Account (Y/n) >> ")
            if q == 'Y':
                cursorA.execute("UPDATE accounts SET ACTIVE=1 WHERE AcctID={}".format(acctID))
            else:
                mode="Not " + mode

        elif op == '3':
            mode="Deleted"
            q = ("Delete This Account\n WARNING THIS CHANGE IS PERMANANT (Y/n) >> ")
            if q == 'Y':
                cursorA.execute("DELETE FROM accounts WHERE AcctID={}".format(acctID))
            else:
                mode="Not " + mode

        elif op == '0':
            print("Going Back")
            return 0

        db.commit()
        print("Account ", mode)
           
        

def SysAdmin():
    log = input("Password >> ")
    if log == "password":
        cursorA.execute(query)
        while True:
            op = input("\n1. Show All Accounts\n2. Add An New Account\n3. Manipulate Account\n0. Go Back\n\n>> ")
            if op == '1':
                cursorA.execute(query)
                data = cursorA.fetchall()
                print("Showing")
                print(tabulate(data, headers=cursorA.column_names))
            elif op == '2':
                print("Inserting Data")
                name = input("Name of Holder: ")
                bal = int(input("Balance: "))
                passw = input("Set Password: ")
                try:
                    cursorA.execute("SELECT * FROM accounts ORDER BY AcctID DESC LIMIT 1")
                    row = cursorA.fetchone()
                    Aid = int(row[0]) + 1
                    print(Aid)
                    cursorA.execute("INSERT INTO accounts VALUES (%s, %s, %s, %s, %s);", (str(Aid), name, bal, True, passw))
                    db.commit()
                except AttributeError:
                    print("Error")

            elif op == '3':
                ManAccount()

            elif op == '0':
                return 0


def start_menu():
    while (True):
        print(50*'-', "\nChoose a option")
        print("\n1. Login As SysAdmin\n2. Login As Account Holder\n0. Exit\n\n>> ", end='')
        op = input()
        print('-'*50)
        if op == '1':
            SysAdmin()
        elif op == '2':
            AccountLog()
        elif op == '0':
            print("Exiting")
            db.close()
            exit(0)

def initialize_new_database(cursor, database):
    cursor.execute(
        "CREATE TABLE accounts (AcctID INT NOT NULL, Holder CHAR(64), Balance DECIMAL(15,5), ACTIVE BOOLEAN, pass CHAR(16), PRIMARY KEY (AcctID))")

    cursor.execute(
        "INSERT INTO ACCOUNTS (`AcctID`, `Holder`, `Balance`, `ACTIVE`, `pass`) VALUES"
        "(001, \"Marcus S.\", 2000, TRUE, \"p1\"),"
        "(002, \"Jasmine Tagore\", 10000, TRUE, \"p2\"),"
        "(003, \"Rafael K.K\", 50, TRUE, \"p3\")")
    database.commit()
    

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
        print("Database {} does not exists.".format(db_name))

        if err.errno == ms.errorcode.ER_BAD_DB_ERROR:
            query = input("Do You want To Create a New Database? (Y/n) : ")

            if query == 'Y':
                create_new_database(cursorA, db_name)
                
                print("Database {} created successfully.".format(db_name))
                db.database = db_name
                initialize_new_database(cursorA, db)
                return True
            else:
                print("Exiting")
                exit(0)

        else:
            print(err)
            exit(1)

if __name__ == '__main__':
    database_name = "a"  # Name of the database to be connected
    if check_database_exist(database_name) == True:
        print("Connected To " + database_name)
        start_menu()


db.close()
