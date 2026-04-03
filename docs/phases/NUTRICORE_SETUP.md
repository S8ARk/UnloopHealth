# NutriCore - Complete Setup & Documentation

## 📋 Overview

NutriCore is an **AI-powered personalized nutrition and diet tracking application** that provides:

- ✅ **User Authentication System** - Secure login/registration with local database
- ✅ **Comprehensive Food Database** - 100+ foods including Indian staples
- ✅ **Disease-Specific Diet Plans** - Customized meal plans for 9+ health conditions
- ✅ **Nutrition Tracking** - Real-time meal logging and nutrient analysis
- ✅ **Health Scoring** - Dynamic health score based on dietary choices
- ✅ **Multi-Language Support** - Staples, Dairy, Vegetables, Protein, Snacks, Indian Staples

---

## 🎯 Key Features

### 1. **Food Database** (foodDatabase.js)
Contains **107 foods** organized by category:
- **Staples/Grains**: Rice, bread, oatmeal, pasta, cereal (7 items)
- **Dairy**: Milk, butter, cheese, yogurt, ghee (6 items)
- **Vegetables/Fruits**: Apple, banana, carrot, broccoli, potato, onion, tomato + 75+ variants
- **Protein**: Chicken, beef, fish, eggs, beans, legumes (8 items)
- **Snacks/Misc**: Soup, pizza, cookies, nuts, honey (7 items)
- **Indian Staples**: Dal, roti, sabzi, poha, idli (5 items)

**Each food item includes:**
- Calories, protein, carbs, fat, fiber, sugar
- Glycemic Index & Glycemic Score
- Vitamins & minerals
- Health benefits & warnings
- Portion sizes

### 2. **Disease Diet Plans** (diseaseDietPlans.js)
Specialized nutrition plans for 9+ conditions:

#### **Diabetes Management**
- Daily Calories: 1800-2000
- Macros: 40-45% carbs, 25-30% protein, 25-30% fat
- Recommendations: Low GI foods, whole grains, legumes, lean proteins
- Key Nutrients: Fiber, Chromium, Magnesium, Vitamin D
- Sample Meals: Brown rice + lentils, grilled chicken with vegetables, idli with sambhar

#### **Hypertension (High Blood Pressure)**
- Daily Calories: 1800-2200
- Sodium Limit: <1,500-2,300mg/day
- DASH Diet Focus: High potassium, calcium, magnesium, fiber
- Recommendations: Fresh fruits, leafy greens, whole grains, low-fat dairy
- Sample Meals: Salmon with broccoli, lentil dal with brown rice, turkey with sweet potato

#### **Heart Disease Prevention**
- Daily Calories: 1800-2000
- Mediterranean-style diet with healthy fats
- Recommendations: Fish 2-3x/week, olive oil, nuts, whole grains
- Key Nutrients: Omega-3 fatty acids, Fiber, Potassium, Magnesium
- Sample Meals: Baked salmon with vegetables, chicken salad, bean curry

#### **Weight Loss & Obesity**
- Daily Calories: 1500-1800 (calorie-controlled)
- Macros: 45-50% carbs, 30-35% protein, 20-25% fat
- High-protein, high-fiber approach
- Sample Meals: Egg whites with whole wheat toast, grilled chicken with brown rice
- Target: 0.5-1 kg loss per week

#### **Celiac Disease (Gluten-Free)**
- 100% elimination of wheat, barley, rye
- Safe foods: Rice, potatoes, corn, quinoa, all meats, vegetables
- Indian staples: Dal, rice, potatoes (always check packaged items)

#### **Chronic Kidney Disease**
- Low sodium, controlled protein (varies by stage)
- Limited potassium (bananas, tomatoes, oranges)
- Limited phosphorus (nuts, seeds, whole grains)
- Consult nephrologist for personalized targets

