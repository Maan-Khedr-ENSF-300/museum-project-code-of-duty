
import mysql.connector 
user = input('please enter a username for SQL connection (ex: root): ')
password = input("please enter your connection's password: ")
port = input('please enter your port number (ex: 3306): ')
host = input('please enter your host number (ex: 127.0.0.01): ')

data = mysql.connector.connect(host=f'{host}',
                              port = port,
                              user=f'{user}',
                              database = 'museum',
                              password=f'{password}')

cur = data.cursor()

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

def display_table(col, rows):
    print(f"Current information in table\n")
    for i in range(len(col)):
        print(col[i], end='\t') #change this to trace length of string 
    print()
    print(120*'-')
    for i in range(len(rows)):
        for x in range(len(rows[i])):
            print(rows[i][x], end='\t') #change this to trace length of string 
        print()
    print()

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
                        if modify == '1': #modify attribute in table
                            print('List of All Tables in Museum DataFrame')
                            cur.execute('SHOW TABLES')
                            for table_name in cur:
                                table_name1 = str(table_name).replace('(','').replace(')','').replace('\'','').replace(',','')
                                print(table_name1)
                            table = input('Please enter the name of the table you would like to modify the attributes of: ')
                            cur.execute(f"SELECT * FROM {table}")
                            col_names = cur.column_names
                            rows = cur.fetchall()
                            if table == 'ACCOUNTS':
                                print('You do not have the permission to view this table. Redirecting to Admin Menu...')
                                break
                            display_table(col_names, rows)

                            choice = input('Please enter an option: \n1.Add attribute \n2.Update attribute \n3.Delete attribute\n')
                            
                            if choice == '1': # add attribute 
                                new_cul_name = input('Please enter the name of the new attribute you would like to add to {}\n'.format(table))
                                cul_def = input('Please enter the definition or datatype of your new attribute:\n Example: INT, VARCHAR(10)\n\n')
                                cur.execute(f"ALTER TABLE {table} ADD {new_cul_name} {cul_def}")
                                data.commit()
                                print('Changes successfully made. Returning to Database Management Menu...')

                            elif choice == '2': #Update attribute 
                                new_cul_name = input('Please enter the name of the attribute you would like to update within {}\n'.format(table))
                                cul_def = input('Please enter the new datatype of your attribute:\n Example: INT, VARCHAR(10)\n\n')
                                cur.execute(f"ALTER TABLE {table} MODIFY {new_cul_name} {cul_def}")
                                data.commit()
                                print('Changes successfully made. Returning to Database Management Menu...')

                            elif choice == '3': #Delete attribute 
                                new_cul_name = input('Please enter the name of the attribute you would like to delete within {}\n'.format(table))
                                cur.execute(f"ALTER TABLE {table} DROP COLUMN {new_cul_name}")
                                data.commit()
                                print('Changes successfully made. Returning to Database Management Menu...')
                            
                            modify = input('Please select what you would like to do with a table:\n1. Modify Table Attributes\n2. Modify Table Constraints\n3. Modify Table Tuples\n0. Exit Database Management Menu\n')

                        elif modify == '2': #modify constraint in table
                            print('List of All Tables in Museum DataFrame')
                            cur.execute('SHOW TABLES')
                            for table_name in cur:
                                table_name1 = str(table_name).replace('(','').replace(')','').replace('\'','').replace(',','')
                                print(table_name1)
                            table = input('Please enter the name of the table you would like to modify the constraints of: ')
                            cur.execute(f"SELECT * FROM {table}")
                            col_names = cur.column_names
                            rows = cur.fetchall()
                            if table == 'ACCOUNTS':
                                print('You do not have the permission to view this table. Redirecting to Admin Menu...')
                                break
                            display_table(col_names, rows)
                            
                            choice = input('Please enter the number of your modification choice:\n1.Rename a constraint\n2.Add a unique constraint\n3.Add a primary constraint\n4.Delete a constraint\n')
                            
                            if choice == '1': # rename constraint
                                old_const = input('Please enter the name of the constraint you would like to change: ')
                                new_const = input('Please enter your new constraint name: ')
                                cur.execute(f"ALTER TABLE {table} RENAME CONSTRAINT {old_const} TO {new_const}")
                                data.commit()
                                print('Changes successfully made. Returning to Database Management Menu...')

                            elif choice == '2': # Add a primary constraint 
                                prim_key = input('Please enter the name of the new primary key: ')
                                attr_prim = input('Please enter the name of the attribute you would like to add this primary key to: ')
                                cur.execute(f"ALTER TABLE {table} ADD CONSTRAINT {prim_key} PRIMARY KEY {attr_prim}")
                                data.commit() 
                                print('Changes successfully made. Returning to Database Management Menu...')                         

                            elif choice == '3': # Add a unique constraint 
                                prim_key = input('Please enter the name of the new unique key: ')
                                attr_prim = input('Please enter the name of the attribute you would like to add this unique key to: ')
                                cur.execute(f"ALTER TABLE {table} ADD CONSTRAINT {prim_key} UNIQUE KEY {attr_prim}")
                                data.commit()

                            elif choice == '4': # Delete a constraint
                                del_const = input('Please enter the name of the constraint you would like to delete: ')
                                cur.execute(f"ALTER TABLE {table} DROP CONSTRAINT {del_const}")
                                data.commit()
                                print('Changes successfully made. Returning to Database Management Menu...')
                            
                            modify = input('Please select what you would like to do with a table:\n1. Modify Table Attributes\n2. Modify Table Constraints\n3. Modify Table Tuples\n0. Exit Database Management Menu\n')

                        elif modify == '3': #modify tuple in table
                            print('List of All Tables in Museum DataFrame')
                            cur.execute('SHOW TABLES')
                            for table_name in cur:
                                table_name1 = str(table_name).replace('(','').replace(')','').replace('\'','').replace(',','')
                                print(table_name1)
                            table = input('Please enter the name of the table from the above list that you would like to modify: ')
                            cur.execute(f"SELECT * FROM {table}")
                            col_names = cur.column_names
                            rows = cur.fetchall()
                            if table == 'ACCOUNTS':
                                print('You do not have the permission to view this table. Redirecting to Admin Menu...')
                                break
                            display_table(col_names, rows)
                            
                            tuple_option = input('Please select what to do with the tuple:\n1. Add a tuple\n2. Modify existing tuple\n3. Delete a tuple\n')
                            if tuple_option == '1': #add tuple
                                insert_table = (f"INSERT INTO {table} (")
                                for attribute in col_names:
                                    insert_table += f'{attribute},'
                                insert_table = insert_table[:-1]
                                insert_table += ') VALUES'
                                
                                table_data = input('Please enter the following attributes, separated by a comma WITHOUT any spaces between commas {}: '.format(col_names))
                                table_data = tuple((str(x) for x in table_data.split(",")))
                                
                                insert_table1 = '('+','.join(table_data) + ')'
                                insert_table1 = insert_table1.replace(",","','").replace("(","('").replace(")","')")
                                insert_table += insert_table1
                                
                                cur.execute(insert_table)
                                data.commit()
                                print('Changes successfully made. Returning to Database Management Menu...')
                                
                            elif tuple_option == '2': #update tuple
                                update_tuple = input('Please enter the UPDATE command using the following syntax: UPDATE table_name SET column1 = value1, column2 = value2, ... WHERE condition\nPlease also be considerate of the following rules:\n- Make sure that the condition references the primary key of the table.\n- Put all variables in quotation marks.\n')
                                cur.execute(update_tuple)
                                data.commit()
                                print('Changes successfully made. Returning to Database Management Menu...')
                                
                            elif tuple_option == '3': #delete tuple
                                delete_tuple = input('Please enter the DELETE command using the following syntax: DELETE FROM table_name WHERE condition\nPlease also be considerate of the following rules:\n- Make sure that the condition references the primary key of the table.\n- Put all variables in quotation marks.\n')
                                cur.execute(delete_tuple)
                                data.commit()
                                print('Changes successfully made. Returning to Database Management Menu...')
                                
                            else:
                                print('Incorrect command entered.')
                            
                            modify = input('Please select what you would like to do with a table:\n1. Modify Table Attributes\n2. Modify Table Constraints\n3. Modify Table Tuples\n0. Exit Database Management Menu\n')
                    choice = input('Please select an option:\n1. Add Users \n2. Edit Users\n3. Block Users\n4. Modify Database\n0. Exit Admin Menu\n')

        elif (username, password, 'data entry') in ACCOUNTS: # if user is data entry type
            choice = input('Please select an option:\n1. Browse Database\n2. Modify Database Tuples\n0. Exit Data Entry Menu\n')
            while choice != '0':
                if choice == '1': #search database
                    selection_string = ""
                    user_input = int(input("Please enter the corresponding number for what you would like to be displayed from Museum database: \n 1 - Art Objects \n 2 - Artists \n 3 - Borrowed Objects \n 4 - Collections Borrowed From \n 5 - Permanent Collection \n 6 - Only Paintings \n 7 - Only Sculptures \n 8 - All Other Art Objects \n 9 - Exhibition Information \n 10 - Limited Artist Information \n 11 - Oldest to Latest Art Objects \n 12 - Art Objects from Same Origin as Artist Leonardo Da Vinci \n 13 - Paintings and Sculptures with Modern Style \n 0 - Quit \n"))
                    search_database(user_input)
                    choice = input('Please select an option:\n1. Browse Database\n2. Modify Database Tuples\n0. Exit Data Entry Menu\n')
                
                elif choice == '2': #modify database (can only insert, delete, or update tuples)
                    print('List of All Tables in Museum DataFrame')
                    cur.execute('SHOW TABLES')
                    for table_name in cur:
                        table_name1 = str(table_name).replace('(','').replace(')','').replace('\'','').replace(',','')
                        print(table_name1)
                    table = input('Please enter the name of the table from the above list that you would like to modify: ')
                    cur.execute(f"SELECT * FROM {table}")
                    col_names = cur.column_names
                    rows = cur.fetchall()
                    if table == 'ACCOUNTS':
                                print('You do not have the permission to view this table. Redirecting to Data Entry Menu...')
                                break
                    display_table(col_names, rows)
                    
                    tuple_option = input('Please select what to do with the tuple:\n1. Add a tuple\n2. Modify existing tuple\n3. Delete a tuple\n')
                    if tuple_option == '1': #add tuple
                        insert_table = (f"INSERT INTO {table} (")
                        for attribute in col_names:
                            insert_table += f'{attribute},'
                        insert_table = insert_table[:-1]
                        insert_table += ') VALUES'
                        
                        table_data = input('Please enter the following attributes, separated by a comma WITHOUT any spaces between commas {}: '.format(col_names))
                        table_data = tuple((str(x) for x in table_data.split(",")))
                        
                        insert_table1 = '('+','.join(table_data) + ')'
                        insert_table1 = insert_table1.replace(",","','").replace("(","('").replace(")","')")
                        insert_table += insert_table1
                        
                        cur.execute(insert_table)
                        data.commit()
                        print('Changes successfully made. Returning to Data Entry User Menu...')
                        
                    elif tuple_option == '2': #update tuple
                        update_tuple = input('Please enter the UPDATE command using the following syntax: UPDATE table_name SET column1 = value1, column2 = value2, ... WHERE condition\nPlease also be considerate of the following rules:\n- Make sure that the condition references the primary key of the table.\n- Put all variables in quotation marks.\n')
                        cur.execute(update_tuple)
                        data.commit()
                        print('Changes successfully made. Returning to Data Entry User Menu...')
                        
                    elif tuple_option == '3': #delete tuple
                        delete_tuple = input('Please enter the DELETE command using the following syntax: DELETE FROM table_name WHERE condition\nPlease also be considerate of the following rules:\n- Make sure that the condition references the primary key of the table.\n- Put all variables in quotation marks.\n')
                        cur.execute(delete_tuple)
                        data.commit()
                        print('Changes successfully made. Returning to Data Entry User Menu...')
                        
                    else:
                        print('Incorrect command entered.')
                    
                    choice = input('Please select an option:\n1. Browse Database\n2. Modify Database Tuples\n0. Exit Data Entry Menu\n')

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