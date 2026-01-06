"""
Làm sạch và chuẩn hóa dữ liệu thô:
- Xử lý các giá trị còn thiếu
- Chuẩn hóa giá cả và diện tích
- Phân tích ngày giờ
Output: data_processed/
"""
# khai báo thư viện
import numpy as np
import pandas as pd
from etl.logger_utils import  setup_logger
from pandas import DataFrame
from pathlib import Path
import os

PROCESSED_PATH =  "data_processed"
logger = setup_logger("transform")


# xử lý cột loại hình đất
def loai_hinh_dat(data : DataFrame) -> DataFrame:
    """
    Chuẩn hoá cột 'Loại hình đất' trong DataFrame bất động sản.

    Hàm này ánh xạ các giá trị trong cột 'Loại hình đất' về một tập
    nhãn cố định (ví dụ: Nhà biệt thự, Căn hộ chung cư, Bán đất, ...),
    dựa trên việc kiểm tra chuỗi con (substring matching).

    Nếu một giá trị không khớp với bất kỳ loại nào trong danh sách,
    giá trị gốc sẽ được giữ nguyên.

    Parameters
    ----------
    data : pandas.DataFrame
        DataFrame chứa cột 'Loại hình đất' cần được chuẩn hoá.

    Returns
    -------
    pandas.DataFrame
        DataFrame sau khi chuẩn hoá cột 'Loại hình đất'.

    Notes
    -----
    - So khớp chuỗi không phân biệt NaN (na=False).
    - Mỗi dòng chỉ được gán vào loại đầu tiên khớp trong danh sách conditions.
    - Thứ tự các điều kiện trong 'conditions' là quan trọng.
    """
    col = data['Loại hình đất']

    conditions = [
        col.str.contains("Nhà biệt thự", na=False),
        col.str.contains("Căn hộ chung cư", na=False),
        col.str.contains("Nhà mặt phố", na=False),
        col.str.contains("Bán đất", na=False),
        col.str.contains("Văn phòng", na=False),
        col.str.contains("Nhà riêng", na=False),
        col.str.contains("Condotel", na=False),
        col.str.contains("Đất nền", na=False),
        col.str.contains("Shophouse", na=False),
        col.str.contains("Nhà trọ", na=False),
        col.str.contains("Chung cư mini, căn hộ", na=False),
        col.str.contains("Kho", na=False),
        col.str.contains("Trang trại", na=False),
        col.str.contains("Cửa hàng", na=False),
        col.str.contains("Loại bất động sản khác", na=False)
    ]

    choices = [
        "Nhà biệt thự",
        "Căn hộ chung cư",
        "Nhà mặt phố",
        "Bán đất",
        "Văn phòng",
        "Nhà riêng",
        "Condotel",
        "Đất nền",
        "Shophouse",
        "Nhà trọ",
        "Chung cư mini, căn hộ",
        "Kho",
        "Trang trại",
        "Cửa hàng",
        "Loại bất động sản khác"

    ]

    data['Loại hình đất'] = np.select(conditions, choices, default=col)
    return data

# xử lý cột diện tích
def dien_tich(data : DataFrame) -> DataFrame:
    """
        Chuẩn hoá cột 'Diện tích' trong DataFrame bất động sản.

        Hàm chuyển các giá trị diện tích dạng chuỗi (ví dụ: "96 m²", "120,5 m²")
        về số thực (float). Các ký tự đơn vị được loại bỏ, dấu phẩy được
        chuyển thành dấu chấm.

        Các giá trị không hợp lệ hoặc không thể chuyển đổi sẽ được gán NaN.

        Parameters
        ----------
        data : pandas.DataFrame
            DataFrame chứa cột 'Diện tích'.

        Returns
        -------
        pandas.DataFrame
            DataFrame sau khi chuẩn hoá cột 'Diện tích'.
    """

    data['Diện tích'] = (
        data['Diện tích']
        .astype(str)
        .str.lower()
        .str.replace("m²", "")
        .str.replace(',', '.', regex=False)
        .pipe(pd.to_numeric, errors='coerce')
    )
    return data


