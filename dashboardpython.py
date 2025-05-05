import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# definisco le coordinate geografiche delle miniere per visualizzarle su una mappa
coordinate_miniere = {
    "Miniera1": {"lat": 67.9061, "lon": 20.9575},
    "Miniera2": {"lat": 60.2761, "lon": 16.1706},
    "Miniera3": {"lat": 67.7066, "lon": 25.9403}
}


# carico i dati delle miniere da un file CSV e converte la colonna "Data" nel formato datetime
df = pd.read_csv("dati_miniere123.csv", parse_dates=["Data"], dayfirst=True)


# assicuro che la colonna "Data" sia nel formato datetime corretto
df['Data'] = pd.to_datetime(df['Data'], format='%d/%m/%Y')


# aggiungo una nuova colonna "%_Rame_Pulita", che prende il valore di "%_Rame" solo se le tonnellate giornaliere sono superiori a 0.19
df['%_Rame_Pulita'] = df.apply(lambda row: row['%_Rame'] if row['Tonnellate_giornaliere'] >= 0.19 else None, axis=1)  



# inizzializzo l'applicazione Dash
app = dash.Dash(__name__)
app.title = "Dashboard Miniere"


# layout dell'app: struttura e design della pagina web
app.layout = html.Div(style={'backgroundColor': '#121212', 'padding': '20px', 'color': '#E0E0E0'}, children=[        
    html.H1("MINIERE DI RAME IN SCANDINAVIA", style={'textAlign': 'center', 'color': '#00BFFF'}),                    # titolo principale della pagina, con stile per il colore e l'allineamento
    html.Div([                                                                                                       # sezione per visualizzare la mappa delle miniere
        dcc.Graph(id='mappa-miniere')                                                                                # definisco il componente grafico della mappa
    ], style={'marginBottom': '50px'}),                                                                              # aggiungo uno spazio sotto la mappa
    

    # sezione per la selezione della miniera tramite un menu a tendina
    html.Div([
        html.Label("Seleziona la Miniera", style={'marginRight': '10px'}),                                           # etichetta per il menu a tendina
        dcc.Dropdown(                                                                                                # componente dropdown per selezionare la miniera 
            id='miniera-dropdown',                                                                                   # ID univoco del componente
            options=[{'label': m, 'value': m} for m in df['Miniera'].unique()],                                      # opzioni basate sulle miniere nel dataframe
            value='Miniera1',                                                                                        # imposta il valore di default
            style={'width': '300px', 'color': '#000000'}                                                             # stile: larghezza e colore del testo
        ),

        html.Br(),                                                                                                   # linea di separazione tra i componenti

        html.Label("Seleziona intervallo di date"),                                                                  # etichetta per il selettore dell'intervallo di date  
        
        # componente per selezionare un intervallo di date
        dcc.DatePickerRange(                                                                                        
            id='date-picker',                                                                                        # ID componente
            min_date_allowed=df['Data'].min(),                                                                       # imposto la data minima selezionabile
            max_date_allowed=df['Data'].max(),                                                                       # imposto la data massima selezionabile
            start_date=df['Data'].min(),                                                                             # data di inzio dataset
            end_date=df['Data'].max(),                                                                               # data di fine dataset
            display_format='DD/MM/YYYY',                                                                             # mostro le date nel formato che preferisco
            style={'color': '#000000'}                                                                               # imposto il colore del selettore
        )
    ], style={'marginBottom': '40px'}),                                                                              # aggiungo uno spazio sotto la sezione della data


    # grafico per la correlazione tra Temperatura e Consumo Energetico
    html.Div([
        html.H2("Correlazione Temperatura vs Consumo Energetico", style={'color': '#00BFFF'}),                       # titolo della sezione
        dcc.Graph(id='grafico-temperatura-energia')                                                                  # definisco il grafico per la correlazione tra temperatura e consumo energetico
    ], style={'marginBottom': '50px'}),                                                                              # aggiungo uno spazio sotto il grafico


    # sezione per monitorare la sicurezza sul lavoro con una tabella
    html.Div([
        html.H2("Monitoraggio Sicurezza Lavoratori", style={'color': '#00BFFF'}),                                    # titolo della sezione di sicurezza
        dcc.Loading(                                                                                                 # componente di caricamento 
            id="loading-tabella",                                                
            type="circle",                                                                                           # tipo di caricamento cerchio rotante
            children=[
                dash.dash_table.DataTable(                                                                                                          # tabella per monitorare la sicurezza
                    id='tabella-sicurezza',                                                      
                    columns=[                                                                                                                       # definizione delle colonne
                        {'name': 'Giorno', 'id': 'Data', 'type': 'text'},                                                                           # colonna data
                        {'name': 'Miniera', 'id': 'Miniera'},                                                                                       # colonna nome miniera
                        {'name': 'Incidenti', 'id': 'Incidenti'},                                                                                   # colonna per il numero incidenti
                        {'name': 'Ore Senza Incidenti', 'id': 'Ore_Senza_Incidenti'},                                                               # colonna per le ore senza incidenti
                        {'name': 'Giorni Senza Incidenti', 'id': 'Giorni_senza_incidenti_consecutivi'},                                             # colonna per i giorni senza incidenti
                        {'name': 'Media Giorni Senza Incidenti', 'id': 'Media_Giorni', 'type': 'numeric', 'format': {'specifier': '.2f'}}           # colonna per la media dei giorni senza incidenti
                    ],
                    style_table={'overflowX': 'auto'},                                                               # abilita lo scorrimento orizzontale della tabella se necessario
                    style_cell={                                                                                     # definizione dello stile per le celle della tabella
                        'backgroundColor': '#1e1e1e',
                        'color': '#E0E0E0',
                        'padding': '10px',
                        'textAling': 'center'                                                                        # allinea il testo al centro delle celle
                    },
                    style_header={                                                                                   # stile per l'intestazione della tabella
                        'backgroundColor': '#00BFFF',
                        'color': 'black',
                        'fontWeight': 'bold'                                                                         # rende il testo per l'intestazione in grassetto
                    },
                    page_size=10                                                                                     # limita a 10 il numero di righe  visualizzate per pagina
                )
            ]
        )
    ], style={'marginBottom': '50px'}),                                                                              # aggiunge uno spazio sotto la sezione della tabella


    # gruppo di grafici (produzione, energia, CO2, costi) da visualizzare
    html.Div([
        dcc.Graph(id='grafico-produzione'),                                                                          # grafico produzione giornaliera
        dcc.Graph(id='grafico-energia-co2'),                                                                         # grafico energia ed emissioni CO2
        dcc.Graph(id='grafico-costi-torta')                                                                          # grafico per visualizzare i costi
    ])
])