#### **Thyroid Disease**
- Focus on: Selenium, Iodine, Zinc, Iron
- Recommendations: Fish, dairy, Brazil nuts, eggs, chickpeas
- Note: Take thyroid medication 30-60 min before breakfast, separate from supplements

#### **Anemia (Iron Deficiency)**
- Iron-rich foods: Red meat, fish, dal, leafy greens, fortified cereals
- Vitamin C enhances iron absorption (pair with tomato, orange, bell pepper)
- Avoid excess tea/coffee with meals (blocks iron absorption)

#### **Arthritis & Inflammation**
- Anti-inflammatory focus: Omega-3, antioxidants, low saturated fat
- Foods: Fatty fish, nuts, seeds, olive oil, vegetables, turmeric, ginger

---

## 🔐 Login & Authentication System

### **Features:**
- **Secure User Registration** - Email and password validation
- **Login Session Management** - Token-based authentication
- **Local Storage Database** - User data stored securely in browser
- **Demo Account** - Try the app without creating account

### **Test Accounts (Pre-loaded):**
```
Email: demo@nutricore.app
Password: nutricore2024
```

### **User Data Structure:**
```javascript
{
  name: "User Name",
  email: "user@email.com",
  password: "hashed_password",
  createdAt: "2024-02-25T...",
  profile: {
    age: 30,
    weight: 70,
    height: 175,
    diseaseConditions: ["diabetes", "hypertension"],
    dietPreference: "vegetarian|non-vegetarian|both"
  },
  meals: [{
    id: 1708945200000,
    date: "2024-02-25T...",
    foods: [...],
    totalNutrients: {...}
  }],
  dietPlans: [{
    id: 1708945200000,
    disease: "diabetes",
    meals: [...],
    createdAt: "2024-02-25T..."
  }],
  health: {
    score: 78,
    lastUpdated: "2024-02-25T..."
  }
}
```

---

## 🗄️ Database Implementation

### **Current: LocalStorage (Browser)**
- No server required
- Works offline
- Data persists in browser
- Limited to ~5-10MB

### **Recommended Upgrade: Firebase**

#### **Setup Steps:**

1. **Create Firebase Project**
   - Go to https://console.firebase.google.com/
   - Click "Create Project"
   - Name: `nutricore-app`
   - Enable Analytics (optional)

2. **Enable Authentication**
   ```
   Authentication → Sign-in method → Email/Password
   Enable both "Email/Password" options
   ```

3. **Create Firestore Database**
   ```
   Firestore Database → Create Database
   Start in test mode (for development)
   Location: Choose closest region
   ```

4. **Get Firebase Config**
   - Project Settings → Web App
   - Copy the config object
   - Replace values in `authDatabase.js`:
   ```javascript
   const firebaseConfig = {
     apiKey: "YOUR_API_KEY",
     authDomain: "nutricore-app.firebaseapp.com",
     projectId: "nutricore-app",
     storageBucket: "nutricore-app.appspot.com",
     messagingSenderId: "YOUR_MESSAGING_SENDER_ID",
     appId: "YOUR_APP_ID"
   };
   ```

5. **Update HTML with Firebase Scripts**
   ```html
   <script src="https://www.gstatic.com/firebasejs/9.22.0/firebase-app.js"></script>
   <script src="https://www.gstatic.com/firebasejs/9.22.0/firebase-auth.js"></script>
   <script src="https://www.gstatic.com/firebasejs/9.22.0/firebase-firestore.js"></script>
   ```

6. **Set Firestore Security Rules** (test mode for development)
   ```
   rules_version = '2';
   service cloud.firestore {
     match /databases/{database}/documents {
       match /users/{userId} {
         allow create, read, update, delete: if request.auth.uid == userId;
       }
     }
   }
   ```

---

## 📱 How to Use the App

### **Login/Registration**
1. Open the app - you'll see the login screen
2. **New User**: Click "Create Account" → Enter name, email, password
3. **Existing User**: Enter email and password
4. **Demo Mode**: Click "Try Demo Account" to explore without creating account

