# dim_location

create table iff not exists dim_location(
    location_id integer primary key AUTOINCREMENT ,
    province text not null,
    district text
)

# dim_time
CREATE TABLE IF NOT EXISTS dim_time (
    time_id INTEGER PRIMARY KEY AUTOINCREMENT,
    posted_date DATE NOT NULL,
    crawl_date DATE,
    day INTEGER,
    month INTEGER,
    year INTEGER
);

# dim_property
CREATE TABLE IF NOT EXISTS dim_property (
    property_id INTEGER PRIMARY KEY AUTOINCREMENT,
    property_type TEXT,        -- Loại hình đất
    legal_status TEXT,         -- Pháp lý
    interior TEXT,             -- Nội thất
    house_direction TEXT,      -- Hướng nhà
    balcony_direction TEXT     -- Hướng ban công
);

# fact_real_estate
CREATE TABLE IF NOT EXISTS fact_real_estate (
    listing_id INTEGER PRIMARY KEY AUTOINCREMENT,

    location_id INTEGER NOT NULL,
    property_id INTEGER NOT NULL,
    time_id INTEGER NOT NULL,

    transaction_type TEXT,     -- Loại giao dịch
    price REAL NOT NULL,       -- Giá
    price_per_m2 real ,
    price_unit TEXT,            -- Đơn vị(Mức giá)

    area REAL,                 -- Diện tích
    bedrooms INTEGER,           -- Số phòng ngủ
    bathrooms INTEGER,          -- Số phòng tắm
    floors INTEGER,             -- Số tầng

    frontage REAL,              -- Mặt tiền
    road_width REAL,            -- Đường vào

    FOREIGN KEY (location_id) REFERENCES dim_location(location_id),
    FOREIGN KEY (property_id) REFERENCES dim_property(property_id),
    FOREIGN KEY (time_id) REFERENCES dim_time(time_id)
);


