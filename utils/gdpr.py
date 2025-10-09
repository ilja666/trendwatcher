"""
GDPR Compliance Utilities
Consent logging, data erasure, user rights management
"""

import os
import csv
import hashlib
from datetime import datetime
import threading

_gdpr_lock = threading.Lock()

# File paths
CONSENT_LOG = "data/consent_log.csv"
SUBSCRIBERS_FILE = "data/subscribers.csv"

def hash_ip(ip_address):
    """Hash IP address for privacy (GDPR minimization)"""
    if not ip_address:
        return "unknown"
    return hashlib.sha256(ip_address.encode()).hexdigest()[:16]

def log_consent(email, ip, purpose, consent_given=True, extra_data=None):
    """
    Log user consent for GDPR audit trail

    Args:
        email: User email
        ip: IP address (will be hashed)
        purpose: Purpose of consent (newsletter, analytics, marketing)
        consent_given: True for opt-in, False for opt-out
        extra_data: Additional context (e.g., consent version)
    """
    os.makedirs("data", exist_ok=True)

    with _gdpr_lock:
        file_exists = os.path.exists(CONSENT_LOG)

        with open(CONSENT_LOG, "a", encoding="utf-8", newline='') as f:
            writer = csv.writer(f)

            if not file_exists:
                writer.writerow([
                    "timestamp", "email", "ip_hash", "purpose",
                    "consent_given", "extra_data"
                ])

            writer.writerow([
                datetime.now().isoformat(),
                email,
                hash_ip(ip),
                purpose,
                "yes" if consent_given else "no",
                extra_data or ""
            ])

    print(f"[GDPR] Consent logged: {email} - {purpose} - {consent_given}")

def withdraw_consent(email, purpose="all"):
    """
    Log consent withdrawal

    Args:
        email: User email
        purpose: Which consent to withdraw ("all", "newsletter", "analytics", "marketing")
    """
    log_consent(email, None, purpose, consent_given=False, extra_data="withdrawal")

    # If newsletter withdrawal, remove from subscribers
    if purpose in ["all", "newsletter"]:
        remove_subscriber(email)

def remove_subscriber(email):
    """Remove email from newsletter subscribers"""
    if not os.path.exists(SUBSCRIBERS_FILE):
        return

    with _gdpr_lock:
        # Read all subscribers
        subscribers = []
        with open(SUBSCRIBERS_FILE, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            subscribers = [row for row in reader if row['email'] != email]

        # Write back without the removed email
        with open(SUBSCRIBERS_FILE, "w", encoding="utf-8", newline='') as f:
            if subscribers:
                fieldnames = subscribers[0].keys()
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(subscribers)

    print(f"[GDPR] Subscriber removed: {email}")

def get_user_data(email):
    """
    Get all data we have for a user (GDPR right to access)

    Returns dict with all user data
    """
    user_data = {
        "email": email,
        "newsletter_subscribed": False,
        "consent_logs": [],
        "clicks": []
    }

    # Check newsletter subscription
    if os.path.exists(SUBSCRIBERS_FILE):
        with open(SUBSCRIBERS_FILE, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['email'] == email:
                    user_data["newsletter_subscribed"] = True
                    user_data["subscription_date"] = row.get('timestamp', '')
                    break

    # Get consent logs
    if os.path.exists(CONSENT_LOG):
        with open(CONSENT_LOG, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['email'] == email:
                    user_data["consent_logs"].append(row)

    # Get click logs (if they exist)
    clicks_file = "data/clicks.csv"
    if os.path.exists(clicks_file):
        with open(clicks_file, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Clicks are not tied to email, skip for now
                pass

    return user_data

def delete_user_data(email):
    """
    Delete all user data (GDPR right to erasure / right to be forgotten)

    Args:
        email: User email to delete

    Returns:
        bool: True if data was deleted
    """
    deleted = False

    # Remove from subscribers
    if os.path.exists(SUBSCRIBERS_FILE):
        with _gdpr_lock:
            subscribers = []
            with open(SUBSCRIBERS_FILE, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                subscribers = [row for row in reader if row['email'] != email]

            with open(SUBSCRIBERS_FILE, "w", encoding="utf-8", newline='') as f:
                if subscribers:
                    fieldnames = subscribers[0].keys()
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(subscribers)
            deleted = True

    # Log erasure in consent log (for audit purposes)
    log_consent(email, None, "data_erasure", consent_given=False, extra_data="Right to be forgotten")

    print(f"[GDPR] User data deleted: {email}")
    return deleted

def get_consent_records():
    """Get all consent records (for admin dashboard)"""
    records = []

    if os.path.exists(CONSENT_LOG):
        with open(CONSENT_LOG, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            records = list(reader)

    return records