### **Setting Up Your Profile**
1. After login, go to **Tracker Tab**
2. Fill in your profile:
   - Age, weight, activity level
   - Choose diet preference (Vegetarian/Non-Vegetarian/Flexitarian)
   - Select health conditions
3. Click "Recalculate Targets" to set personalized calorie goals

### **Logging Meals**
1. **Tracker Tab** → Search foods
2. Filter by: Diet preference, Category
3. Click food to see details
4. Add to specific meal: Breakfast/Lunch/Dinner/Snacks
5. View meal totals at the bottom

### **Understanding Reports**
Go to **Report Tab** to see:
- **Health Score** (0-100 based on nutrients)
- **Nutrient Analysis** - What you're getting/missing
- **Disease Risk** - Predictions based on your diet
- **Recommendations** - Personalized suggestions

### **Creating Diet Plans**
1. Go to **Protocol Tab**
2. Your personalized macros appear automatically
3. Select proposed meal plan based on health goals
4. Save to your diet history

---

## 🍽️ Disease-Specific Examples

### **Sample Day - Diabetic Diet**
**Breakfast (7:00 AM)**
- Idli (2) with vegetable sambhar
- Calories: ~140 | GI: 30 | Protein: 5g

**Mid-Morning (10:00 AM)**
- Apple (medium)
- Calories: ~52 | GI: 36 | Fiber: 2.4g

**Lunch (1:00 PM)**
- Lentil dal (1 cup cooked)
- Brown rice (150g cooked)
- Sabzi (vegetable curry)
- Calories: ~367 | Fiber: 11g | Protein: 13g

**Evening (4:00 PM)**
- Almonds (23 pieces)
- Calories: ~160 | Magnesium: Good

**Dinner (8:00 PM)**
- Grilled chicken breast (100g)
- Steamed broccoli
- Whole wheat roti (1)
- Calories: ~320 | Protein: 32g | GI: Medium

**Daily Total**: ~1,039 calories | GI Score: ~34 (Excellent for diabetes)

---

## 🔍 Key Nutrients Tracked

### **Macronutrients**
- Protein (g)
- Carbohydrates (g)
- Fat (g)
- Fiber (g)

### **Micronutrients**
- Calcium, Iron, Magnesium
- Vitamins: A, B1, B2, B3, B6, B12, C, D, E, K
- Minerals: Potassium, Phosphorus, Zinc, Selenium, Copper
- Antioxidants, Omega-3 fatty acids

### **Special Markers**
- **Glycemic Index (GI)**: How fast food raises blood sugar
- **Glycemic Score (GS)**: Combined effect of food amount + GI
- **Anti-inflammatory Score**: Antioxidant & phytochemical content
- **Organ Health Indicators**: Disease-specific nutrient tracking

---

## 📊 Health Score Calculation

**Formula:**
```
Health Score = (Nutrient Coverage × 0.4) + (Disease Risk × 0.35) + (Balance × 0.25)

Where:
- Nutrient Coverage = % of RDA for 15 key nutrients met
- Disease Risk = Inverse of detected disease risk factors (0-100)
- Balance = Macro distribution (ideal: 45-55% carbs, 20-30% protein, 20-30% fat)
```

**Score Interpretation:**
- 90-100: Excellent - Optimal nutrition & health
- 75-89: Good - Balanced diet with minor gaps
- 60-74: Fair - Some deficiencies or imbalances
- 45-59: Poor - Significant nutritional gaps
- <45: Critical - Major health risk factors

---

## 🌐 Integration with Other Services

### **Future Enhancements**

1. **Wearable Integration**
   - Fitbit, Apple Watch, Google Fit APIs
   - Auto-sync activity and step data

2. **Medical Records**
   - Lab test results (blood glucose, lipids, etc.)
   - Doctor integration with real-time recommendations

