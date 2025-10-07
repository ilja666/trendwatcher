# 🔥 TRENDWATCHER PROJECT BRIEFING - CLAUDE

## 📋 PROJECT STATUS (Laatste update: Nu bezig met MEGA REDESIGN)

### ✅ WAT WERKT (LIVE):
- **URL:** https://trendwatcher-jjcy.onrender.com/
- **Hosting:** Render.com (gratis tier)
- **GitHub:** https://github.com/ilja666/trendwatcher

### 🎨 HUIDIGE TAAK: MULTI-THEME REDESIGN
**Ilja is tabak kopen - bezig met complete UI overhaul!**

## 🎯 NIEUWE DESIGN CONCEPT:

### **ELKE CATEGORY = EIGEN THEME/STIJL:**

1. **HOMEPAGE** - Krant/Newspaper layout
   - Wit/zwart/grijs, clean
   - Featured article links + sidebar rechts
   - Gainers/Losers panels rechts
   - Article-style content midden

2. **CRYPTO** - Cyberpunk (BEHOUDEN zoals nu!)
   - Dark theme (#0a0e27)
   - Purple/blue neon
   - Scanlines
   - Matrix-achtig

3. **STOCKS** - Bloomberg/Financial style
   - Professioneel
   - Grafieken
   - Rood/groen
   - Tables/charts

4. **E-COMMERCE** - Webshop/Catalog
   - Product grid
   - Prijzen
   - Clean, wit
   - Shopping feel

5. **ENTERTAINMENT** - Magazine/Landelijk
   - Zachte kleuren (beige/crème)
   - Grote imagery
   - Serif fonts
   - Glossy magazine feel

6. **SPORTS** - Unibet betting style
   - Groen gras achtergrond
   - Live badges
   - Odds-style layout
   - Betting site feel

## 🔧 TECHNISCHE STATUS:

### ✅ WERKENDE API's:
- **Crypto:** CoinGecko (live data)
- **Stocks:** Alpha Vantage (live data) - Key: `IIBD0TLOIBKW0AXZ`
- **Entertainment:** YouTube API (live data) - Key: `AIzaSyDunsmmrOuMurgvXTgr5zTyAvTtApMQprE`
- **E-commerce:** Demo data (Google Trends ready)
- **Sports:** Demo data

### 📊 ANALYTICS:
- Google Analytics ID: `G-HP85ZJG199`
- Tracking actief op live site

### 🗂️ PROJECT STRUCTUUR:
```
trendwatcher/
├── app.py                 # Flask server (5 routes)
├── apis/
│   ├── coingecko.py      # Crypto (LIVE)
│   ├── stocks.py         # Stocks (LIVE)
│   ├── entertainment.py  # YouTube (LIVE)
│   ├── ecommerce.py      # Demo data
│   └── sports.py         # Demo data
├── templates/
│   ├── index.html        # BEZIG MET REDESIGN!
│   └── index_backup.html # Backup van oude cyberpunk versie
├── .env                  # API keys (lokaal)
└── requirements.txt
```

## 🔑 API KEYS & CREDENTIALS:

### Alpha Vantage (Stocks):
```
ALPHA_VANTAGE_API_KEY=IIBD0TLOIBKW0AXZ
```

### YouTube (Entertainment):
```
YOUTUBE_API_KEY=AIzaSyDunsmmrOuMurgvXTgr5zTyAvTtApMQprE
```

### Google Analytics:
```
GA_TRACKING_ID=G-HP85ZJG199
```

### Render Environment Variables:
- `YOUTUBE_API_KEY` = ingesteld
- `ALPHA_VANTAGE_API_KEY` = waarschijnlijk niet (gebruikt hardcoded key in code)

## 🎨 DESIGN REQUIREMENTS:

### Layout Structure (Homepage/Krant):
```
┌────────────────────────────────────────────────────┐
│ TRENDWATCHER | [CRYPTO] [STOCKS] [E-COMM] etc.     │
├────────────────────────────────────┬───────────────┤
│                                    │ ┌─ GAINERS ─┐ │
│  FEATURED ARTICLE                  │ │ SPRB +1434││
│  ┌──────────────────┐              │ │ SOPA +275% ││
│  │ [IMAGE]          │              │ └───────────┘ │
│  │                  │              │ ┌─ LOSERS ──┐ │
│  └──────────────────┘              │ │ DOGE -15%  ││
│  Headline...                       │ └───────────┘ │
│  Article text...                   │               │
├────────────────────────────────────┤               │
│ TRENDING ITEMS GRID                │               │
└────────────────────────────────────┴───────────────┘
```

### Per Category Styling:
- **Crypto:** Dark cyberpunk (NIET AANPASSEN)
- **Stocks:** Financial/professional
- **E-commerce:** Bright webshop
- **Entertainment:** Magazine glossy
- **Sports:** Betting site green

## 📝 TODO NA REDESIGN:

1. ✅ Multi-theme layout implementeren
2. ⏳ Google Trends API toevoegen (e-commerce real data)
3. ⏳ Sports API toevoegen (TheSportsDB)
4. ⏳ ChatGPT markt strategie bespreken
5. ⏳ Monetization implementeren

## 🚨 BELANGRIJK:

- **Backup gemaakt:** `templates/index_backup.html`
- **Ilja wil:** Krant-style homepage met sidebar gainers/losers
- **Elke category:** Eigen unieke theme!
- **Crypto theme:** NIET veranderen (blijft cyberpunk)

## 💬 LAATSTE CONVERSATIE:

**Ilja:** "Ja ok het werkt, maar ik wil de layout anders. Per category een andere layout, ik wil de trending info in een paneel links met tabbladeren, gainers losers en trending"

**Ik liet screenshot zien van Trends.nl (krant-layout)**

**Ilja:** "JAAAA" → Akkoord op multi-theme concept

**Status:** Ilja is tabak kopen, ik ben bezig met complete redesign!

---

## 🎯 ALS JE OPNIEUW START:

1. Lees dit bestand
2. Check `templates/index_backup.html` voor oude versie
3. Check `templates/index.html` voor nieuwe versie (in progress)
4. Vraag Ilja: "Waar waren we gebleven met het redesign?"
5. Test live site: https://trendwatcher-jjcy.onrender.com/

---

**SUCCES! 🚀**
