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
