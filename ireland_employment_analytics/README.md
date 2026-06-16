# 🇮🇪 Ireland Employment Analytics Pipeline

End-to-end modern data stack project analysing Irish employment and earnings trends using official CSO Ireland government data.

## 📊 Project Overview

Built a production-grade analytics pipeline that ingests, transforms, and visualises 144,156 rows of Irish employment data spanning 2008–2026 across all major economic sectors.

**Key Finding:** IT and Financial Services sectors have seen the strongest earnings growth in Ireland over the past decade, with average weekly earnings growing significantly faster than the national average.

## 🛠️ Tech Stack

| Layer | Tool | Purpose |
|---|---|---|
| Data Source | CSO Ireland (cso.ie) | Official government employment data |
| Ingestion | Python + Pandas | Download and load raw CSV data |
| Storage | Snowflake | Cloud data warehouse |
| Transformation | dbt Core | Bronze → Silver → Gold medallion architecture |
| Data Quality | dbt tests | 10 automated data quality tests |
| Documentation | dbt docs | Auto-generated lineage diagram |
| Visualisation | Power BI | Interactive dashboard |

## 🏗️ Architecture
## 📸 Lineage Diagram

![dbt Lineage Diagram](https://raw.githubusercontent.com/VamshiKondra77/ireland-employment-analytics/main/ireland_employment_analytics/images/lineage.png)