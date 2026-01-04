"""
Tải dữ liệu đã xử lý vào kho dữ liệu (PostgreSQL).
"""
from pathlib import Path
from pandas import DataFrame
from etl.logger_utils import setup_logger

logger = setup_logger("load")


def save_processed_data(
    data: DataFrame,
    output_path: str = "data_processed/gia_nha_processed.csv"
):
    """
    Lưu dữ liệu đã xử lý ra file CSV.

    Parameters
    ----------
    data : pandas.DataFrame
        Dữ liệu sau bước transform.
    output_path : str
        Đường dẫn file output.
    """
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    data.to_csv(
        output_path,
        index=False,
        encoding="utf-8-sig"
    )

    logger.info(f"Saved processed data to {output_path}")

