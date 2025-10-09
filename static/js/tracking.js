/**
 * Affiliate Click Tracking
 * Tracks clicks on affiliate links for analytics
 */

document.addEventListener('DOMContentLoaded', function() {
  // Track all affiliate button clicks
  const affiliateLinks = document.querySelectorAll('a.affiliate-btn, a[href*="amazon"], a[href*="etoro"], a[href*="bol.com"]');

  affiliateLinks.forEach(link => {
    link.addEventListener('click', function(e) {
      const url = this.href;
      const label = this.textContent.trim();

      // Send tracking event to backend
      fetch('/track_click', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          url: url,
          label: label,
          timestamp: new Date().toISOString()
        })
      }).catch(err => console.error('Tracking failed:', err));

      // Don't prevent default - let link open normally
    });
  });

  // Track newsletter signups
  const newsletterForm = document.querySelector('.newsletter-form');
  if (newsletterForm) {
    newsletterForm.addEventListener('submit', function() {
      fetch('/track_click', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          url: '/subscribe',
          label: 'Newsletter Signup',
          timestamp: new Date().toISOString()
        })
      }).catch(err => console.error('Tracking failed:', err));
    });
  }
});
