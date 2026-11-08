# improt libraries

import pandas as pd         #import data analysis library
from pathlib import Path    # helps python locate files

# 1. Project directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent  # stores location of project folder

# 2. Dataset location
DATA_PATH = PROJECT_ROOT / "data" / "raw" / "pumf_chss.csv"  # stores location of main CSV file

# 3. Load CHSS dataset
df = pd.read_csv(DATA_PATH, low_memory = False)  # reads CSV and creates Dataframe

# 4. Examine dataset
print("CHSS DATASET OVERVIEW")
print("-" * 40)

print("Number of rows:", df.shape[0])       # number of rows
print("Number of columns:", df.shape[1])    # number of columns

print("\nFirst 5 observations:")    
print(df.head().to_string())        # displays first 5 rows

print("\nDataset columns:")
print(df.columns.tolist())      # list all column names

print("\nData types:")
print(df.dtypes.to_string())    # data type of each column


# chosen variables relevant to WellnessIQ
important_variables = [
    "ADM_RNO2",
    "GEOGPRV",
    "DHHGAGE",
    "LON_01",
    "LON_02",
    "LON_03",
    "LONDVSCR",
    "WTS_CM"
]

# check which variables exists
available_variables = [
    col for col in important_variables # goe through every variale in important_variable and keep it if that variable exists in the dataset
    if col in df.columns
]

missing_variables = [
    col for col in important_variables
    if col not in df.columns
]

print("\nAVAILABLE VARIABLES:")
print(available_variables)

print("\nVARIABLES NOT FOUND:")
print(missing_variables)


# Since CHSS uses a complex survey design, we need bootstrap weights.
# bootstraps helps us estimate the statistical uncertainty of population estimates

# load bootstrap weights
BSW_PATH = PROJECT_ROOT / "data" / "raw" / "chss_ecsa_bsw.csv"

bsw = pd.read_csv(BSW_PATH, low_memory = False)

print("\nBOOTSTRAP WEIGHTS DATASET")
print("Number of rows:", bsw.shape[0])
print("Number of columns:", bsw.shape[1])

print("\nFirst 10 column names:")
print(bsw.columns[:10].tolist())

# bootstrap rows: 41550
#bootstrap cols: 1002

# Now we examine loneliness variables

# explore loneliness variables
loneliness_variables = [
    "LON_01",
    "LON_02",
    "LON_03",
    "LONDVSCR"
]

print("\nLONELINESS VARIABLE DISTRIBUTIONS")
print("-" * 40)

for col in loneliness_variables:
    print(f"\nVariable: {col}")
    print(df[col].value_counts(dropna = False).sort_index())
    
# LON_01: how often do you feel that you lack companionship
# LON_02: how often do you feel left out
# LON_03: how often do you feel isolated from others
# LONDVSCR: combined loneliness score

# 1	Hardly ever
# 2	Some of the time
# 3	Often
# 7	Don't know
# 8	Refusal
# 9	Not stated

# handling missing values

import numpy as np

# select bariables relevant to our analysis
columns = [
    "ADM_RNO2",
    "GEOGPRV",
    "DHHGAGE",
    "LON_01",
    "LON_02",
    "LON_03",
    "LONDVSCR",
    "WTS_CM"
]

loneliness_df = df[columns].copy()

# replace non-response codes with missing values
for col in ["LON_01", "LON_02", "LON_03"]:
    loneliness_df[col] = loneliness_df[col].replace({
        7: np.nan,
        8: np.nan,
        9: np.nan
    })

# Replace the invalid score code
loneliness_df["LONDVSCR"] = (
    loneliness_df["LONDVSCR"].replace(99, np.nan)
)

# Examine missing values
print("\nMISSING VALUES AFTER CLEANING")
print(loneliness_df.isna().sum())

# Count respondents with valid loneliness scores
valid_scores = loneliness_df["LONDVSCR"].notna().sum()

print("\nRespondents with valid scores:", valid_scores)
print("Total respondents:", len(loneliness_df))


# explore demographic variables

demographic_variables = [
    "DHHGAGE",
    "GEOGPRV"
]

print("\nDEMOGRAPHIC VARIABLE DISTRIBUTIONS")
print("-" * 40)

