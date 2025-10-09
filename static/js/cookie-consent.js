/**
 * Cookie Consent Banner - Belgian/EU GDPR Compliant
 * No cookie walls allowed - users can reject all cookies
 */

(function() {
  const CONSENT_KEY = 'tw_cookie_consent';
  const CONSENT_VERSION = '1.0';

  // Check if consent already given
  const existingConsent = localStorage.getItem(CONSENT_KEY);
  if (existingConsent) {
    const consent = JSON.parse(existingConsent);
    applyConsent(consent);
    return; // Don't show banner
  }

  // Show banner on first visit
  showConsentBanner();

  function showConsentBanner() {
    const banner = document.createElement('div');
    banner.id = 'cookie-consent-banner';
    banner.innerHTML = `
      <div style="position: fixed; bottom: 0; left: 0; right: 0; background: #1a1a1a; color: #fff; padding: 1.5rem; box-shadow: 0 -4px 20px rgba(0,0,0,0.3); z-index: 10000; border-top: 2px solid #7c3aed;">
        <div style="max-width: 1200px; margin: 0 auto; display: flex; gap: 1.5rem; align-items: center; flex-wrap: wrap;">
          <div style="flex: 1; min-width: 300px;">
            <h3 style="margin: 0 0 0.5rem; font-size: 1.1rem;">🍪 We Respect Your Privacy</h3>
            <p style="margin: 0; font-size: 0.9rem; color: #ccc;">
              We use cookies to improve your experience. You can accept all, reject all, or customize your preferences.
              <a href="/cookies" style="color: #7c3aed; text-decoration: underline;">Learn more</a>
            </p>
          </div>
          <div style="display: flex; gap: 0.75rem; flex-wrap: wrap;">
            <button onclick="cookieConsent.rejectAll()" style="padding: 0.75rem 1.5rem; background: #333; color: #fff; border: 1px solid #555; border-radius: 6px; cursor: pointer; font-weight: 600;">
              Reject All
            </button>
            <button onclick="cookieConsent.customize()" style="padding: 0.75rem 1.5rem; background: #444; color: #fff; border: 1px solid #666; border-radius: 6px; cursor: pointer; font-weight: 600;">
              Customize
            </button>
            <button onclick="cookieConsent.acceptAll()" style="padding: 0.75rem 1.5rem; background: #7c3aed; color: #fff; border: none; border-radius: 6px; cursor: pointer; font-weight: 600;">
              Accept All
            </button>
          </div>
        </div>
      </div>
    `;
    document.body.appendChild(banner);
  }

  function showCustomizeBanner() {
    const existing = document.getElementById('cookie-consent-banner');
    if (existing) existing.remove();

    const banner = document.createElement('div');
    banner.id = 'cookie-consent-banner';
    banner.innerHTML = `
      <div style="position: fixed; bottom: 0; left: 0; right: 0; background: #1a1a1a; color: #fff; padding: 1.5rem; box-shadow: 0 -4px 20px rgba(0,0,0,0.3); z-index: 10000; border-top: 2px solid #7c3aed; max-height: 80vh; overflow-y: auto;">
        <div style="max-width: 800px; margin: 0 auto;">
          <h3 style="margin: 0 0 1rem; font-size: 1.2rem;">🍪 Cookie Preferences</h3>

          <div style="margin-bottom: 1rem; padding: 1rem; background: #2a2a2a; border-radius: 6px;">
            <label style="display: flex; align-items: center; cursor: not-allowed;">
              <input type="checkbox" checked disabled style="margin-right: 0.75rem; width: 20px; height: 20px;">
              <div>
                <strong>Essential Cookies</strong>
                <p style="margin: 0.25rem 0 0; font-size: 0.85rem; color: #aaa;">Required for the website to function. Cannot be disabled.</p>
              </div>
            </label>
          </div>

          <div style="margin-bottom: 1rem; padding: 1rem; background: #2a2a2a; border-radius: 6px;">
            <label style="display: flex; align-items: center; cursor: pointer;">
              <input type="checkbox" id="consent-analytics" style="margin-right: 0.75rem; width: 20px; height: 20px;">
              <div>
                <strong>Analytics Cookies</strong>
                <p style="margin: 0.25rem 0 0; font-size: 0.85rem; color: #aaa;">Help us understand how visitors use the site (Google Analytics).</p>
              </div>
            </label>
          </div>

          <div style="margin-bottom: 1.5rem; padding: 1rem; background: #2a2a2a; border-radius: 6px;">
            <label style="display: flex; align-items: center; cursor: pointer;">
              <input type="checkbox" id="consent-marketing" style="margin-right: 0.75rem; width: 20px; height: 20px;">
              <div>
                <strong>Marketing Cookies</strong>
                <p style="margin: 0.25rem 0 0; font-size: 0.85rem; color: #aaa;">Track affiliate clicks to measure product recommendations.</p>
              </div>
            </label>
          </div>

          <div style="display: flex; gap: 0.75rem; justify-content: flex-end;">
            <button onclick="cookieConsent.saveCustom()" style="padding: 0.75rem 2rem; background: #7c3aed; color: #fff; border: none; border-radius: 6px; cursor: pointer; font-weight: 600;">
              Save Preferences
            </button>
          </div>
        </div>
      </div>
    `;
    document.body.appendChild(banner);
  }

  function saveConsent(consent) {
    const consentData = {
      version: CONSENT_VERSION,
      timestamp: new Date().toISOString(),
      essential: true, // Always true
      analytics: consent.analytics || false,
      marketing: consent.marketing || false
    };

    localStorage.setItem(CONSENT_KEY, JSON.stringify(consentData));

    // Send to backend for logging
    fetch('/cookie_consent', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(consentData)
    }).catch(err => console.error('Consent logging failed:', err));

    applyConsent(consentData);
    removeBanner();
  }

  function applyConsent(consent) {
    // Apply analytics consent
    if (consent.analytics) {
      loadGoogleAnalytics();
    }

    // Marketing cookies are handled by tracking.js based on consent
    window.cookieConsentGranted = {
      analytics: consent.analytics,
      marketing: consent.marketing
    };
  }

  function loadGoogleAnalytics() {
    // Only load GA if consent given
    const GA_ID = document.querySelector('script[src*="gtag"]')?.src.match(/id=(G-[A-Z0-9]+)/)?.[1];
    if (!GA_ID) return;

    // GA is already loaded in base.html, just configure it
    if (window.gtag) {
      window.gtag('consent', 'update', {
        'analytics_storage': 'granted'
      });
    }
  }

  function removeBanner() {
    const banner = document.getElementById('cookie-consent-banner');
    if (banner) banner.remove();
  }

  // Public API
  window.cookieConsent = {
    acceptAll: function() {
      saveConsent({ analytics: true, marketing: true });
    },

    rejectAll: function() {
      saveConsent({ analytics: false, marketing: false });
    },

    customize: function() {
      showCustomizeBanner();
    },

    saveCustom: function() {
      const analytics = document.getElementById('consent-analytics')?.checked || false;
      const marketing = document.getElementById('consent-marketing')?.checked || false;
      saveConsent({ analytics, marketing });
    },

    reset: function() {
      localStorage.removeItem(CONSENT_KEY);
      location.reload();
    }
  };
})();
