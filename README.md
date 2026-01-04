# 🏘️ Xây dựng pineline dữ liệu nhà đất phục vụ dự đoán giá nhà

## 📌 Project Overview 

Dự án này tập trung vào việc xây dựng quy trình Kỹ thuật dữ liệu từ đầu đến cuối cho dữ liệu bất động sản để hỗ trợ dự đoán giá nhà.

Quy trình thu thập dữ liệu nhà ở thô từ các trang web bất động sản, xử lý và lưu trữ dữ liệu đó ở định dạng có cấu trúc, đồng thời chuẩn bị dữ liệu cho các mô hình học máy.

Dự án này được thiết kế dành cho những người mới bắt đầu Kỹ thuật dữ liệu muốn thực hành làm việc với dữ liệu trong thế giới thực và hiểu cách các đường dẫn dữ liệu hỗ trợ phân tích dự đoán.

---- 

## 🎯 Project Objectives 

* Thu thập dữ liệu bất động sản từ các nguồn trực tuyến.
* Làm sạch và xử lý dữ liệu thô , không có cấu trúc.
* Lưu trữ dữ liệu đã xử lý trong cơ sở dữ liệu.
* Chuẩn bị đặc trưng cho các mô hình dự đoán giá nhà.
* Xây dựng các mô hình phục vụ bài tóa dự đoán giá.
* xây dựng giao diện demo 

----

## 🌐 Data source 

+) crawl dữ liệu từ trang web batdongsan.com.

----

## 🧱 Pineline Overview 

```
Web / API 
-> Ingest (Python)
-> Raw Data (CSV / JSON / raw tables)
-> Clean & Normalize (python)
-> Data warehouse (Postgres)

-> dbt (Analytics layer)
   ├── fact_listings
   ├── dim_location
   ├── dim_time
   └── fact_price_history

→ Feature Engineering (Python)
   ├── encode
   ├── scale
   ├── aggregate
   └── feature store / dataset_ml

→ Train ML Model
→ Prediction / Evaluation
```

---

## 🔄 Data Pipeline Architecture

Quy trình này bao gồm các giai đoạn sau: 

1. **Data Ingestion**

   * thu thập dữ liệu giá nhà bằng Selenium & BeautifulSoup
   * trích xuất các thuộc tính như:

     * Location
     * Area (m²)
     * Number of bedrooms
     * Price
     * Property type

2. **Data Cleaning & Validation**

   * Xóa dữ liệu trùng lặp.
   * xử lý các giá trị bị thiếu hoặc không hợp lệ.
   * Chuẩn hóa đơn vị giá cả và diện tích.

3. **Data Storage**

   * Lưu trữ dữ liệu đã làm sạch vào các tệp CSV và cơ sở dữ liệu SQLite.
   * Đảm bảo tính nhất quán của dữ liệu để phục vụ cho việc phân tích tiếp theo.

4. **Feature Engineering**

   * Encode categorical variables (One-Hot Encoding)
   * Normalize numerical features
   * Generate feature vectors for ML models

5. **Data Serving for ML**

   * Export final dataset for training and evaluation
   * Support house price prediction models

---

## 🛠 Tech Stack

* **Programming Language:** Python
* **Web Scraping:** Selenium, BeautifulSoup
* **Data Processing:** Pandas, NumPy
* **Database:** SQLite
* **Machine Learning:** Scikit-learn
* **Visualization:** Matplotlib

---

## 📂 Project Structure

```
real-estate-data-pipeline/
│── data_raw/
│   ├── raw/       
│   ├── cleaned/       
│
│── etl/
│   ├── extract.py 
│   ├── transfomer.py 
│   ├── load.py 
│
│── data_processed/
│   ├── clean_data.py
│   ├── feature_engineering.py
│
│── warehouse 
│   ├── database.db
│
│── ml/
│   ├── train_model.py
│
│── main.py                # Run full pipeline
│── requirements.txt
│── README.md
```



