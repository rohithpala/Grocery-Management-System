from sqlite3 import connect
from re import match, search
from os import _exit as exit, system, name as _name

conn = connect("gms.db") # establishing connection with the database
cur = conn.cursor() # creating a cursor

# declarations
role, username, password, name, gender, email = "", "", "", "", "", ""
uid, phone = 0, 0

# closing the cursor and connection objects
def closeAll():
    cur.close()
    conn.close()


# validations
# username validation
def validateUsername(username):
    error = ""
    if len(username) < 4:
        error += "Make sure your username is at lest 4 letters\n"
    if search('[a-z]', username) is None:
        error += "Make sure your username has a lowercase letter in it\n"
    return error

# password validation
def validatePassword(password):
    error = ""
    if len(password) < 8:
        error += "Make sure your password is at lest 8 letters\n"
    if search('[a-z]',password) is None: 
        error += "Make sure your password has a lowercase letter in it\n"
    if search('[A-Z]',password) is None: 
        error += "Make sure your password has a uppercase letter in it\n"
    if search('[0-9]',password) is None:
        error += "Make sure your password has a number in it\n"
    if search('[!#@?+_=.*]', password) is None:
        error += "Make sure your password has a special character in it\n"
    return error

# email validation
def validateEmail(email):
    return match('\w+@\w+\.\w+', email) is not None

# phone number validation
def validatePhoneNumber(phone):
    return match('[6-9][0-9]{9}', phone) is not None

# authentication
def login():
    global role, uid, username, password, name, gender, email, phone
    try:
        username = input("Username: ")
        password = input("Password: ")
        cur.execute("select * from {} where username='{}' and password='{}'".format(role, username, password))
        record = cur.fetchone()
        if len(record) == 0:
            print("You don't have an Admin Account. Please SignUp first")
            return False
        else:
            uid, name, gender, email, phone = record[0], record[3], record[4], record[5], record[6]
            print("\nWelcome", name, "\n")
            return True
    except:
        return False

def signUp():
    global role, uid, username, password, name, gender, email, phone, name
    try:
        while True:
            username = input("Username: ")
            error = validateUsername(username)
            if error == "":
                if cur.execute("select * from {} where username='{}'".format(role, username)).fetchone() == None:
                    while True:
                        password = input("Set Password: ")
                        error = validatePassword(password)
                        if error == "":
                            name = input("Name: ")
                            gender = input("Gender [M/F]: ")
                            while True:
                                email = input("Email ID: ")
                                if not validateEmail(email):
                                    print("Type a Valid Email Address")
                                else:
                                    break
                            
                            while True:
                                phone = input("Mobile Number: ")
                                if not validatePhoneNumber(phone):
                                    print("Type a Valid Phone Number")
                                else:
                                    break

                            cur.execute("insert into {} (username, password, name, gender, email, phone) values('{}', '{}', '{}', '{}', '{}', '{}')".format(role, username, password, name, gender, email, phone))
                            conn.commit()
                            uid= cur.execute("select {}id from {} where username='{}'".format(role[0], role, username)).fetchone()[0]
                            print("\nAccount Created Successfully\n")
                            return True
                        else:
                            print(error)
                            inp = input("Wanna try with a new password [Y/N]: ").lower()
                            if inp == "n":
                                return False
                else:
                    print(role[0].upper() + role[1:len(role)] + " already exists with this username\nPlease change the username and try again\n")
                    return signUp()
            else:
                print(error)
    except Exception as e:
        return False

