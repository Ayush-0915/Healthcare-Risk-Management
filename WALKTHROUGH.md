# Technical Walkthrough - Healthcare Risk Management Analytics System

This walkthrough provides a comprehensive developer and analyst guide to the codebase, methodologies, and engineering decisions implemented in the **Healthcare Risk Management Analytics System**.

---

## 📖 Introduction

This project is a data engineering, predictive modeling, and analytics application designed to translate high-dimensional clinical records into actionable intelligence. The core application provides:
1.  **Exploratory Insights**: Helping healthcare executives understand cohorts, patient demographics, and billing distributions.
2.  **Risk Segmentation**: Identifying vulnerable cohorts (high & critical risk) to prioritize care and resource allocation.
3.  **Predictive Risk Inference**: Querying a regularized Machine Learning classifier to estimate a patient's risk category on or prior to admission.

---

## 📂 Folder Explanation

The project is structured logically to separate concerns between raw assets, data pickles, notebooks, application modules, and layouts:

*   **`.streamlit/`**: Streamlit environment settings. Contains `config.toml`, which configures the dark theme colors and disables the default sidebar page navigation list to allow our custom navbar to handle page routing.
*   **`assets/`**: Contains branding assets, including the sidebar logo and page background templates.
*   **`components/`**: Clean, reusable UI modules:
    *   `cards.py`: Generates custom HTML/CSS glassmorphic KPI panels, info cards, and pill badges.
    *   `footer.py`: Standardized global page footer.
    *   `hero.py`: Renders the high-impact base64 image-coded hero container on the home page.
    *   `plotly_theme.py`: Programmatically applies an `'Inter'` typography grid, unified legend, Sky-cyan SaaS colors, and custom hover borders to all Plotly figures.
    *   `sidebar.py`: Builds the main glassmorphic navigation panel using `st.sidebar.page_link`.
    *   `theme.py`: Custom CSS injector that reads `style.css` and injects style blocks into Streamlit container grids.
*   **`data/`**: Centralized storage for CSV files and pickled models.
*   **`notebooks/`**: Chronological workflow files from data cleaning, EDA, and statistical risk analysis to model training.
*   **`pages/`**: Single-page modules representing the different functional blocks of the SaaS platform.
*   **`app.py`**: The application's landing page and platform overview.
*   **`style.css`**: Core design system containing style classes for colors, gradients, rounded cards, scrollbars, expanders, and page link hover effects.

---

## 📓 Notebook & Analysis Pipeline

The analytic foundation of the project resides in the `notebooks/` directory. Each notebook represents a discrete stage in the lifecycle of the data project:

### 1. Data Cleaning (`01_Data_Cleaning.ipynb`)
*   **Goal**: Standardize column names, handle missing data, strip Whitespace, and format fields.
*   **ETL Steps**:
    *   Duplicate rows are identified and dropped.
    *   `Date of Admission` and `Discharge Date` are parsed into pandas `datetime` format.
    *   The `Length of Stay` feature is engineered as:
        $$\text{Length of Stay} = \text{Discharge Date} - \text{Date of Admission (in days)}$$
    *   Text values in clinical columns (like Hospital, Medical Condition, Medication, Test Results) are stripped of extra spaces and converted to title case.
*   **Risk Score Engineering**: 
    A synthetic `Risk Score` (ranging 0 to 3) is generated to act as our training target:
    $$\text{Senior Citizen} = (\text{Age} \geq 65)$$
    $$\text{Emergency Admission} = (\text{Admission Type} == \text{'Emergency'})$$
    $$\text{Abnormal Test} = (\text{Test Results} == \text{'Abnormal'})$$
    $$\text{Risk Score} = \text{Senior Citizen} + \text{Emergency Admission} + \text{Abnormal Test}$$
    The score is mapped to `Risk Category` levels: `0 -> Low`, `1 -> Medium`, `2 -> High`, `3 -> Critical`.

### 2. Exploratory Data Analysis (`02_EDA.ipynb`)
*   **Goal**: Profile patient distributions and identify raw correlations.
*   **Visualizations**:
    *   Histograms to verify normal/uniform distributions of age and length of stay.
    *   Pie charts showing gender distribution.
    *   Bar charts representing medical condition frequencies, insurance provider market shares, and hospital volumes.

### 3. Risk Analysis (`03_Risk_Analysis.ipynb`)
*   **Goal**: Study the relationships between patient cohorts and the engineered risk levels.
*   **Insights**:
    *   A breakdown of risk levels across admission types, hospitals, and gender categories.
    *   Analyses showing billing amount and length of stay variance across different risk categories.

