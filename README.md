# Expense Tracker - IT Paušalni Obrt

Moderna web aplikacija za praćenje troškova izrađena pomoću Flask frameworka, prilagođena potrebama IT paušalnog obrta u Hrvatskoj. Aplikacija omogućuje kompletno upravljanje troškovima s naprednim funkcionalnostima za analizu i vizualizaciju podataka.

## ✨ Ključne Značajke

- 📊 **Kompletno praćenje troškova** - dodavanje, uređivanje, brisanje s detaljnim opisima
- 🏷️ **Upravljanje kategorijama** - prilagođene kategorije za IT obrt (hardver, softver, licence, porezi)
- 📈 **Napredni izvještaji** - interaktivni grafikoni i analitika trendova
- 🔄 **Ponavljajući troškovi** - označavanje redovitih plaćanja (osiguranje, porezi, pretplate)
- 📃 **Paginacija** - efikasno pregledavanje velikih količina podataka (10, 25, 50, 100, sve)
- 🔍 **Napredni filtri** - sortiranje po datumu, iznosu, kategoriji ili ID-u
- 📱 **Responzivni dizajn** - optimizirano za desktop i mobilne uređaje
- 🐳 **Docker podrška** - jednostavno pokretanje i deployment

## 🛠️ Tehnologije

- **Backend:** Python 3.12, Flask 2.3.3
- **Baza podataka:** SQLite s PonyORM 0.7.16
- **Frontend:** HTML5, CSS3, JavaScript (ES6+)
- **UI Framework:** Bootstrap 5
- **Grafikoni:** Chart.js
- **Containerization:** Docker & Docker Compose

## 📋 Preduvjeti

- Python 3.12+ ili Docker (ovisno o načinu pokretanja)

## 🚀 Pokretanje Docker containera

```bash
# Kloniraj repozitorij
git clone [repository-url]
cd expense_tracker_infsus

# Pokreni s Docker Compose
docker-compose up --build
```

Aplikacija će biti dostupna na `http://localhost:5001`

## 💻 Lokalna Instalacija

### 1. Kloniranje i setup
```bash
git clone [repository-url]
cd expense_tracker_infsus
```

### 2. Virtualno okruženje
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. Instalacija ovisnosti
```bash
pip install -r requirements.txt
```

### 4. Pokretanje
```bash
python app.py
```

## 📁 Struktura Projekta

```
expense_tracker_infsus/
├── 🐳 Docker konfiguracija
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── .dockerignore
│   └── requirements.txt
├── 🐍 Backend
│   ├── app.py                    # Glavna Flask aplikacija
│   └── populate_data.py          # Skripta za generiranje test podataka
├── 🎨 Frontend
│   ├── templates/
│   │   ├── layout.html           # Osnovni template
│   │   ├── index.html            # Dashboard
│   │   ├── expenses.html         # Upravljanje troškovima s paginacijom
│   │   ├── categories.html       # Upravljanje kategorijama
│   │   └── reports.html          # Izvještaji s Chart.js grafovima
│   └── static/
│       └── css/                  # Prilagođeni stilovi
├── 💾 Baza podataka
│   └── expense_tracker.sqlite    # SQLite baza (auto-generirana)
└── 📄 Dokumentacija
    └── README.md
```

## 🎯 Kategorije Troškova za IT Obrt

Aplikacija dolazi s unaprijed definiranim kategorijama prilagođenim hrvatskom IT paušalnom obrtu:

- **💊 Zdravstveno osiguranje** - HZZO doprinosi (118.67 EUR/mj)
- **👴 Mirovinsko osiguranje** - MIO I. stup (107.88 EUR/mj), MIO II. stup (35.96 EUR/mj)
- **💰 Paušalni porez** - Mjesečni paušalni porez (719.20 EUR/mj)
- **📜 Licence** - Softverske licence i pretplate
- **🏢 Najam** - Uredski prostor, hosting, cloud servisi
- **📢 Marketing** - Reklame, web stranica, branding
- **💻 Hardver** - Računala, oprema, periferali
- **💿 Softver** - Aplikacije, alati, subscriptions

