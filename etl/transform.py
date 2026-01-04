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


# hàm transfomer dữ liệu
# def transfomer(data : DataFrame) -> DataFrame:
#     data = pd.read_csv("../data_raw/gia_nha.csv")
#     logger.info("Start transfomer data ...")
#     logger.info(f"data shape : {data.shape}")
#     logger.info(f"start clean land type")
#     try :
#         data = loai_hinh_dat(data)
#     except Exception as e :
#         logger.error(f"error : {e}")
#     logger.info(f"end clean land type")
#     logger.info(f"start clean acreage")
#     try :
#         data = dien_tich(data)
#     except Exception as e :
#         logger.error(f"error : {e}")
#     logger.info(f"end clean acreage")
#     logger.info(f"start clean price level")
#     try :
#         data = muc_gia(
#             data
#         )
#     except Exception as e :
#         logger.error(f"error : {e}")
#     logger.info(f"end clean price level")
#     logger.info(f"start clean number of bedrooms")
#     try :
#         data = so_phong_ngu(
#             data
#         )
#     except Exception as e :
#         logger.error(f"error : {e}")
#     logger.info(f"end clean number of bedrooms")
#     logger.info(f"start clean number of floors")
#     try :
#         data = so_tang(
#             data
#         )
#     except Exception as e :
#         logger.error(f"error : {e}")
#     logger.info(f"end clean number of bedrooms")
#     logger.info(f"start clean number of bathrooms")
#     try :
#         data = so_phong_tam(
#             data
#         )
#     except Exception as e :
#         logger.error(f"error : {e}")
#     logger.info("end clean number of bathrooms")
#     logger.info(f"start clean facade")
#     try :
#         data = mat_tien(
#             data
#         )
#     except Exception as e :
#         logger.error(f"error : {e}")
#     logger.info(f"end clean facade")
#     logger.info(f"start clean entrance")
#     try :
#         data = duong_vao(
#             data
#         )
#     except Exception as e :
#         logger.error(f"error : {e}")
#     logger.info(f"end clean entranceed")
#     logger.info(f"start clean posting date")
#     try :
#         data = ngay_dang(
#             data
#         )
#     except Exception as e :
#         logger.error(f"error : {e}")
#     logger.info(f"end clean posting date")
#     logger.info(f"start clean crawl_date ")
#     try :
#         data = crawl_date(
#             data
#         )
#     except Exception as e :
#         logger.error(f"error : {e}")
#     logger.info(f"end clean crawl_date")
#     logger.info(f"start remove duplicates")
#     try :
#         data = xoa_trung_lap(
#             data
#         )
#     except Exception as e :
#         logger.error(f"error : {e}")
#     logger.info(f"end remove duplicates")
#     logger.info(f"start remove duplicates by column")
#     try :
#         data = xoa_trung_lap_theo_cot(
#             data ,
#             subset = ["Loại giao dịch", "Thành phố", "Quận/huyện", "Loại hình đất",
#                       "Mức giá", "Diện tích", "Số phòng ngủ", "Số phòng tắm, vệ sinh",
#                       "Số tầng", "Hướng nhà", "Hướng ban công", "Mặt tiền", "Đường vào",
#                       "Pháp lý", "Nội thất", "Ngày đăng"],
#             keep = "first"
#         )
#     except Exception as e :
#         logger.error(f"error : {e}")
#     logger.info(f"end remove duplicates")


# hàm transfomer dữ liệu

def transformer(data: DataFrame) -> DataFrame:
    logger.info("Start transformer data ...")
    logger.info(f"Initial shape: {data.shape}")

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
    except Exception as e:
        logger.exception(f"Transformer failed: {e}")

    logger.info(f"Final shape: {data.shape}")

    return data



