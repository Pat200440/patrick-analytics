# 📘 Spiegazione avanzata del progetto -- Superstore BI Dashboard

Questa guida è una versione più completa e più forte della spiegazione
del progetto.\
È pensata per un profilo **junior**, quindi spiega le cose in modo
semplice, senza dare nulla per scontato.

L'obiettivo è aiutarti a capire:

-   il **flusso del progetto**
-   la **logica del codice**
-   l'**architettura della dashboard**
-   come **raccontarlo bene a un colloquio**

------------------------------------------------------------------------

# 🧠 Obiettivo del progetto

Questo progetto serve a costruire una **dashboard di Business
Intelligence** usando:

-   **Python**
-   **Streamlit**
-   **Pandas**
-   **Plotly**

La dashboard analizza un dataset di vendite retail e risponde a domande
di business come:

-   quali mercati generano più vendite
-   quali categorie performano meglio
-   come gli sconti influenzano il profitto
-   quali modalità di spedizione vengono usate di più
-   quali segmenti cliente portano più fatturato

------------------------------------------------------------------------

# 🔄 Diagramma del flusso del progetto

## Vista sintetica

``` text
[CSV Dataset]
      ↓
[load_data()]
      ↓
[Pulizia colonne]
      ↓
[Pulizia dati numerici e date]
      ↓
[Creazione sidebar filtri]
      ↓
[Applicazione filtri globali]
      ↓
[Creazione dataframe separato per discount chart]
      ↓
[Calcolo KPI]
      ↓
[Creazione grafici]
      ↓
[Visualizzazione dashboard]
      ↓
[Anteprima dati filtrati]
```

## Vista spiegata

### 1. Input dati

Il progetto parte da un file CSV:

``` text
SuperStoreOrders - SuperStoreOrders.csv
```

Questo file contiene tutte le informazioni sulle vendite.

### 2. Caricamento dati

Il file viene letto con Pandas e trasformato in un **DataFrame**, cioè
una tabella Python su cui possiamo lavorare.

### 3. Pulizia

Prima di analizzare i dati, il codice: - uniforma i nomi delle colonne -
converte le colonne numeriche - trasforma eventuali date in formato
corretto

### 4. Filtri utente

La sidebar permette all'utente di scegliere: - market - country -
category - segment - ship mode

### 5. Applicazione filtri

I filtri vengono applicati per creare un dataframe filtrato:

``` text
filtered_df
```

### 6. Grafico discount con logica dedicata

Per il grafico **Discount vs Profit** viene creato un dataframe
separato, in modo che il filtro categoria del grafico possa funzionare
in modo indipendente.

### 7. KPI e grafici

Dopo il filtraggio, il codice calcola KPI e aggregazioni: - somme -
medie - conteggi - groupby

### 8. Output finale

Streamlit mostra tutto in dashboard: - KPI - grafici - tabella finale

------------------------------------------------------------------------

# 🏗️ Schema architetturale della dashboard

``` text
┌──────────────────────────────────────────────┐
│                STREAMLIT APP                 │
├──────────────────────────────────────────────┤
│ 1. Data Layer                               │
│    - CSV dataset                            │
│    - Pandas DataFrame                       │
├──────────────────────────────────────────────┤
│ 2. Data Preparation Layer                   │
│    - clean column names                     │
│    - numeric conversion                     │
│    - date parsing                           │
├──────────────────────────────────────────────┤
│ 3. Filtering Layer                          │
│    - global filters                         │
│    - discount chart dedicated filter        │
├──────────────────────────────────────────────┤
│ 4. Analytics Layer                          │
│    - KPI calculations                       │
│    - groupby aggregations                   │
│    - sorting and top-N analysis             │
├──────────────────────────────────────────────┤
│ 5. Visualization Layer                      │
│    - Plotly bar charts                      │
│    - Plotly scatter plot                    │
│    - Streamlit KPI metrics                  │
│    - Data preview table                     │
└──────────────────────────────────────────────┘
```

## Cosa significa questa architettura

### Data Layer

