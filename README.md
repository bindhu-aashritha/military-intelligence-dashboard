# AI-BASED MILITARY INTELLIGENCE DASHBOARD
## Predictive Modelling, Spatial Analytics, and Automated SITREP Generation

An enterprise-grade defense analytics platform built on the Global Terrorism Database (GTD). This application transforms raw, complex kinetic incident data into actionable tactical intelligence through geospatial threat mapping, machine learning predictions, explainable AI metrics, and automated Situation Report (SITREP) generation.

---

## OVERVIEW AND OBJECTIVES

Kinetic threat assessment requires rapid data processing and actionable insights. This project bridges machine learning engineering and tactical usability by providing defense analysts with an interactive suite for real-time monitoring and threat assessment.  

### Core Objectives:
* **Geospatial Threat Mapping:** Real-time location tracking and density or hotspot identification weighted by incident casualties.  
* **Machine Learning Predictive Models:** Automated inference pipelines for identifying tactical attack vectors and assessing threat severity levels.  
* **Explainable AI (XAI):** Transparent model decision-making via dynamic feature importance and detailed classification reports.  
* **Automated Intelligence SITREPs:** Instant generation of ISO-timestamped Situation Reports, downloadable in `.md` and `.txt` formats.  

---
Dashboard – Global Security Summary
Description: Displays macro-level intelligence metrics across the global dataset, highlighting total logged incidents, casualties, and impacted sovereign nations. The accompanying line chart highlights operational trends over time.
<img width="1001" height="418" alt="image" src="https://github.com/user-attachments/assets/2777f6f6-7063-4d0f-9453-cad4e509e23c" />

Global Threat Map – Scatter Mapbox View
Description: Illustrates individual geolocated kinetic attacks globally using Mapbox scatter visualization. Incident markers are color-coded by specific tactical attack types to provide real-time spatial awareness of operational methods across regions.
<img width="1013" height="626" alt="image" src="https://github.com/user-attachments/assets/aa893854-5a98-41bb-ad28-dd8dd59f2aae" />

Global Threat Map – Density Hotspot Assessment
Description: Visualizes localized threat concentrations via a Mapbox density heatmap weighted by casualty severity (nkill). Dynamic hover tooltips expose latitude, longitude, and fatality counts, pinpointing high-impact operational zones across North Africa, the Middle East, and South Asia.
<img width="1119" height="544" alt="image" src="https://github.com/user-attachments/assets/5e371418-c665-4784-a6f5-3864ad19486e" />

Tactical Country Intelligence Analysis
Description: Provides localized country-level intelligence (e.g., India), breaking down total incidents, fatalities, injured, and active threat factions. Interactive line and pie charts track temporal attack velocity alongside tactical method proportions.
<img width="1103" height="482" alt="image" src="https://github.com/user-attachments/assets/cc1e1baf-f2cf-4fa4-8296-806c3dc16e69" />

Tactical Attack Vector Prediction Model UI
Description: Features the machine learning inference interface for tactical attack vector classification. Users input scenario variables (e.g., Target Country, Region, Weapon Type, Threat Faction, Mission Type) to execute the trained model, returning the predicted vector (e.g., Bombing/Explosion) along with a confidence metric.
<img width="1010" height="541" alt="image" src="https://github.com/user-attachments/assets/c43eec82-1cee-475e-8c5a-e97a6b7e707c" />

Long-Term Attack Forecasting Engine – Trajectory Plot
Description: Displays multi-year incident forecasting using historical time-series data. The visualization contrasts historical observed attack frequencies against the projected trajectory over a configurable 5-year forecast horizon.
<img width="1008" height="484" alt="image" src="https://github.com/user-attachments/assets/01e06998-6e77-429e-8ed4-d5a6955059c1" />
 