3. **Meal Planning Services**
   - Recipe recommendations based on diet plan
   - Grocery list generation
   - Restaurant menu matching

4. **Payment Integration**
   - Premium features (meal plans, personalized coaching)
   - Subscription management

---

## 🛠️ Technical Stack

- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Database**: LocalStorage (current) → Firebase (recommended)
- **Authentication**: Custom with bcrypt (client-side hashing for demo)
- **Data Format**: JSON
- **Responsive**: Mobile-first design, works on all devices

---

## 📝 File Structure

```
d:\.vscode\
├── PROJECT.html                 # Main application file
├── foodDatabase.js              # Food data with nutrition info
├── diseaseDietPlans.js          # Disease-specific meal plans
├── authDatabase.js              # Authentication & user management
└── NUTRICORE_SETUP.md           # This file
```

---

## 🚀 Deployment

### **Quick Deploy (GitHub Pages)**
1. Create GitHub repository
2. Push files to `gh-pages` branch
3. Enable GitHub Pages in settings
4. Access at `https://username.github.io/nutricore`

### **Deploy to Web Host**
1. Upload all files via FTP
2. Ensure PROJECT.html is the index
3. Test login system works
4. Add SSL certificate (recommended)

### **Firebase Hosting**
```bash
npm install -g firebase-tools
firebase init
firebase deploy
```

---

## 🔒 Security Notes

⚠️ **For Production:**
1. Use **HTTPS only**
2. Implement server-side password hashing (bcrypt, Argon2)
3. Use Firebase Authentication instead of local storage
4. Implement rate limiting on login attempts
5. Add email verification
6. Use secure password reset flow
7. Enable CORS protection
8. Implement data encryption at rest

---

## 📞 Support & Troubleshooting

### **Login Issues**
- Clear browser cache: Ctrl+Shift+Delete
- Check browser console for errors: F12
- Ensure JavaScript is enabled

### **Food Not Showing**
- Check diet preference filter
- Verify category selection
- Search using food name

### **Data Not Saving**
- Enable cookies in browser
- Check if storage quota exceeded
- Try incognito/private mode

### **Performance Issues**
- Disable browser extensions
- Clear localStorage: Open Console → `localStorage.clear()`
- Use modern browser (Chrome, Firefox, Safari, Edge)

---

## 📚 API Reference

### **Authentication Functions**
```javascript
// Register new user
authDB.createUser(name, email, password)

// Login
authDB.loginUser(email, password)

// Logout
authDB.logoutUser()

// Get current user
authDB.getCurrentUser()

// Get session
authDB.getCurrentSession()
```

### **User Profile Functions**
```javascript
// Update profile
authDB.updateUserProfile(email, {age, weight, diseaseConditions})

// Save meal
authDB.saveMeal(email, mealData)
```

### **Food Database Functions**
```javascript
// Get all foods
foodDatabase.getAllFoods()

// Search foods
foodDatabase.searchFoods(query)

// Get foods by category
foodDatabase.staples, dairy, vegetables_fruits, protein, snacks_misc, indian_staples
```

### **Diet Plan Functions**
```javascript
// Get diet plan for disease
diseaseDietPlans.getDietPlan(disease)

// List available diseases
diseaseDietPlans.getAvailableDiseases()
```

---

## 📄 License

This project is provided for educational and personal use. Feel free to modify and distribute with proper attribution.

---

## 🤝 Contributing

To add new features:
1. Add food items to `foodDatabase.js`
2. Add new disease plans to `diseaseDietPlans.js`
3. Update authentication logic in `authDatabase.js`
4. Test thoroughly before deploying

---

## 📞 Contact & Support

For issues, suggestions, or questions:
- Check the Troubleshooting section above
- Test in private/incognito mode
- Clear cache and try again
- Contact support with browser console errors

---

**Last Updated**: February 25, 2026
**Version**: 1.0.0
**Status**: Production Ready ✅
