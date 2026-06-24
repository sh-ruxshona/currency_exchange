import pandas as pd
import pyodbc
import logging
import config

logging.basicConfig(
    filename=config.LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(message)s")

def get_connection():
    conn_str = (
        f"DRIVER={{{config.DB_DRIVER}}};"
        f"SERVER={config.DB_SERVER};"
        f"DATABASE={config.DB_NAME};"
        f"Trusted_Connection=yes;")
    return pyodbc.connect(conn_str)

def read_raw():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM raw_currency_rates", conn)
    conn.close()
    print(f"{len(df)} records read from raw table!")
    logging.info(f"{len(df)} records read from raw table")
    return df

def transform(df):

    df = df.drop_duplicates(subset=["ccy", "date"])

    df = df.dropna(subset=["ccy", "rate", "date"])

    df["rate"] = pd.to_numeric(df["rate"], errors="coerce")
    df["diff"] = pd.to_numeric(df["diff"], errors="coerce")
    df["nominal"] = pd.to_numeric(df["nominal"], errors="coerce").fillna(1).astype(int)
    df["date"] = pd.to_datetime(df["date"])

    df["rate_per_unit"] = df["rate"] / df["nominal"]

    df["change_direction"] = df["diff"].apply(
        lambda x: "Increased" if x > 0 else ("Decreased" if x < 0 else "No Change"))

   
    df["is_appreciated"] = (df["diff"] > 0).astype(int)
    df["is_depreciated"] = (df["diff"] < 0).astype(int)

    print("Transformation completed!")
    logging.info("Transformation completed")
    return df

def load_to_clean(df):
    conn = get_connection()
    cursor = conn.cursor()
    inserted = 0

    for _, row in df.iterrows():
        try:
            cursor.execute("""
                INSERT INTO clean_currency_rates
                    (currency_code, currency_name, nominal,
                     rate_uzs, diff_uzs, rate_date,
                     rate_per_unit, change_direction,
                     is_appreciated, is_depreciated)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
                row["ccy"],
                row["ccy_nm_en"],
                row["nominal"],
                row["rate"],
                row["diff"],
                row["date"],
                row["rate_per_unit"],
                row["change_direction"],
                row["is_appreciated"],
                row["is_depreciated"])
            inserted += 1
        except pyodbc.IntegrityError:
            pass

    conn.commit()
    conn.close()
    print(f"{inserted} records saved to clean table!")
    logging.info(f"{inserted} records saved to clean table")

def run_transform():
    df = read_raw()
    df = transform(df)
    load_to_clean(df)

if __name__ == "__main__":
    run_transform()