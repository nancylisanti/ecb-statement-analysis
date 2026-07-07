# Intelligenza Artificiale e politica monetaria: un'analisi delle comunicazioni della BCE attraverso la text analysis

## Descrizione progetto 
L'obbiettivo della ricerca è analizzare il contenuto delle conferenze stampa della Banca Centrale Europea (BCE) mediante l'utilizzo di strumenti di intelligenza artificiale e l'analisi del linguaggio utilizzato, al fine di costruire un indice in grado di sintetizzare l'orientamento della comunicazione di politica monetaria. Tale indice testuale è successivamente integrato in un modello econometrico, insieme a variabili macroeconomiche di controllo, al fine di valutarne la capacità predittiva rispetto alle successive decisioni della BCE relative ai tassi di interesse. 

# Workflow del progetto 
Il progetto è stato sviluppato nel seguente ordine:
1. Raccolta delle conferenze stampa della BCE svolte nel periodo 2022-2024
2. Costruzione del Pesci Index mediante analisi testuale 
3. Costruzione del dataset econometrico 
4. Integrazione delle variabili macroeconomiche
5. Stima dei modelli di regressione 
6. Analisi dei risultati e controlli diagnostici 

---------------
# Dataset utilizzati 
Sono stati utilizzati i seguenti dataset: 
- Conferenze stampa della BCE (2022-2024)
- Main Refinancing Operations Rate (MRO)
- Inflazione HICP (Eurostat)
- Euribor a 1 mese 
- Indice di volatilità VSTOXX 

---------------
# Struttura del repository

## 01_pesci_dictionary_count.py
Costruzione di un primo indice testuale mediante il conteggio di termini classificati come Hawkish, Dovish e neutral. Nello stesso output prodotto, sono stati integrati i punteggi ottenuti mediante ChatGPT (AI Index), che costituiscono l'indice utilizzato nelle successive analisi econometriche 
**Output:**
- Pesci_Index.xlsx

> Nota Metodologica: il *Pesci Index* rappresenta una versione più snella dell'indice sviluppato da Pesci. è riportato a fini dimostrativi e come riferimento per confrontarlo con il successivo indice sviluppato mediante intelligenza artificiale. 

---------------
## 02_build_dataset.py
Costruzione del dataset finale utilizzato per l'analisi econometrica mediante l'integrazione dell'AI_Index, del tasso MRO e delle variabili macroeconomiche (Inflazione HICP, Euribor a 1 mese e VSTOXX). Lo script costituisce inoltre la variabile dipendente delta_MRO. 
**Output:**
- Dataset_Regressione_Finale.xlsx

---------------
## 03_regression.py
Stima dei modelli econometrici e dei relativi controlli diagnostici. 
L'analisi comprende: 
- Regressione OLS;
- grafico dei residui;
- matrice di correlazione;
- Variance Inflation Factor (VIF);
- errori standard robusti HC3;
- test di Breusch-Pagan;
- modelli alternativi di regressione; 
- tabella riassuntiva dei risultati.
**Output:** 
- Regression_Table.xlsx
- Residuals_Plot.png

---------------
## Variabili utilizzate 
# Variabile indipendente 
- DeltaMRO

# Variabile esplicativa principale
- AI Index

# Variabili di controllo
- Inflazione HICP 
- Euribor a 1 mese
- VSTOXX

---------------
## Tecnologie utilizzate
# Linguaggio di programmazione 
- Python

# Librerie Python
- pandas
- statsmodels
- matplotlib

# Software 
- Microsoft Excel 
- Git 
# Piattaforma di versionamento
- GitHub

---------------
# Autrice 
**Nancy Lisanti**
Corso di Laurea Magistrale Finanza e Risk Management 
Università di Parma
