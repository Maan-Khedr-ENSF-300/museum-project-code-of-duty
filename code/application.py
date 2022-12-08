
import mysql.connector
data = mysql.connector.connect(host='127.0.0.01',
                              port = 3306,
                              user='root',
                              database = 'museum',
                              password='Haider1970')
cur = data.cursor()

def list_tables():
    print('List of All Tables in Museum DataFrame')
    cur.execute('SHOW TABLES')
    for table_name in cur:
        table_name1 = str(table_name).replace('(','').replace(')','').replace('\'','').replace(',','')
        print(table_name1)
    table = input('Please enter the name of the table from the above list that you would like to modify: ')
    return table

def modify_users(user1, password, role, user2):
    if password == role == user2 == None:
        statement = f"DELETE FROM ACCOUNTS WHERE username = '{user1}';"
    elif user2 == None:
        statement = f"INSERT INTO ACCOUNTS VALUES ('{user1}', '{password}', '{role}');"
    elif user2 != None:
        statement = f"UPDATE ACCOUNTS SET username = '{user1}', pass = '{password}', role = '{role}' WHERE username = '{user2}';"
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
        print('Thank you for using the Museum Database.')
        break
    
    guest_input = input("Are you a guest user? (Y/N) ")
    if guest_input == 'N':
        print("Please enter your username and password.\n")
        username = input('Username: ')
        password = input('Password: ')

        # simultaneously check if user exists and their account type
        if (username, password, 'admin') in ACCOUNTS: # if user is admin
            user_info = ['','','','']
            choice = input('Please select an option:\n1. Add Users \n2. Edit Users\n3. Remove Users\n4. Browse Database\n5. Modify Database\n0. Exit Admin Menu\n')
            while choice != '0':
                if choice == '1': # add users
                    insert_user = print("Please complete the SQL INSERT statement:\n INSERT INTO ACCOUNTS VALUES (new username, new password, new role)")
                    user_info[0] = input('New Username: ')
                    user_info[1] = input('New Password: ')
                    user_info[2] = input('New Role: ')
                    modify_users(user_info[0], user_info[1], user_info[2], None)
                    print('User successfully inserted. Returning to Admin menu...')
                    choice = input('Please select an option:\n1. Add Users \n2. Edit Users\n3. Remove Users\n4. Modify Database\n0. Exit Admin Menu\n')

                elif choice == '2': # edit users
                    update_user = print("Please complete the SQL UPDATE statement:\n UPDATE ACCOUNTS SET username = new username, password = new password, role = new role)")
                    user_info[0] = input('Existing Username: ')
                    user_info[3] = input('New Username: ')
                    user_info[1] = input('New Password: ')
                    user_info[2] = input('New Role: ')
                    modify_users(user_info[3], user_info[1], user_info[2], user_info[0])
                    print('User successfully inserted. Returning to Admin menu...')
                    choice = input('Please select an option:\n1. Add Users \n2. Edit Users\n3. Remove Users\n4. Modify Database\n0. Exit Admin Menu\n')

                elif choice == '3': # delete users
                    delete_user = print("Please complete the SQL DELETE statement: DELETE FROM ACCOUNTS WHERE Username = Old Username")
                    user_info[0] = input('Old Username: ')
                    modify_users(user_info[0], None, None, None)
                    print('User successfully removed. Returning to Admin menu...')
                    choice = input('Please select an option:\n1. Add Users \n2. Edit Users\n3. Remove Users\n4. Modify Database\n0. Exit Admin Menu\n')

                elif choice == '4': #search database
                    selection_string = ""
                    user_input = int(input("Please enter the corresponding number for what you would like to be displayed from Museum database: \n 1 - Art Objects \n 2 - Artists \n 3 - Borrowed Objects \n 4 - Collections Borrowed From \n 5 - Permanent Collection \n 6 - Only Paintings \n 7 - Only Sculptures \n 8 - All Other Art Objects \n 9 - Exhibition Information \n 10 - Limited Artist Information \n 11 - Oldest to Latest Art Objects \n 12 - Art Objects from Same Origin as Artist Leonardo Da Vinci \n 13 - Paintings and Sculptures with Modern Style \n 0 - Quit \n"))
                    search_database(user_input)
                    choice = input('Please select an option:\n1. Add Users \n2. Edit Users\n3. Block Users\n4. Modify Database\n0. Exit Admin Menu\n')

                elif choice == '5': # modify database
                    #admin can modify tuples, can modify constraints, can modify attributes
                    
                    modify = input('Please select what you would like to do with a table:\n1. Modify Table Attributes\n2. Modify Table Constraints\n3. Modify Table Tuples\n0. Exit Database Management Menu\n')
                    while modify != '0':
                        if modify == '1': # FIXME: SABA modify attribute in table
                            list_tables()
                            table = input('Please enter the name of the table you would like to modify the attributes of: ') #check if table exists
                            choice = input('Please enter an option: \n1.Add attribute \n2.Update attribute \n3.Delete attribute')
                            
                            if choice == '1': # add attribute 
                                new_cul_name = input('Please enter the name of the new attribute you would like to add to {}\n'.format(table))
                                cul_def = input('Please enter the definition or datatype of your new attribute:\n Example: NULL, NOT NULL, varchar(10)\n\n')
                                cur.execute(''' ALTER TABLE %s ADD %s %s''',table, new_cul_name, cul_def)

                            elif choice == '2': #Update attribute 
                                new_cul_name = input('Please enter the name of the attribute you would like to update within {}\n'.format(table))
                                cul_def = input('Please enter the definition or datatype of your new attribute:\n Example: NULL, NOT NULL, varchar(10)\n\n')
                                cur.execute(''' ALTER TABLE %s MODIFY %s %s''',table, new_cul_name, cul_def)

                            elif choice == '3': #Delete attribute 
                                new_cul_name = input('Please enter the name of the attribute you would like to delete within {}\n'.format(table))
                                cur.execute(''' ALTER TABLE %s DROP COLUMN %s''',table, new_cul_name)
                            break

                        elif modify == '2': # FIXME: SABA modify constraint in table
                            list_tables()
                            table = input('Please enter the name of the table you would like to modify the constraints of: ') #check if table exists
                            print('modify constraint in table')
                            break
                        
                        elif modify == '3': # FIXME: ISHA modify tuple in table
                            list_tables()
                            table = input('Please enter the name of the table you would like to modify the tuples of: ') #check if table exists
                            print('modify tuple in table')
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
        
        else: # user is not valid
            print('Username or password are incorrect. You will be redirected to the Main Page.')
            continue
    
    elif guest_input == 'Y': # if user is end type
        selection_string = "" 
        print('A guest user is limited to only viewing information from the database, they are not allowed to make any modifications.')
        user_input = int(input("Please enter the corresponding number for what you would like to be displayed from Museum database: \n 1 - Art Objects \n 2 - Artists \n 3 - Borrowed Objects \n 4 - Collections Borrowed From \n 5 - Permanent Collection \n 6 - Only Paintings \n 7 - Only Sculptures \n 8 - All Other Art Objects \n 9 - Exhibition Information \n 10 - Limited Artist Information \n 11 - Oldest to Latest Art Objects \n 12 - Art Objects from Same Origin as Artist Leonardo Da Vinci \n 13 - Paintings and Sculptures with Modern Style \n 0 - Quit \n"))
        search_database(user_input)
    
    else:
        print("You have entered a value that is not 'Y' or 'N'. You will be redirected to the Main Page.")
        continue

data.close()