
import mysql.connector

cnx = mysql.connector.connect(
    user = 'root', 
    password = 'password',
    host = '127.0.0.1',
    database = 'MUSEUM')

cur = cnx.cursor()

# login
cur.execute('use museum')
cur.execute('SELECT * FROM ACCOUNTS') # execute query to get all users
ACCOUNTS = cur.fetchall() # list of users (tuples)

print(' Museum Database. Please login below:')
status = True

while status == True:
    print("If you are a guest, please enter 'none' for username and password.")
    username = input('Username: ')
    password = input('Password: ')

    # simultaneously check if user exists and their account type
    if (username, password, 'admin') in ACCOUNTS: # if user is admin
        choice = input('Please select an option:\n1. Add User\n2. Edit User\n3. Block User\n4. Modify Database\n')
        
        if choice == '1': # add users
            insert_user = ("insert into accounts"
                           "values (%s, %s, %s)")
            user_data = input('Please enter the Username, Password, and Account Type (admin, data entry, end) separated by a comma:')
            user_data = tuple(str(x) for x in user_data.split(","))
            cur.execute(insert_user, user_data)
            cnx.commit()

        elif choice == '2': # edit users
            username1 = str(input('Please enter the currnt username that would like to update: '))
            up_username = str(input('Enter the updated username: '))
            up_password = str(input('Enter the updated password: '))
            up_acc_type = str(input('Enter your updated account type (admin, data entry, end): '))

            cur.execute('''
                        UPDATE accounts
                        SET username = %s, pass = %s, role = %s
                        WHERE username = %s
                        ''', up_username, up_password, up_acc_type , username1)
            cnx.commit()

        elif choice == '3': # block users
            del_user = str(input('Please enter the username of the user you wish to block from the database: '))
            cur.execute(''' 
                        DELETE FROM accounts
                        WHERE username = %s
                        ''', del_user)
            cnx.commit()

        elif choice == '4': # change database
            table = input('Please enter the name of the table you would like to modify: ')
            modify = input('If you would like to modify an attribute of a table, please enter 1.\nIf you would like to modify table constraints, please enter 2.\n')
            
            if modify == '1': # modify attribute in table
                cur.execute(''' 
                            ALTER TABLE %s
                            ADD 
                            ''')

            
            attributes = 
    elif (username, password, 'data entry') in users: # if user is data entry type
        # add information tuples (info meets contraints)

        # modify existing information in database

    elif (username, password, 'guest') in users: # if user is end type


    else: # user is not valid
        print('Username or password are incorrect.')
        if input('Enter 1 to exit: ') == 1:
            print('Thank you for using the Museum Database.')
            status = False


cnx.close()

