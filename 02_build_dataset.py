from pathlib import Path
import pandas as pd

# Cartella di lavoro
folder = Path(".")

# File di input
index_file = folder / "Pesci_Index.xlsx"
mro_file = folder / "ECB Data Portal_20260705171628.csv"

# Lettura dataset con indici
df_index = pd.read_excel(index_file)

# Lettura serie BCE MRO
df_mro = pd.read_csv(mro_file)

# Manteniamo solo le colonne necessarie della serie MRO
df_mro = df_mro.iloc[:, [0, 2]]
df_mro.columns = ["date", "MRO_Rate"]

# Convertiamo le date
df_index["date"] = pd.to_datetime(df_index["date"])
df_mro["date"] = pd.to_datetime(df_mro["date"])

# Uniamo dataset indici e tasso MRO
df = pd.merge(
    df_index,
    df_mro,
    on="date",
    how="left"
)

# Costruiamo il tasso due meeting dopo
df["MRO_t2"] = df["MRO_Rate"].shift(-2)

# Variabile dipendente della regressione
df["Delta_MRO"] = df["MRO_t2"] - df["MRO_Rate"]

# ==========================
# LETTURA FILE INFLAZIONE
# ==========================

inflation_file = folder / "Inflation_HICP.csv"

df_inflation = pd.read_csv(inflation_file, low_memory=False)

# Manteniamo solo Area Euro
df_inflation = df_inflation[df_inflation["geo"] == "EA"]

# Manteniamo solo l'inflazione generale (Headline HICP)
df_inflation = df_inflation[df_inflation["coicop"] == "CP00"]

# Manteniamo solo le colonne necessarie
df_inflation = df_inflation[
    [
        "TIME_PERIOD",
        "OBS_VALUE"
    ]
]

# Rinominiamo
df_inflation.columns = ["month", "Inflation"]

# Convertiamo il mese
df_inflation["month"] = pd.to_datetime(
    df_inflation["month"]
).dt.to_period("M")


# Lettura file Euribor 1M
euribor_file = folder / "Euribor_1M.csv"

df_euribor = pd.read_csv(euribor_file)

# Manteniamo solo le colonne necessarie
df_euribor = df_euribor[
    [
        "DATE",
        "Euribor 1-month - Historical close, average of observations through period (FM.M.U2.EUR.RT.MM.EURIBOR1MD_.HSTA)"
    ]
]

# Rinominiamo
df_euribor.columns = ["date", "Euribor_1M"]

# Convertiamo la data
df_euribor["date"] = pd.to_datetime(df_euribor["date"])


# Lettura file VSTOXX
vstoxx_file = folder / "VSTOXX.txt"

df_vstoxx = pd.read_csv(vstoxx_file, sep=";")

# Manteniamo solo data e valore VSTOXX
df_vstoxx = df_vstoxx[["Date", "Indexvalue"]]

# Rinominiamo
df_vstoxx.columns = ["date", "VSTOXX"]

# Convertiamo la data
df_vstoxx["date"] = pd.to_datetime(df_vstoxx["date"], format="%d.%m.%Y")

print(df_vstoxx.head())

# Filtro periodo di analisi
start_date = "2022-01-01"
end_date = "2024-12-31"

df_euribor = df_euribor[
    (df_euribor["date"] >= start_date) &
    (df_euribor["date"] <= end_date)
]

df_vstoxx = df_vstoxx[
    (df_vstoxx["date"] >= start_date) &
    (df_vstoxx["date"] <= end_date)
]

# Creiamo la colonna mese per il dataset principale e per Euribor
df["month"] = df["date"].dt.to_period("M")
df_euribor["month"] = df_euribor["date"].dt.to_period("M")


# Merge inflazione
df = pd.merge(
    df,
    df_inflation,
    on="month",
    how="left"
)

# Merge Euribor per mese
df = pd.merge(
    df,
    df_euribor[["month", "Euribor_1M"]],
    on="month",
    how="left"
)

# Merge VSTOXX
df = pd.merge(df, df_vstoxx, on="date", how="left")

print(df[["date", "AI_Index", "Delta_MRO", "Inflation", "Euribor_1M", "VSTOXX"]])

# Manteniamo solo le osservazioni complete 
df = df.dropna()

# Eliminiamo la colonna month (non serve più)
df = df.drop(columns=["month"])

# Manteniamo solo la data (senza orario)
df["date"] = df["date"].dt.date

df.to_excel("Dataset_Regressione_Finale.xlsx", index=False)

print("Dataset_Regressione_Finale.xlsx creato correttamente.")