# Building an end-to-end data pipeline for house price prediction in Vietnam


## Overview
This project provides a comprehensive data engineering and machine learning pipeline for real estate price prediction. The solution encompasses automated data cleaning, validation, feature engineering, and a benchmark suite of models—from simple baseline metrics to custom multi-layer perceptrons (MLP). The objective is to provide a reproducible and modular framework for analyzing real estate trends and building predictive models for Springer-quality research and production environments.

## Project Structure
```text
.
├── config.yaml             # Global configuration for crawling and processing
├── data/
│   ├── raw/                # Source CSV files (raw data)
│   ├── staging/            # Cleaned and validated intermediate data
├── logs/                   # timestamped execution logs
├── models/                 # Saved model artifacts (.joblib)
├── notebooks/              # Jupyter notebooks for exploratory analysis
├── reports/
│   └── figures/            # High-resolution plots and visualizations
├── run_pipeline_clean.py   # Entry point for data cleaning and validation
├── src/
│   ├── data/               # Modular data logic (clean, validate, etl)
│   ├── features/           # Feature engineering and scaling
│   ├── models/             # Model architectures and definitions
│   ├── pipelines/          # Training and evaluation orchestration
│   └── utils/              # Shared utilities (logging, metrics, io)
├── README.md               # Project documentation
└── requirements.txt        # Dependency list
```

## Data / Input
The primary input is a raw real estate dataset located at `data/raw/gia_nha.csv`. 
- **Format**: CSV
- **Content**: Vietnamese real estate listings including location, price, area, room counts, and property attributes.
- **Acquisition**: The raw dataset can be downloaded from [https://www.kaggle.com/datasets/thunvthun/house-price/data]. Alternatively, the project includes an automated extraction module in `src/data/etl/extract.py`.

## Workflow / Pipeline
1. **Extraction**: Collect raw listing data from real estate portals.
2. **Preprocessing**: Execute `run_pipeline_clean.py` to perform:
   - Type conversion and normalization.
   - Outlier removal and duplicate filtering.
   - Validation against predefined schemas.
3. **Feature Engineering**: Automated generation of time-based features, categorical encoding, and numerical scaling.
4. **Training**: Orchestrate training across different model families (Linear, Tree, MLP) via scripts in `src/pipelines/`.
5. **Evaluation**: Generate comparative metrics (MAE, RMSE, R2) and diagnostic plots.

## How to Run
### Environment Requirements
- Python 3.10+
- Recommended: Virtual environment (venv or conda)
- Kaggle API

### Installation
```bash
git clone https://github.com/your-username/project_price.git
cd project_price
pip install -r requirements.txt
```

## Download Raw Dataset
The raw housing price dataset is publicly available on Kaggle.

**Dataset Link**: [https://www.kaggle.com/datasets/thunvthun/house-price/data]
To download the dataset programmatically, please follow these steps:

### Dataset Download
#### Kaggle API Setup
```bash
pip install kaggle
```

1. Go to Kaggle -> Account -> API -> Create New Token
2. Download `kaggle.json`
3. Move it to: `~/.kaggle/kaggle.json`
4. Set permissions:
```bash
chmod 600 ~/.kaggle/kaggle.json
```

#### Option 1: Use Raw Data and Run Cleaning Pipeline
This option reproduces the full data preprocessing workflow.
```bash
mkdir -p data/raw
kaggle datasets download -d thunvthun/house-price -p data/raw
unzip data/raw/house-price.zip -d data/raw
```
Expected file: `data/raw/gia_nha.csv`

Run the cleaning pipeline:
```bash
export PYTHONPATH=$PYTHONPATH:.
python3 run_pipeline_clean.py
```
Output: `data/staging/data_sau_clean.csv`

#### Option 2: Use Cleaned Data Directly (Skip Cleaning)
This option is recommended if you only want to reproduce training and evaluation results.
```bash

kaggle datasets download -d thunvthun/house-price -p data/staging
unzip data/staging/house-price.zip -d data/staging
```
Use the following file directly: `data/staging/data_sau_clean.csv`

### Model Training and Evaluation
Once `data_sau_clean.csv` is available (from Option 1 or Option 2), run:

```bash
export PYTHONPATH=$PYTHONPATH:.

# Baseline model
python3 src/pipelines/train_baseline.py

# Linear regression models
python3 src/pipelines/train_linear.py

# Tree-based models
python3 src/pipelines/train_tree.py

# Custom MLP model
python3 src/pipelines/train_mlp.py
```

## Configuration
Major parameters are managed in `config.yaml`:
- **CRAWL**: Paging, batch size, and sleep intervals for web scraping.
- **File Paths**: Global paths for raw data and database objects.
- **Model Params**: Hyperparameters for the Custom MLP can be found in `src/config/default.yaml`.

## Output / Results
- **Models**: Serialized files in `models/` (e.g., `mlp_model.joblib`).
- **Reports**: Statistical plots and performance figures in `reports/figures/`.
- **Data**: Final processed dataset in `data/staging/data_sau_clean.csv`.

## Logging & Reproducibility
- **Logging**: The project uses the standard Python `logging` module. Console outputs provide real-time counts of processed vs. dropped records. Logs are also persisted in the `logs/` directory.
- **Reproducibility**:
  - Seeds are fixed for train/test splits.
  - Transformation logic is versioned within `src/data/clean/`.
  - The pipeline architecture ensures that starting from the same `data/raw/` file will always yield identical metrics.

## Notes / Limitations
- Web scraping modules require a compatible Chrome driver and local browser profile.
- The `CustomMLP` implementation is a pure NumPy/Standard-lib approach for research transparency; for large-scale production, a framework like PyTorch/TensorFlow is recommended.

## License
MIT License
