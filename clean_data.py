import pandas as pd

pd.set_option("display.max_columns", None)

def convert_height(value):
    if pd.isna(value):
        return None

    value = str(value).strip().lower()

    if value.endswith("cm"):
        return int(value[:-2])

    if "'" in value:
        feet, inches = value.replace('"', "").split("'")
        return round(int(feet) * 30.48 + int(inches) * 2.54)

    return None
    

def convert_numbers(value):
    if pd.isna(value):
        return 0

    value = str(value).strip().replace("€", "").lower()

    if value.endswith("m"):
        return int(float(value[:-1]) * 1_000_000)

    if value.endswith("k"):
        return int(float(value[:-1]) * 1_000)
    return int(value)

def convert_weight(value):
    if pd.isna(value):
        return 0
    if value.endswith("lbs"):
        return int(float(value[:-3])*0.453)
    if value.endswith("kg"):
        return int(value[:-2])


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean the football dataset."""

    # Remove leading/trailing whitespace
    df["Club"] = df["Club"].str.strip()

    # Replace missing profile views with 0
    df["Hits"] = df["Hits"].apply(convert_numbers)

    df["Hits"] = df["Hits"].fillna(0)

#Formatting wage column

    df["Wage"] = df["Wage"].apply(convert_numbers)

#Formatting Value & Release Clause columns 
    df["Value"] = df["Value"].apply(convert_numbers)


    df["Release Clause"] = df["Release Clause"].apply(convert_numbers)

#Formmating metrics cm/kg

    df["Weight"] = df["Weight"].apply(convert_weight)

    df["Height"] = df["Height"].apply(convert_height)

#Rename OVA column, for the future queries using SQL

    df = df.rename(columns={
    "↓OVA": "OVA",
    "↓POT": "POT"
})


    return df


def main():
    df = pd.read_csv("football_data.csv", low_memory=False)
    df = clean_data(df)

    df.to_csv("football_data_clean.csv", index=False)

if __name__ == "__main__":
    main()




