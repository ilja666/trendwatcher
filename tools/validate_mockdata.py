"""
Mockdata Validation Script
===========================
Validates all mockdata JSON files for required fields.
"""

import json
import os

def validate_all():
    """Validate all mockdata files for required keys"""
    base = "static/mockdata"
    required = {
        "crypto": ["name", "symbol", "image", "price", "change"],
        "stocks": ["symbol", "name", "image", "price", "change"],
        "ecommerce": ["keyword", "category", "image", "value", "growth"],
        "entertainment": ["title", "type", "image", "platform", "popularity"],
        "sports": ["title", "sport", "league", "image", "status"]
    }

    print("🔍 Validating mockdata files...\n")
    errors_found = False

    for file in os.listdir(base):
        if not file.endswith('.json'):
            continue

        cat = file.replace(".json", "")
        keys = required.get(cat, [])
        filepath = os.path.join(base, file)

        print(f"📁 Checking {file}...")

        with open(filepath, encoding='utf-8') as f:
            data = json.load(f)

        for i, d in enumerate(data):
            missing = [k for k in keys if k not in d]
            if missing:
                print(f"   ❌ Item {i} missing keys: {missing}")
                errors_found = True

        if not any([k for k in keys if k not in item] for item in data):
            print(f"   ✅ All items valid ({len(data)} items)")

    if errors_found:
        print("\n⚠️  Validation failed! Fix missing keys above.")
        return False
    else:
        print("\n✅ All mockdata files valid!")
        return True

if __name__ == "__main__":
    success = validate_all()
    exit(0 if success else 1)
