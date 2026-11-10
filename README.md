# PashuSeva

## Project Overview

PashuSeva is a dairy animal care information platform designed to provide reliable, source-based information about animal feeding, calf rearing, vaccination, and common diseases.

The project uses information from trusted dairy farming resources such as NDDB Farmers' Corner and the Handbook of Good Dairy Husbandry Practices.

The current prototype focuses on dairy animal feeding information and provides data analysis, smart search, and API-based access to records.

## Target User

A small woman dairy farmer in Rahata who owns three crossbred cows and one calf, sells milk to the village dairy society, and wants to reduce feed costs and prevent repeated mastitis.

## Problem Statement

Small dairy farmers often struggle to find reliable and easy-to-understand information about animal nutrition, calf care, vaccination schedules, and common diseases.

Incorrect feeding practices and delayed disease management can increase costs and affect milk production.

## Project Objective

To provide accessible, source-based dairy animal care information and practical guidance for small dairy farmers across India.

## Data Sources

- NDDB Farmers' Corner
- Handbook of Good Dairy Husbandry Practices

## Project Features

- Dairy animal feeding information
- JSON-based record storage
- Data ingestion and processing
- PDF document downloading
- Data analysis using Pandas
- Smart search using TF-IDF and cosine similarity
- FastAPI-based REST API
- Question-based information retrieval

## Project Structure

```text
GEN-AI-TRAINING/
│
├── app/
│   ├── cli.py
│   ├── fetch.py
│   ├── ingest.py
│   ├── models.py
│   ├── records.py
│   ├── smart_search.py
│   └── main.py
│
├── analysis/
│   └── explore.py
│
├── data/
│   ├── raw/
│   ├── downloads/
│   ├── records.json
│   └── sample_records.py
│
├── requirements.txt
└── README.md
```

## Technologies Used

- Python
- FastAPI
- Pandas
- Scikit-learn
- TF-IDF
- Cosine Similarity
- JSON
- Requests
- Uvicorn
- Git and GitHub

## How to Run PashuSeva

### 1. Clone the Repository

```bash
git clone https://github.com/shravani28-18/GEN-AI-TRAINING.git
cd GEN-AI-TRAINING
```

### 2. Create a Virtual Environment (Optional)

```bash
python -m venv venv
```

Activate the environment on Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run Data Analysis

```bash
python -m analysis.explore
```

This displays:

- Total number of records
- Records grouped by topic
- Records grouped by animal type

### 5. Start the FastAPI Server

```bash
python -m uvicorn app.main:app --reload
```

### 6. Open API Documentation

Open the following URL in your browser:

http://127.0.0.1:8000/docs

## Available API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Check API status |
| GET | `/records?limit=5` | Retrieve records |
| GET | `/records/{id}` | Retrieve a record by ID |
| GET | `/search?q=green%20fodder` | Search records using smart search |
| POST | `/questions` | Ask an animal-care question |

## Example Question Request

POST `/questions`

Request Body:

```json
{
    "question": "How much green fodder should I feed?"
}
```

The API searches the available records and returns the most relevant recommendation with its source information.

## Data Analysis

The project uses Pandas to analyse the available PashuSeva records.

The analysis includes:

1. Total number of records.
2. Number of records under each topic.
3. Number of records for each animal type.

## Smart Search

PashuSeva uses TF-IDF (Term Frequency-Inverse Document Frequency) and cosine similarity to identify records relevant to a farmer's question.

The search results are ranked according to