# xử lý cột mức giá
def muc_gia(data : DataFrame) -> DataFrame:
    """
        Chuẩn hoá cột 'Mức giá' trong DataFrame bất động sản.

        Hàm chuyển các giá trị diện tích dạng chuỗi (ví dụ: "96 m²", "120,5 m²")
        về số thực (float). Các ký tự đơn vị được loại bỏ, dấu phẩy được
        chuyển thành dấu chấm.

        Các giá trị không hợp lệ hoặc không thể chuyển đổi sẽ được gán NaN.

        Parameters
        ----------
        data : pandas.DataFrame
            DataFrame chứa cột 'Diện tích'.

        Returns
        -------
        pandas.DataFrame
            DataFrame sau khi chuẩn hoá cột 'Diện tích'.
    """

    pattern = r"(?P<Gia>\d+(?:[.,]\d+)?)\s*(?P<Don_vi>.*)"

    tmp = data["Mức giá"].str.extract(pattern)

    data["Giá"] = (
        tmp["Gia"]
        .str.replace(",", ".", regex=False)
        .astype(float)
    )

    data["Đơn vị(Mức giá)"] = tmp["Don_vi"]


    return data

# xử lý cột số phòng ngủ
def so_phong_ngu(data : DataFrame) -> DataFrame:
    """
        Chuẩn hoá cột "Số phòng ngủ" trong DataFrame bất động sản.

        Hàm chuyển các giá trị Số phòng ngủ dạng chuỗi (ví dụ: "9 phòng", "9")
        về số nguyên int64 . loại bỏ chữ , xóa khoảng trắng.

        Các giá trị không hợp lệ hoặc không thể chuyển đổi sẽ được gán NaN.

        Parameters
        ----------
        data : pandas.DataFrame
            DataFrame chứa cột "Số phòng ngủ".

        Returns
        -------
        pandas.DataFrame
            DataFrame sau khi chuẩn hoá cột "Số phòng ngủ".
    """
    data["Số phòng ngủ"] = (
        data["Số phòng ngủ"]
        .astype(str)
        .str.replace("phòng", "")
        .str.strip()
        .pipe(pd.to_numeric, errors='coerce')
        .astype("float")
    )
    return data

# xử lý cột số phòng tắm, vệ sinh
def so_phong_tam(data : DataFrame ) -> DataFrame:
    """
    Chuẩn hoá cột 'Số phòng tắm, vệ sinh' trong DataFrame bất động sản.

    Hàm này chuyển các giá trị trong cột 'Số phòng tắm, vệ sinh' từ dạng
    chuỗi (ví dụ: "2 phòng", "1") sang kiểu số nguyên (Int64).
    Từ khoá "phòng" sẽ được loại bỏ, các giá trị không hợp lệ hoặc
    không thể chuyển đổi sẽ được gán NaN.

    Kiểu dữ liệu Int64 (nullable integer) được sử dụng để cho phép
    tồn tại giá trị NaN sau khi chuyển đổi.

    Parameters
    ----------
    data : pandas.DataFrame
        DataFrame chứa cột 'Số phòng tắm, vệ sinh'.

    Returns
    -------
    pandas.DataFrame
        DataFrame sau khi chuẩn hoá cột 'Số phòng tắm, vệ sinh'.
    """
    data["Số phòng tắm, vệ sinh"] = (
        data["Số phòng tắm, vệ sinh"]
        .astype(str)
        .str.replace("phòng", "")
        .str.strip()
        .pipe(pd.to_numeric, errors='coerce')
        .astype("Int64")
    )
    return data

