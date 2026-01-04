from etl.extract import extract
from etl.transform import transformer
from etl.load import save_processed_data
import pandas as pd

def run_pipeline():
    data = pd.read_csv("data_raw/gia_nha.csv")
    data_processed = transformer(data )
    save_processed_data(data_processed)
