CREATE TABLE airport (
    airportcode  VARCHAR2(64) NOT NULL,
    locationlat  NUMBER(9, 6) NOT NULL,
    locationlng  NUMBER(9, 6) NOT NULL
);

ALTER TABLE airport ADD CONSTRAINT airport_pk PRIMARY KEY ( airportcode );

CREATE TABLE city (
    city    VARCHAR2(64) NOT NULL,
    county  VARCHAR2(64) NOT NULL
);

ALTER TABLE city ADD CONSTRAINT city_pk PRIMARY KEY ( city );

CREATE TABLE event (
    eventid      VARCHAR2(16) NOT NULL,
    airportcode  VARCHAR2(64) NOT NULL,
    starttime    TIMESTAMP NOT NULL,
    endtime      TIMESTAMP NOT NULL,
    severity     VARCHAR2(64) NOT NULL,
    etype        VARCHAR2(64) NOT NULL
);

ALTER TABLE event ADD CONSTRAINT event_pk PRIMARY KEY ( eventid );

CREATE TABLE eventperiod (
    starttime  TIMESTAMP NOT NULL,
    endtime    TIMESTAMP NOT NULL
);

ALTER TABLE eventperiod ADD CONSTRAINT eventperiod_pk PRIMARY KEY ( starttime,
                                                                    endtime );

CREATE TABLE eventseverity (
    severity VARCHAR2(64) NOT NULL
);

ALTER TABLE eventseverity ADD CONSTRAINT eventseverity_pk PRIMARY KEY ( severity );

CREATE TABLE eventtype (
    etype VARCHAR2(64) NOT NULL
);

ALTER TABLE eventtype ADD CONSTRAINT eventtype_pk PRIMARY KEY ( etype );

CREATE TABLE location (
    locationlat  NUMBER(9, 6) NOT NULL,
    locationlng  NUMBER(9, 6) NOT NULL,
    city         VARCHAR2(64) NOT NULL,
    zipcode      NUMBER(5) NOT NULL
);

ALTER TABLE location ADD CONSTRAINT location_pk PRIMARY KEY ( locationlat,
                                                              locationlng );

CREATE TABLE okrug (
    county     VARCHAR2(64) NOT NULL,
    statename  VARCHAR2(64) NOT NULL
);

ALTER TABLE okrug ADD CONSTRAINT okrug_pk PRIMARY KEY ( county );

CREATE TABLE states (
    statename VARCHAR2(64) NOT NULL
);

ALTER TABLE states ADD CONSTRAINT states_pk PRIMARY KEY ( statename );

CREATE TABLE zipcode (
    zipcode NUMBER(5) NOT NULL
);

ALTER TABLE zipcode ADD CONSTRAINT zipcode_pk PRIMARY KEY ( zipcode );

ALTER TABLE airport
    ADD CONSTRAINT airport_location_fk FOREIGN KEY ( locationlat,
                                                     locationlng )
        REFERENCES location ( locationlat,
                              locationlng );

ALTER TABLE city
    ADD CONSTRAINT city_okrug_fk FOREIGN KEY ( county )
        REFERENCES okrug ( county );

ALTER TABLE event
    ADD CONSTRAINT event_airport_fk FOREIGN KEY ( airportcode )
        REFERENCES airport ( airportcode );

ALTER TABLE event
    ADD CONSTRAINT event_eventperiod_fk FOREIGN KEY ( starttime,
                                                      endtime )
        REFERENCES eventperiod ( starttime,
                                 endtime );

ALTER TABLE event
    ADD CONSTRAINT event_eventseverity_fk FOREIGN KEY ( severity )
        REFERENCES eventseverity ( severity );

ALTER TABLE event
    ADD CONSTRAINT event_eventtype_fk FOREIGN KEY ( etype )
        REFERENCES eventtype ( etype );

ALTER TABLE location
    ADD CONSTRAINT location_city_fk FOREIGN KEY ( city )
        REFERENCES city ( city );

ALTER TABLE location
    ADD CONSTRAINT location_zipcode_fk FOREIGN KEY ( zipcode )
        REFERENCES zipcode ( zipcode );

ALTER TABLE okrug
    ADD CONSTRAINT okrug_states_fk FOREIGN KEY ( statename )
        REFERENCES states ( statename );