# xử lý cột số tầng
def so_tang(data : DataFrame) -> DataFrame:
    """
    Chuẩn hoá cột 'Số tầng' trong DataFrame bất động sản.

    Hàm chuyển các giá trị trong cột 'Số tầng' từ dạng chuỗi
    (ví dụ: "3 tầng", "5") sang kiểu số nguyên (Int64).
    Từ khoá "tầng" được loại bỏ, các giá trị không hợp lệ hoặc
    không thể chuyển đổi sẽ được gán NaN.

    Kiểu Int64 (nullable integer) được sử dụng để cho phép
    tồn tại giá trị NaN sau khi chuẩn hoá.

    Parameters
    ----------
    data : pandas.DataFrame
        DataFrame chứa cột 'Số tầng'.

    Returns
    -------
    pandas.DataFrame
        DataFrame sau khi chuẩn hoá cột 'Số tầng'.
    """
    data["Số tầng"] = (
        data["Số tầng"]
        .astype(str)
        .str.replace("tầng", "")
        .str.strip()
        .pipe(pd.to_numeric, errors='coerce')
        .astype("Int64")
    )
    return data

# xử lý cột mặt tiền
def mat_tien(data : DataFrame) -> DataFrame:
    """
    Chuẩn hoá cột 'Mặt tiền' trong DataFrame bất động sản.

    Hàm chuyển các giá trị trong cột 'Mặt tiền' từ dạng chuỗi
    (ví dụ: "4m", "5.5 m") sang kiểu số thực (float).
    Ký tự đơn vị "m" được loại bỏ, các giá trị không hợp lệ
    hoặc không thể chuyển đổi sẽ được gán NaN.

    Parameters
    ----------
    data : pandas.DataFrame
        DataFrame chứa cột 'Mặt tiền'.

    Returns
    -------
    pandas.DataFrame
        DataFrame sau khi chuẩn hoá cột 'Mặt tiền'.
    """
    data["Mặt tiền"] = (
        data["Mặt tiền"]
        .astype(str)
        .str.replace("m", "")
        .str.strip()
        .pipe(pd.to_numeric, errors='coerce')
    )
    return data

# xử lý cột đường vào
def duong_vao(data : DataFrame) -> DataFrame:
    """
    Chuẩn hoá cột 'Đường vào' trong DataFrame bất động sản.

    Hàm chuyển các giá trị trong cột 'Đường vào' từ dạng chuỗi
    (ví dụ: "3m", "5.5 m") sang kiểu số thực (float).
    Ký tự đơn vị "m" được loại bỏ, các giá trị không hợp lệ
    hoặc không thể chuyển đổi sẽ được gán NaN.

    Parameters
    ----------
    data : pandas.DataFrame
        DataFrame chứa cột 'Đường vào'.

    Returns
    -------
    pandas.DataFrame
        DataFrame sau khi chuẩn hoá cột 'Đường vào'.
    """
    data["Đường vào"] = (
        data["Đường vào"]
        .astype(str)
        .str.replace("m", "")
        .str.strip()
        .pipe(pd.to_numeric, errors='coerce')
    )
    return data

# xử lý cột ngày đăng
def ngay_dang(data : DataFrame) -> DataFrame:
    """
    Chuẩn hoá cột 'Ngày đăng' trong DataFrame bất động sản.

    Hàm chuyển các giá trị ngày đăng từ nhiều định dạng chuỗi
    (ví dụ: '05-06-2025', '24/06/2025') về kiểu datetime64.
    Các giá trị không hợp lệ sẽ được gán NaT.

    Parameters
    ----------
    data : pandas.DataFrame

    Returns
    -------
    pandas.DataFrame
    """
    data["Ngày đăng"] = (
        data["Ngày đăng"]
        .astype(str)
        .str.replace("/", "-")
        .str.strip()
        .replace({"nan": None})
    )

    data["Ngày đăng"] = pd.to_datetime(
        data["Ngày đăng"],
        dayfirst=True,
        errors="coerce"
    )

    return data

# hàm xử lý cột ngày lấy dữ liệu
def crawl_date(data : DataFrame) -> DataFrame :
    """
    Chuẩn hóa cột "craw_date" trong dataframe bất động sản.

    Hàm chuyển các giá trị ngày lấy dữ liệu ( 2025-08-07 ) về định dạng datetime64
    các giá trị không hợp lệ thì gá giá trị NAN.
    :param data:
    ------------
    data : pandas.DataFrame
    :return:
    ----------
    pandas.DataFrame
    """
    data["crawl_date"] = pd.to_datetime(
        data["crawl_date"],
        errors="coerce"

    )
    return data