### 4. Machine Learning (`04_Machine_Learning.ipynb`)
*   **Goal**: Train, tune, and evaluate a predictive model to classify a patient's risk category.
*   **Audit for Target Leakage**: 
    The initial model used `Age`, `Admission Type`, and `Test Results` to predict `Risk Category`. Since these three columns directly calculate the target, the model achieved a trivial 100% accuracy.
    To eliminate this leakage, we updated the feature matrix to:
    $$\text{Features} = \{\text{Age}, \text{Gender}, \text{Blood Type}, \text{Medical Condition}, \text{Medication}, \text{Length of Stay}\}$$
    We dropped `Admission Type` and `Test Results` because they act as direct target leaks and are logistics/post-admission outcomes that are not typically available when predicting patient risk on arrival.
*   **Model Tuning & Size Optimization**:
    An unconstrained Random Forest model created a huge pickle file of **72.9 MB**.
    To find the optimal classifier, we benchmarked 10 algorithms (`Logistic Regression`, `Decision Tree`, `Random Forest`, `Extra Trees`, `Gradient Boosting`, `HistGradientBoosting`, `AdaBoost`, `Linear SVM`, `KNN`, and `Naive Bayes`) using **Stratified 5-Fold Cross-Validation** on the training set and an independent **80/20 train/test split**.
    The cross-validation confirmed that **Random Forest Classifier** with hyperparameters `n_estimators=100`, `max_depth=10`, and `min_samples_leaf=5` yielded the highest CV accuracy (**46.22%**) and test accuracy (**45.50%**), making it our final choice. This regularization reduced the model footprint to **11.04 MB** (a **84.8% size reduction**).

    > [!NOTE]
    > Since the dataset columns are generated independently using Faker, features other than Age have exactly zero physical correlation with the risk labels. The model correctly focuses on the Age threshold ($\text{Age} \geq 65$, contributing 77.4% of feature importance) to separate patient categories. The project focuses on demonstrating data engineering pipelines, leakage audits, and cross-validation workflows rather than fabricating high scores.

---

## 💻 Dashboard Explanation

The Streamlit web application is divided into pages under the `pages/` directory:

1.  **Home Page (`app.py`)**: Features a high-impact base64 image hero banner, 4 global KPI panels, a module index showing platform capabilities, and a raw dataset snapshot.
2.  **Executive Dashboard (`pages/1_📊_Executive_Dashboard.py`)**: Offers multi-parameter filters (gender, risk, admission) and renders 6 responsive Plotly figures detailing risk ratios, monthly trends, top diseases, billing aggregates, and length of stay box plots.
3.  **Patient Explorer (`pages/2_🏥_Patient_Explorer.py`)**: Lists patient records with live sorting and text searches. Supports CSV exports of the filtered search grids.
4.  **Risk Analysis (`pages/3_🚨_Risk_Analysis.py`)**: Isolates high-risk cohorts and renders risk distributions, crosstabs, and medical summaries.
5.  **ML Predictions (`pages/4_🤖_ML_Predictions.py`)**: Form-driven inference where users input patient features and receive a predicted risk level and clinical advice.
6.  **Advanced Analytics (`pages/5_📈_Advanced_Analytics.py`)**: Renders high-volume analytics including healthcare benchmarks and medication counts.
7.  **About (`pages/6_ℹ️_About.py`)**: Full technical specifications, data details, and developer profiles.

---

## 🚀 Deployment Process

The app is optimized for deployment on **Streamlit Community Cloud**:
1.  Push the codebase to GitHub.
2.  Log in to [share.streamlit.io](https://share.streamlit.io/).
3.  Select the repository, the `main` branch, and `app.py` as the entry file path.
4.  Deploy. Streamlit Cloud reads `requirements.txt`, installs dependencies, and serves the application.
5.  The custom `.streamlit/config.toml` configures theme layouts and hides default sidebars, ensuring the live version matches your local environment.

---

## 🧠 Challenges, Lessons Learned & Roadmap

### Challenges Faced
*   **Target Leakage**: The initial pipeline's 100% accuracy model looked impressive, but was unusable because it relied on the direct components of the target label. Fixing this required rethinking the clinical scenario to focus on pre-admission inputs.
*   **Model Pickle Size**: A 73 MB model file is too large for GitHub and slows down Streamlit Cloud builds. Regularizing the tree depth and leaf samples successfully solved this problem.

### Lessons Learned
*   **Regularization**: Regularization is critical for both model generalization and optimizing model size in production deployments.
*   **Streamlit Configuration**: Using native configuration parameters like `showSidebarNavigation = false` under `[client]` in `config.toml` is much more robust than relying on custom CSS classes to modify Streamlit layouts.

### Future Roadmap
1.  Implement **Explainable AI (XAI)** using SHAP plots in the ML Predictions tab.
2.  Connect to a secure relational database (e.g. PostgreSQL) instead of static CSV files.
3.  Integrate PDF report generators so clinical staff can print risk cards.
