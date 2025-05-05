# librerie per la gestione numerica, tabelle e dati
import numpy as np
import pandas as pd
from datetime import datetime, timedelta


# questa funzione serve per distribuire casualmente le tonnellate prodotte durante l'anno
def distribuisci_tonnellate(totale_annuo, giorni):                                                          
    pesi = np.random.rand(giorni)                                                                                      # genera un peso casuale per ogni giorno
    pesi_normalizzati = pesi / pesi.sum()                                                                              # normalizza i pesi per ottenere una distribuzione proporzionale
    valori = (pesi_normalizzati * totale_annuo)                                                                        # fornisce il totale annuo proporzionalmente
    return np.round(valori, 2)                                                                                         # arrotonda a due decimali per migliorare la leggibilità


# creo le date per un anno intero
start_date = datetime(2024, 1, 1)                                                                                      # impostazione data di inizio anno (1 gennaio 2024)
end_date = datetime(2024, 12, 31)                                                                                      # impostazione data di fine anno   (31 dicembre 2024)
date_range = [start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)]                         # genera una lista con tutte le date dal 1 gennaio al 31 dicembre 2024 (anno bisestile, quindi 366 giorni) 


# definizione delle miniere simulate con produzione annua e coordinate GPS indicative
miniere = {
    "Miniera 1": {                                                                                 # localizzata al nord della Svezia
        "Tonnellate_annue": 40840,                                                                 # produzione totale annua
        "Coordinate": (67.9061, 20.9575)                                                           # coordinate GPS indicative  
    },
    "Miniera 2": {                                                                                 # localizzata al Sud della Svezia
        "Tonnellate_annue": 3455,                                                                  # produzione totale annua
        "Coordinate": (60.2761, 16.1706)                                                           # coordinate GPS indicative
    },
    "Miniera 3": {                                                                                 # localizzata al Nord della Finlandia
        "Tonnellate_annue": 9850,                                                                  # produzione totale annua
        "Coordinate": (67.7066, 25.9403)                                                           # coordinate GPS indicative
    }
}

# creo un dizionario dove per ogni miniera genero una lista di tonnellate giornaliere
# la quantità annuale viene distribuita su tutti i giorni dell'anno (usando la funzione distribuisci_tonnellate)
tonnellate_giornaliere_per_miniera = {
    nome: distribuisci_tonnellate(info["Tonnellate_annue"], len(date_range))
    for nome, info in miniere.items()
}


# creo una lista vuota per raccogliere tutti i dati simulati giornalieri delle miniere
data = []

# inizializzo il contatore per tenere traccia dei giorni consecutivi senza incidenti per ciascuna miniera
contatore_sicurezza = {nome: 0 for nome in miniere.keys()}

