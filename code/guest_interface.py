import mysql.connector

data = mysql.connector.connect(host='127.0.0.01',
                              port = 3306,
                              user='root',
                              database = 'museum',
                              password='Haider1970')
cur = data.cursor()
selection_string = "" 
user_input = int(input("Display: \n 1 - Art Objects \n 2 - Artists \n 3 - Borrowed Objects \n 4 - Collections Borrowed From \n 5 - Permanent Collection \n 6 - Only Paintings \n 7 - Only Sculptures \n 8 - All Other Art Objects \n 9 - Exhibition Information \n 10 - Limited Artist Information \n 11 - Oldest to Latest Art Objects \n 12 - Art Objects from Same Origin as Artist Leonardo Da Vinci \n 13 - Paintings and Sculptures with Modern Style \n 0 - Quit \n"))
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
    user_input = int(input("Display: \n 1 - Art Objects \n 2 - Artists \n 3 - Borrowed Objects \n 4 - Collections Borrowed From \n 5 - Permanent Collection \n 6 - Only Paintings \n 7 - Only Sculptures \n 8 - All Other Art Objects \n 9 - Exhibition Information \n 10 - Limited Artist Information \n 11 - Oldest to Latest Art Objects \n 12 - Art Objects from Same Origin as Artist Leonardo Da Vinci \n 13 - Paintings and Sculptures with Modern Style \n 0 - Quit \n"))

