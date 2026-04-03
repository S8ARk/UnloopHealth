import os
import sys
from pymongo import MongoClient
from dotenv import load_dotenv

# Add parent directory to path so we can import from models
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models.database import db_instance

# Indian Food Staples - Normalized for 100g
INDIAN_STAPLES = [
    {"name": "Whole Wheat Roti", "category": "Bread", "calories": 264, "protein": 9.1, "carbs": 51.5, "fat": 3.2, "fiber": 7.0, "sugar": 0.4, "gi_index": 62},
    {"name": "Cooked Basmati Rice", "category": "Grain", "calories": 130, "protein": 2.7, "carbs": 28.2, "fat": 0.3, "fiber": 0.4, "sugar": 0.1, "gi_index": 50},
    {"name": "Yellow Moong Dal (Cooked)", "category": "Legumes", "calories": 105, "protein": 7.0, "carbs": 19.1, "fat": 0.4, "fiber": 4.5, "sugar": 1.2, "gi_index": 25},
    {"name": "Paneer (Cottage Cheese)", "category": "Dairy", "calories": 265, "protein": 18.3, "carbs": 3.4, "fat": 20.8, "fiber": 0, "sugar": 2.6, "gi_index": 5},
    {"name": "Chicken Curry", "category": "Poultry", "calories": 177, "protein": 19.5, "carbs": 3.2, "fat": 8.1, "fiber": 1.2, "sugar": 1.0, "gi_index": 0},
    {"name": "Mixed Vegetable Sabji", "category": "Vegetable", "calories": 85, "protein": 2.4, "carbs": 9.8, "fat": 4.5, "fiber": 3.1, "sugar": 2.5, "gi_index": 35},
    {"name": "Curd (Plain)", "category": "Dairy", "calories": 98, "protein": 3.4, "carbs": 4.7, "fat": 4.3, "fiber": 0, "sugar": 4.7, "gi_index": 28},
    {"name": "Idli (Rice & Lentil)", "category": "Breakfast", "calories": 39, "protein": 2.0, "carbs": 7.9, "fat": 0.1, "fiber": 0.5, "sugar": 0.2, "gi_index": 70},
    {"name": "Sambar", "category": "Legumes", "calories": 60, "protein": 3.2, "carbs": 9.5, "fat": 1.1, "fiber": 2.8, "sugar": 1.5, "gi_index": 30},
    {"name": "Masala Dosa", "category": "Breakfast", "calories": 168, "protein": 3.9, "carbs": 29.5, "fat": 3.7, "fiber": 2.1, "sugar": 0.5, "gi_index": 77},
    {"name": "Chana Masala", "category": "Legumes", "calories": 120, "protein": 5.4, "carbs": 18.2, "fat": 2.5, "fiber": 6.8, "sugar": 2.1, "gi_index": 28},
    {"name": "Aloo Paratha", "category": "Bread", "calories": 230, "protein": 4.5, "carbs": 35.2, "fat": 8.5, "fiber": 3.8, "sugar": 1.2, "gi_index": 70},
    {"name": "Gulab Jamun (1 piece)", "category": "Dessert", "calories": 150, "protein": 2.5, "carbs": 25.0, "fat": 6.0, "fiber": 0.1, "sugar": 22.0, "gi_index": 85},
    {"name": "Tea with Milk & Sugar", "category": "Beverage", "calories": 45, "protein": 1.2, "carbs": 7.5, "fat": 1.1, "fiber": 0, "sugar": 6.5, "gi_index": 45},
    {"name": "Samosa (1 piece)", "category": "Snack", "calories": 262, "protein": 4.5, "carbs": 24.5, "fat": 17.5, "fiber": 2.1, "sugar": 1.5, "gi_index": 80},
]

def seed_foods():
    # Connect to MongoDB
    if not db_instance.connect():
        print("Failed to connect for seeding.")
        return

    collection = db_instance.get_collection('foods')
    
    # Create text index for search
    collection.create_index([("name", "text")])
    print("Created text index for 'name'")

    # Clear existing data optional
    # collection.delete_many({})
    # print("Cleared existing foods")

    # Insert staples
    for food in INDIAN_STAPLES:
        collection.update_one(
            {"name": food["name"]},
            {"$set": food},
            upsert=True
        )
    
    print(f"Successfully seeded {len(INDIAN_STAPLES)} staples into the 'foods' collection.")

if __name__ == "__main__":
    seed_foods()