# hàm xóa các bản ghi giống nhau hoàn toàn
def xoa_trung_lap(data: pd.DataFrame) -> pd.DataFrame:
    """
    Loại bỏ các bản ghi trùng nhau hoàn toàn trong DataFrame.

    Returns
    -------
    pd.DataFrame
        DataFrame sau khi đã loại bỏ các dòng trùng.
    """
    truoc = len(data)
    data = data.drop_duplicates()
    sau = len(data)
    logger.info(f"so ban ghi da xoa : {truoc - sau}")
    return data

# hàm xóa bản ghi trùng theo cột chỉ định
def xoa_trung_lap_theo_cot(
    data: pd.DataFrame,
    subset: list[str],
    keep: str = "first"
) -> pd.DataFrame:
    """
    Loại bỏ các bản ghi trùng nhau theo các cột chỉ định.

    Parameters
    ----------
    subset : list[str]
        Danh sách cột dùng để kiểm tra trùng lặp.
    keep : {"first", "last", False}
        Giữ bản ghi nào.

    Returns
    -------
    pd.DataFrame
    """
    return data.drop_duplicates(subset=subset, keep=keep)

def validate_price(data: DataFrame) -> DataFrame:

    data = data[data["Giá"] > 0 ]
    data = data.dropna(subset=["Giá"])
    data = data.drop(columns=["Mức giá"])

    return data
def validate_area(data : DataFrame) -> DataFrame:

    data = data[data["Diện tích"] > 0  ]
    data = data.dropna(subset=["Diện tích"])

    return data

def validate_location(data : DataFrame) -> DataFrame:
    data = data[
        data["Thành phố"].notna() & data["Quận/huyện"].notna() ]
    return data

def build_dim_location(data: DataFrame) -> DataFrame:
    """
    Xây dựng bảng dimension location (dim_location) từ dữ liệu thô.

    Mục đích:
    - Loại bỏ các bản ghi trùng lặp
    - Tạo khóa thay thế (surrogate key) cho bảng dim_location

    Tham số:
    ----------
    data : DataFrame
        DataFrame đầu vào chứa dữ liệu thô, bao gồm các cột:
        - "Thành phố"
        - "Quận/huyện"

    Giá trị trả về:
    ---------------
    DataFrame
        Bảng dim_location với các cột:
        - location_id : int
            Khóa chính (surrogate key) cho mỗi địa điểm
        - city : str
            Tên thành phố
        - district : str
            Tên quận/huyện
    """
    dim = (
        data[["Thành phố", "Quận/huyện"]]
        .rename(columns={
            "Thành phố": "city",
            "Quận/huyện": "district"
        })
        .drop_duplicates()
        .reset_index(drop=True)
    )
    dim["location_id"] = dim.index + 1
    return dim
def build_dim_property(data: DataFrame) -> DataFrame:
    """
    Xây dựng bảng dimention property (dim_property) từ dữ liệu thô.

    Mục đích:
      - loại bỏ các bản ghi trùng lặp.
      - Tạo khóa thay thế (surrogate key) cho bảng dim_property

    :param data :
    ----------
    data : DataFrame
        DataFrame đầu vào chứa dữ liệu thô, bao gồm các cột:
        - "Loại hình đất"
        - "Pháp lý"
        - "Nội thất"
        - "Hướng nhà"
        - "Hướng ban công

    :return :
    ---------------
    DataFrame
        Bảng dim_property với các cột:
        - property_id : int
          Khóa chính (surrogate key)
        - property_type : str
        - legal_status :  str
        - interior     :  str
        - house_direction : str
        - balcony_direction : str

    """
    dim = (
        data[
            [
                "Loại hình đất",
                "Pháp lý",
                "Nội thất",
                "Hướng nhà",
                "Hướng ban công"
            ]
        ]
        .rename(columns={
            "Loại hình đất": "property_type",
            "Pháp lý": "legal_status",
            "Nội thất": "interior",
            "Hướng nhà": "house_direction",
            "Hướng ban công": "balcony_direction"
        })
        .drop_duplicates()
        .reset_index(drop=True)
    )
    dim["property_id"] = dim.index + 1
    return dim
