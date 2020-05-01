import cx_Oracle

username = 'system'
password = 'databon'
dsn = 'localhost/xe'

connection = cx_Oracle.connect(username, password, dsn)
cursor = connection.cursor()

# Запит 1 - вивести аеропорти та кількість зафіксованих ними явищ
query = '''
SELECT airportcode, COUNT(*) AS occured_events
FROM workshop_queries
GROUP BY airportcode
'''

print('Запит 1')
cursor.execute(query)
row = cursor.fetchone()
while row:
    print(row)
    row = cursor.fetchone()
print('\n\n')

# Запит 2 - для кожного погодного явища вивести його
# відсоток відносно усієї кількості зафіксованих явищ
query = '''
SELECT eType AS event, ROUND(COUNT(eType) * 100 / (SELECT COUNT(*) FROM Event), 2)
AS percentage
FROM workshop_queries
GROUP BY eType
'''

print('Запит 2')
cursor.execute(query)
row = cursor.fetchone()
while row:
    print(row)
    row = cursor.fetchone()
print('\n\n')

# Запит 3 - вивести динаміку дощів по місяцях за 2016 рік
query = '''
SELECT month, COUNT(*) AS times_occured
FROM (
    SELECT EXTRACT(MONTH FROM starttime) AS month
    FROM workshop_queries
    WHERE EXTRACT(YEAR FROM starttime) = '2016' AND EXTRACT(YEAR FROM endtime) = '2016' AND TRIM(eType)='Rain'
)
GROUP BY month
ORDER BY month
'''

print('Запит 3')
cursor.execute(query)
row = cursor.fetchone()
while row:
    print (row)
    row = cursor.fetchone()

cursor.close()
connection.close()
