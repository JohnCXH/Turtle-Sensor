import mysql.connector
import time
import csv

def InsertRecords(id,color,TimeStamp):

    cnx = mysql.connector.connect(user='root',database='turtle')

    column_names = []

    cursor = cnx.cursor()
     

    with open ('Log.csv', newline='') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        for row in csv_reader:
            column_names = row
            break


    filename = "Log.csv"

    row_fields  = [id, color , TimeStamp]

    fields = ["Bounding Box ID" , "Colour Change" , "Time Changed"] 


    cursor.execute('''CREATE TABLE IF NOT EXISTS colour_changes
                 (colour_change VARCHAR(20),
                  time_changed DATETIME,
                  bounding_box_id INTEGER NOT NULL PRIMARY KEY)''')
    cnx.commit()

    cursor.execute("SELECT colour_change FROM colour_changes WHERE bounding_box_id = %s",(id,))
    
    dbcolor = cursor.fetchone()
    
    if(dbcolor == None):

        cursor.execute("INSERT INTO colour_changes (colour_change, time_changed, bounding_box_id) VALUES (%s, %s, %s)",(color,TimeStamp,id))

        if(column_names != fields):
            with open(filename, 'a', encoding='UTF8', newline='') as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow(fields)
                csvwriter.writerow(row_fields)
        else:
            with open(filename, 'a', encoding='UTF8', newline='') as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow(row_fields)

    elif(dbcolor[0] != color):
        
        if(column_names != fields):
            with open(filename, 'a', encoding='UTF8', newline='') as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow(fields)
                csvwriter.writerow(row_fields)
        else:
            with open(filename, 'a', encoding='UTF8', newline='') as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow(row_fields)

        cursor.execute("UPDATE colour_changes SET colour_change  = %s , time_changed = %s WHERE bounding_box_id = %s",(color,TimeStamp,id))
    
    else:

        return

    cnx.commit()
    cursor.close()
    cnx.close()

def SelectRecords(search_query,search_column):

    local_iteration = 0

    cnx = mysql.connector.connect(user='root',database='turtle')
    
    cursor = cnx.cursor()


    cursor.execute('''CREATE TABLE IF NOT EXISTS colour_changes
                 (colour_change VARCHAR(20),
                  time_changed DATETIME,
                  bounding_box_id INTEGER NOT NULL PRIMARY KEY)''')
    cnx.commit()

    if(search_column == 'bounding_box_id'):
        cursor.execute("SELECT * FROM colour_changes WHERE bounding_box_id = %s",(search_query,))
    elif(search_column == 'colour_change'): 
        cursor.execute("SELECT * FROM colour_changes WHERE colour_change LIKE %s",("%"+search_query+"%",))
    elif(search_column == 'time_changed'):
        cursor.execute("SELECT * FROM colour_changes WHERE time_changed LIKE %s",("%"+search_query+"%",))

    results = cursor.fetchall()

    print(results)

    cursor.close()
    cnx.close()

    return results