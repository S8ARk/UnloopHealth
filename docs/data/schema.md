# Database Schemas & DDL (Multi-Modal)

## Relational Layer (PostgreSQL)
Handles robust, structured relations.

### `users` Table
- `id` (UUID, Primary Key)
- `email` (VARCHAR, Unique, Indexed)
- `password_hash` (VARCHAR)
- `created_at` (TIMESTAMP)
- `updated_at` (TIMESTAMP)

### `profiles` Table
- `id` (UUID, Primary Key)
- `user_id` (UUID, Foreign Key -> users.id)
- `name` (VARCHAR)
- `age` (INTEGER)
- `weight_kg` (DECIMAL)
- `height_cm` (DECIMAL)
- `diet_preference` (VARCHAR)
- `disease_conditions` (ARRAY/JSONB)

### `goals` Table
- `id` (UUID, Primary Key)
- `user_id` (UUID, Foreign Key -> users.id)
- `target_calories` (INTEGER)
- `target_protein_g` (INTEGER)
- `target_carbs_g` (INTEGER)
- `target_fat_g` (INTEGER)
- `created_at` (TIMESTAMP)

---

## Document Layer (MongoDB)
Handles flexible, semi-structured schemas.

### `foods` Collection
```json
{
  "_id": "ObjectId",
  "name": "String",
  "category": "String",
  "calories": "Number",
  "macros": {
    "protein": "Number",
    "carbs": "Number",
    "fat": "Number"
  },
  "micros": {
    "vitamins": "Map",
    "minerals": "Map"
  },
  "gi_index": "Number",
  "ai_metadata": "Object"
}
```

### `meal_logs` Collection
```json
{
  "_id": "ObjectId",
  "user_id": "String (UUID from PostgreSQL)",
  "timestamp": "ISODate",
  "meal_type": "String (Breakfast/Lunch/Dinner/Snack)",
  "foods_consumed": [
    {
      "food_id": "ObjectId",
      "quantity_g": "Number",
      "ai_confidence_score": "Number (optional)"
    }
  ],
  "total_nutrients_calculated": "Object",
  "health_score_impact": "Number"
}
```
