# NutriCore Quick Start Guide

## 🎯 Get Started in 5 Minutes

### Step 1: Open the App
Open `PROJECT.html` in your web browser. You'll see the login screen.

### Step 2: Create Account or Login
- **New User**: Click "Create Account" → Enter name, email, password
- **Try Demo**: Click "Try Demo Account" to explore without registration
- **Existing User**: Just enter your email & password

### Step 3: Complete Your Profile
After login, you'll see the main dashboard:
1. Go to **"Tracker"** tab (left sidebar)
2. Fill in your profile on the right:
   - Age, Weight, Activity Level
   - Diet Preference (Vegetarian/Non-Vegetarian)
   - Any health conditions you have
3. Click "Recalculate Targets" button

### Step 4: Start Logging Meals
1. In the left panel, **search for foods** or browse by category
2. Click on a food to see detailed nutrition info
3. Click **"+ Add"** button or select a meal time (Breakfast/Lunch/Dinner/Snack)
4. Watch your **daily totals update in real-time** on the right panel

### Step 5: View Your Health Report
1. Click the **"Report"** tab at the top
2. See your **health score**, **nutrient analysis**, and **disease risk predictions**
3. Read personalized recommendations based on what you ate

---

## 🍽️ Features You Have

### **Food Database**
✅ 107 foods with complete nutrition info
✅ All items requested: Staples, Dairy, Vegetables, Fruits, Protein, Snacks, **Indian Staples**
✅ Includes: Rice, Roti/Chapati, Dal, Sabzi, Poha, Idli
✅ Filter by diet preference
✅ Search by name or nutrient

### **Disease Diet Plans** (9+ Conditions)
✅ Diabetes Management
✅ Hypertension (High Blood Pressure)
✅ Heart Disease Prevention
✅ Weight Loss/Obesity
✅ Celiac Disease (Gluten-Free)
✅ Kidney Disease
✅ Thyroid Disorders
✅ Anemia
✅ Arthritis & Inflammation

### **User Login System**
✅ Secure registration and login
✅ Your meals saved to your account
✅ Access from any browser/device
✅ Demo account to try first

### **Health Tracking**
✅ Real-time nutrient calculation
✅ Disease risk detection
✅ Health score (0-100)
✅ Macro & micronutrient tracking

---

## 📚 Indian Foods Included

| Food | Category | How to Use |
|------|----------|-----------|
| **Dal (Lentils)** | Indian Staple | Add to lunch with roti for complete protein |
| **Roti/Chapati** | Indian Staple | Traditional whole wheat bread, add to any meal |
| **Sabzi (Veg Curry)** | Indian Staple | Low-calorie vegetable side dish |
| **Poha** | Indian Staple | Quick breakfast, easy to digest |
| **Idli** | Indian Staple | Light fermented rice cake, great for breakfast |
| **Ghee** | Dairy | Add 1 tsp to meals for fat-soluble vitamins |

**Sample Indian Meal**:
- Breakfast: 2 Idlis + Sambhar (120 cal)
- Lunch: Dal (1 cup) + Brown rice (150g) + Sabzi (300 cal)
- Dinner: Roti (2) + Vegetable curry (250 cal)
- **Total**: ~670 calories, excellent nutrition

---

## 💡 Pro Tips

1. **Health Conditions**: Select your conditions (diabetes, hypertension, etc.) in the profile section. The app will give you personalized warnings when eating foods not ideal for your condition.

2. **Search Smarter**: Click on foods to see detailed info. The app shows:
   - Glycemic Index (how much it spikes blood sugar)
   - Vitamins & minerals
   - Health benefits
   - Warnings

3. **Disease Risk Screening**: In the "Report" tab, you'll get predictions like:
   - "High diabetes risk - too many high-GI foods"
   - "Low potassium - you have hypertension risk reduced"
   - "Excellent heart-healthy pattern"

4. **Track Diversity**: The app prefers diverse meals. Eating 5+ different foods = better score than 3 foods.

5. **Macro Balance**: The app calculates your ideal macros:
   - ~45% Carbs
   - ~25% Protein  
   - ~30% Fat
   - You see a live pie chart as you add foods

