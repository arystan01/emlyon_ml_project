# Credit Risk Assessment

ML model to predict credit risk using LightGBM and Streamlit for deployment.

### 1. Clone repo
```bash
git clone <https://github.com/arystan01/emlyon_ml_project>
cd emlyon_ml_project
```

### 2. Create conda environment
```bash
conda env create -f environment.yml
```

### 3. Activate environment
```bash
conda activate credit_risk
```

### 4. Demo 
```bash
streamlit run app.py
```

## Project structure

```
emlyon_ml_project/
├── app.py                  # Streamlit
├── environment.yml         # Conda environment
├── notebooks/              # jupyter notebooks
│    ├── 00_Draft.ipynb
│    ├── 01_EDA.ipynb
│    ├── 02_Preprocessing.ipynb
│    └── 03_Modeling.ipynb
├── models/
│    └── best_lgbm.pkl       # best model
└── data/                    # data
```
