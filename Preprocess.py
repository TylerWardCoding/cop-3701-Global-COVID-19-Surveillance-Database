import oracledb
import pandas as pd
import random
from datetime import datetime, timedelta

# --- CONFIGURATION ---
LIB_DIR = r"C:\oraclexe\instantclient_23_0"

# Your Oracle Credentials
DB_USER = "Username"
DB_PASS = "Password"
DB_DSN = "DSN"

# Initialize Oracle Client
oracledb.init_oracle_client(lib_dir=LIB_DIR)

# Connect to database
conn = oracledb.connect(user=DB_USER, password=DB_PASS, dsn=DB_DSN)
cursor = conn.cursor()

print("Connected to Oracle Database")


raw_data = pd.read_csv(r"C:\Users\swimm\Downloads\country_wise_latest.csv")


# 1. Region table
region_df = raw_data[['WHO_Region']].drop_duplicates().reset_index(drop=True)
region_df['REG_ID'] = region_df.index + 1  # Generate unique IDs
region_df = region_df[['REG_ID', 'WHO_Region']]  # Reorder columns
region_df.to_csv("Region.csv", index=False)

print("Region done")

# 2. Country table
country_df = raw_data[['Country', 'Population', 'ISO_CODE', 'WHO_Region']].drop_duplicates()
country_df = country_df.merge(region_df, how='left', left_on='WHO_Region', right_on='WHO_Region')
country_df['CON_ID'] = range(1, len(country_df) + 1)  # Generate unique country IDs
country_df = country_df[['CON_ID', 'Country', 'Population', 'ISO_CODE', 'REG_ID']]
country_df.to_csv("Country.csv", index=False)

print("Country done")

# 3. CountryProfile table
country_profile_df = raw_data[['Country', 'CEOworld_Healthcare_Index', 'GDP', 'Vaccine_Policy']].drop_duplicates()
country_profile_df = country_profile_df.merge(country_df[['CON_ID', 'Country']], on='Country', how='left')
country_profile_df = country_profile_df[['CON_ID', 'CEOworld_Healthcare_Index', 'GDP', 'Vaccine_Policy']]
country_profile_df.to_csv("CountryProfile.csv", index=False)

print("CountryProfile done")

# 4. InfectStatus table
infect_status_df = raw_data[['Country', 'REPORT_DATE', 'Confirmed', 'Deaths', 'Recovered']]
infect_status_df = infect_status_df.merge(country_df[['CON_ID', 'Country']], on='Country', how='left')
infect_status_df = infect_status_df[['CON_ID', 'REPORT_DATE', 'Confirmed', 'Deaths', 'Recovered']]
infect_status_df.to_csv("InfectStatus.csv", index=False)

print("InfectStatus done")

# 5. Vaccine table
vaccine_df = raw_data[['VAC_NAME']].drop_duplicates().reset_index(drop=True)
vaccine_df['VAC_ID'] = vaccine_df.index + 1
vaccine_df = vaccine_df[['VAC_ID', 'VAC_NAME']]
vaccine_df.to_csv("Vaccine.csv", index=False)

print("Vaccine done")

# 6. CountryVaccine table
country_vaccine_df = raw_data[['Country', 'VAC_NAME', 'DOSE_AMOUNT', 'VAC_START_DAY', 'USAGE_PERC']]
country_vaccine_df = country_vaccine_df.merge(country_df[['CON_ID', 'Country']], on='Country', how='left')
country_vaccine_df = country_vaccine_df.merge(vaccine_df[['VAC_ID', 'VAC_NAME']], on='VAC_NAME', how='left')
country_vaccine_df = country_vaccine_df[['CON_ID', 'VAC_ID', 'DOSE_AMOUNT', 'VAC_START_DAY', 'USAGE_PERC']]
country_vaccine_df.to_csv("CountryVaccine.csv", index=False)

print("CountryVaccine done")

# 7. NewInfect Table
New_Infect_df = raw_data[['Country', 'WEEK_START', 'NEW_CONFIRM', 'NEW_DEATH', 'NEW_RECOV', 'WEEKLY_INC']]
New_Infect_df = New_Infect_df.merge(country_df[['CON_ID', 'Country']], on='Country', how='left')
New_Infect_df = New_Infect_df.drop_duplicates(subset=['CON_ID', 'WEEK_START'])
New_Infect_df = New_Infect_df[['CON_ID', 'WEEK_START', 'NEW_CONFIRM', 'NEW_DEATH', 'NEW_RECOV', 'WEEKLY_INC']]
New_Infect_df.to_csv("NewInfect.csv", index=False)


print("All tables processed.")

cursor.close()
conn.close()

print("Oracle connection closed.")