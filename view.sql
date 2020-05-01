CREATE VIEW workshop_queries AS
    SELECT eType,
        airport.airportcode,
        starttime,
        endtime
    FROM Event
    JOIN Airport ON event.airportcode = airport.airportcode;