Long-Term Attack Forecasting Engine – Quantitative Metrics
Description: Summarizes projected incident counts year-over-year in a structured data table alongside high-level forecasting KPIs, including recent observed annual attacks, projected 5-year volume, and expected overall growth percentage.
<img width="1016" height="482" alt="image" src="https://github.com/user-attachments/assets/18b05747-c4f8-4af8-82f9-5b94fb923c4e" />

Automated AI Situation Report (SITREP) – Executive Briefing
Description: Shows the automated ISO-timestamped Situation Report generator. It aggregates key quantitative metrics (total incidents, casualties, affected nations) and primary intelligence insights (leading high-risk regions, dominant threat factions, primary tactical vectors).
<img width="1025" height="484" alt="image" src="https://github.com/user-attachments/assets/7d95b51c-3a62-4595-94a3-8bd17bab1ef8" />

Automated AI Situation Report (SITREP) – Risk Distribution & Export
Description: Highlights top high-risk sovereign areas and active threat factions through horizontal bar charts within the SITREP module. Actionable export buttons enable immediate downloading of formatted Markdown (.md) or plain text (.txt) operational briefings.
<img width="939" height="483" alt="image" src="https://github.com/user-attachments/assets/f356dfa3-f3df-4df1-ad06-fe28a2d38a51" />

Global Terrorism Data Explorer
Description: Presents an interactive data table allowing deep-dive inspection and filtering of raw incident records. Features side-panel multi-select filters for years, target countries, and attack types, with real-time record summaries and a CSV download capability.
<img width="983" height="431" alt="image" src="https://github.com/user-attachments/assets/9ea3b21c-72e6-4d8e-ac5c-873a6176323a" />

Operations and Settings Dashboard
Description: Shows the global configuration panel where operational defaults are managed. Users can set persistent target countries, map tile styles, forecasting horizons, confidence thresholds, and machine learning display settings across all dashboard views.
<img width="998" height="445" alt="image" src="https://github.com/user-attachments/assets/43f95b09-f31f-4486-94c1-0259eb1748af" />

## SYSTEM ARCHITECTURE AND WORKFLOW

The platform follows a modular, leak-free pipeline architecture to ensure data integrity and seamless user interface synchronization:  

1. **Data Ingestion:** Loads historical kinetic event records from the raw Global Terrorism Database CSV file.
2. **Preprocessing and Leakage Prevention:** Uses Scikit-Learn `ColumnTransformer` and `OrdinalEncoder` fitted only on training splits inside an `sklearn.pipeline.Pipeline` object.
3. **Artifact Serialization:** Trained models are serialized into binary `.pkl` files inside the `models/` folder using `joblib`.
4. **Dashboard Serving:** Streamlit loads the pre-trained pipelines to supply multi-page analytics and real-time predictions.
5. **Executive SITREP Export:** Converts live system insights directly into formatted Markdown (`.md`) or plain text (`.txt`) Situation Reports.  

---

## TECH STACK AND TECHNOLOGIES USED

* **Language:** Python 3.14
* **User Interface:** Streamlit (with reactive `st.session_state` management)
* **Machine Learning:** Scikit-Learn (`RandomForestClassifier`, `Pipeline`, `ColumnTransformer`, `OrdinalEncoder`)
* **Data Processing:** Pandas, NumPy
* **Visualization and Geospatial:** Plotly Express (`scatter_mapbox`, `density_mapbox`)
* **Model Serialization:** Joblib

---

## DATA SCHEMA AND FEATURE ENGINEERING

Key features engineered from the GTD dataset for training and prediction:

