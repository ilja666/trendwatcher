# ⚖️ LEGAL COMPLIANCE CHECKLIST — TrendWatcher (België / EU)

**Last updated:** 2025-10-09
**Jurisdiction:** België / European Union
**Applicable laws:** GDPR, EU Copyright Directive 2019/790, Belgian e-Privacy Law (Boek XII)

---

## 📋 Quick Status Overview

| Category | Status | Notes |
|----------|--------|-------|
| 🔒 GDPR Compliance | ⚠️ In Progress | Consent logging implemented, need privacy policy |
| 📧 Email Marketing | ⚠️ In Progress | Newsletter works, needs double opt-in |
| 🍪 Cookie Consent | ❌ Not Started | Required: banner + preference management |
| ©️ Copyright | ⚠️ Partial | Sources attributed, need licensing info |
| 🛡️ Data Security | ✅ Good | HTTPS, encrypted storage, minimal data |
| 📄 Legal Pages | ❌ Missing | Need /privacy, /terms, /cookies |

---

## 1️⃣ GDPR / AVG Compliance

### ✅ Data Minimization
- [ ] Only collect essential data (email, timestamp, IP hash)
- [ ] No unnecessary tracking or profiling
- [ ] Regular data cleanup (delete old logs after X days)

### ✅ Consent Management
- [x] Opt-in checkbox in newsletter form *(implemented)*
- [ ] Double opt-in confirmation email
- [x] Consent logs stored with timestamp *(data/subscribers.csv)*
- [ ] Consent withdrawal mechanism (`/unsubscribe`)
- [ ] Function: `log_consent(email, ip, timestamp, purpose)`
- [ ] Function: `withdraw_consent(email)`

### ✅ Transparency (Art. 13/14 GDPR)
- [ ] Privacy policy page (`/privacy`)
  - [ ] Who we are (legal entity, contact)
  - [ ] What data we collect (email, IP, clicks)
  - [ ] Why we collect it (newsletter, analytics, affiliate)
  - [ ] How long we keep it (retention periods)
  - [ ] Who has access (third parties: Render, NewsData.io)
  - [ ] User rights (access, rectification, erasure, portability)
- [ ] Cookie policy page (`/cookies`)
- [ ] Links to legal pages in footer *(needs update)*

### ✅ User Rights
- [ ] Right to access: `/account/data` endpoint to download user data
- [ ] Right to erasure: `/account/delete` to remove all data
- [ ] Right to rectification: ability to update email
- [ ] Right to object: unsubscribe from marketing
- [ ] Function: `delete_user_data(email)`

### ✅ Data Security
- [x] HTTPS enforced *(Render default)*
- [x] Password hashing (if applicable)
- [ ] IP address masking in logs (last octet: `192.168.1.xxx`)
- [ ] Encrypted database connections
- [ ] Regular security audits