def build_dim_time(data : DataFrame) -> DataFrame:
    """
        Xây dựng bảng dimension thời gian (dim_time) từ dữ liệu thô.

        Mục đích:
        - Chuẩn hóa thông tin thời gian từ các mốc ngày khác nhau
          (ngày đăng tin và ngày crawl dữ liệu)
        - Loại bỏ các bản ghi trùng lặp
        - Tạo khóa thay thế (surrogate key) cho bảng dim_time
        - Phục vụ phân tích xu hướng và mô hình hóa theo thời gian

        :param data :
        ----------
        data : DataFrame
            DataFrame đầu vào chứa dữ liệu thô, bao gồm các cột:
            - "Ngày đăng"   : ngày tin đăng được tạo
            - "crawl_date"  : ngày hệ thống thu thập dữ liệu

        :return :
        ---------------
        DataFrame
            Bảng dim_time với các cột:
            - time_id : int
                Khóa chính (surrogate key) cho mỗi mốc thời gian
            - posted_date : datetime
                Ngày đăng tin bất động sản
            - crawl_date : datetime
                Ngày crawl dữ liệu
            - day : int
                Ngày trong tháng (1–31)
            - month : int
                Tháng trong năm (1–12)
            - year : int
                Năm
    """

    dim = (
        data[["Ngày đăng", "crawl_date"]]
        .rename(columns={"Ngày đăng": "posted_date"})
        .drop_duplicates()
        .reset_index(drop=True)
    )

    dim["posted_date"] = pd.to_datetime(dim["posted_date"], errors="coerce")
    dim["crawl_date"] = pd.to_datetime(dim["crawl_date"], errors="coerce")

    dim["day"] = dim["posted_date"].dt.day
    dim["month"] = dim["posted_date"].dt.month
    dim["year"] = dim["posted_date"].dt.year

    dim["time_id"] = dim.index + 1
    return dim
def build_fact_real_estate(data , dim_location , dim_property , dim_time):
    """
        Xây dựng bảng fact_real_estate (bảng fact trung tâm) từ dữ liệu thô
        bằng cách liên kết với các bảng dimension.

        Mục đích:
        - Chuẩn hóa dữ liệu thô sang schema Data Warehouse
        - Ánh xạ các thuộc tính phân loại sang khóa ngoại (FK)
        - Chuẩn bị dữ liệu cho phân tích và huấn luyện mô hình học máy

        :param data :
        ----------
        data : DataFrame
            Dữ liệu thô thu thập từ crawler, chứa thông tin chi tiết tin đăng BĐS

        dim_location : DataFrame
            Bảng dimension vị trí (dim_location), chứa:
            - location_id
            - city
            - district

        dim_property : DataFrame
            Bảng dimension thuộc tính BĐS (dim_property), chứa:
            - property_id
            - property_type
            - legal_status
            - interior
            - house_direction
            - balcony_direction

        dim_time : DataFrame
            Bảng dimension thời gian (dim_time), chứa:
            - time_id
            - posted_date
            - crawl_date

    :return :
        ---------------
        DataFrame
            Bảng fact_real_estate với các cột:
            - location_id (FK)
            - property_id (FK)
            - time_id (FK)
            - transaction_type
            - price
            - price_unit
            - area
            - bedrooms
            - bathrooms
            - floors
            - frontage
            - road_width
    """
    df_fact = data.rename(columns={
        "Loại giao dịch": "transaction_type",
        "Giá": "price",
        "Đơn vị(Mức giá)": "price_unit",
        "Diện tích": "area",
        "Số phòng ngủ": "bedrooms",
        "Số phòng tắm, vệ sinh": "bathrooms",
        "Số tầng": "floors",
        "Mặt tiền": "frontage",
        "Đường vào": "road_width",
        "Thành phố": "city",
        "Quận/huyện": "district",
        "Loại hình đất": "property_type",
        "Pháp lý": "legal_status",
        "Nội thất": "interior",
        "Hướng nhà": "house_direction",
        "Hướng ban công": "balcony_direction",
        "Ngày đăng": "posted_date"
    })

    df_fact = (
        df_fact
        .merge(dim_location, on=["city", "district"], how="left")
        .merge(dim_property, on=[
            "property_type",
            "legal_status",
            "interior",
            "house_direction",
            "balcony_direction"
        ], how="left")
        .merge(dim_time, on=["posted_date", "crawl_date"], how="left")
    )

    fact = df_fact[
        [
            "location_id",
            "property_id",
            "time_id",
            "transaction_type",
            "price",
            "price_unit",
            "area",
            "bedrooms",
            "bathrooms",
            "floors",
            "frontage",
            "road_width"
        ]
    ]

    return fact