È il livello dove vivono i dati grezzi.\
Qui c'è il CSV e il DataFrame iniziale.

### Data Preparation Layer

È il livello di pulizia.\
Qui trasformiamo i dati da "sporchi" a "utilizzabili".

### Filtering Layer

È il livello interattivo.\
Qui l'utente decide cosa vedere.

### Analytics Layer

È il livello dove facciamo i calcoli.

### Visualization Layer

È il livello finale che mostra tutto all'utente.

------------------------------------------------------------------------

# 🧩 Spiegazione del codice riga per riga

Di seguito trovi una spiegazione molto dettagliata del codice.

------------------------------------------------------------------------

## 1. Import delle librerie

``` python
import streamlit as st
import pandas as pd
import plotly.express as px
```

### Cosa fanno

-   `streamlit` serve per costruire la dashboard
-   `pandas` serve per lavorare con i dati
-   `plotly.express` serve per creare i grafici

### Perché usiamo gli alias

-   `st` è più comodo di scrivere sempre `streamlit`
-   `pd` è la convenzione classica per Pandas
-   `px` è la convenzione classica per Plotly Express

------------------------------------------------------------------------

## 2. Configurazione della pagina

``` python
st.set_page_config(
    page_title="Superstore BI Dashboard",
    page_icon="📊",
    layout="wide"
)
```

### Riga per riga

-   `page_title`: imposta il titolo della scheda del browser
-   `page_icon`: imposta un'icona
-   `layout="wide"`: usa tutta la larghezza disponibile

### Perché è utile

Una dashboard con molti grafici ha bisogno di spazio.\
Il layout wide rende tutto più leggibile.

------------------------------------------------------------------------

## 3. Titolo e descrizione

``` python
st.title("📊 Superstore Business Intelligence Dashboard")
st.caption("Interactive BI dashboard built with Streamlit, Pandas and Plotly")
```

### Cosa fanno

-   `st.title()` mostra il titolo principale
-   `st.caption()` mostra un sottotitolo piccolo

### Perché servono

Aiutano l'utente a capire subito cos'è l'applicazione.

------------------------------------------------------------------------

## 4. Funzione per caricare i dati

``` python
@st.cache_data
def load_data() -> pd.DataFrame:
    df = pd.read_csv("SuperStoreOrders - SuperStoreOrders.csv")
    return df
```

### Riga per riga

-   `@st.cache_data`: dice a Streamlit di salvare in cache il risultato
-   `def load_data()`: definisce una funzione
-   `-> pd.DataFrame`: indica che la funzione restituisce un DataFrame
-   `pd.read_csv(...)`: legge il file CSV
-   `return df`: restituisce il dataframe

### Perché usare una funzione

È più ordinato rispetto a scrivere tutto direttamente nel codice
principale.

### Perché usare la cache

Senza cache, Streamlit ricaricherebbe il CSV troppo spesso.\
Con la cache l'app è più veloce.

------------------------------------------------------------------------

## 5. Esecuzione del caricamento

``` python
df = load_data()
```

### Cosa significa

Chiamiamo la funzione e salviamo il risultato dentro `df`.

### Cos'è `df`

È il dataframe principale del progetto.

------------------------------------------------------------------------

## 6. Pulizia dei nomi delle colonne

``` python
df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
    .str.replace("-", "_")
)
```

### Perché serve

I nomi delle colonne nel CSV potrebbero contenere: - spazi - maiuscole -
trattini - formati incoerenti

### Esempio

-   `Order Date` diventa `order_date`
-   `Sub-Category` diventa `sub_category`

### Vantaggio

I nomi diventano più facili da usare nel codice.

------------------------------------------------------------------------

## 7. Definizione delle colonne numeriche

``` python
numeric_cols = ["sales", "profit", "discount"]
```

### Perché serve

Vogliamo pulire più colonne con un ciclo invece di ripetere codice.

------------------------------------------------------------------------

## 8. Ciclo di conversione numerica

