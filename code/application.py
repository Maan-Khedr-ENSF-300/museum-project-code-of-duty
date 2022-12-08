
import mysql.connector
data = mysql.connector.connect(host='127.0.0.01',
                              port = 3306,
                              user='root',
                              database = 'museum',
                              password='Haider1970')
cur = data.cursor()

def modify_users(value1, value2, value3, value4):
    if value2 == value3 == value4 == None:
        statement = f"DELETE FROM ACCOUNTS WHERE username = '{value1}';"
    elif value4 == None:
        statement = f"INSERT INTO ACCOUNTS VALUES ('{value1}', '{value2}', '{value3}');"
    elif value4 != None:
        statement = f"UPDATE ACCOUNTS SET username = '{value1}', pass = '{value2}', role = '{value3}' WHERE username = '{value4}';"
    cur.execute('use museum')
    cur.execute(statement)
    data.commit() 

def search_database(user_input):
    while(user_input != 0):
        if(user_input == 1):
            selection_string = "SELECT * FROM ART_OBJECT"
        elif(user_input == 2):
            selection_string = "SELECT * FROM ARTIST"
        elif(user_input == 3):
            selection_string = "SELECT * FROM BORROWED"
        elif(user_input == 4):
            selection_string = "SELECT * FROM COLLECTION"
        elif(user_input == 5):
            selection_string = "SELECT * FROM PERMANENT_COLLECTION"
        elif(user_input == 6):
            selection_string = "SELECT * FROM PAINTING"
        elif(user_input == 7):
            selection_string = "SELECT * FROM SCULPTURE"
        elif(user_input == 8):
            selection_string = "SELECT * FROM OTHER"
        elif(user_input == 9):
            selection_string = "SELECT * FROM EXHIBITION"
        elif(user_input == 10):  
            selection_string = "SELECT AName, DateBorn, Country_origin FROM ARTIST AS A, ART_OBJECT AS O WHERE A.AName = O.C_AName"
        elif(user_input == 11):  
            selection_string = "SELECT A.ID_no AS 'ID Number', A.Title AS 'Title', A.Yr AS 'Year' FROM ART_OBJECT AS A ORDER BY A.Yr ASC"
        elif(user_input == 12):  
            selection_string =  "SELECT O.Id_no, A.AName, O.Yr FROM  ART_OBJECT AS O, ARTIST AS A WHERE O.C_AName = A.AName AND O.Origin IN(SELECT A.Country_origin FROM  ARTIST AS A WHERE A.AName = 'Leonardo Da Vinci')"
        elif(user_input == 13):  
            selection_string = "SELECT A.Id_No, A.Title FROM ART_OBJECT A WHERE A.Style = 'Modern' AND A.Id_No IN (SELECT AId_No FROM ART_OBJECT A RIGHT JOIN PAINTING P ON A.Id_No = P.AId_No UNION ALL SELECT AId_No FROM ART_OBJECT A RIGHT JOIN SCULPTURE S ON A.Id_No = S.AId_No)"
        elif(user_input == 0):
            break
        
        cur.execute(selection_string)
        myresult = cur.fetchall()
        for x in myresult:
            print(x)
        
        selection_string = "SELECT * FROM"
        user_input = int(input("Please enter the corresponding number for what you would like to be displayed from Museum database: \n 1 - Art Objects \n 2 - Artists \n 3 - Borrowed Objects \n 4 - Collections Borrowed From \n 5 - Permanent Collection \n 6 - Only Paintings \n 7 - Only Sculptures \n 8 - All Other Art Objects \n 9 - Exhibition Information \n 10 - Limited Artist Information \n 11 - Oldest to Latest Art Objects \n 12 - Art Objects from Same Origin as Artist Leonardo Da Vinci \n 13 - Paintings and Sculptures with Modern Style \n 0 - Quit \n"))

# login
cur.execute('use museum')
cur.execute('SELECT * FROM ACCOUNTS') # execute query to get all users
ACCOUNTS = cur.fetchall() # list of users (tuples)

print('\nWelcome to the ENSF300 Museum Database. Please login below:')
exit = '1'

