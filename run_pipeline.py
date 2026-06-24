import logging
import config
from extract_to_raw import run_extract
from transform_to_clean import run_transform

logging.basicConfig(
    filename=config.LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(message)s")

def run_pipeline():
    print("===== PIPELINE STARTED =====")
    logging.info("===== PIPELINE STARTED =====")

    print("Step 1: Extract started...")
    run_extract()

    print("Step 2: Transform started...")
    run_transform()

    print("===== PIPELINE COMPLETED =====")
    logging.info("===== PIPELINE COMPLETED =====")

if __name__ == "__main__":
    run_pipeline()