``` python
for col in numeric_cols:
    if col in df.columns:
        df[col] = (
            df[col]
            .astype(str)
            .str.replace("$", "", regex=False)
            .str.replace(",", "", regex=False)
            .str.strip()
        )
        df[col] = pd.to_numeric(df[col], errors="coerce")
```

### Riga per riga

-   `for col in numeric_cols:`: scorri ogni nome colonna
-   `if col in df.columns:`: controlla che la colonna esista
-   `.astype(str)`: converte i valori in stringa
-   `.str.replace("$", "", regex=False)`: rimuove il simbolo \$
-   `.str.replace(",", "", regex=False)`: rimuove le virgole
-   `.str.strip()`: rimuove spazi inutili
-   `pd.to_numeric(..., errors="coerce")`: converte in numero

### Cosa significa `errors="coerce"`

Se un valore è sbagliato o non convertibile, Pandas lo trasforma in
`NaN`.

### Perché è utile

Evita che il codice vada in errore per valori sporchi.

------------------------------------------------------------------------

## 9. Conversione della data

``` python
if "order_date" in df.columns:
    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
```

### Cosa fa

Trasforma la colonna `order_date` in un vero formato data.

### Perché è utile

Le date così possono essere usate meglio in analisi future.

------------------------------------------------------------------------

## 10. Titolo dei filtri sidebar

``` python
st.sidebar.header("Filters")
```

### Cosa fa

Crea il titolo della sidebar.

------------------------------------------------------------------------

## 11. Funzione di supporto per le opzioni dei filtri

``` python
def build_options(dataframe: pd.DataFrame, column: str) -> list[str]:
    if column not in dataframe.columns:
        return ["All"]
    return ["All"] + sorted(dataframe[column].dropna().astype(str).unique().tolist())
```

### Perché serve

Questa funzione evita di scrivere più volte la stessa logica.

### Riga per riga

-   controlla se la colonna esiste
-   rimuove i valori nulli
-   converte i valori in stringa
-   prende solo i valori unici
-   li ordina
-   aggiunge `"All"` come prima opzione

### Perché `"All"` è importante

Permette all'utente di non filtrare quel campo.

------------------------------------------------------------------------

## 12. Costruzione delle opzioni

``` python
market_options = build_options(df, "market")
country_options = build_options(df, "country")
category_options = build_options(df, "category")
segment_options = build_options(df, "segment")
ship_mode_options = build_options(df, "ship_mode")
```

### Cosa fanno

Creano le liste di opzioni che useremo nei menu a tendina.

------------------------------------------------------------------------

## 13. Creazione dei selectbox

``` python
selected_market = st.sidebar.selectbox("Market", market_options)
selected_country = st.sidebar.selectbox("Country", country_options)
selected_category = st.sidebar.selectbox("Category", category_options)
selected_segment = st.sidebar.selectbox("Segment", segment_options)
selected_ship_mode = st.sidebar.selectbox("Ship Mode", ship_mode_options)
```

### Cosa fanno

Creano i menu selezionabili nella sidebar.

### Cosa contengono

Ogni variabile `selected_...` contiene il valore scelto dall'utente.

------------------------------------------------------------------------

## 14. Sezione dedicata al grafico discount

``` python
st.sidebar.markdown("---")
st.sidebar.subheader("Discount Chart Filter")
```

### Cosa fa

Aggiunge una separazione visiva e un sottotitolo nella sidebar.

------------------------------------------------------------------------

## 15. Opzioni per il multiselect del discount chart

``` python
discount_chart_options = (
    sorted(df["category"].dropna().astype(str).unique().tolist())
    if "category" in df.columns
    else []
)
```

### Perché serve

Qui prepariamo le categorie disponibili per il grafico degli sconti.

------------------------------------------------------------------------

## 16. Multiselect per il grafico discount

``` python
selected_discount_categories = st.sidebar.multiselect(
    "Select categories for Discount vs Profit",
    discount_chart_options,
    default=discount_chart_options
)
```

### Cosa fa

Permette all'utente di scegliere una o più categorie da visualizzare nel
grafico scatter.

### Perché è utile

