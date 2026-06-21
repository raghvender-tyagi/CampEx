import os
import django

# Set settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
django.setup()

from listings.models import Category

def seed_categories():
    categories = [
        {"name": "Books & Study", "slug": "books", "icon": "book"},
        {"name": "Electronics", "slug": "electronics", "icon": "laptop"},
        {"name": "Cycles & Rides", "slug": "cycles", "icon": "bike"},
        {"name": "Hostel Essentials", "slug": "hostel-essentials", "icon": "home"},
        {"name": "Fashion & Wearables", "slug": "fashion", "icon": "shirt"},
        {"name": "Stationery & Tools", "slug": "stationery", "icon": "pen-tool"}
    ]
    
    print("Seeding categories...")
    for cat in categories:
        obj, created = Category.objects.get_or_create(
            slug=cat["slug"],
            defaults={"name": cat["name"], "icon": cat["icon"]}
        )
        if created:
            print(f"Created category: {cat['name']}")
        else:
            obj.name = cat["name"]
            obj.icon = cat["icon"]
            obj.save()
            print(f"Updated/Verified category: {cat['name']}")

if __name__ == "__main__":
    seed_categories()