# settings
def updateDetails(option):
    global role, username, password, name, gender, email, phone
    if option == 1:
            newUsername = input("Enter New Username: ")
            if newUsername == "":
                updateDetails(1)
            elif newUsername == username:
                print("New Username cannot be Same as old one")
            else:
                error = validateUsername(newUsername)
                if error == "":
                    cur.execute("select * from {} where username='{}'".format(role, newUsername))
                    if cur.fetchone() == None:
                        cur.execute("update {} set username='{}' where username='{}'".format(role, newUsername, username))
                        conn.commit()
                        username = newUsername
                        print("Username Updated")
                    else:
                        print("Username already taken")
                        if input("Wanna try Again [Y/N]? ").lower() == 'y':
                            updateDetails(1)
                else:
                    print(error)
    elif option == 2:
        try:
            newPassword = input("Enter New Password: ")
            error = validatePassword(newPassword)
            if error == "":
                cur.execute("update {} set password='{}' where username='{}'".format(role, newPassword, username))
                conn.commit()
                password = newPassword
                print("Password Changed")
            else:
                print(error)
        except:
            print("Password couldn't be changed due to some Error")
    elif option == 3:
        newName = input("Enter New Name: ")
        if newName == name:
            print("New Name is same as Old Name")
        else:
            cur.execute("update {} set name='{}' where username='{}'".format(role, newName, username))
            conn.commit()
            name = newName
            print("Name Updated")
    elif option == 4:
        cur.execute("update {} set gender='{}' where username='{}'".format(role, input("Enter Gender: "), username))
        conn.commit()
        print("Gender Updated")
    elif option == 5:
        newEmail = input("Enter New Email ID: ")
        if validateEmail(newEmail):
            cur.execute("select * from {} where email='{}'".format(role, newEmail))
            if cur.fetchone() == None:
                cur.execute("update {} set email='{}' where username='{}'".format(role, newEmail, username))
                conn.commit()
                email = newEmail
                print("Email ID Updated")
            else:
                print(role , "already exists with this Email ID")
        else:
            print("Type a Valid Email Address")
    elif option == 6:
        newPhone = input("Enter New Phone Number: ")
        if validatePhoneNumber(newPhone):
            cur.execute("select * from {} where phone='{}'".format(role, newPhone))
            if cur.fetchone() == None:
                cur.execute("update {} set phone='{}' where username='{}'".format(role, newPhone, username))
                conn.commit()
                phone = newPhone
                print("Phone Number Updated")
        else:
            print("Type a Valid Phone Number")

# delete a customer record
def deleteCustomerRecord():
    username = input("Enter Username of the Customer: ")
    cur.execute("select * from customer where username='{}'".format(username))
    record = cur.fetchone()
    if len(record) == 0:
        print("The Customer with the given Detail doesn't exist")
    else:
        print(record[0], record[1], record[3], record[4], record[5], record[6])
        inp = input("This is irreversible. Are you Sure [Y/N]? ").lower()
        if inp == 'y':
            try:
                cur.execute("delete from customer where username='{}'".format(username))
                conn.commit()
                print("Account associated with username", username, "has been deleted Successfully")
            except:
                print("Account not Deleted due to some Error")
        else:
            print("OK !!!")

# show all customer details
def fetchAllCustomerDetails():
    print("ID  Username" + " "*13 + "Name" + " "*17 + "Gender  Email ID" + " "*8 + "Phone No." + " "*4)
    records = cur.execute("select * from customer").fetchall()
    for record in records:
        # formatting problem
        print("{} {} {} {} {} {}".format(record[0], record[1], record[3], record[4], record[5], record[6]))

# logout
def logout():
    global role, username, password, name, gender, email, phone
    role, username, password, name, gender, email = "", "", "", "", "", ""
    uid, phone = 0, 0
    system('cls' if _name == 'nt' else 'clear')
    main()

# groceries and orders
def showGroceries():
    print("ID  Name" + " "*15 + "Weight(in KGs)  Price(in /-)" + " "*20 + "Description" + " "*25 + "Type" + " "*9 + "MFG" + " "*10 + "EXP" + " "*5 + "Stock Left")
    groceries = cur.execute("select * from grocery").fetchall()
    for grocery in groceries:
        print("{:<3} {:<20} {:<15} {:<13} {:<50} {:<10} {:<12} {:<12} {}".format(grocery[0], grocery[1], grocery[2], grocery[3], grocery[4], grocery[5], grocery[6], grocery[7], grocery[8]))
    return grocery[8]