# callback per aggiornare i grafici e la tabella in base ai parametri di input selezionati
@app.callback(
    [Output('grafico-produzione', 'figure'),
     Output('grafico-energia-co2', 'figure'),
     Output('grafico-costi-torta', 'figure'),
     Output('tabella-sicurezza', 'data'),
     Output('grafico-temperatura-energia', 'figure')],
     [Input('miniera-dropdown', 'value'),
      Input('date-picker', 'start_date'),
      Input('date-picker', 'end_date')]
)
def aggiorna_grafici(miniera, start_date, end_date):
    # filtro il DataFrame in base alla miniera e l'intervallo di date selezionato
    dff = df[(df['Miniera'] == miniera) &
             (df['Data'] >= pd.to_datetime(start_date)) &
             (df['Data'] <= pd.to_datetime(end_date))].copy()
    
    
    # calcolo la media dei giorni senza incidenti, per la miniera selezionata e il filtro delle date
    media_giorni = dff['Giorni_senza_incidenti_consecutivi'].mean()
    dff['Media_Giorni'] = round(media_giorni, 2)                                                                    # arrotondo il risultato a 2 decimali
    dff['Data'] = dff['Data'].dt.strftime('%d/%m/%Y')                                                               # converte la data in formato giorno/mese/anno                                                             
                                  
    # prepara i dati da visualizzare nella tabella
    dati_tabella = dff[['Data', 'Miniera', 'Incidenti', 'Ore_Senza_Incidenti', 'Giorni_senza_incidenti_consecutivi', 'Media_Giorni']]
    
    
    # grafico combinato a barre per visualizzare la produzione giornaliera e la percentuale di Rame
    fig1 = go.Figure()
    fig1.add_trace(go.Bar(
        x=dff['Data'],                                                                            # asse x: data
        y=dff['Tonnellate_giornaliere'],                                                          # asse y: tonnellate giornaliere
        name='Tonnellate giornaliere',                                                            # etichetta per la barra delle tonnellate
        marker_color='#00BFFF',
        yaxis='y1',                                                                               # asse y primario per le tonnellate
        hovertemplate='%{y} tonnellate<br>%{x|%d/%m/%Y}'                                          # template per il tooltip
    ))
    # aggiungo un grafico a linee per la percentuale di rame pulita
    fig1.add_trace(go.Scatter(
        x=dff['Data'],                                                                            # asse x: data
        y=dff['%_Rame_Pulita'],                                                                   # asse y: % rame
        name='% di Rame',                                                                         # etichetta per la linea della percentuale di rame
        mode='lines+markers',                                                                     # mosta sia la linea che i punti
        line=dict(color='#FFA500'),
        yaxis='y2',                                                                               # asse y secondario per la percentuale di rame
        hovertemplate='%{y:.2f}% rame<br>%{x|%d/%m/%Y}'                                           # template per il tooltip
    ))
    # configuro il layout del grafico combinato
    fig1.update_layout(
        template='plotly_dark',                                                                   # tema del grafico
        title='Produzione Giornaliera e % di Rame',                                               # titolo
        xaxis=dict(title='Data'),                                                                 # etichetta asse x
        yaxis=dict(title='Tonnellate', side='left'),                                              # etichetta asse y primario
        yaxis2=dict(title='% di Rame', overlaying='y', side='right'),                             # etichetta asse y secondario
        legend=dict(x=0.4, y=1.1, orientation="h"),                                               # posizionamento della legenda
        margin=dict(l=40, r=40, t=50, b=40)                                                       # margini per evitare sovrapposizioni
    )


    # GRAFICO A LINEE: Consumo di Energia & Emissioni di CO2
    fig2 = go.Figure()
    # linea per il consumo energetico (in kWh)
    fig2.add_trace(go.Scatter(
        x=dff['Data'],                                                                            # asse x: data
        y=dff['Consumo_Energia_kWh'],                                                             # asse y: consumo energia kWh
        name='Consumo Enegia (kWh)',                                                              # etichetta della legenda
        mode='lines+markers',                                                                     # linea con punti visibili
        line=dict(color='limegreen'),                                               
        hovertemplate='%{y:.2f} kWh<br>%{x|%d/%m/%Y}'                                             # tooltip dettagliato
    ))
    # linea per le emissioni di CO₂ (in kg)
    fig2.add_trace(go.Scatter(
        x=dff['Data'],
        y=dff['Emissioni_CO2_kg'],
        name='Emissioni CO₂ (kg)',
        mode='lines+markers',
        line=dict(color='crimson'),
        hovertemplate='%{y:.2f} kg CO₂<br>%{x|%d/%m/%Y}'                                          # tooltip
    ))
    # layout del grafico a linee
    fig2.update_layout(
        title='Consumo di Energia e Emissioni di CO₂',
        template='plotly_dark',
        xaxis=dict(title='Data'),
        yaxis=dict(title='Valore'),
        legend=dict(x=0.4, y=1.1, orientation="h"),                                               # posizione e orientamento della legenda
        margin=dict(l=40, r=40, t=50, b=40)
)
    
    # grafico a ciambella: distribuzione dei costi (lavoro, macchinari, energia)
    # calcolo dei costi totali per ciascuna categoria
    costi = [
        round(dff['Costo_Lavoro'].sum(), 2),
        round(dff['Costo_Macchinari'].sum(), 2),
        round(dff['Costo_Energia'].sum(), 2)
    ]
    
    labels = ['Costo_lavoro', 'Costo_Macchinari', 'Costo_Energia']                                # etichette per la legenda
    # creazione del grafico a ciambella
    fig3 = go.Figure(data=[go.Pie(
        labels=labels,
        values=costi,
        hole=0.4,                                                                                 # impostazione del buco al centro per rendere il grafico a ciambella
        marker=dict(colors=['#1f77b4', '#ff7f0e', '#2ca02c']),
        hovertemplate='%{label}: %{value} €'                                                      # tooltip personalizzato
    )])
    # layout del grafico a ciambella
    fig3.update_layout(
        title='Distribuzione dei Costi (Lavoro, Macchinari, Energia)',
        template='plotly_dark',
        margin=dict(l=40, r=40, t=50, b=40)
    )


    # grafico scatter: temperatura vs consumo energia
    fig4 = px.scatter(
        dff,
        x='Temperatura_C',                                                                        # asse x: temperatura
        y='Consumo_Energia_kWh',                                                                  # asse y: consumo energia kWh
        trendline='ols',                                                                          # aggiungo una linea di regressione
        title='Temperatura vs Consumo Energetico',
        labels={'Temperatura_C': 'Temperatura (°C)',
                'Consumo_Energia_kWh': 'Consumo Energetico (kWh)'},
        color='Temperatura_C',                                                                    # colore dei punti basato sulla temperatura
        color_continuous_scale='Viridis',                                                         # scala di colore continua
        template='plotly_dark'
    )

    fig4.update_layout(
        margin=dict(l=40, r=40, t=50, b=40),
        xaxis=dict(title='Temperatura (°C)'),
        yaxis=dict(title='Consumo Energetico (kWh)'),
        showlegend=False
    )

    # RESTITUZIONE DEI GRAFICI
    # dati_tabella viene convertito in formato dizionario per essere compatibile con il DataTable
    return fig1, fig2, fig3, dati_tabella.to_dict('records'), fig4