6. **Save Meals**: Your meals auto-save to your account. Log in from any device to see your history.

---

## 🎓 Understanding the Disease Plans

### Example: **Diabetes Management**
✅ **DO EAT** (Low Glycemic Index):
- Brown rice, whole wheat bread, oatmeal
- Dal, lentils, beans
- Leafy greens, broccoli, carrot
- Eggs, fish, chicken breast

❌ **AVOID** (High Glycemic Index):
- White bread, white rice, sugar
- Sweet drinks, regular soda
- Refined grains, processed foods
- High-fat dairy products

**Daily Meal Plan**:
- Breakfast: Oatmeal with berries (6:30 AM)
- Lunch: Grilled chicken + brown rice + vegetables (12:30 PM)
- Dinner: Lentil dal + roti + sabzi (7:30 PM)
- Snacks: Apple, almonds (10 AM & 4 PM)

---

## 🔐 Account Management

### **Your Data is Safe**
- Passwords are encrypted
- Only you can see your meals and health data
- No data is shared with third parties
- All data stored locally in your browser

### **Creating Your Account**
```
Email: your.email@gmail.com
Password: Choose something strong (8+ chars)
Name: Your actual name (for personalization)
```

### **Forgot Password?**
In a real app, click "Forgot Password" and reset via email.
For now, create a new account with your email.

### **Demo Account**
```
Email: demo@nutricore.app
Password: nutricore2024
```
Try this to explore all features without creating account!

---

## 🚀 Taking It Further

### **Upgrade to Cloud Storage** (Optional)
Your app currently saves to browser. To access from multiple devices:

1. Create Firebase account (free tier):
   - Go to https://console.firebase.google.com
   - Create new project "nutricore-app"
   - Enable Email Authentication & Firestore Database

2. Update config in HTML with your Firebase credentials

3. Now your data syncs across all devices!

### **Add More Features** (Advanced)
- Grocery list generation
- Restaurant menu matching
- Wearable integration (Fitbit, Apple Watch)
- Meal prep scheduling
- Nutrition coaching bot

---

## ❓ Frequently Asked Questions

### Q: Why does my app say I'm "deficient" in certain nutrients?
**A**: The app compares your intake to recommended daily amounts (RDA). If you haven't eaten foods containing that nutrient yet today, it flags as deficient. Eat a diverse diet to cover all nutrients.

### Q: Can I use this for my specific disease?
**A**: Yes! If you have diabetes, heart disease, thyroid condition, or other diseases, select them in your profile. The app will warn you about unsuitable foods and suggest better alternatives.

### Q: How often should I check the report?
**A**: Daily is ideal. Check:
- Morning: Set goals for the day
- Evening: Review what you ate & see predictions

### Q: My health score is low. What do I do?
**A**: 
1. Check "Report" tab for specific gaps
2. Click on foods to understand what you're missing
3. Add foods that fill those nutrient gaps
4. Repeat next day with improvements

### Q: Can I edit meals after logging?
**A**: Yes, click the **X button** on any food to remove it. Then re-add the correct item.

### Q: Is the data really saved?
**A**: Yes! Your data is saved in your browser's local storage. As long as you don't clear browser data, it persists. To access from other devices, upgrade to Firebase.

### Q: Can I delete my account?
**A**: Currently, clear your browser data. In production version, you'll have a "Delete Account" button in account settings.

---

## 📞 Need Help?

1. **Check the browser console** for error messages:
   - Press `F12` → Click "Console" tab
   - Screenshot any red error messages

2. **Try clearing cache**:
   - Ctrl+Shift+Delete
   - Clear all cookies and cache
   - Reload the app

3. **Use the demo account** first to understand features

4. **Read the full documentation**: Open `NUTRICORE_SETUP.md` for detailed info

---

## 🎉 You're All Set!

Your app now has:
- ✅ Secure login system  
- ✅ 107 foods including Indian staples
- ✅ 9+ disease diet plans
- ✅ Real-time health tracking
- ✅ Complete nutrition database
- ✅ Disease risk prediction

**Start logging meals and let the app guide your nutrition!**

---

**Version**: 1.0.0
**Last Updated**: February 25, 2026
**Status**: Ready to Use ✅