È più flessibile di un semplice selectbox.

------------------------------------------------------------------------

## 17. Creazione del dataframe filtrato globale

``` python
filtered_df = df.copy()
```

### Perché usiamo `.copy()`

Così non modifichiamo il dataframe originale `df`.

------------------------------------------------------------------------

## 18. Applicazione dei filtri globali

``` python
if selected_market != "All" and "market" in filtered_df.columns:
    filtered_df = filtered_df[filtered_df["market"] == selected_market]
```

La stessa logica viene poi ripetuta per: - country - category -
segment - ship_mode

### Come funziona

Se l'utente non sceglie `"All"`, il dataframe viene filtrato.

### Effetto

Tutti i KPI e quasi tutti i grafici usano `filtered_df`.

------------------------------------------------------------------------

## 19. Creazione del dataframe base per il discount chart

``` python
discount_base_df = df.copy()
```

### Perché esiste un dataframe separato

Perché il grafico `Discount vs Profit` ha un filtro categoria dedicato.

Se usassimo direttamente `filtered_df`, il filtro globale category
potrebbe bloccare il comportamento del multiselect del grafico.

------------------------------------------------------------------------

## 20. Applicazione parziale dei filtri al discount chart

Nel discount chart applichiamo: - market - country - segment - ship_mode

ma **non** il filtro globale category.

### Perché

Così il multiselect `selected_discount_categories` continua a funzionare
davvero.

------------------------------------------------------------------------

## 21. Controllo dataframe vuoto

``` python
if filtered_df.empty:
    st.warning("No data available for the selected filters.")
    st.stop()
```

### Cosa fa

Se i filtri selezionati eliminano tutte le righe, mostra un messaggio e
ferma l'app.

### Perché è importante

Evita errori nei grafici successivi.

------------------------------------------------------------------------

## 22. Calcolo KPI

``` python
total_sales = filtered_df["sales"].sum() if "sales" in filtered_df.columns else 0
total_profit = filtered_df["profit"].sum() if "profit" in filtered_df.columns else 0
avg_discount = filtered_df["discount"].mean() if "discount" in filtered_df.columns else 0
total_orders = filtered_df["order_id"].nunique() if "order_id" in filtered_df.columns else len(filtered_df)
```

### Cosa fanno

-   `sum()`: somma i valori
-   `mean()`: calcola la media
-   `nunique()`: conta i valori unici

### Perché usiamo `if ... in filtered_df.columns`

Per rendere il codice più robusto.

------------------------------------------------------------------------

## 23. Visualizzazione KPI

``` python
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Sales", f"${total_sales:,.0f}")
col2.metric("Total Profit", f"${total_profit:,.0f}")
col3.metric("Avg Discount", f"{avg_discount:.2%}")
col4.metric("Total Orders", f"{total_orders:,}")
```

### Cosa fa

Divide la pagina in 4 colonne e mostra le metriche.

### Formattazione

-   `:,.0f` formatta i numeri con separatore migliaia
-   `:.2%` mostra una percentuale con due decimali

------------------------------------------------------------------------

## 24. Sezione Geographic Performance

``` python
st.header("Geographic Performance")
```

### Cosa fa

Mostra il titolo della sezione geografica.

------------------------------------------------------------------------

## 25. Layout a due colonne per i grafici geografici

``` python
col1, col2 = st.columns(2)
```

### Perché serve

Permette di mettere due grafici affiancati.

------------------------------------------------------------------------

## 26. Sales by Market

``` python
market_sales = (
    filtered_df.groupby("market", as_index=False)["sales"]
    .sum()
    .sort_values("sales", ascending=False)
)
```

### Cosa succede

-   `groupby("market")`: raggruppa per mercato
-   `["sales"].sum()`: somma le vendite
-   `sort_values(...)`: ordina in modo decrescente

Poi:

``` python
fig_market = px.bar(
    market_sales,
    x="market",
    y="sales",
    text="sales",
    title="Sales by Market"
)
```

### Cosa fa

Crea un grafico a barre.

### `text="sales"`

