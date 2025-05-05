# Data Engineering Machine Learning Pipeline


---

## 🚀 Project Goals

- ✅ Automate fetching real-time trending YouTube data via the Kaggle API
- ✅ Perform robust ML-based imputation for missing data
- ✅ Store and serve cleaned data in PostgreSQL and AWS S3
- ✅ Orchestrate the end-to-end pipeline using Airflow
- ✅ Dockerize the pipeline for portability and reproducibility
- ✅ Showcase real-world data engineering skills in a GitHub-ready project

---

## 🔄 Data Pipeline Overview

### 1. 🧲 Data Ingestion

- **Script:** `scripts/fetch_data.py`
- **Source:** Kaggle Dataset [`datasnaek/youtube-new`](https://www.kaggle.com/datasets/datasnaek/youtube-new)
- **Auth:** `kaggle.json` via `/root/.kaggle` (set by environment variable `KAGGLE_CONFIG_DIR`)
- **Output:** Downloads and extracts country-wise `.csv` files → standardizes into `youtube_trending.csv`

### 2. 🧼 Data Cleaning & ML-Based Imputation

- **Script:** `notebooks/DataCleaning.py`
- **Library Used:** `scikit-learn`, `pandas`, `joblib`
- **Workflow:**
  - Automatically identifies categorical vs numerical features
  - Trains a `RandomForestRegressor` or `RandomForestClassifier` per column
  - Saves trained models into `notebooks/impute_models/`
  - Applies predictions to fill missing values
- **Command:** `fill_null_ML(df)` auto-triggers column-wise ML imputation

### 3. 🗃️ Load to PostgreSQL

- **Script:** `scripts/load_to_postgres.py`
- **Library:** `SQLAlchemy`
- **Database:** `PostgreSQL` (assumes local setup)
- **Table:** `trending_videos`
- **Note:** You must replace the DB connection URI with your credentials

### 4. ☁️ Upload to AWS S3

- **Script:** `scripts/upload_to_s3.py`
- **Library:** `boto3`
- **Bucket Name:** `youtube-trending-data-pipeline`
- **Environment:** Assumes AWS credentials are available via environment or `~/.aws/credentials`

---

## ⏱️ Workflow Orchestration with Airflow

- **DAG:** `airflow/dags/youtube_pipeline.py`
- **Services:** Airflow webserver, scheduler, and PostgreSQL via `airflow/docker-compose.yml`
- **Pipeline Tasks:**
  - `fetch_data` → `clean_with_ML` → `upload_to_postgres` → `upload_to_s3`

**Run Airflow:**

```bash
cd airflow
docker-compose up
```

## 🚢 Dockerized Environment

To make the project reproducible and easy to deploy, it is containerized using **Docker** and orchestrated using **Docker Compose**.

### 📄 `Dockerfile`

The `Dockerfile` sets up the Python environment and installs all necessary dependencies (as listed in `requirements.txt`), including:

- `pandas`, `numpy`, `scikit-learn` for data processing and ML
- `boto3` for AWS S3 interactions
- `sqlalchemy` for PostgreSQL loading
- `kaggle` API for dataset download
- `apache-airflow` for orchestration

### 🧱 `docker-compose.yml`

The `docker-compose.yml` file spins up the following services:

- **Airflow Scheduler**
- **Airflow Webserver**
- **Airflow Worker**
- **PostgreSQL Database**
- **Airflow Metadata Database**

All containers are networked together for seamless integration and automated pipeline execution.

### 🔧 How to Run Docker Compose

```bash
docker-compose up --build
```

Then visit Airflow UI at: [http://localhost:8080](http://localhost:8080)

## 📡 Airflow DAG: `youtube_pipeline.py`

The DAG defined in `airflow/dags/youtube_pipeline.py` automates the full ETL process:

1. **Fetch Data from Kaggle**  
   Downloads and extracts YouTube trending data using the Kaggle API.

2. **Clean & Impute Missing Values**  
   Uses `DataCleaning.py` to preprocess the dataset and fill missing values via ML models.

3. **Upload Clean Data to AWS S3**  
   Transfers the cleaned `.csv` to your S3 bucket using `upload_to_s3.py`.

4. **Load into PostgreSQL**  
   Inserts data into a PostgreSQL table using `load_to_postgres.py`.

### 🔁 Schedule

You can customize the frequency of the DAG from within the DAG definition (`schedule_interval`). This enables automated, periodic data ingestion and cleaning.

## 💡 Machine Learning-based Data Cleaning

To go beyond basic cleaning, the project uses **ML models to impute missing values** for both numerical and categorical columns.

### Main Script: `notebooks/DataCleaning.py`

- Detects column types (categorical or numerical).
- Trains either a `RandomForestClassifier` or `RandomForestRegressor` based on column type.
- Uses only columns with no missing values as features.
- Serializes trained models using `joblib`.
- Applies trained models to predict missing values.

### Benefits:
- More accurate and intelligent filling of missing data.
- Dynamic and scalable — works on any DataFrame with minimal setup.

## ☁️ AWS S3 Integration

The pipeline supports cloud data storage using **Amazon S3**.

### 🔐 Authentication

Make sure to set up your AWS credentials in `~/.aws/credentials` or via environment variables:

```bash
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret
```

### ☁️ Bucket Upload

The `upload_to_s3.py` script uploads the cleaned dataset to:

```
s3://youtube-trending-data-pipeline/youtube_trending.csv
```

## 🗃️ PostgreSQL Integration

We use **SQLAlchemy** to push the cleaned dataset into a PostgreSQL table.

- Connection string:
```
postgresql://user:password@localhost:5432/youtube
```

- Table name:
```
trending_videos
```

### 📄 Schema Definition

See `sql/create_tables.sql` for manual schema setup, if needed.

## 📊 Jupyter Notebooks

- Exploratory analysis and visualization are handled in `notebooks/analysis.ipynb`.
- You can use it to:
  - Analyze view counts, likes/dislikes
  - Study trends by country, category
  - Detect outliers or bot behavior

## 🔐 Kaggle API Integration

To use Kaggle’s API:

1. Go to [Kaggle Account Settings](https://www.kaggle.com/account)
2. Click on "Create New API Token"
3. Save the downloaded `kaggle.json` file to `.kaggle/` or `/root/.kaggle/` inside Docker
4. Authenticate using:

```python
from kaggle.api.kaggle_api_extended import KaggleApi
api = KaggleApi()
api.authenticate()
```

## 🧪 Requirements

All dependencies are listed in `requirements.txt`. You can install them manually with:

```bash
pip install -r requirements.txt
```

Or rely on Docker to handle the environment setup.

## 🚀 Project Structure Overview

```
└── 📁YoutubeTrends_DataEngineering
        └── config
        └── description
        └── FETCH_HEAD
        └── HEAD
        └── 📁hooks
            └── applypatch-msg.sample
            └── commit-msg.sample
            └── fsmonitor-watchman.sample
            └── post-update.sample
            └── pre-applypatch.sample
            └── pre-commit.sample
            └── pre-merge-commit.sample
            └── pre-push.sample
            └── pre-rebase.sample
            └── pre-receive.sample
            └── prepare-commit-msg.sample
            └── push-to-checkout.sample
            └── update.sample
        └── 📁info
            └── exclude
        └── 📁objects
            └── 📁info
            └── 📁pack
        └── 📁refs
            └── 📁heads
            └── 📁tags
    └── 📁.kaggle
        └── kaggle.json
    └── 📁airflow
        └── 📁dags
            └── youtube_pipeline.py
        └── docker-compose.yml
    └── 📁data
        └── CA_category_id.json
        └── CAvideos.csv
        └── DE_category_id.json
        └── DEvideos.csv
        └── FR_category_id.json
        └── FRvideos.csv
        └── GB_category_id.json
        └── GBvideos.csv
        └── IN_category_id.json
        └── INvideos.csv
        └── JP_category_id.json
        └── JPvideos.csv
        └── KR_category_id.json
        └── KRvideos.csv
        └── MX_category_id.json
        └── MXvideos.csv
        └── RU_category_id.json
        └── RUvideos.csv
        └── US_category_id.json
        └── USvideos.csv
        └── youtube_trending.csv
        └── youtube-new.zip
    └── 📁kaggle
        └── .DS_Store
        └── kaggle.json
    └── 📁notebooks
        └── 📁__pycache__
            └── DataCleaning.cpython-311.pyc
        └── analysis.ipynb
        └── DataCleaning.py
        └── 📁impute_models
    └── 📁scripts
        └── .DS_Store
        └── .gitignore
        └── fetch_data.py
        └── load_to_postgres.py
        └── upload_to_s3.py
    └── 📁sql
        └── create_tables.sql
    └── .DS_Store
    └── .gitignore
    └── docker-compose.yml
    └── Dockerfile
    └── README.md
    └── requirements.txt
```

## 📌 Next Steps & Ideas

- Add unit tests and logging
- Build a dashboard (e.g., using Streamlit or Superset)
- Apply anomaly detection on trending metrics
- Schedule weekly Airflow runs for continuous monitoring

## 🤝 Contributing

Feel free to fork, open issues, and submit pull requests!

## 📝 License

This project is licensed under the MIT License.
