import pandas as pd

# Load CSV files
country_df = pd.read_csv("csv-files/Country.csv")
country_profile_df = pd.read_csv("csv-files/CountryProfile.csv")
country_vaccine_df = pd.read_csv("csv-files/CountryVaccine.csv")
infect_status_df = pd.read_csv("csv-files/InfectStatus.csv")
new_infect_df = pd.read_csv("csv-files/NewInfect.csv")
region_df = pd.read_csv("csv-files/Region.csv")
vaccine_df = pd.read_csv("csv-files/Vaccine.csv")


def show_menu():
    print("\n--- Global COVID-19 Surveillance Database ---")
    print("1. Countries with highest vaccination usage")
    print("2. Region summary statistics")
    print("3. Countries above new infection threshold")
    print("4. Compare two countries weekly infections")
    print("5. Vaccine statistics")
    print("6. Exit")


def feature1():
    min_usage = float(input("Enter minimum vaccine usage percent: "))

    merged = country_df.merge(country_vaccine_df, on="CON_ID") \
                       .merge(vaccine_df, on="VAC_ID") \
                       .merge(country_profile_df, on="CON_ID", how="left")

    result = merged[merged["USAGE_PERC"] >= min_usage][
        ["Country", "VAC_NAME", "USAGE_PERC", "DOSE_AMOUNT", "GDP"]
    ].sort_values(by="USAGE_PERC", ascending=False)

    print("\nCountries with High Vaccine Usage")
    print(result.to_string(index=False))


def feature2():
    region_name = input("Enter WHO Region: ")

    merged = region_df.merge(country_df, on="REG_ID") \
                      .merge(country_profile_df, on="CON_ID", how="left")

    result = merged[merged["WHO_Region"].str.lower() == region_name.lower()]

    if result.empty:
        print("\nNo matching region found.")
        return

    print("\nRegion Summary")
    print(f"WHO Region: {region_name}")
    print(f"Number of Countries: {result['CON_ID'].nunique()}")
    print(f"Average Population: {result['Population'].mean():.2f}")
    print(f"Average GDP: {result['GDP'].mean():.2f}")


def feature3():
    threshold = float(input("Enter minimum new confirmed infections: "))

    merged = country_df.merge(new_infect_df, on="CON_ID")

    result = merged[merged["NEW_CONFIRM"] >= threshold][
        ["Country", "WEEK_START", "NEW_CONFIRM", "NEW_DEATH", "NEW_RECOV", "WEEKLY_INC"]
    ].sort_values(by="NEW_CONFIRM", ascending=False)

    print("\nCountries Above Infection Threshold")
    print(result.to_string(index=False))


def feature4():
    country1 = input("Enter first country: ")
    country2 = input("Enter second country: ")

    merged = country_df.merge(new_infect_df, on="CON_ID")

    c1 = merged[merged["Country"].str.lower() == country1.lower()][
        ["WEEK_START", "Country", "NEW_CONFIRM"]
    ].rename(columns={
        "Country": "Country_1",
        "NEW_CONFIRM": "Country_1_New_Confirm"
    })

    c2 = merged[merged["Country"].str.lower() == country2.lower()][
        ["WEEK_START", "Country", "NEW_CONFIRM"]
    ].rename(columns={
        "Country": "Country_2",
        "NEW_CONFIRM": "Country_2_New_Confirm"
    })

    comparison = c1.merge(c2, on="WEEK_START")

    if comparison.empty:
        print("\nNo matching weekly data found for those countries.")
        return

    print("\nCountry Comparison")
    print(comparison.to_string(index=False))


def feature5():
    merged = vaccine_df.merge(country_vaccine_df, on="VAC_ID")

    result = merged.groupby("VAC_NAME").agg(
        country_count=("CON_ID", "count"),
        avg_usage_percent=("USAGE_PERC", "mean"),
        avg_dose_amount=("DOSE_AMOUNT", "mean")
    ).reset_index().sort_values(by="avg_usage_percent", ascending=False)

    print("\nVaccine Statistics")
    print(result.to_string(index=False))


while True:
    show_menu()
    choice = input("Choose option: ")

    if choice == "1":
        feature1()
    elif choice == "2":
        feature2()
    elif choice == "3":
        feature3()
    elif choice == "4":
        feature4()
    elif choice == "5":
        feature5()
    elif choice == "6":
        print("Goodbye.")
        break
    else:
        print("Invalid choice. Try again.")