while exit != '0':
    exit = input('Please enter 1 to continue. If you would like to exit the Main Menu, please enter 0.\n')
    if exit == '0':
        break
    
    print("Please enter your username and password.\nIf you are a guest, please enter 'none' for username and password.")
    username = input('Username: ')
    password = input('Password: ')

    # simultaneously check if user exists and their account type
    if (username, password, 'admin') in ACCOUNTS: # if user is admin
        user1 = ''
        user2 = ''
        pw = ''
        role = ''
        choice = input('Please select an option:\n1. Add Users \n2. Edit Users\n3. Block Users\n4. Browse Database\n5. Modify Database\n0. Exit Admin Menu\n')
        while choice != '0':
            if choice == '1': # add users
                insert_user = print("Please complete the SQL INSERT statement:\n INSERT INTO ACCOUNTS VALUES (new username, new password, new role)")
                user1 = input('New Username: ')
                pw = input('New Password: ')
                role = input('New Role: ')
                modify_users(user1, pw, role, None)
                print('User successfully inserted. Returning to Admin menu...')
                choice = input('Please select an option:\n1. Add Users \n2. Edit Users\n3. Block Users\n4. Modify Database\n0. Exit Admin Menu\n')

            elif choice == '2': # edit database
                update_user = print("Please complete the SQL UPDATE statement:\n UPDATE ACCOUNTS SET username = new username, password = new password, role = new role)")
                user1 = input('Existing Username: ')
                user2 = input('New Username: ')
                pw = input('New Password: ')
                role = input('New Role: ')
                modify_users(user2, pw, role, user1)
                print('User successfully inserted. Returning to Admin menu...')
                choice = input('Please select an option:\n1. Add Users \n2. Edit Users\n3. Block Users\n4. Modify Database\n0. Exit Admin Menu\n')

            elif choice == '3': # delete users
                delete_user = print("Please complete the SQL DELETE statement: DELETE FROM ACCOUNTS WHERE Username = Old Username")
                user1 = input('Old Username: ')
                modify_users(user1, None, None, None)
                print('User successfully removed. Returning to Admin menu...')
                choice = input('Please select an option:\n1. Add Users \n2. Edit Users\n3. Block Users\n4. Modify Database\n0. Exit Admin Menu\n')

            elif choice == '4': #search database
                selection_string = ""
                user_input = int(input("Please enter the corresponding number for what you would like to be displayed from Museum database: \n 1 - Art Objects \n 2 - Artists \n 3 - Borrowed Objects \n 4 - Collections Borrowed From \n 5 - Permanent Collection \n 6 - Only Paintings \n 7 - Only Sculptures \n 8 - All Other Art Objects \n 9 - Exhibition Information \n 10 - Limited Artist Information \n 11 - Oldest to Latest Art Objects \n 12 - Art Objects from Same Origin as Artist Leonardo Da Vinci \n 13 - Paintings and Sculptures with Modern Style \n 0 - Quit \n"))
                search_database(user_input)
                choice = input('Please select an option:\n1. Add Users \n2. Edit Users\n3. Block Users\n4. Modify Database\n0. Exit Admin Menu\n')

            elif choice == '5': # modify database
                #admin can modify tuples, can modify constraints, can modify attributes
                table = input('Please enter the name of the table you would like to modify: ')
                modify = input('If you would like to modify an attribute of a table, please enter 1.\nIf you would like to modify table constraints, please enter 2.\n')
                
                if modify == '1': # modify attribute in table
                    cur.execute(''' 
                                ALTER TABLE %s
                                ADD 
                                ''')
                
                #attributes = 
                break
            
    elif (username, password, 'data entry') in ACCOUNTS: # if user is data entry type
        choice = input('Please select an option:\n1. Browse Database\n5. Modify Database\n0. Exit Data Entry Menu\n')
        while choice != '0':
            if choice == '1': #search database
                selection_string = ""
                user_input = int(input("Please enter the corresponding number for what you would like to be displayed from Museum database: \n 1 - Art Objects \n 2 - Artists \n 3 - Borrowed Objects \n 4 - Collections Borrowed From \n 5 - Permanent Collection \n 6 - Only Paintings \n 7 - Only Sculptures \n 8 - All Other Art Objects \n 9 - Exhibition Information \n 10 - Limited Artist Information \n 11 - Oldest to Latest Art Objects \n 12 - Art Objects from Same Origin as Artist Leonardo Da Vinci \n 13 - Paintings and Sculptures with Modern Style \n 0 - Quit \n"))
                search_database(user_input)
                choice = input('Please select an option:\n1. Browse Database\n5. Modify Database\n0. Exit Data Entry Menu\n')
            elif choice == '2': #modify database (can only insert, delete, or update tuples)
                break

    elif (username, password, 'guest') in ACCOUNTS: # if user is end type
        selection_string = "" 
        print('A guest user is limited to only viewing information from the database, they are not allowed to make any modifications.')
        user_input = int(input("Please enter the corresponding number for what you would like to be displayed from Museum database: \n 1 - Art Objects \n 2 - Artists \n 3 - Borrowed Objects \n 4 - Collections Borrowed From \n 5 - Permanent Collection \n 6 - Only Paintings \n 7 - Only Sculptures \n 8 - All Other Art Objects \n 9 - Exhibition Information \n 10 - Limited Artist Information \n 11 - Oldest to Latest Art Objects \n 12 - Art Objects from Same Origin as Artist Leonardo Da Vinci \n 13 - Paintings and Sculptures with Modern Style \n 0 - Quit \n"))
        search_database(user_input)

    else: # user is not valid
        print('Username or password are incorrect.')
        if input('Please enter 1 to exit: ') == 1:
            print('Thank you for using the Museum Database.')
            exit = 1

data.close()