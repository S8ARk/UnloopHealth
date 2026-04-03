<parameter name="CodeContent"># 🥗 NutriCore 2.0

> **A personalized AI-driven health intelligence platform** that combines real-time nutrition tracking, biometric risk analysis, and adaptive dietary recommendations — all in a single, beautiful web application.

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-2.x-000000?style=flat&logo=flask)
![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-47A248?style=flat&logo=mongodb&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)

---

## 📋 Table of Contents

1. [What is NutriCore?](#what-is-nutricore)
2. [Features](#features)
3. [Tech Stack](#tech-stack)
4. [Project Structure](#project-structure)
5. [Prerequisites](#prerequisites)
6. [Installation](#installation)
7. [Configuration](#configuration)
8. [Running the Application](#running-the-application)
9. [Application Walkthrough](#application-walkthrough)
10. [API Reference](#api-reference)
11. [How the ML Engine Works](#how-the-ml-engine-works)
12. [Known Issues & Limitations](#known-issues--limitations)
13. [Roadmap](#roadmap)
14. [Contributing](#contributing)
15. [Authors & Acknowledgements](#authors--acknowledgements)
16. [License](#license)

---

## What is NutriCore?

NutriCore is a full-stack health intelligence web application designed to provide **personalized, data-driven dietary guidance** to users based on their unique biometric profile. It tracks daily nutrition, analyzes health risk vectors, and delivers context-aware food recommendations — going far beyond a basic calorie counter.

**Problem it solves:** Generic nutrition apps treat everyone the same. NutriCore adapts every target, recommendation, and risk assessment to the individual — factoring in BMI, medical history, activity levels, and real daily eating patterns.

**Who it's for:** Health-conscious individuals, fitness enthusiasts, people managing chronic conditions (hypertension, diabetes, obesity), and developers/researchers exploring personalized health AI.

---

## Features

### ✅ Authentication & Security
- JWT-based secure login and registration
- Password hashing with bcrypt
- Session management via `sessionStorage`
- Protected API routes — all data endpoints require valid tokens

### ✅ Health Profile Management
- Store and update personal biometrics: height, weight, age, activity level
- Log known medical conditions and allergies (free-text)
- Set daily step goals and water intake targets
- Profile data drives all downstream recommendations and risk calculations

### ✅ Smart Meal Tracker
- **Food search** with a tagged database of 20+ common foods
- **Dietary filters**: Vegetarian, Vegan, Non-Veg — applied at the database query level
- **Meal categorization**: Log food under Breakfast, Lunch, Dinner, or Snacks
- **Meal deletion**: Remove any logged meal with one click
- **Dynamic daily targets**: Caloric and macro targets recalculated from your actual body weight and activity multiplier — not hardcoded defaults
- **Predictive gap planner**: Shows exactly how many calories and grams of protein you still need to hit your personal daily targets

### ✅ Analytics Dashboard
- Overview cards: BMI, daily steps, sleep hours, water intake
- Personalized "Dos" and "Don'ts" recommendations powered by a rules-based ML engine
- Risk score label (Low / Moderate / High) calculated from biometric data

### ✅ Vulnerability Matrix (AI Risk Engine)
- Calculates **four distinct disease-risk vectors** based on user biometrics:
  - 🫀 **Cardiovascular Risk** — driven by BMI + inactivity
  - 🩺 **Hypertension Risk** — elevated by known medical conditions + BMI
  - ⚖️ **Metabolic Syndrome Risk** — driven by high BMI + poor sleep + low activity
  - 🛡️ **Immune Fatigue Risk** — driven by sleep deprivation + low step counts
- Results sorted by severity — highest risks render at the top
- Colour-coded bars: Red (>70%), Orange (>45%), Yellow (>25%), Green (safe)
- Fully isolated from the main dashboard; changes here do not affect other components

---

## Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | Python 3.10+, Flask 2.x, Flask-JWT-Extended, Flask-CORS |
| **Database** | MongoDB Atlas (cloud) via PyMongo |
| **Auth** | JWT (JSON Web Tokens) + bcrypt password hashing |
| **Frontend** | Vanilla HTML5, CSS3, JavaScript ES Modules |
| **Styling** | Custom CSS with glassmorphism design system, CSS variables |
| **Fonts** | Google Fonts — Outfit, Inter |
| **ML / Rules Engine** | Pure Python heuristic scoring (no external ML framework required) |
| **Data** | CSV-based diet recommendation dataset (764KB, included) |
| **Testing** | pytest + mongomock |
| **Dev Server** | Python's built-in `http.server` (frontend) + Flask dev server (backend) |

---

## Project Structure

```
NTR_pro/
│
├── client/                         # Frontend — all HTML, CSS, JS
│   ├── index.html                  # Landing page / entry point
│   ├── css/
│   │   └── base.css                # Global design system, variables, utilities
│   ├── js/
│   │   └── api.js                  # Centralized API service (all fetch calls, JWT injection)
│   └── pages/
│       ├── login.html              # Authentication — login form
│       ├── register.html           # Authentication — registration form
│       ├── dashboard.html          # Main overview dashboard
│       ├── tracker.html            # Meal tracker with dietary filters
│       ├── profile.html            # Health profile editor
│       └── report.html             # Analytics & Vulnerability Matrix
│
├── server/                         # Backend — Flask REST API
│   ├── app.py                      # App factory, blueprint registration, CORS, JWT setup
│   ├── .env                        # Your local environment variables (gitignored)
│   ├── .env.example                # Template — copy this to .env
│   ├── requirements.txt            # Python dependencies
│   ├── blueprints/
│   │   ├── auth_bp.py              # POST /api/auth/register, POST /api/auth/login
│   │   ├── analytics_bp.py         # POST /api/analytics/profile, GET /api/analytics/predict
│   │   └── tracker_bp.py           # GET /tracker/search, POST/DELETE /tracker/meal, GET /tracker/day
│   ├── models/
│   │   └── database.py             # MongoDB connection singleton (db_instance)
│   ├── services/
│   │   └── ml_service.py           # Risk vector engine + recommendation rules engine
│   └── tests/                      # pytest unit tests (gitignored output files)
│
├── data/                           # Datasets for demo and ML reference
│   ├── Personalized_Diet_Recommendations.csv   # Main demo dataset (764KB — committed)
│   ├── sample_diet_recommendations.csv          # 200-row quick-start sample
│   └── model_insights.png          # ML pipeline analysis visualization
│
├── scripts/                        # Developer utilities
│   ├── seed_foods.py               # Seeds MongoDB foods collection with tagged diet data
│   ├── debug_dash.py               # End-to-end API smoke test
│   ├── debug_login.py              # Auth flow debugger
│   └── debug_e2e.py                # Full E2E integration test runner
│
├── logs/                           # Test outputs and QA reports (gitignored)
├── tmp/                            # Scratch files (gitignored)
├── docs/                           # Extended documentation
├── SDLC.md                         # Full software development lifecycle documentation
├── SPEC.md                         # Original feature specification
├── PROJECT_RULES.md                # Development conventions and code rules
├── Hackathon_Project_Report.md     # Project overview report
└── .gitignore                      # Ignores venv, .env, large CSVs, logs, tmp
```

---

## Prerequisites

Before you begin, ensure you have the following installed on your machine:

| Requirement | Version | Notes |
|---|---|---|
| **Python** | 3.10 or higher | [Download](https://www.python.org/downloads/) |
| **MongoDB Atlas account** | — | Free tier works perfectly. [Sign up](https://www.mongodb.com/cloud/atlas) |
| **Git** | Any | For cloning the repo |
| **A modern browser** | Chrome / Firefox / Edge | Required for ES Module support |

> **Note:** No Node.js is required. The frontend uses plain HTML/CSS/JS with no build step.

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/NTR_pro.git
cd NTR_pro
```

### 2. Set up the Python virtual environment

```bash
cd server
python -m venv venv
```

Activate the environment:

- **Windows (PowerShell):**
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```
- **Windows (CMD):**
  ```cmd
  venv\Scripts\activate.bat
  ```
- **macOS / Linux:**
  ```bash
  source venv/bin/activate
  ```

### 3. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 4. Seed the food database

Go back to the project root and run:

```bash
cd ..
python scripts/seed_foods.py
```

This populates your MongoDB `foods` collection with 20 tagged food entries (Vegetarian, Vegan, Non-Veg) required for the Meal Tracker search to work.

---

## Configuration

### 1. Create your `.env` file

```bash
cp server/.env.example server/.env
```

### 2. Edit `server/.env` with your values

```env
# MongoDB — get this from your Atlas dashboard > Connect > Drivers
MONGO_URI=mongodb+srv://<username>:<password>@cluster0.mongodb.net/nutricore?retryWrites=true&w=majority

# JWT Secrets — generate any strong random strings
JWT_SECRET_KEY=your-very-secret-key-here
JWT_REFRESH_SECRET=your-refresh-secret-here

# Flask
FLASK_APP=app.py
FLASK_ENV=development
PORT=5000
```

> ⚠️ **Never commit your `.env` file.** It is already listed in `.gitignore`.

### 3. MongoDB Atlas setup (if starting fresh)

1. Create a free cluster on [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Under **Network Access**, add `0.0.0.0/0` (allow all IPs) for local development
3. Create a **database user** with read/write permissions
4. Copy the **connection string** into your `MONGO_URI`

The application will automatically create the following collections on first run:
- `users` — authentication records
- `health_profiles` — user biometric data
- `meal_logs` — daily food tracking entries
- `foods` — food database (seeded by `scripts/seed_foods.py`)

---

## Running the Application

You need **two terminals running simultaneously** — one for the backend API, one for the frontend server.

### Terminal 1 — Start the Flask Backend

```bash
# From project root, with venv activated
cd server
python app.py
```

You should see:
```
 * Running on http://0.0.0.0:5000
 * Debug mode: on
```

Verify it's alive:
```bash
curl http://localhost:5000/api/health
```
Expected: `{"status": "healthy", "message": "NutriCore 2.0 API is running"}`

### Terminal 2 — Start the Frontend Server

```bash
# From project root
cd client
python -m http.server 8000
```

### Open the Application

Navigate to: **[http://localhost:8000/](http://localhost:8000/)**

> ⚠️ **Do not open HTML files directly in your browser** (e.g., `file:///...`). The app uses ES Modules which require an HTTP server to function. Always use `http://localhost:8000`.

---

## Application Walkthrough

### Step 1 — Register
Go to `http://localhost:8000` → click **Get Started** → fill in your name, email, and password → **Register**.

### Step 2 — Build Your Health Profile
After login, navigate to **Health Profile** from the sidebar. Enter:
- Age, Height (cm), Weight (kg)
- Sleep hours per night
- Activity level (Sedentary / Moderate / Active)
- Daily steps goal, water intake goal
- Any known medical conditions or allergies (e.g., "Hypertension, Nut Allergy")

Click **Update My Diagnostic Baseline**. This data powers all downstream recommendations and risk calculations.

### Step 3 — Track Your Meals
Navigate to **Meal Tracker**:
1. Select your **meal type** (Breakfast / Lunch / Snacks / Dinner) from the first dropdown
2. Select your **dietary preference** (All / Vegetarian / Vegan / Non-Veg) from the second dropdown
3. Type a food name in the search box (e.g., "Rice", "Chicken", "Tofu")
4. Click any result to log it
5. Your **Daily Metrics** panel (right side) updates in real-time, showing your progress against your personal caloric and macro targets derived from your profile
6. The **Routine Planner** shows exactly how many calories and grams of protein you still need for the day
7. To delete a logged meal, click the red **Delete** button next to it

### Step 4 — View Your Analytics
Navigate to **Analytics**:
- The top cards show your current BMI, sleep hours, daily steps, and water intake
- **Personalized Recommendations** lists context-aware Dos and Don'ts based on your specific conditions
- **Vulnerability Matrix** shows your four disease risk scores, sorted by severity with colour-coded bars

### Step 5 — Understand Your Risk
The Vulnerability Matrix assesses four health dimensions:

| Risk Category | What drives it high |
|---|---|
| 🫀 Cardiovascular | BMI > 30 + steps < 5,000/day |
| 🩺 Hypertension | Known hypertension condition + elevated BMI |
| ⚖️ Metabolic Syndrome | High BMI + poor sleep + sedentary activity |
| 🛡️ Immune Fatigue | Sleep < 6 hours + steps < 4,000/day |

---

## API Reference

All endpoints are prefixed with `http://localhost:5000/api`.

Authentication endpoints are public. All other endpoints require the header:
```
Authorization: Bearer <access_token>
```

### Auth

| Method | Endpoint | Body | Description |
|---|---|---|---|
| `POST` | `/auth/register` | `{name, email, password}` | Create new user account |
| `POST` | `/auth/login` | `{email, password}` | Returns `access_token` |

### Analytics

| Method | Endpoint | Body | Description |
|---|---|---|---|
| `POST` | `/analytics/profile` | biometric fields | Save/update health profile |
| `GET` | `/analytics/predict` | — | Returns risk scores + recommendations |

### Tracker

| Method | Endpoint | Params / Body | Description |
|---|---|---|---|
| `GET` | `/tracker/search` | `?q=<query>&diet=<type>` | Search food database with dietary filter |
| `POST` | `/tracker/meal` | `{name, calories, protein, carbs, fats, meal_type}` | Log a meal entry |
| `DELETE` | `/tracker/meal/<meal_id>` | — | Delete a specific logged meal |
| `GET` | `/tracker/day` | — | Get today's summary + targets + all logged meals |

---

## How the ML Engine Works

NutriCore does **not** require a trained machine learning model file. The risk scoring and recommendation system is a fully transparent **rules-based heuristic engine** in `server/services/ml_service.py`.

### Risk Vector Calculation (`predict_risk`)

For each user, four probability scores (0.0 → 1.0) are calculated:

```
Hypertension base = 0.15
  + 0.3  if "hypertension" in medical_history
  + 0.2  if BMI > 30
  + 0.15 if BMI > 25

Cardiovascular base = 0.1
  + 0.25 if BMI > 30
  + 0.2  if daily_steps < 5000
  + 0.2  if "heart disease" in medical_history

Metabolic Syndrome base = 0.1
  + 0.3  if BMI > 30
  + 0.15 if sleep < 6 hours
  + 0.2  if activity == "sedentary"

Immune Fatigue base = 0.1
  + 0.25 if sleep < 5 hours
  + 0.2  if daily_steps < 4000
```

All scores are capped at 1.0. The frontend sorts results by score descending and applies colour thresholds:
- 🔴 Red: > 0.70
- 🟠 Orange: > 0.45
- 🟡 Yellow: > 0.25
- 🟢 Green: ≤ 0.25

### Recommendation Engine (`generate_recs`)

Rules evaluate the same biometric inputs to produce personalized Dos and Don'ts. Examples:
- BMI > 30 → "Do: follow a calorie deficit diet" / "Don't: consume refined sugars"
- Known hypertension → "Do: limit sodium to under 1500mg" / "Don't: consume caffeine"
- Sleep < 6 hours → "Do: prioritize 7–8 hours of sleep" / "Don't: eat heavy meals before bed"
- Steps < 5000 → "Do: incorporate a 30-min walk daily"

---

## Known Issues & Limitations

| Issue | Status | Notes |
|---|---|---|
| Food database is small (20 items) | ⚠️ Known | The seeder provides a starter set. Full integration with the 764KB CSV dataset is a planned feature |
| No production WSGI server | ⚠️ Known | Currently runs on Flask dev server. Gunicorn/Waitress recommended for production |
| No email verification | ⚠️ Known | Registration accepts any email format; no confirmation step |
| Single-day tracker | ⚠️ Known | The tracker only shows today's logs; no historical view yet |
| No token refresh | ⚠️ Known | JWT tokens expire after the Flask default; user must re-login |
| Diet filter requires manual re-search | ⚠️ Known | Changing the diet dropdown doesn't auto-refresh results — requires re-typing |

---

## Roadmap

- [ ] **Historical meal logs** — view nutrition trends over weekly/monthly timelines
- [ ] **Full food database integration** — import and serve all 5,000 entries from the CSV dataset via API
- [ ] **Recipe builder** — combine foods into named meals for one-click logging
- [ ] **Water intake tracker** — log glasses throughout the day
- [ ] **Gunicorn/Waitress deployment** — production-ready WSGI server setup
- [ ] **Progressive Web App (PWA)** — installable on mobile devices
- [ ] **Token refresh** — silent JWT refresh without re-login

---

## Running Tests

```bash
cd server
python -m pytest tests/ -v
```

Tests use `mongomock` to run against an in-memory MongoDB mock — no Atlas connection required for testing.

---

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feat/your-feature-name`
3. Make your changes following the conventions in `PROJECT_RULES.md`
4. Commit with a clear message: `git commit -m "feat: add water intake tracker"`
5. Push: `git push origin feat/your-feature-name`
6. Open a Pull Request against `main`

**Commit conventions:**
- `feat:` — new feature
- `fix:` — bug fix
- `chore:` — tooling, structure, dependencies
- `docs:` — documentation only

---

## Authors & Acknowledgements

**Built by:** The NutriCore development team

**Key dependencies:**
- [Flask](https://flask.palletsprojects.com/) — lightweight Python web framework
- [Flask-JWT-Extended](https://flask-jwt-extended.readthedocs.io/) — JWT authentication
- [PyMongo](https://pymongo.readthedocs.io/) — MongoDB Python driver
- [bcrypt](https://pypi.org/project/bcrypt/) — password hashing
- [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) — cloud database
- [Google Fonts](https://fonts.google.com/) — Outfit and Inter typefaces

**Dataset reference:**
- `Personalized_Diet_Recommendations.csv` — synthetic health and dietary dataset used for demonstration and ML pipeline exploration

---

## License

This project is licensed under the **MIT License**.

```
MIT License — free to use, modify, and distribute with attribution.
```

---

<p align="center">Built with ❤️ using Flask + MongoDB + Vanilla JS</p>