# ciclo su ogni miniera e su ogni giorno dell'anno
for miniera, info in miniere.items():
    for i, day in enumerate(date_range):
        tonnellate = tonnellate_giornaliere_per_miniera[miniera][i]                                 # tonnellate prodotte nel giorno corrente


        # calcolo della temperatura media giornaliera simulata, basata sul mese dell'anno
        month = day.month                                                                           # mese corrente
        if month in [6, 7, 8]:                                                                      # mesi estivi, giugno, luglio ed agosto
            Temperatura = np.random.uniform(15, 25)                                                 # temperature più alte, tra 15°C e 25°C
        elif month in [12, 1, 2]:                                                                   # mesi invernali, dicembre, gennaio, febbraio
            Temperatura = np.random.uniform(-25, 0)                                                 # temperature sotto lo zero, tra -25°C e 0°C
        else:                                                                                       # marzo-maggio, settembre-novembre (primavera-autunno)
            Temperatura = np.random.uniform(-10, 15)                                                # temperatura tra -10°C e 15°C

        
        # calcolo del consumo energetico in kWh, influenzato dalla temperatura
        if Temperatura < 0:                                                                                         # maggior freddo, maggiore consumo
            Consumo_energia = round(np.random.uniform(2000000, 4000000) * (1 + abs(Temperatura) / 25), 2)           
        elif Temperatura > 15:                                                                                      # caldo, consumo medio
            Consumo_energia = round(np.random.uniform(2000000, 3000000), 2)                
        else:                                                                                                       # temperature più moderate, consumo leggermente aumentato
            Consumo_energia = round(np.random.uniform(2000000, 3000000) * (1 +(Temperatura - 5) / 10), 2)           


        # aggiungo un fattore correttivo al consumo energetico in base alle tonnellate estratte
        # ogni 100 tonnellate giornaliere aumentano il consumo del +1%
        Fattore_tonnellate = 1 + (tonnellate / 100)                                        
        Consumo_energia = round(Consumo_energia * Fattore_tonnellate, 2)


        # Calcolo delle emissioni di CO2: ipotizzo che siano pari al 3% del consumo energetico
        Emissioni_co2 = round(Consumo_energia * 0.03, 2)                                   

        # assegno una percentuale di rame variabile in base alla miniera
        if miniera == "Miniera 1":
            Percentuale_rame = round(np.random.uniform(5, 10), 2)                                              # contenuto di rame più alto
        elif miniera == "Miniera 2":
            Percentuale_rame = round(np.random.uniform(3, 6), 2)                                               # contenuto di rame più basso
        elif miniera == "Miniera 3":
            Percentuale_rame = round(np.random.uniform(5, 8), 2)                                               # contenuto di rame medio
        

        #  stima del salario medio annuo (in euro) per lavoratore nelle miniere del Nord Europa
        salario_medio_euro = 50000

        # numero medio dei dipendenti impiegati per ciascuna miniera
        dipendenti_per_miniera = {"Miniera 1": 800, "Miniera 2": 450, "Miniera 3": 500}


        # calcolo dei costi operativi giornalieri
        Costo_lavoro = round((salario_medio_euro * dipendenti_per_miniera[miniera]) /366, 2)  # dividendo per 366 perchè il 2024 è bisestile
        Costo_macchinari = round(np.random.uniform(15000, 30000), 2)                          # costo giornaliero stimato dei macchinari
        

        # calcolo del costo dell’energia in euro (usando un prezzo medio per kWh)
        prezzo_energia_kwh = 0.12                                                             # ipotesi di 12 centesimi per kWh
        Costo_energia = round(Consumo_energia * prezzo_energia_kwh, 2)                        

        # simulazione del rischio di incidenti sul lavoro
        # più alta è la produzione o più bassa la temperatura, minore è il rischio stimato
        if tonnellate > 150 or Temperatura < -10:                                             # rischio basso
            probabilità_incidente = 0.03
        elif tonnellate > 100:                                                                # rischio medio
            probabilità_incidente = 0.05
        else:                                                                                 # rischio alto
            probabilità_incidente = 0.07
        
        # genero l'incidente usando la probabilità calcolata sopra
        Incidenti = np.random.choice([0, 1], p=[1 - probabilità_incidente, probabilità_incidente])                                  

        # aggiorno il contatore dei giorni consecutivi senza incidenti
        if Incidenti == 0:
            contatore_sicurezza[miniera] += 1                                                 # incremento il contatore se non ci sono incidenti
        else:
            contatore_sicurezza[miniera] = 0                                                  # resetto il contatore se c'è stato un incidente
        
        # salvo i giorni consecutivi senza incidenti per il giorno corrente
        Giorni_senza_incidenti_consecutivi = contatore_sicurezza[miniera]

        # calcolo le ore senza incidenti (24 ore per ogni giorno)
        Ore_senza_incidenti = Giorni_senza_incidenti_consecutivi * 24
        

        # aggiungo i dati del giorno corrente alla lista
        data.append([
            day.strftime("%d/%m/%Y"), miniera,
            tonnellate, info["Coordinate"][0], info["Coordinate"][1],
            Consumo_energia, Emissioni_co2, Percentuale_rame, Costo_lavoro, Costo_macchinari, Costo_energia,
            Incidenti, Ore_senza_incidenti, Temperatura, Giorni_senza_incidenti_consecutivi
        ])


# creo il DataFrame con i dati raccolti e assegno nomi alle colonne
df = pd.DataFrame(data, columns=[
    "Data", "Miniera", "Tonnellate_giornaliere",
    "Latitudine", "Longitudine",
    "Consumo_Energia_kWh", "Emissioni_CO2_kg", "%_Rame",
    "Costo_Lavoro", "Costo_Macchinari", "Costo_Energia",
    "Incidenti", "Ore_Senza_Incidenti", "Temperatura_C",
    "Giorni_senza_incidenti_consecutivi"   
])



# salvo il dataframe in un file .csv
df.to_csv("dati_miniere123.csv", index=False)

# messaggio di conferma
print("Dati simulati salvati in dati_miniere123.csv")                           



         



                                        