# callback per aggiornare la mappa interattiva delle miniere
@app.callback(
    Output('mappa-miniere', 'figure'),
    Input('miniera-dropdown', 'value')
)
def aggiorna_mappa(miniera_selezionata):
     # creo un DataFrame con nomi e coordinate di tutte le miniere (serve per disegnare i punti sulla mappa)
    df_map = pd.DataFrame([
        {'Miniera': nome, 'lat': val['lat'], 'lon': val['lon']}
        for nome, val in coordinate_miniere.items()
    ])
    # creo la mappa interattiva con Plotly Express usando Mapbox
    fig = px.scatter_mapbox(
        df_map,
        lat='lat',
        lon='lon',
        hover_name='Miniera',                                                                      # mostra il nome al passaggio del mouse
        zoom=3,                                                                                    # livello di zzom iniziale
        height=400,                                                                                # altezza in pixel della mappa
        color_discrete_sequence=["#00BFFF"]                                                        # colore blu per i marker iniziali
    )
    # personalizzo i marker: dimensione + aggiungo il nome miniera ai dati personalizzati
    fig.update_traces(
        marker=dict(size=15),
        customdata=df_map[['Miniera']].values
    )
    # imposto lo stile della mappa, centro geografico sulla Scandinavia, e layout scuro coerente col resto
    fig.update_layout(
        mapbox_style='carto-darkmatter',
        mapbox_center={"lat": 64.0, "lon": 20.0},                                                  # centro sulla Scandinavia
        margin=dict(l=0, r=0, t=0, b=0),
        template='plotly_dark'
    )
    # evidenzio la miniera selezionata con un marker
    selected = df_map[df_map['Miniera'] == miniera_selezionata]
    if not selected.empty:
        fig.add_trace(go.Scattermapbox(
            lat=selected['lat'],
            lon=selected['lon'],
            mode='markers',
            marker=dict(size=25, color='orange'),
            hoverinfo='none',
            showlegend=False
        ))
    
    return fig                                                                                    # restituisco la figura finale completa


# avvio il server di Dash
if __name__== '__main__':
    app.run_server(debug=True)