| Feature Name | Data Type | Encoding / Preprocessing Standard | Operational Role |
| :--- | :--- | :--- | :--- |
| `iyear` | Integer | Preserved for temporal filtering | Temporal Scope |
| `country_txt` | Categorical | `OrdinalEncoder(handle_unknown='use_encoded_value')` | Target Geography |
| `region_txt` | Categorical | `OrdinalEncoder(handle_unknown='use_encoded_value')` | Regional Scope |
| `weaptype1_txt` | Categorical | `OrdinalEncoder(handle_unknown='use_encoded_value')` | Weaponry Capability |
| `targtype1_txt` | Categorical | `OrdinalEncoder(handle_unknown='use_encoded_value')` | Target Category |
| `gname` | Categorical | `OrdinalEncoder(handle_unknown='use_encoded_value')` | Faction / Threat Actor |
| `nkill` | Numeric | Direct passthrough / Imputed | Fatality Count |
| `nwound` | Numeric | Direct passthrough / Imputed | Casualties Count |
| `attacktype1_txt` | Categorical | Target Class Variable | Attack Vector Target |
| `threat_level` | Categorical | Derived Binned Target (`nkill` + `nwound`) | Threat Severity Target |

### Threat Severity Index Calculation:
Threat level is calculated dynamically using casualty impact binning:
* **LOW:** Impact score less than or equal to 2 (Fatalities + Wounded)
* **MEDIUM:** Impact score between 3 and 10
* **HIGH:** Impact score greater than 10

---

## MACHINE LEARNING MODELS AND EVALUATION

### Attack Vector Prediction Model
* **Algorithm:** Random Forest Classifier (200 Estimators)
* **Inputs:** `country_txt`, `region_txt`, `weaptype1_txt`, `targtype1_txt`, `gname`, `success`, `suicide`
* **Target:** Tactical attack type (e.g., Bombing/Explosion, Armed Assault, Assassination)

### Threat Level Index Model
* **Algorithm:** Random Forest Classifier (200 Estimators)
* **Target:** Binned Threat Index (`LOW`, `MEDIUM`, `HIGH`)

### Model Explainability and Evaluation Metrics
* **Explainable AI (XAI):** Dynamic feature importance weight extraction (`rf_model.feature_importances_`) shown inline with predictions.
* **Evaluation Metrics:** Class-level validation performance inspected using `classification_report` outputting Precision, Recall, and F1-Score across threat classes.

---

## KEY OPERATIONAL MODULES AND PAGES

* **Global Threat Map (`pages/2_Global_Threat_Map.py`):** Interactive map toggled between Scatter Mapbox for individual events and Density Mapbox for heatmaps weighted by casualties.
* **Tactical Attack Prediction (`pages/4_Attack_Prediction.py`):** Multi-variable form for live inference, real-time confidence scores, decision weight charts, and evaluator metrics.
* **Threat Level Assessment (`pages/5_Threat_Level.py`):** Dynamic threat severity classification with output class probability distributions.
* **AI Intelligence Briefings (`pages/7_AI_Intelligence.py`):** Automated ISO-timestamped SITREP generator supporting downloadable `.md` and `.txt` files.  
* **Operations Settings (`pages/9_Setting.py`):** Centralized state management using `st.session_state` and `st.rerun()` to update global map themes and operational defaults across pages.

---

## GETTING STARTED AND INSTALLATION

### Prerequisites:
* Python 3.14 and above
* Git

### Step-by-Step Setup:

1. **Clone the Repository:**
   git clone [https://github.com/bindhu-aashritha/military-intelligence-dashboard.git](https://github.com/bindhu-aashritha/military-intelligence-dashboard.git)
   cd military-intelligence-dashboard
   
2. Set Up Virtual Environment:
Windows (PowerShell):
python -m venv venv
.\venv\Scripts\activate

4. Install Dependencies:
pip install -r requirements.txt
Data Placement:
Place the raw Global Terrorism Database CSV file at data/globalterrorism.csv.

5. Train Pipelines and Generate Models:
Run the training script to execute preprocessing and save model pipeline .pkl files:
python train_models.py

6. Run the Dashboard:
streamlit run app.py

## FUTURE ENHANCEMENTS
-Integration of SHAP (SHapley Additive exPlanations) values for deeper instance-level model explainability.
-Implementation of time-series forecasting algorithms (such as Prophet or ARIMA) for predicting monthly regional event frequency.
-Automated PDF report generation using ReportLab or HTML-to-PDF conversion tools.
