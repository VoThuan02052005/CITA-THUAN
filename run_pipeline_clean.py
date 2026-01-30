import logging
import pandas as pd
from src.data.clean.clean_data import clean_data
from src.data.validate.validate_data import validate_data
from src.utils.io import save_csv

# Cấu hình logging theo chuẩn best practice
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("pipeline_clean")

if __name__ == "__main__":
    logger.info("Bắt đầu quá trình làm sạch dữ liệu...")

    # 1. Tải dữ liệu thô
    raw_path = "data/raw/gia_nha.csv"
    logger.info(f"Đang tải dữ liệu từ: {raw_path}")
    data = pd.read_csv(raw_path)
    
    initial_count = len(data)
    logger.info(f"Số lượng dữ liệu ban đầu: {initial_count} dòng")

    # 2. Bước làm sạch (Clean)
    logger.info("Đang thực hiện bước làm sạch (Clean)...")
    data = clean_data(data)
    after_clean_count = len(data)
    removed_clean = initial_count - after_clean_count
    logger.info(f"Sau khi làm sạch: còn {after_clean_count} dòng (Đã loại bỏ: {removed_clean} dòng)")

    # 3. Bước kiểm định (Validate)
    logger.info("Đang thực hiện bước kiểm định (Validate)...")
    data = validate_data(data)
    final_count = len(data)
    removed_validate = after_clean_count - final_count
    logger.info(f"Sau khi kiểm định: còn {final_count} dòng (Đã loại bỏ thêm: {removed_validate} dòng)")

    # 4. Lưu kết quả
    output_path = "data/processed/data_sau_clean.csv"
    save_csv(data, output_path)
    
    total_removed = initial_count - final_count
    logger.info(f"Quá trình hoàn tất. Tổng cộng đã loại bỏ: {total_removed} dòng")
    logger.info(f"Dữ liệu cuối cùng được lưu tại: {output_path} với {final_count} dòng")