Mostra il valore sopra ogni barra.

------------------------------------------------------------------------

## 27. Top Countries by Sales

La logica è simile a quella del market, ma qui: - raggruppiamo per
`country` - ordiniamo - prendiamo i primi 15

``` python
.head(15)
```

### Perché

Troppi paesi in un solo grafico renderebbero tutto poco leggibile.

------------------------------------------------------------------------

## 28. Sezione Product Performance

Qui analizziamo: - vendite per categoria - profitto per sub-category

### Sales by Category

Stessa logica del groupby: - raggruppa per categoria - somma le
vendite - ordina

### Top 10 Sub-Categories by Profit

Qui raggruppiamo per sub-category e sommiamo il profitto.

------------------------------------------------------------------------

## 29. Sezione Discount Impact on Profitability

``` python
discount_df = discount_base_df.dropna(subset=["sales", "profit", "discount", "category"]).copy()
discount_df = discount_df[discount_df["sales"] > 0]
```

### Cosa fa

-   elimina righe con valori nulli
-   tiene solo righe con sales \> 0

### Perché

Evita errori e rende il grafico più sensato.

Poi:

``` python
if selected_discount_categories:
    discount_df = discount_df[
        discount_df["category"].isin(selected_discount_categories)
    ]
else:
    discount_df = discount_df.iloc[0:0]
```

### Cosa fa

Filtra il dataframe in base alle categorie selezionate nel multiselect.

### `.isin(...)`

Controlla se il valore di categoria è presente nella lista scelta.

------------------------------------------------------------------------

## 30. Creazione scatter plot

``` python
fig_discount = px.scatter(
    discount_df,
    x="discount",
    y="profit",
    color="category",
    hover_data=["sales", "profit", "discount"],
    title="Discount vs Profit"
)
```

### Cosa rappresenta

-   asse X = discount
-   asse Y = profit
-   colore = categoria

### Cosa significa

Ogni punto rappresenta un'osservazione del dataset.

------------------------------------------------------------------------

## 31. Miglioria visiva del grafico scatter

``` python
fig_discount.update_traces(
    marker=dict(
        size=9,
        opacity=0.65,
        line=dict(width=1, color="black")
    )
)
```

### Cosa fa

-   `size=9`: rende i punti più grandi
-   `opacity=0.65`: li rende semi-trasparenti
-   `line=...`: aggiunge un bordo nero

### Perché è utile

I punti si leggono meglio.

------------------------------------------------------------------------

## 32. Layout del grafico scatter

``` python
fig_discount.update_layout(
    xaxis_title="Discount",
    yaxis_title="Profit",
    legend_title="Category",
    height=550,
    plot_bgcolor="white"
)
```

### Cosa fa

Migliora l'aspetto generale del grafico.

------------------------------------------------------------------------

## 33. Griglia degli assi

``` python
fig_discount.update_xaxes(
    showgrid=True,
    gridcolor="lightgray",
    dtick=0.1
)

fig_discount.update_yaxes(
    showgrid=True,
    gridcolor="lightgray"
)
```

### Cosa fa

Rende la griglia più leggibile.

### `dtick=0.1`

Imposta i tick dell'asse X a intervalli di 0.1.

------------------------------------------------------------------------

## 34. Shipping Analysis

In questa sezione usiamo `value_counts()`.

### Esempio

``` python
ship_mode_df = filtered_df["ship_mode"].value_counts().reset_index()
ship_mode_df.columns = ["ship_mode", "count"]
```

### Cosa fa

Conta quante volte compare ogni modalità di spedizione.

Poi il risultato viene mostrato con un grafico a barre.

La stessa logica vale per `order_priority`.

------------------------------------------------------------------------

## 35. Customer Segment Revenue

``` python
segment_sales = (
    filtered_df.groupby("segment", as_index=False)["sales"]
    .sum()
    .sort_values("sales", ascending=False)
)
```

### Cosa fa

Calcola il fatturato totale per segmento cliente.

### Perché è utile

Aiuta a capire quale segmento genera più revenue.

