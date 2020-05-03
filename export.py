import cx_Oracle
from csv import writer

username = 'system'
password = 'databon'
dsn = 'localhost/xe'

connection = cx_Oracle.connect(username, password, dsn)
cursor = connection.cursor()

tables = [
         'Event',
         'EventType',
         'EventSeverity',
         'EventPeriod',
         'Airport',
         'Location',
         'Zipcode',
         'City',
         'Okrug',
         'States'
         ]

try:
    for tbl in tables:
        with open(tbl + '.csv', 'w', newline='') as file:
            query = 'SELECT * FROM ' + tbl
            cursor.execute(query)
            cwriter = writer(file, delimiter=',')

            header = [i[0] for i in cursor.description]
            cwriter.writerow(header)
            row = cursor.fetchone()

            while row:
                cwriter.writerow(row)
                row = cursor.fetchone()
except Exception as e:
        print(f'Error! {e}')
cursor.close()
connection.close()