### ✅ Data Breach Protocol
- [ ] Documented procedure for 72-hour notification to Belgian DPA
- [ ] Contact: [Autoriteit Bescherming Persoonsgegevens](https://www.gegevensbeschermingsautoriteit.be/)
- [ ] User notification process if breach affects them

### ✅ Processor Agreements
- [ ] Render.com: Data Processing Agreement (DPA) ✅
- [ ] NewsData.io: Check their GDPR compliance
- [ ] Mailchimp/Brevo: DPA when newsletter service is added

---

## 2️⃣ E-Marketing / Nieuwsbrief (Belgian Law)

### ✅ Consent Requirements
- [x] Explicit opt-in (checkbox) *(implemented)*
- [ ] **Double opt-in** (confirmation email) *(required in Belgium!)*
- [ ] Clear purpose description: "Weekly trend digest"
- [ ] Option to refuse at point of collection

### ✅ Soft Opt-In Exception
Only applicable if:
- [ ] User already purchased/used paid service
- [ ] Marketing is for similar products/services
- [ ] User had clear opt-out at initial collection

**TrendWatcher:** Currently free → use full opt-in, NOT soft opt-in

### ✅ Every Marketing Email Must Have
- [x] Unsubscribe link *(needs implementation)*
- [ ] Sender identity: "TrendWatcher - Brussel, België"
- [ ] Contact info: `legal@trendwatcher.be` or `info@trendwatcher.be`
- [ ] Reason for email: "You subscribed to our weekly trends"

### ✅ Record Keeping
- [x] Log: email, timestamp, IP (hashed), consent text version
- [ ] Ability to prove consent in case of complaint to DPA
- [ ] Retention: keep logs for 3 years after unsubscribe

---

## 3️⃣ Cookie Consent (Belgian/EU Rules)

### ✅ Cookie Banner Required
- [ ] Banner appears on first visit
- [ ] Categories: Essential, Analytics, Marketing
- [ ] User can accept/reject per category
- [ ] "Reject all" button (Belgian law: no cookie walls!)
- [ ] Link to full cookie policy

### ✅ Cookie Management
- [ ] Essential cookies (session): no consent needed
- [x] Analytics (Google Analytics): **needs consent** *(currently loads without asking!)*
- [x] Affiliate tracking cookies: **needs consent**
- [ ] Store preference in `localStorage`
- [ ] POST to `/cookie_consent` to log choice

### ✅ Implementation
- [ ] `static/js/cookies.js` with banner logic
- [ ] Conditional GA loading: only if `analytics=accepted`
- [ ] Cookie policy page with full list of cookies

**Reference:** [Didomi Belgium Cookie Rules](https://www.didomi.io/)

---

## 4️⃣ Copyright & Content Licensing

### ✅ EU Directive 2019/790 (Belgium)
- [ ] Press publishers' rights: need permission for article excerpts
- [ ] Belgian case law: Google News was sued for using headlines without license
- [ ] Solution: Use **only short summaries + link to source**

### ✅ Safe Practices
- [x] Article cards show: title, description (<200 chars), source, link *(implemented)*
- [x] "Read more →" links to original article *(implemented)*
- [ ] Copyright attribution: "© [Source Name]" visible on each card
- [ ] Disclaimer in footer: "TrendWatcher is a news aggregator. All content belongs to respective publishers."

### ✅ Licensing Strategy
- [ ] Whitelist of approved sources (where we have permission)
- [ ] Function: `check_source(source_url)` in `utils/licensing.py`
- [ ] Auto-citation: `build_citation(title, source, url)`

### ✅ DMCA / Takedown Procedure
- [ ] `/legal/report` form for copyright complaints
- [ ] Email: `dmca@trendwatcher.be`
- [ ] Process: remove within 24h, log complaint, notify uploader
- [ ] Counter-notice procedure

**Belgian contacts:**
- [SABAM](https://www.sabam.be/) (music/text rights)
- [Copiepresse](https://www.copiepresse.be/) (press rights)

---

## 5️⃣ Terms of Use / Disclaimer

### ✅ Required Sections
- [ ] Service description: "News aggregation and trending insights"
- [ ] User obligations: no scraping, no spam, lawful use only
- [ ] Intellectual property: "Content belongs to publishers, not us"
- [ ] Affiliate disclosure: "We earn commission from Amazon/eToro links"
- [ ] Limitation of liability: "We don't guarantee accuracy of trends"
- [ ] Dispute resolution: Belgian law applies, court in Brussels
- [ ] Modification clause: "We can update Terms, users will be notified"

### ✅ Affiliate Disclosure
Must be clearly visible:
> "TrendWatcher participates in affiliate programs. When you click product links, we may earn a commission at no extra cost to you."

**Location:** Footer + `/terms` page

---

## 6️⃣ Data Security Measures

### ✅ Technical Measures
- [x] HTTPS (SSL/TLS) *(Render default)*
- [ ] CSP (Content Security Policy) headers
- [x] SQL injection prevention (parameterized queries)
- [ ] XSS protection (escape user input)
- [ ] Rate limiting on forms (prevent spam)

### ✅ Organizational Measures
- [ ] Access control: only admin can view subscriber data
- [ ] Regular backups (Render auto-backup)
- [ ] Incident response plan documented

### ✅ Monitoring
- [x] Click tracking logs *(data/clicks.csv)*
- [x] Consent logs *(data/subscribers.csv)*
- [ ] Error logs (anonymized IPs)

---

## 7️⃣ Children's Data (Age Verification)

**Belgian rule:** Children 13+ can give consent themselves

- [ ] If target audience includes <13: require parental consent
- [ ] If not targeting children: add age gate or Terms clause: "Service is 13+ only"

**TrendWatcher:** Not targeting children → add to Terms: "You must be 13 or older to use this service"

---

## 8️⃣ Admin / Compliance Dashboard

### ✅ `/admin/compliance` Page
- [ ] List all consent records (email, date, status)
- [ ] Export button: download GDPR data as CSV
- [ ] Stats: total subscribers, opt-outs, cookie preferences
- [ ] Delete user button (GDPR erasure)

### ✅ Audit Trail
- [x] `data/subscribers.csv` - newsletter signups
- [x] `data/clicks.csv` - affiliate tracking
- [ ] `data/consent_log.csv` - detailed GDPR consent with IP, purpose, version
- [ ] `data/gdpr_requests.csv` - user requests (access, erasure)

---

## 9️⃣ Legal Entity Information

### ✅ Required in Footer
```
TrendWatcher
Brussel, België
KBO/BCE: [bedrijfsnummer wanneer je bedrijf hebt]
BTW: [btw-nummer wanneer omzet >25k€]
Contact: legal@trendwatcher.be
```

**If sole proprietor (eenmanszaak):**
```
TrendWatcher
Eigenaar: [Jouw naam]
Adres: [Straat, Postcode, Stad]
Email: info@trendwatcher.be
```

**If you don't have a company yet:** You can operate as individual, but once revenue starts, register as **eenmanszaak** or **BV** (Belgian company).

---

## 🔟 Pre-Launch Checklist

Before going live or promoting TrendWatcher:

- [ ] Privacy policy live at `/privacy`
- [ ] Terms of use live at `/terms`
- [ ] Cookie policy live at `/cookies`
- [ ] Cookie banner functional (with reject option)
- [ ] Newsletter has double opt-in confirmation
- [ ] Unsubscribe link works and logs action
- [ ] Footer has legal entity info + links to legal pages
- [ ] Affiliate disclosure visible
- [ ] DMCA form available at `/legal/report`
- [ ] Copyright attribution on every article card
- [ ] HTTPS enforced
- [ ] Google Analytics only loads with consent
- [ ] Test: full GDPR request flow (access, erasure)

---

## 📞 Legal Support Contacts

**If you need legal review:**
- **Belgian DPA:** https://www.gegevensbeschermingsautoriteit.be/
- **GDPR help:** info@privacycommission.be
- **Copyright Belgium:** https://economie.fgov.be/nl/themas/intellectuele-eigendom
- **Belgian bar association:** advocaat.be (find privacy lawyer)

**Recommended actions:**
1. Implement checklist items
2. Have a lawyer review privacy policy (€200-500 typically)
3. Register company if monetizing (KBO registration)
4. Get legal liability insurance (€150/year)

---

## ✅ Sign-Off

Once all items are checked:

**Reviewed by:** [Your name]
**Date:** [Date]
**Next review:** [Date + 6 months]

**Legal advisor consulted:** [ ] Yes [ ] No
**DPO appointed (if required):** [ ] Yes [ ] No (not required for small sites)

---

**Document version:** 1.0
**Last updated:** 2025-10-09
