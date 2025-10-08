# 🚀 FASE 4.9 — Live News Feed Integration

## 📋 Overzicht
Integreer echte nieuwsartikelen via NewsData.io API in alle categorieën.
Elke pagina toont relevante trending nieuws met thumbnails, titels en links.

## 🎯 Doelen
- ✅ Alle categorieën tonen échte nieuwsartikels
- ✅ Unified data structure (title, description, image, url, source)
- ✅ Caching om rate limits te respecteren (15 min TTL)
- ✅ Fallback naar mockdata bij API failures
- ✅ Automatisch up-to-date content

---

## 🧠 Architectuur

### API Source Mapping
| Categorie | API Source | Query |
|-----------|-----------|-------|
| **Crypto** | NewsData.io | "cryptocurrency OR bitcoin OR blockchain" |
| **Stocks** | NewsData.io | "stock market OR finance OR earnings" |
| **E-commerce** | NewsData.io | "e-commerce OR shopping OR retail" |
| **Entertainment** | NewsData.io | "music OR movies OR celebrity" |
| **Sports** | NewsData.io | "sports OR football OR basketball" |

### Data Structure
```python
{
    "title": "Article headline",
    "description": "Brief summary (200 chars)",
    "source": "Source name",
    "url": "Article URL",
    "image": "Thumbnail URL",
    "published": "ISO timestamp"
}
```

---

## 🛠️ Implementatie

### 1. NewsData.io API Integration
**File:** `apis/newsfeeds.py` ✅ (Already created with caching)

Key features:
- Query per category via `CATEGORY_QUERIES` dict
- 15-minute cache via `utils/cache.py`
- Fallback to mockdata when API unavailable
- Limit to 10 articles per request

### 2. Update App Routes
**File:** `app.py`

Replace current API calls with newsfeeds:

```python
from apis.newsfeeds import get_articles

@app.route('/crypto')
def crypto():
    # Get news articles instead of coins
    articles = get_articles("crypto", limit=10)

    # Keep gainers/losers from CoinGecko for sidebar
    coins = get_trending_crypto() or load_mock('crypto')
    gainers = sorted(coins, key=lambda x: x.get('change', 0), reverse=True)[:5]
    losers = sorted(coins, key=lambda x: x.get('change', 0))[:5]

    return render_template(
        'crypto.html',
        category='crypto',
        theme='cyberpunk',
        articles=articles,  # News articles in main feed
        gainers=gainers,    # Crypto gainers in sidebar
        losers=losers,
        trending=articles[:5],
        GA_ID=GA_TRACKING_ID
    )
```

**Apply same pattern to:**
- `/stocks` - Stock news + stock gainers/losers
- `/ecommerce` - Shopping news + trending products
- `/entertainment` - Entertainment news + trending shows
- `/sports` - Sports news + upcoming matches

### 3. Template Integration
**File:** `templates/base_category.html` ✅ (Already supports articles)

Current template already handles:
- `item.image or item.thumb` for thumbnails
- `item.title or item.name` for headlines
- `item.description` for summaries
- Article cards with images

**Enhancement needed:**
- Add `item.url` for external links
- Add `item.source` for attribution
- Add "Read more →" link to full article

---

## 🔧 Technical Details

### Caching Strategy
```python
# Cache key per category
cache_key = f"news_{category}"

# 15 minute TTL (900 seconds)
set_cache(cache_key, articles, ttl=900)

# Result: 200 requests/day → 96 requests/day (at 15min intervals)
```

### Rate Limit Management
**NewsData.io Free Tier:**
- 200 requests/day
- With 5 categories × 96 requests/day = 480 potential requests
- With caching: 5 × 96 = 480 → Too high!
- **Solution**: Share cache across similar queries OR increase TTL to 30min

### Fallback Hierarchy
1. **Cache hit** → Return cached articles (fastest)
2. **API call** → Fetch fresh articles from NewsData.io
3. **API failure** → Load mockdata from `static/mockdata/{category}.json`
4. **No mockdata** → Return empty list

---

## 📦 Environment Variables

Add to Render.com environment:
```bash
NEWSDATA_API_KEY=your_newsdata_api_key_here
```

Get free key: https://newsdata.io/register

---

## ✅ Testing Checklist

- [ ] Local: All categories show news articles with images
- [ ] Local: Sidebar still shows gainers/losers (separate API)
- [ ] Local: Cache reduces API calls (check console logs)
- [ ] Local: Fallback works when API key is missing
- [ ] Deploy: Set NEWSDATA_API_KEY on Render
- [ ] Production: Verify all pages load with fresh news
- [ ] Production: Check 15min cache is working (timestamps)

---

## 🚀 Deployment Steps

1. **Test locally** with/without API key
2. **Commit changes** to main branch
3. **Add API key** to Render environment variables
4. **Deploy** via GitHub push
5. **Verify** all categories on production

---

## 📊 Expected Outcome

**Before:**
- Static mockdata with placeholder content
- No real-time updates
- Manual data maintenance

**After:**
- Live news articles from NewsData.io
- Auto-refresh every 15 minutes
- Thumbnails, titles, descriptions, source attribution
- External links to full articles
- Fully automated content pipeline

---

**Status:** Ready for implementation ✅
**Dependencies:** newsfeeds.py ✅, cache.py ✅, base_category.html ✅
**Next Step:** Update app.py routes