# hàm lưu dữ liệu sau khi xử lý
def save_processed_data(dim_location, dim_property, dim_time, fact):
    """
    Lưu các bảng dimension và fact sau khi xử lý vào thư mục processed.

    Mục đích:
    - Ghi kết quả của bước Transform (ETL) ra file CSV
    - Chuẩn hóa đầu ra cho các bước phân tích, trực quan hóa
      và huấn luyện mô hình học máy
    - Đảm bảo dữ liệu đã được tách theo mô hình Star Schema

    Tham số:
    ----------
    dim_location : DataFrame
        Bảng dimension vị trí địa lý (dim_location)

    dim_property : DataFrame
        Bảng dimension thuộc tính bất động sản (dim_property)

    dim_time : DataFrame
        Bảng dimension thời gian (dim_time)

    fact : DataFrame
        Bảng fact trung tâm (fact_real_estate)
    """
    os.makedirs(PROCESSED_PATH, exist_ok=True)

    dim_location.to_csv(
        f"{PROCESSED_PATH}/dim_location.csv", index=False
    )
    dim_property.to_csv(
        f"{PROCESSED_PATH}/dim_property.csv", index=False
    )
    dim_time.to_csv(
        f"{PROCESSED_PATH}/dim_time.csv", index=False
    )
    fact.to_csv(
        f"{PROCESSED_PATH}/fact_real_estate.csv", index=False
    )

    logger.info("Processed data saved successfully")

# hàm transfomer dữ liệu

def transformer(data: DataFrame) -> DataFrame:
    logger.info("Start transformer data ...")
    logger.info(f"Initial shape: {data.shape}")
    k = len(data )
    logger.info(f"số bản ghi trước khi xóa: {k}")
    try:
        data = loai_hinh_dat(data)
        data = dien_tich(data)
        data = muc_gia(data)
        data = so_phong_ngu(data)
        data = so_tang(data)
        data = so_phong_tam(data)
        data = mat_tien(data)
        data = duong_vao(data)
        data = ngay_dang(data)
        data = crawl_date(data)

        data = xoa_trung_lap(data)
        data = xoa_trung_lap_theo_cot(
            data,
            subset=[
                "Loại giao dịch", "Thành phố", "Quận/huyện", "Loại hình đất",
                "Mức giá", "Diện tích", "Số phòng ngủ", "Số phòng tắm, vệ sinh",
                "Số tầng", "Hướng nhà", "Hướng ban công", "Mặt tiền",
                "Đường vào", "Pháp lý", "Nội thất", "Ngày đăng"
            ],
            keep="first"
        )
        data = validate_price(data)
        data = validate_area(data)
        data = validate_location(data)
        dim_location = build_dim_location(data )
        dim_property = build_dim_property(data )
        dim_time = build_dim_time(data)

        fact = build_fact_real_estate(
            data, dim_location, dim_property, dim_time
        )

        save_processed_data(
            dim_location, dim_property, dim_time, fact
        )

    except Exception as e:
        logger.exception(f"Transformer failed: {e}")
    g = len(data)
    logger.info(f"số bản ghi đã xóa: {k - g }")
    logger.info(f"số bản ghi sau khi xóa: {g }")
    logger.info(f"Final shape: {data.shape}")

    return dim_location, dim_property, dim_time, fact



