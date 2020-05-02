-- Для заведення timestamp у форматі 2016-01-07 замість 2016-JAN-07 (формат за замовчуванням)
ALTER SESSION SET nls_timestamp_format = 'YYYY-MM-DD HH24:MI:SS.FF';

DECLARE
    row_cnt INT := 10;
BEGIN
    INSERT INTO EventType (eType) VALUES ('Rain');
    INSERT INTO EventSeverity (severity) VALUES ('Light');
    INSERT INTO EventPeriod (starttime, endtime) VALUES ('2016-01-07 04:14:00', '2016-01-07 04:54:00');
    INSERT INTO ZipCode (zipcode) VALUES (81149);
    INSERT INTO States (statename) VALUES ('C0');
    INSERT INTO Okrug (county, statename) VALUES ('Saguache', 'C0');
    INSERT INTO City (city, county) VALUES ('Saguache', 'Saguache');
    INSERT INTO Location (locationlat, locationlng, city, zipcode) VALUES (38.0972, -106.1689, 'Saguache', 81149);
    
    FOR i IN 1..row_cnt
    LOOP
        INSERT INTO Airport (airportcode, locationlat, locationlng)
        VALUES ('K0' || i || 'V', 38.0972, -106.1689);
    END LOOP;
    
    
    FOR i IN 1..row_cnt
    LOOP
        INSERT INTO Event (eventid, airportcode, starttime, endtime, eType, severity)
        VALUES ('W-' || i, 'K0' || i || 'V', '2016-01-07 04:14:00', '2016-01-07 04:54:00', 'Rain', 'Light');
    END LOOP;
END;