for col in demographic_variables:
    print(f"\nVariable: {col}")
    print(
        loneliness_df[col]
        .value_counts(dropna=False)
        .sort_index()
    )


# 10	Newfoundland and Labrador
# 11	Prince Edward Island
# 12	Nova Scotia
# 13	New Brunswick
# 24	Quebec
# 35	Ontario
# 46	Manitoba
# 47	Saskatchewan
# 48	Alberta
# 59	British Columbia

# create a dictionary mapping province codes to names
province_mapping = {
    10: "Newfoundland and Labrador",
    11: "Prince Edward Island",
    12: "Nova Scotia",
    13: "New Brunswick",
    24: "Quebec",
    35: "Ontario",
    46: "Manitoba",
    47: "Saskatchewan",
    48: "Alberta",
    59: "British Columbia"
}

# Create a new column with province names
loneliness_df["province"] = (
    loneliness_df["GEOGPRV"].map(province_mapping)
)

# Display the number of respondents by province
print("\nRESPONDENTS BY PROVINCE")
print(
    loneliness_df["province"]
    .value_counts()
)

# chart with Matplotlib
import matplotlib.pyplot as plt

# Count survey respondents in each province
province_counts = (
    loneliness_df["province"]
    .value_counts()
    .sort_values()
)

# Create a horizontal bar chart
plt.figure(figsize=(10, 6))

province_counts.plot(kind="barh")

plt.title("CHSS Survey Respondents by Province")
plt.xlabel("Number of Respondents")
plt.ylabel("Province")

plt.tight_layout()
plt.show()


# data quality assessment

# check missing values
print("\nDATA QUALITY ASSESSMENT")
print("-" * 40)

# Count missing values in each column
missing_counts = loneliness_df.isna().sum() # .sum() counts missing values

# Calculate the percentage of missing values
missing_percent = (
    loneliness_df.isna().mean() * 100 # isna() identifies missing values
)

# Combine results into one table
missing_summary = pd.DataFrame({
    "Missing Count": missing_counts,
    "Missing %": missing_percent
})

print("\nMISSING VALUES SUMMARY")
print(missing_summary.round(2))


# check for duplicate respondent
duplicate_count = (
    loneliness_df["ADM_RNO2"]
    .duplicated()
    .sum()
)

print("\nDUPLICATE RESPONDENT IDS")
print("Number of duplicates:", duplicate_count)

# Check unique respondents
unique_count = (
    loneliness_df["ADM_RNO2"]
    .nunique()
)

print("Unique respondents:", unique_count)
print("Total rows:", len(loneliness_df))

# values after loneliness cleaning
print("\nVALUE VALIDATION")
print("-" * 40)

for col in ["LON_01", "LON_02", "LON_03"]:
    invalid = (
        loneliness_df[col].notna()
        & ~loneliness_df[col].isin([1, 2, 3])
    )

    print(f"{col}: {invalid.sum()} invalid values")

# LONDVSCR should range from 3 to 9
invalid_scores = (
    loneliness_df["LONDVSCR"].notna()
    & ~loneliness_df["LONDVSCR"].between(3, 9)
)

print(
    "LONDVSCR invalid values:",
    invalid_scores.sum()
)


# check survey sampling weights
print("\nSURVEY WEIGHT VALIDATION")
print("-" * 40)

print("Missing weights:", loneliness_df["WTS_CM"].isna().sum())

print("Zero or negative weights:", (loneliness_df["WTS_CM"] <= 0).sum())

print("\nWeight summary:")
print(loneliness_df["WTS_CM"].describe())

# save the dataset
# Define output directory
OUTPUT_DIR = PROJECT_ROOT / "data" / "processed"

# Create the directory if it does not exist
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Define output file path
OUTPUT_PATH = OUTPUT_DIR / "chss_cleaned.csv"

# Save cleaned DataFrame as CSV
loneliness_df.to_csv(OUTPUT_PATH, index=False)

print("\nPROCESSED DATASET SAVED")
print("File:", OUTPUT_PATH)
print("Rows:", loneliness_df.shape[0])
print("Columns:", loneliness_df.shape[1])