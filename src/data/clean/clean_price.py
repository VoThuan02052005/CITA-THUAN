from src.data.clean.common import DataFrame

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
