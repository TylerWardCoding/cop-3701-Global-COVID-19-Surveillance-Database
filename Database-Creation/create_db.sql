BEGIN
  FOR c IN (SELECT table_name FROM user_tables) LOOP
    EXECUTE IMMEDIATE ('DROP TABLE "' || c.table_name || '" CASCADE CONSTRAINTS');
  END LOOP;
END;
/


create Table Country (
  CON_ID integer,
  Country varchar(40),
  Population int,
  ISO_CODE varchar(40),
  REG_ID int
);

ALTER TABLE country
ADD CONSTRAINT PK_country
PRIMARY KEY (CON_ID);


create Table CountryProfile(
  CON_ID int,
  CEOworld_Healthcare_Index float,
  GDP int,
  Vaccine_Policy varchar(40)
);

ALTER TABLE CountryProfile
ADD CONSTRAINT FK_CountryProfile
FOREIGN KEY (CON_ID)
REFERENCES Country(CON_ID);


create Table Region(
  REG_ID int,
  WHO_Region varchar(40)
);

ALTER TABLE Region
ADD CONSTRAINT PK_Region
PRIMARY KEY (REG_ID);

ALTER TABLE Country
ADD CONSTRAINT FK_Country
FOREIGN KEY (REG_ID)
REFERENCES REGIOn(REG_ID);


CREATE Table InfectStatus(
  CON_ID int,
  REPORT_DATE date,
  Confirmed int,
  Deaths int,
  Recovered int,
  PRIMARY KEY (CON_ID, REPORT_DATE)
);

/*
ALTER TABLE InfectStatus
ADD CONSTRAINT PK_Infect_status
PRIMARY KEY (CON_ID);

ALTER TABLE InfectStatus
ADD CONSTRAINT PK_Infect_status_two
PRIMARY KEY (REPORT_DATE);
*/

ALTER TABLE InfectStatus
ADD CONSTRAINT FK_InfectStatus
FOREIGN KEY (CON_ID)
REFERENCES COUNTRY(CON_ID);


CREATE Table NewInfect(
  CON_ID int,
  WEEK_START date,
  NEW_CONFIRM int,
  NEW_DEATH int,
  NEW_RECOV int,
  WEEKLY_INC int
);

ALTER TABLE NewInfect
ADD CONSTRAINT PK_New_con
PRIMARY KEY (CON_ID, WEEK_START);

ALTER TABLE NewInfect
ADD CONSTRAINT FK_NewInfect
FOREIGN KEY (CON_ID)
REFERENCES COUNTRY(CON_ID);


CREATE Table Vaccine(
  VAC_ID int,
  VAC_NAME varchar(40)
);

ALTER TABLE Vaccine
ADD CONSTRAINT PK_Vaccine
PRIMARY KEY (VAC_ID);


CREATE Table CountryVaccine(
  CON_ID int,
  VAC_ID int,
  DOSE_AMOUNT int,
  VAC_START_DAY date not null,
  USAGE_PERC int,
  Primary Key (CON_ID, VAC_ID)
);

ALTER TABLE CountryVaccine
ADD CONSTRAINT FK_CountryVaccine_con
FOREIGN KEY (CON_ID)
REFERENCES COUNTRY(CON_ID);

ALTER TABLE CountryVaccine
ADD CONSTRAINT FK_CountryVaccine_vac
FOREIGN KEY (VAC_ID)
REFERENCES VACCINE(VAC_ID);
