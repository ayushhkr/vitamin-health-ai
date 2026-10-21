# Vitamin D Prediction Module

A reproducible Vitamin D level regression project and Streamlit interface. This is the first module of the planned Vitamin D and B12 final-year project.

## Data and integrity

`data/VitaminD_Dataset.csv` is the 10,000-row custom CSV copied from the supplied legacy repository. That repository does not document whether it is synthetic, so generated reports label its provenance as **custom dataset; synthetic status not documented**. Do not present its metrics as clinical performance.

The regression target is `VitaminD_Level_ng_ml`. `VitaminD_Category`, `Deficiency_Status`, and `Risk_Score` are excluded before any split, preprocessing, cross-validation, or prediction.

## Run

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m src.train
.\.venv\Scripts\streamlit.exe run app.py
```

## Streamlit experience and optional AI assistant

The Streamlit app provides a quick estimate and a detailed analysis view with
transparent lifestyle explanations, recommendations, and prediction-based
what-if scenarios. All predictions, including the scenarios, use the saved
pipeline through `src.predict`; they do not modify training or evaluation.

The detailed view also includes an optional OpenAI chat assistant. Set its key
in the process environment before starting Streamlit:

```powershell
$env:OPENAI_API_KEY = "your-key"
.\.venv\Scripts\streamlit.exe run app.py
```

The key is never requested in the interface, stored in source code, or read
from an `.env` file. If `OPENAI_API_KEY` is unavailable, the chat continues in
offline, rule-based guidance mode. Responses are educational only and are not
medical diagnoses or supplement prescriptions.

Training makes an 80/20 held-out split, compares Linear Regression, Random Forest, XGBoost, and CatBoost with five-fold shuffled cross-validation on the training data, then saves:

- `models/vitamin_d_pipeline.joblib` — best fully fitted preprocessing and model pipeline
- `models/metadata.json` — input schema and data provenance
- `reports/model_metrics.csv` — CV and holdout R², MAE, and RMSE
- `reports/holdout_predictions.csv` — predictions for the untouched holdout set

The winning model is selected by mean cross-validation RMSE. The holdout set is used once for reporting.
