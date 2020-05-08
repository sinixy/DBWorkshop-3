'''
УВАГА
Даний скрипт імпортує всі 5 млн записів із .csv файлу, що займає дуже багато часу. Для перевірки краще запускати kaggle_import
_first40000rows.py - імпорт лише перших 40000 записів'''
import cx_Oracle
from csv import reader
import re

username = 'system'
password = 'databon'
dsn = 'localhost/xe'

connection = cx_Oracle.connect(username, password, dsn)
cursor = connection.cursor()

# Для заведення timestamp у форматі 2016-01-07 замість 2016-JAN-07 (формат за замовчуванням)
cursor.execute("""ALTER SESSION SET nls_timestamp_format = 'YYYY-MM-DD HH24:MI:SS.FF'""")

# Допоміжні функції для валідації
def isFloat(num):
	regex = '^[+-]?[0-9]+\.[0-9]+$'
	if re.search(regex, num):
		return True
	return False
def isZipcode(zipcode):
	regex = '^[0-9]{4,5}$'
	if re.search(regex, zipcode):
		return True
	return False

with open('US_WeatherEvents_2016-2019.csv') as file:
	reader = reader(file, delimiter=',')
	header = next(reader)
	rowCnt = 1
	# Створюємо списки для перевірки вже записаних даних
	typeLst, severityLst, airportLst, locationLst, periodLst, cityLst, countyLst, stateLst, zipLst = [[] for i in range(9)]
	try:
		for row in reader:
			# Отримуємо необхідні дані
			eventId, eType, severity, startTime,\
			endTime, airportCode, locationLat, locationLng,\
			city, county, state, zipcode = [row[i].strip() for i in range(13) if i != 5]

			# Оброблюемо числові дані
			if isFloat(locationLat):
				locationLat = float(locationLat)
			else:
				# Встановлюєм значення за замовчуванням 0.1
				locationLat = 0.1
			if isFloat(locationLng):
				locationLng = float(locationLng)
			else:
				locationLng = 0.1
			if isZipcode(zipcode):
				zipcode = int(zipcode)
			else:
				zipcode = 111

			location = (locationLat, locationLng)
			period = (startTime, endTime)

			# Перевіряємо, чи не були дані вже занесені в таблиці
			# Також відстежуємо можливу відсутність даних
			if eType not in typeLst:
				typeLst.append(eType)
				if not eType:
					eType = 'Undefined Type'
				query = '''INSERT INTO EventType (eType) VALUES (:eType)'''
				cursor.execute(query, eType=eType)

			if severity not in severityLst:
				severityLst.append(severity)
				if not severity:
					severity = 'Undefined Type'
				query = '''INSERT INTO EventSeverity (severity) VALUES (:severity)'''
				cursor.execute(query, severity=severity)

			if period not in periodLst:
				periodLst.append(period)
				if not startTime:
					startTime = '2000-01-01 22:00:00'
				if not endTime:
					endTime = '2000-01-01 23:00:00'
				query = '''INSERT INTO EventPeriod (starttime, endtime) VALUES (:starttime, :endtime)'''
				cursor.execute(query, starttime=startTime, endtime=endTime)

			if state not in stateLst:
				stateLst.append(state)
				if not state:
					state = 'Undefined state'
				query = '''INSERT INTO States (statename) VALUES (:state)'''
				cursor.execute(query, state=state)

			if county not in countyLst:
				countyLst.append(county)
				if not county:
					county = 'Undefined county'
				query = '''INSERT INTO Okrug (county, statename) VALUES (:county, :state)'''
				cursor.execute(query, county=county, state=state)

			if city not in cityLst:
				cityLst.append(city)
				if not city:
					city = 'Undefined city'
				query = '''INSERT INTO City (city, county) VALUES (:city, :county)'''
				cursor.execute(query, city=city, county=county)

			if zipcode not in zipLst:
				zipLst.append(zipcode)
				query = '''INSERT INTO ZipCode (zipcode) VALUES (:zipcode)'''
				cursor.execute(query, zipcode=zipcode)

			if location not in locationLst:
				locationLst.append(location)
				query = '''INSERT INTO Location (locationlat, locationlng, city, zipcode)
				VALUES (:locationlat, :locationlng, :city, :zipcode)'''
				cursor.execute(query, locationlat=locationLat, locationlng=locationLng, city=city, zipcode=zipcode)

			if airportCode not in airportLst:
				airportLst.append(airportCode)
				if not airportCode:
					airportCode = 'Undefined code'
				query = '''INSERT INTO Airport (airportcode, locationlat, locationlng)
				VALUES (:airportcode, :locationlat, :locationlng)'''
				cursor.execute(query, airportcode=airportCode, locationlat=locationLat, locationlng=locationLng)

			query = '''INSERT INTO Event (eventId, airportCode, startTime, endTime, severity, eType)
			VALUES (:eventId, :airportCode, :startTime, :endTime, :severity, :eType)'''
			cursor.execute(query,
				eventId=eventId,
				airportCode=airportCode,
				startTime=startTime,
				endTime=endTime,
				severity=severity,
				eType=eType)
			
			rowCnt += 1
	except Exception as e:
		print(f'Error! {e}\nLine {rowCnt}')

connection.commit()
cursor.close()
connection.close()
