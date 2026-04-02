import oracledb

# --- CONFIGURATION ---
LIB_DIR = r"C:\oraclexe\instantclient_23_0"

# Your Oracle Credentials
DB_USER = "TWARD7760_SCHEMA_0V37J"
DB_PASS = "8BSZT9UAsMFYCUUZFM6350VL1ZHN$G"
DB_DSN = "db.freesql.com:1521/23ai_34ui2"

# Initialize Oracle Client
oracledb.init_oracle_client(lib_dir=LIB_DIR)

# Connect to database
conn = oracledb.connect(user=DB_USER, password=DB_PASS, dsn=DB_DSN)
cursor = conn.cursor()

print("Connected to Oracle Database")

import oracledb
import pandas as pd

# Region Table
region_df = pd.read_csv(f"Region.csv")

for _, row in region_df.iterrows():
    cursor.execute(
        "INSERT INTO Region (REG_ID, WHO_Region) VALUES (:1, :2)",
        [int(row["REG_ID"]), row["WHO_Region"]]
    )

print("Region table loaded")


# Country Table
country_df = pd.read_csv(f"Country.csv")

for _, row in country_df.iterrows():

    cursor.execute(
        """INSERT INTO Country (CON_ID, Country, Population, ISO_CODE, REG_ID) VALUES (:1, :2, :3, :4, :5)""",
        [
            int(row["CON_ID"]),
            row["Country"],
            int(row["Population"]),
            row["ISO_CODE"],
            int(row["REG_ID"])
        ]
    )

print("Country table loaded")


# CountryProfile Table
profile_df = pd.read_csv(f"CountryProfile.csv")

for _, row in profile_df.iterrows():

##GDP has missing values so have to fix that here
    gdp_value = row["GDP"]

    try:
        if pd.isna(gdp_value):
            gdp_value = None
        else:
            gdp_value = int(gdp_value)
    except:
        print("Bad GDP value detected:", gdp_value)
        gdp_value = None

##Healthcare has missing values too so awesome and cool
    healthcare = row["CEOworld_Healthcare_Index"]
    try:
        if pd.isna(healthcare):
            healthcare = None
        else:
            healthcare = float(healthcare)
    except:
        print("Bad healthcare value detected:", healthcare)
        healthcare = None


    cursor.execute(
        """INSERT INTO CountryProfile (CON_ID, CEOworld_Healthcare_Index, GDP, Vaccine_Policy) VALUES (:1, :2, :3, :4)""",
        [
            int(row["CON_ID"]),
            healthcare,
            gdp_value,
            row["Vaccine_Policy"]
        ]
    )

print("CountryProfile table loaded")


# Vaccine Table
vaccine_df = pd.read_csv(f"Vaccine.csv")

for _, row in vaccine_df.iterrows():
    cursor.execute(
        "INSERT INTO Vaccine (VAC_ID, VAC_NAME) VALUES (:1, :2)",
        [int(row["VAC_ID"]), row["VAC_NAME"]]
    )

print("Vaccine table loaded")


# InfectStatus Table
infect_df = pd.read_csv(f"InfectStatus.csv")

for _, row in infect_df.iterrows():
    cursor.execute(
        """INSERT INTO InfectStatus 
        (CON_ID, REPORT_DATE, Confirmed, Deaths, Recovered)
        VALUES (:1, TO_DATE(:2,'MM-DD-YYYY'), :3, :4, :5)""",
        [
            int(row["CON_ID"]),
            row["REPORT_DATE"],
            int(row["Confirmed"]),
            int(row["Deaths"]),
            int(row["Recovered"])
        ]
    )

print("InfectStatus table loaded")


# NewInfect Table
newinfect_df = pd.read_csv(f"NewInfect.csv")

for _, row in newinfect_df.iterrows():
    cursor.execute(
        """INSERT INTO NewInfect
        (CON_ID, WEEK_START, NEW_CONFIRM, NEW_DEATH, NEW_RECOV, WEEKLY_INC)
        VALUES (:1, TO_DATE(:2,'MM-DD-YYYY'), :3, :4, :5, :6)""",
        [
            int(row["CON_ID"]),
            row["WEEK_START"],
            int(row["NEW_CONFIRM"]),
            int(row["NEW_DEATH"]),
            int(row["NEW_RECOV"]),
            int(row["WEEKLY_INC"])
        ]
    )

print("NewInfect table loaded")


# CountryVaccine Table
cv_df = pd.read_csv(f"CountryVaccine.csv")

for _, row in cv_df.iterrows():
    cursor.execute(
        """INSERT INTO CountryVaccine
        (CON_ID, VAC_ID, DOSE_AMOUNT, VAC_START_DAY, USAGE_PERC)
        VALUES (:1, :2, :3, TO_DATE(:4,'MM-DD-YYYY'), :5)""",
        [
            int(row["CON_ID"]),
            int(row["VAC_ID"]),
            int(row["DOSE_AMOUNT"]),
            row["VAC_START_DAY"],
            int(row["USAGE_PERC"])
        ]
    )

print("CountryVaccine table loaded")


# Commit and close
conn.commit()

cursor.close()
conn.close()

print("All CSV data successfully loaded into Oracle!")