# previous orders placed by customers
def showPreviousOrders():
    global uid
    cart = cur.execute("select g.gid, g.name, g.weight, g.price, g.description, g.type, g.mfg, g.exp, g.stock_remaining, c.quantity from grocery g, cart c where g.gid=c.gid and cid='{}'".format(uid)).fetchall()
    if len(cart) == 0:
        print("\nYou have no Previous orders\n")
    else:
        print("\nYour Previous Orders:\nID  Name" + " "*15 + "Weight(in KGs)  Price(in /-)" + " "*23 + "Description" + " "*25 + "Type" + " "*9 + "MFG" + " "*10 + "EXP" + " "*5 + "Quantity")
        for item in cart:
            print("{:<3} {:<20} {:<16} {:<15} {:<50} {:<10} {:<12} {:<12} {}".format(item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7], item[9]))

# lets user place an order
def placeOrder():
    global uid
    showGroceries()
    gid = input("Enter the ID of the Grocery: ")
    cur.execute("select stock_remaining from grocery where gid='{}'".format(gid))
    stockLeft = cur.fetchone()[0]
    print(stockLeft)
    while True:
        quantity = int(input("Enter Quantity of the Grocery Required: "))
        if quantity > stockLeft:
            print("Quantity Demanded is Greater than the Stock Left")
        else:
            try:
                cur.execute("insert into cart values('{}', '{}', '{}')".format(uid, gid, quantity))
                conn.commit()
                stockLeft -= quantity
                cur.execute("update grocery set stock_remaining='{}' where gid='{}'".format(stockLeft, gid))
                conn.commit()
                print("\nOrder Placed\n")
            except Exception as e:
                print("Order didn't get placed due to some error\n", e)
            break


# display menu with available options based on role
def displayMenu():
    global role
    try:
        print("1) Edit Username\n2) Edit Password\n3) Edit Name\n4) Edit Gender\n5) Edit Email ID\n6) Edit Mobile Number")
        if role == "admin":
            print("7) Terminate Someone's Account\n8) Get all Customer Details\n9) Logout\n10) Exit\n")
            while True:
                try:
                    option = int(input('Select an Option: '))
                except ValueError:
                    closeAll()
                    exit(1) 
                if 1 <= option <= 6:
                    updateDetails(option)
                elif option == 7:
                    deleteCustomerRecord()
                elif option == 8:
                    fetchAllCustomerDetails()
                elif option == 9:
                    logout()
                elif option == 10:
                    closeAll()
                    exit(1)
                else:
                    print("Enter Valid Option")
        else:
            print("7) Show Available Groceries\n8) Show Previous Orders\n9) Place Order\n10) Logout\n11) Exit\n")
            while True:
                try:
                    option = int(input('Select an Option: '))
                except ValueError:
                    closeAll()
                    exit(1)
                if 1 <= option <= 6:
                    updateDetails(option)
                elif option == 7:
                    showGroceries()
                elif option == 8:
                    showPreviousOrders()
                elif option == 9:
                    placeOrder()
                elif option == 10:
                    logout()
                elif option == 11:
                    exit(1)
                else:
                    print("Enter Valid Option")
    except:
        closeAll()
        exit(1)

# main function
def main():
    global role
    try:
        while role != "admin" and role != "customer" and role != "a" and role != "c":
            role = input("Continue as Admin/Customer: ").lower()
            
            if role == "a": role = "admin"
            elif role == "c": role = "customer"

            if role == "exit":
                closeAll()
                exit(1)

        success = False
        # prompting for login or signup untill user enters exit or logs in or signs up
        while not success:
            inp = input("Login or SignUp: ").lower()
            if inp == "login":
                success = login()
            elif inp == "signup":
                success = signUp()
            elif inp == "exit":
                closeAll()
                exit(1)
            else:
                print("\nPlease type a valid word (login/signup)\n")

            # if successful login or signup, the menu is displayed
            if success:
                displayMenu()
                closeAll()
                exit(1)
            else: # else we again prompt for authentication
                print("Try Again !!\n")
    except:
        closeAll()
        exit(1)

# calling main function
if __name__ == "__main__":
    main()