------------------------------------------------------------------------

## 36. Anteprima dati filtrati

``` python
with st.expander("Show filtered data preview"):
    st.dataframe(filtered_df, use_container_width=True)
```

### Cosa fa

Mostra una tabella apribile con i dati filtrati.

### Perché è utile

Permette di controllare cosa c'è davvero dietro ai grafici.

------------------------------------------------------------------------

# 💡 Concetti chiave da ricordare

## DataFrame

È la struttura dati principale di Pandas.\
Assomiglia a una tabella Excel.

## Filtering

È il processo con cui selezioni solo le righe che ti interessano.

## GroupBy

Serve a raggruppare i dati per una categoria e calcolare statistiche.

## KPI

Sono metriche sintetiche per valutare l'andamento del business.

## Scatter Plot

Mostra la relazione tra due variabili numeriche.

## Bar Chart

Mostra confronti tra categorie.

------------------------------------------------------------------------

# 🗣️ Come presentarlo al colloquio

Questa è una delle parti più importanti.

## Versione semplice

> Ho sviluppato una dashboard di Business Intelligence in Python usando
> Streamlit, Pandas e Plotly.\
> Il progetto analizza un dataset retail e permette di esplorare
> vendite, profitto, segmenti cliente, spedizioni e impatto degli sconti
> attraverso filtri interattivi e grafici dinamici.

## Versione un po' più forte

> The goal of the project was to transform raw retail data into business
> insights through an interactive dashboard.\
> I implemented data cleaning, dynamic filtering, KPI calculation and
> multiple visualizations to answer business questions about sales
> performance, profitability, customer segments and logistics.

## Cosa dire tecnicamente

Puoi dire che hai lavorato su 4 aspetti:

### 1. Data Cleaning

> I cleaned column names, converted numeric fields and handled missing
> values.

### 2. Data Analysis

> I used Pandas groupby operations to aggregate sales, profit and order
> metrics.

### 3. Dashboard Logic

> I created global filters and a dedicated filtering logic for the
> discount analysis chart.

### 4. Data Visualization

> I used Plotly charts integrated into Streamlit to make the dashboard
> interactive and user friendly.

------------------------------------------------------------------------

# 🎯 Punti forti da sottolineare al colloquio

## Hai trasformato un CSV in uno strumento decisionale

Non hai solo letto un file: lo hai reso utile per prendere decisioni.

## Hai pensato all'utente

La sidebar e i filtri rendono la dashboard interattiva e user friendly.

## Hai gestito un caso reale di logica

Il discount chart ha un filtro separato: questo dimostra ragionamento,
non solo codice.

## Hai collegato dati e business

Non hai fatto grafici "casuali", ma visualizzazioni che rispondono a
domande di business.

------------------------------------------------------------------------

# ❓ Possibili domande al colloquio e risposte

## Perché hai usato Streamlit?

Perché permette di creare dashboard interattive in Python in modo rapido
e leggibile.

## Perché hai usato Pandas?

Perché è una libreria molto forte per pulizia, trasformazione e
aggregazione dati.

## Perché hai creato un dataframe separato per il grafico discount?

Per evitare che il filtro globale category bloccasse il funzionamento
del filtro dedicato del grafico.

## Cosa hai imparato?

Ho imparato a unire data cleaning, business logic, visualizzazione e
user interaction in un unico progetto.

------------------------------------------------------------------------

# 🚀 Miglioramenti futuri

Puoi proporre queste evoluzioni:

-   filtro temporale su order date
-   mappa geografica
-   profit margin
-   top customer analysis
-   export dati filtrati
-   insight automatici scritti sotto i grafici

------------------------------------------------------------------------

# 👨‍💻 Conclusione

Questo progetto è utile perché ti allena su competenze reali:

-   leggere dati
-   pulirli
-   filtrarli
-   analizzarli
-   visualizzarli
-   raccontarli in modo business-oriented

Per un profilo junior è un ottimo progetto da portfolio perché mostra
sia competenze tecniche sia capacità di ragionamento.
