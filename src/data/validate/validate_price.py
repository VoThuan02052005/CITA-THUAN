from .common import np , pd , DataFrame

from .common import np, pd, DataFrame

def validate_price(data: DataFrame) -> DataFrame:
    """
    Chuẩn hóa và kiểm tra giá bán bất động sản (1 hàm duy nhất).

    Chức năng:
    - Chuẩn hóa giá bán về đơn vị VND
    - Tự động loại bỏ giao dịch cho thuê
    - Loại bỏ giá không hợp lệ (NaN, <= 0)
    - Xóa các cột trung gian không cần thiết
    """

    def _normalize(row):
        price = row["Giá"]
        unit = str(row['Đơn vị(Mức giá)']).lower()
        area = row['Diện tích']

        if "/tháng" in unit:
            return None

        if unit == "tỷ":
            return price * 1e9

        if unit == "triệu":
            return price * 1e6

        if unit == "triệu/m²" and pd.notna(area):
            return price * 1e6 * area

        if unit == "nghìn/m²" and pd.notna(area):
            return price * 1e3 * area

        if unit == "nghìn":
            return price * 1e3

        if unit == "tỷ/m²" and pd.notna(area):
            return price * 1e9 * area

        return None

    data["Giá"] = data.apply(_normalize, axis=1)
    data = data.dropna(subset=["Giá"])
    data = data[data["Giá"] > 0]

    cols_drop = ['Đơn vị(Mức giá)', "Mức giá", ]
    data = data.drop(columns=[c for c in cols_drop if c in data.columns])

    return data

