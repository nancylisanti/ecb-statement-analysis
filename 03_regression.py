from pathlib import Path
import pandas as pd
import statsmodels.api as sm

from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.stats.diagnostic import het_breuschpagan

# Cartella in cui si trova questo script
folder = Path(".")
dataset_file = folder / "Dataset_Regressione_Finale.xlsx"
df = pd.read_excel(dataset_file)

# Variabile dipendente
y = df["Delta_MRO"]

# Variabili indipendenti
X = df[["AI_Index", "Inflation", "Euribor_1M", "VSTOXX"]]

# Aggiungiamo la costante alpha
X = sm.add_constant(X)

# Stima OLS
model = sm.OLS(y, X).fit()
print("\n==============================")
print("MODELLO PRINCIPALE")
print("==============================")
print(model.summary())

# ==========================
# CONTROLLI DIAGNOSTICI
# ==========================

# 1. Matrice di correlazione
print("\nMatrice di correlazione:")
corr = df[["AI_Index", "Inflation", "Euribor_1M", "VSTOXX"]].corr()
print(corr)

# 2. VIF
print("\nVIF:")
vif_data = pd.DataFrame()
vif_data["Variable"] = X.columns
vif_data["VIF"] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
print(vif_data)

# 3. Regressione con errori standard robusti HC3
print("\nOLS con errori standard robusti HC3:")
robust_model = model.get_robustcov_results(cov_type="HC3")
print(robust_model.summary())

# 4. Test Breusch-Pagan
print("\nBreusch-Pagan test:")
bp_test = het_breuschpagan(model.resid, model.model.exog)

bp_labels = ["LM Statistic", "LM p-value", "F Statistic", "F p-value"]
print(dict(zip(bp_labels, bp_test)))

print(df.describe())

print("\n==============================")
print("MODELLO 1 - SOLO AI_INDEX")
print("==============================")

X1 = sm.add_constant(df[["AI_Index"]])
m1 = sm.OLS(y, X1).fit()
print(m1.summary())


print("\n==============================")
print("MODELLO 2 - AI + INFLATION")
print("==============================")

X2 = sm.add_constant(df[["AI_Index", "Inflation"]])
m2 = sm.OLS(y, X2).fit()
print(m2.summary())


print("\n==============================")
print("MODELLO 3 - AI + INFLATION + EURIBOR")
print("==============================")

X3 = sm.add_constant(df[["AI_Index", "Inflation", "Euribor_1M"]])
m3 = sm.OLS(y, X3).fit()
print(m3.summary())


print("\n==============================")
print("MODELLO 4 - MODELLO COMPLETO")
print("==============================")

X4 = sm.add_constant(df[["AI_Index", "Inflation", "Euribor_1M", "VSTOXX"]])
m4 = sm.OLS(y, X4).fit()
print(m4.summary())

# ==========================
# TABELLA FINALE REGRESSIONI
# ==========================

regression_table = pd.DataFrame({
    "Model 1": [
        m1.params.get("AI_Index"),
        m1.pvalues.get("AI_Index"),
        None,
        None,
        None,
        None,
        None,
        None,
        m1.rsquared,
        m1.rsquared_adj,
        int(m1.nobs)
    ],
    "Model 2": [
        m2.params.get("AI_Index"),
        m2.pvalues.get("AI_Index"),
        m2.params.get("Inflation"),
        m2.pvalues.get("Inflation"),
        None,
        None,
        None,
        None,
        m2.rsquared,
        m2.rsquared_adj,
        int(m2.nobs)
    ],
    "Model 3": [
        m3.params.get("AI_Index"),
        m3.pvalues.get("AI_Index"),
        m3.params.get("Inflation"),
        m3.pvalues.get("Inflation"),
        m3.params.get("Euribor_1M"),
        m3.pvalues.get("Euribor_1M"),
        None,
        None,
        m3.rsquared,
        m3.rsquared_adj,
        int(m3.nobs)
    ],
    "Model 4": [
        m4.params.get("AI_Index"),
        m4.pvalues.get("AI_Index"),
        m4.params.get("Inflation"),
        m4.pvalues.get("Inflation"),
        m4.params.get("Euribor_1M"),
        m4.pvalues.get("Euribor_1M"),
        m4.params.get("VSTOXX"),
        m4.pvalues.get("VSTOXX"),
        m4.rsquared,
        m4.rsquared_adj,
        int(m4.nobs)
    ]
}, index=[
    "AI_Index coef.",
    "AI_Index p-value",
    "Inflation coef.",
    "Inflation p-value",
    "Euribor_1M coef.",
    "Euribor_1M p-value",
    "VSTOXX coef.",
    "VSTOXX p-value",
    "R-squared",
    "Adjusted R-squared",
    "Observations"
])

regression_table.to_excel("Regression_Table.xlsx")

print("Regression_Table.xlsx creato correttamente.")