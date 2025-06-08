# Praćenje Troškova

Web aplikacija za praćenje troškova izrađena pomoću Flask frameworka koja pomaže korisnicima u upravljanju i vizualizaciji osobnih troškova.

## Značajke

- Praćenje dnevnih troškova s opisima i kategorijama
- Upravljanje kategorijama troškova
- Pregled detaljnih izvještaja i analitika
- Vizualizacija obrazaca potrošnje kroz interaktivne grafikone
- Responzivni dizajn za desktop i mobilne uređaje

## Tehnologije

- **Backend:** Python 3.9 s Flask-om
- **Baza podataka:** SQLite s PonyORM
- **Frontend:** HTML, CSS, JavaScript
- **UI Framework:** Bootstrap 5
- **Grafikoni:** Chart.js

## Preduvjeti

- Python 3.9 ili noviji
- Docker (opcionalno)

## Instalacija

1. Klonirajte repozitorij:
```bash
git clone [repository-url]
cd expense_tracker_infsus
```

2. Kreirajte virtualno okruženje (preporučeno):
```bash
python -m venv venv
source venv/bin/activate  # Na Windows: venv\Scripts\activate
```

3. Instalirajte potrebne pakete:
```bash
pip install -r requirements.txt
```

## Pokretanje Aplikacije

### Lokalni Razvoj

Pokrenite Flask aplikaciju:
```bash
python app.py
```
Aplikacija će biti dostupna na `http://localhost:5001`

### Korištenje Dockera

1. Izgradite Docker image:
```bash
docker build -t expense-tracker .
```

2. Pokrenite container:
```bash
docker run -p 5001:5001 expense-tracker
```

## Struktura Projekta

```
expense_tracker_infsus/
├── app.py                 # Glavna aplikacijska datoteka
├── requirements.txt       # Python ovisnosti
├── Dockerfile            # Docker konfiguracija
├── expense_tracker.sqlite # SQLite baza podataka
├── static/
│   └── css/
│       └── style.css     # Prilagođeni CSS stilovi
└── templates/            # HTML predlošci
    ├── layout.html       # Osnovni predložak
    ├── index.html        # Početna stranica
    ├── expenses.html     # Upravljanje troškovima
    ├── categories.html   # Upravljanje kategorijama
    └── reports.html      # Izvještaji i analitika
```

## Detaljne Značajke

### Upravljanje Troškovima
- Dodavanje, uređivanje i brisanje troškova
- Kategorizacija troškova
- Postavljanje datuma troška
- Pregled povijesti troškova

### Upravljanje Kategorijama
- Stvaranje prilagođenih kategorija troškova
- Uređivanje naziva kategorija
- Brisanje kategorija (sa pripadajućim troškovima)

### Izvještaji i Analitika
- Pregled ukupnih troškova
- Raspodjela troškova po kategorijama
- Mjesečna usporedba
- Interaktivni grafikoni:
  - Tortni grafikon za raspodjelu kategorija
  - Stupčasti grafikon za usporedbu troškova
  - Linijski grafikon za trendove troškova
  - Kružni grafikon za top kategorije potrošnje

## API Krajnje Točke

### Glavne Rute
- `/` - Početna stranica
- `/expenses` - Upravljanje troškovima
- `/categories` - Upravljanje kategorijama
- `/reports` - Izvještaji i analitika

### API Rute
- `/api/chart-data` - Dohvaćanje podataka o troškovima po kategorijama
- `/api/time-series-data` - Dohvaćanje mjesečnih trendova troškova
- `/api/monthly-comparison` - Dohvaćanje usporedbe trenutnog i prethodnog mjeseca

## Doprinošenje Projektu

1. Fork-ajte repozitorij
2. Kreirajte novu granu za značajku
3. Commit-ajte vaše promjene
4. Push-ajte u granu
5. Kreirajte Pull Request

## Licenca

Ovaj projekt je otvorenog koda i dostupan je pod MIT licencom.