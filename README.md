# 📊 TrendWatcher - Crypto Trending Dashboard

Een eenvoudige Flask webapp die trending cryptocurrency data ophaalt van de gratis CoinGecko API.

## 🚀 Lokaal Starten

### Stap 1: Installeer dependencies
```bash
cd trendwatcher
pip install -r requirements.txt
```

### Stap 2: Start de applicatie
```bash
python app.py
```

### Stap 3: Open in browser
- Dashboard: http://127.0.0.1:5000/dashboard
- API endpoint: http://127.0.0.1:5000/crypto/trending

## 📁 Project Structuur

```
trendwatcher/
├── app.py                  # Hoofd Flask applicatie
├── apis/
│   └── coingecko.py       # CoinGecko API integratie
├── templates/
│   └── index.html         # Dashboard frontend
├── requirements.txt       # Python dependencies
└── README.md             # Deze file
```

## 🌐 Gratis Deployment Opties

### Optie 1: Render.com (Aanbevolen)

1. **Maak een account** op [Render.com](https://render.com)

2. **Maak een `render.yaml` file** in je project root:
```yaml
services:
  - type: web
    name: trendwatcher
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn app:app
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
```

3. **Push naar GitHub** en connect met Render

4. **Deploy!** - Render detecteert automatisch je configuratie

### Optie 2: Railway.app

1. **Maak een account** op [Railway.app](https://railway.app)

2. **Maak een `Procfile`** in je project root:
```
web: gunicorn app:app
```

3. **Connect GitHub repo** en deploy

4. Railway detecteert automatisch Python en installeert dependencies

### Optie 3: PythonAnywhere (Gratis tier beschikbaar)

1. **Maak account** op [PythonAnywhere.com](https://www.pythonanywhere.com)

2. **Upload je bestanden** via de Files tab

3. **Configureer Web app**:
   - Python version: 3.10
   - Source code: `/home/yourusername/trendwatcher`
   - WSGI file: point naar `app.py`

4. **Reload** en je app is live!

## 🔧 Technische Details

- **Backend**: Flask (Python web framework)
- **API**: CoinGecko public API (gratis, geen key nodig)
- **Frontend**: Vanilla JavaScript met Fetch API
- **Styling**: Pure CSS met gradient backgrounds

## 📝 API Endpoints

### GET `/crypto/trending`
Haalt trending crypto data op.

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "name": "Bitcoin",
      "symbol": "BTC",
      "market_cap_rank": 1,
      "thumb": "https://...",
      "score": 0
    }
  ]
}
```

### GET `/dashboard`
Toont het HTML dashboard.

## 💡 Uitbreidingen (Optioneel)

- Voeg meer API endpoints toe (bijv. Bitcoin price, NFT trends)
- Implementeer caching om API calls te beperken
- Voeg een database toe om historische data bij te houden
- Maak een real-time update met WebSockets

## 📄 Licentie

Free to use - MIT License
