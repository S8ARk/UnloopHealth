from server.models.database import db_instance

foods = [
    {"name": "Boiled Eggs", "calories": 155, "protein": 13, "carbs": 1.1, "fats": 11, "dietType": "Non-Veg", "per_unit": "2 whole eggs"},
    {"name": "Chicken Breast (Grilled)", "calories": 165, "protein": 31, "carbs": 0, "fats": 3.6, "dietType": "Non-Veg", "per_unit": "100g"},
    {"name": "Paneer Tikka", "calories": 265, "protein": 14, "carbs": 10, "fats": 20, "dietType": "Veg", "per_unit": "150g"},
    {"name": "Roti", "calories": 105, "protein": 3, "carbs": 22, "fats": 0.5, "dietType": "Vegan", "per_unit": "1 piece"},
    {"name": "Basmati Rice (Cooked)", "calories": 130, "protein": 2.7, "carbs": 28, "fats": 0.3, "dietType": "Vegan", "per_unit": "100g"},
    {"name": "Dal Tadka", "calories": 180, "protein": 9, "carbs": 20, "fats": 6, "dietType": "Vegan", "per_unit": "1 cup"},
    {"name": "Greek Yogurt", "calories": 100, "protein": 10, "carbs": 3, "fats": 4, "dietType": "Veg", "per_unit": "100g"},
    {"name": "Salmon (Grilled)", "calories": 208, "protein": 20, "carbs": 0, "fats": 13, "dietType": "Non-Veg", "per_unit": "100g"},
    {"name": "Oatmeal with Honey", "calories": 150, "protein": 6, "carbs": 27, "fats": 2.5, "dietType": "Veg", "per_unit": "1 bowl"},
    {"name": "Tofu Stir Fry", "calories": 144, "protein": 15, "carbs": 3, "fats": 8, "dietType": "Vegan", "per_unit": "100g"},
    {"name": "Almonds", "calories": 579, "protein": 21, "carbs": 21, "fats": 49, "dietType": "Vegan", "per_unit": "100g"},
    {"name": "Banana", "calories": 89, "protein": 1.1, "carbs": 23, "fats": 0.3, "dietType": "Vegan", "per_unit": "1 medium"},
    {"name": "Avocado", "calories": 160, "protein": 2, "carbs": 8, "fats": 15, "dietType": "Vegan", "per_unit": "1 half"},
    {"name": "Beef Steak", "calories": 271, "protein": 26, "carbs": 0, "fats": 19, "dietType": "Non-Veg", "per_unit": "100g"},
    {"name": "Whey Protein Shake", "calories": 120, "protein": 24, "carbs": 3, "fats": 1, "dietType": "Veg", "per_unit": "1 scoop"},
    {"name": "Quinoa Bowl", "calories": 222, "protein": 8, "carbs": 39, "fats": 3.6, "dietType": "Vegan", "per_unit": "1 cup cooked"},
    {"name": "Sweet Potato (Baked)", "calories": 90, "protein": 2, "carbs": 20, "fats": 0.1, "dietType": "Vegan", "per_unit": "1 medium"},
    {"name": "Black Beans Canned", "calories": 132, "protein": 8.9, "carbs": 23.7, "fats": 0.5, "dietType": "Vegan", "per_unit": "100g"},
    {"name": "Tuna Salad", "calories": 250, "protein": 22, "carbs": 5, "fats": 15, "dietType": "Non-Veg", "per_unit": "1 bowl"},
    {"name": "Scrambled Eggs", "calories": 199, "protein": 14, "carbs": 2, "fats": 15, "dietType": "Non-Veg", "per_unit": "2 eggs with oil"}
]

coll = db_instance.get_collection('foods')
coll.delete_many({}) # Clear old schema elements safely
coll.insert_many(foods)
print(f"Successfully seeded database with {len(foods)} tagged dietary options!")