## 📊 Napredne Funkcionalnosti

### Paginacija i Filtriranje
- **Paginacija:** 10, 25, 50, 100 ili prikaži sve troškove
- **Sortiranje:** po datumu, iznosu, kategoriji ili ID-u
- **Filtriranje:** po kategorijama s behrenjem trenutnih postavki

### Interaktivni Grafovi
- **Pie Chart:** Raspodjela troškova po kategorijama
- **Bar Chart:** Usporedba kategorija
- **Line Chart:** Kretanje troškova kroz vrijeme
- **Doughnut Chart:** Top 5 kategorija potrošnje
- **Comparison Chart:** Usporedba trenutnog i prethodnog mjeseca

### API Endpointi
```
GET  /api/chart-data           # Podaci za osnovne grafove
GET  /api/time-series-data     # Mjesečni trendovi
GET  /api/monthly-comparison   # Usporedba mjeseci
GET  /api/top-categories       # Top 5 kategorija
GET  /api/expense-summary      # Sažetak statistika
```

## 🐳 Docker Upravljanje

```bash
# Pokretanje u pozadini
docker-compose up -d --build

# Pregled logova
docker-compose logs -f

# Zaustavljanje
docker-compose down

# Rebuild bez cache
docker-compose build --no-cache

# Pristup containeru
docker-compose exec expense-tracker bash
```

## 💾 Upravljanje Podacima

### Test Podaci
Aplikacija automatski generira realne test podatke za IT obrt:
- 6 mjeseci povijesti troškova
- Stvarni iznosi poreza i doprinosa
- Realne cijene hardvera i softvera
- Ponavljajući troškovi (porezi, osiguranja)

### Backup Baze
```bash
# Backup SQLite baze
cp expense_tracker.sqlite backup_$(date +%Y%m%d).sqlite

# Restore iz backup-a
cp backup_20241208.sqlite expense_tracker.sqlite
```

## 🔧 Konfiguracija

### Environment Variables
```bash
FLASK_ENV=production          # Produkcijski mod
PYTHONUNBUFFERED=1           # Real-time logovi
```

### Portovi
- **5001** - Flask aplikacija
- **SQLite** - Lokalna baza (bez dodatnih portova)

## 🚀 Deployment

### Produkcija s Dockerom
```bash
# Build production image
docker build -t expense-tracker:prod .

# Deploy s production compose
docker-compose -f docker-compose.prod.yml up -d
```

### Nginx Proxy (preporučeno)
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://localhost:5001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 🤝 Doprinošenje

1. **Fork** repozitorij
2. **Stvori granu:** `git checkout -b feature/nova-funkcionalnost`
3. **Commit promjene:** `git commit -m 'Dodaj novu funkcionalnost'`
4. **Push:** `git push origin feature/nova-funkcionalnost`
5. **Pull Request:** Otvori PR s opisom promjena

## 🐛 Poznati Problemi i Rješenja

### Problem s Chart.js
```javascript
// Ako grafovi ne rade, provjeri console
console.log('Chart data received:', data);
```

### Problem s Pony ORM
```python
# Koristi list() za izbjegavanje lambda problema
expenses = list(Expense.select())
```

## 📞 Podrška

Za pitanja i probleme:
- **GitHub Issues:** [repository-url]/issues
- **Email:** your-email@example.com

## 📄 Licenca

Ovaj projekt je licenciran pod **MIT licencom** - pogledaj [LICENSE](LICENSE) datoteku za detalje.

## 🙏 Zahvale

- **Flask** zajednici za odličan framework
- **PonyORM** za jednostavan rad s bazom podataka
- **Chart.js** za moćne vizualizacije
- **Bootstrap** za responzivni UI

---

**Napravljen s ❤️ za hrvatsku IT zajednicu**