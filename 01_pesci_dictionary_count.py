# importazione librerie necessarie
from pathlib import Path
import pandas as pd

# cartella di lavoro
folder = Path(".")

# Individua tutti i file .txt e li ordina cronologicamente
txt_files = sorted(folder.glob("*.txt"))

# Crea una lista che conterrà tutti i dati di tutti gli statement
data = []

# Legge ogni file di testo e ne salva data, nome e contenuto
for file in txt_files:
    text= file.read_text(encoding="cp1252")
    data.append ({
        "date": file.stem,
        "filename": file.name,
        "text": text
    })

    # Converte la lista in un DataFrame Pandas
    df = pd.DataFrame(data)

    # Elimina eventuali spazi indesiderati nei nomi delle colonne
df.columns = df.columns.str.strip()

# dizionario 
hawkish_terms = [
    "hik", "increas", "ris", "tighten", "rais"
]

dovish_terms = [
    "cut", "decreas", "reduc", "eas",
]

neutral_terms = [
    "remain on hold",
    "remain steady",
    "remain unchanged",
    "stand pat",
    "no change",
    "no hint",
    "no hurry",
    "no move",
    "no signal",
    "wait and see",
    "wait-and-see"
]

# Funzione che conta il numero di occorrenze delle parole del dizionario
def count_terms(text, terms) :
    text =text.lower()
    total =0
    for term in terms:
        total += text.count(term)

    return total

# calcolo il numero di parole H, D e N per ciascuno statement
df["H"] = df["text"].apply(lambda x: count_terms(x, hawkish_terms))
df["D"] = df["text"].apply(lambda x: count_terms(x, dovish_terms))
df["N"] = df["text"].apply(lambda x: count_terms(x, neutral_terms))


# Calcolo Indice di Pesci 
df["Pesci_Index"] = (df["H"] - df["D"]) / (df["H"] + df["D"] + df["N"]).replace(0, pd.NA)
print(df[["date", "H", "D", "N", "Pesci_Index"]])

# Salva il DataFrame in un file Excel 
final_df = df[["date", "H", "D", "N", "Pesci_Index" ]]
final_df.to_excel("Pesci_Index.xlsx", index=False)
print("File Excel creato correttamente.")