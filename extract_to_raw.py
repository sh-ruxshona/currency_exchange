import requests
import pyodbc
import json
import logging
from datetime import datetime
import config

logging.basicConfig(
    filename=config.LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(message)s")

def extract_from_cbu():
    
    print("CBU data extraction started...")
    logging.info("CBU data extraction started")
    
    try:
        response = requests.get(config.CBU_URL, timeout=10)
        data = response.json()
        print(f"{len(data)} currencies received!")
        logging.info(f"{len(data)} currencies received")
        return data
    
    except Exception as e:
        print(f"Error occurred: {e}")
        logging.error(f"Error: {e}")
        return []

def get_connection():
    conn_str = (
        f"DRIVER={{{config.DB_DRIVER}}};"
        f"SERVER={config.DB_SERVER};"
        f"DATABASE={config.DB_NAME};"
        f"Trusted_Connection=yes;")
    return pyodbc.connect(conn_str)

def load_to_raw(data):
    
    if not data:
        print("No data to load!")
        logging.warning("No data to load")
        return

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM raw_currency_rates WHERE loaded_at >= CAST(GETDATE() AS DATE)")
    count = cursor.fetchone()[0]
    
    if count > 0:
        print("Today's data already exists in raw table!")
        logging.info("Today's data already exists in raw table")
        conn.close()
        return
    
    for record in data:
        cursor.execute("""
            INSERT INTO raw_currency_rates
                (ccy, ccy_nm_uz, ccy_nm_ru, ccy_nm_en,
                 nominal, rate, diff, date, raw_json)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
            record.get("Ccy"),
            record.get("CcyNm_UZ"),
            record.get("CcyNm_RU"),
            record.get("CcyNm_EN"),
            int(record.get("Nominal", 1)),
            float(record.get("Rate", 0)),
            float(record.get("Diff", 0)),
            datetime.strptime(record.get("Date"), "%d.%m.%Y").date(),
            json.dumps(record, ensure_ascii=False))

    conn.commit()
    conn.close()
    print(f"{len(data)} records saved to raw table!")
    logging.info(f"{len(data)} records saved to raw table")

def run_extract():
    data = extract_from_cbu()
    load_to_raw(data)

if __name__ == "__main__":
    run_extract()