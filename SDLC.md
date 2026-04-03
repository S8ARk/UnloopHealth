**NutriCore 2.0**

*AI-Powered Predictive Health Platform*

**Software Development Life Cycle (SDLC)**

From Fear-Based Disease Countdown to Holistic Predictive Wellness

|**Version**|1\.0.0 — Initial SDLC Blueprint|
| :- | :- |
|**Project**|NutriCore 2.0 — Reverse-Logic Health Engine|
|**Team**|CodeFin / Lead: Aditya Kumar Singh|
|**Stack**|React + Flask + MongoDB|
|**Deployment**|Localhost → Vercel (Production)|
|**Date**|April 2026|
|**Phase**|Pre-Development / Planning|


# **1. Requirements Analysis**
NutriCore 2.0 moves beyond macro/micro counting to a 'reverse-logic' health model: rather than nudging users to reach an ideal, it reveals what diseases threaten them based on their current lifestyle pattern, scores the proximity and severity of each risk, and drives them toward avoidance with a visceral countdown. This section documents functional requirements, non-functional requirements, user personas, constraints, and prioritisation.

## **1.1  Vision & Core Philosophy**
Traditional nutrition apps ask: 'Did you eat enough protein today?'. NutriCore 2.0 asks: 'If you keep eating the way you did this week, how many months until Type-2 Diabetes risk becomes critical?'. The philosophy is:

- Holistic profiling — nutrition, sleep, activity, stress, genetics, biometrics
- Fear as a motivator — countdown timers and risk trajectories, not abstract percentages
- Pattern recognition — ML models trained on longitudinal data, not single-day snapshots
- Solution-first — every detected risk immediately offers a countermeasure plan
- Progressive disclosure — simple dashboard for casual users, deep analytics for power users

## **1.2  User Personas**

|**Persona**|**Demographics**|**Primary Pain**|**Key Need**|
| :- | :- | :- | :- |
|The Anxious Optimizer|25-35, urban professional|Doesn't know hidden risks|Countdown clock for each disease risk|
|The Diagnosed Manager|40-60, chronic condition|Managing existing disease without worsening|Daily constraint enforcement + progress proof|
|The Family Guardian|30-50, parent / caregiver|Family health patterns & hereditary risk|Multi-profile risk dashboard|
|The Athlete|20-35, fitness-focused|Over-training and micronutrient depletion|Performance + recovery risk flags|
|The Clinical Partner|Medical practitioner|Remote patient compliance monitoring|Exportable patient reports & API integration|

## **1.3  Functional Requirements**
### **1.3.1  Implementable Now (MVP)**
- **FR-01:** User registration, login, and secure session management (JWT)
- **FR-02:** Full health profile: age, sex, weight, height, BMI, activity level, diet type, existing diagnoses
- **FR-03:** Daily meal logging with macro/micro tracking (68+ foods, Indian staples included)
- **FR-04:** Disease Risk Engine: calculates proximity score (0-100) for 10 diseases based on current pattern
- **FR-05:** Risk Countdown Display: visual timer showing 'At this rate, Hypertension risk critical in X months'
- **FR-06:** Pattern Analysis: compares last 7-day, 30-day rolling averages against clinical baselines
- **FR-07:** Solution Prescription: for each flagged risk, auto-generate a corrective action plan
- **FR-08:** Health Score (0-100) multi-dimensional: not one score but sub-scores per organ/system
- **FR-09:** Progress Tracker: shows if countdown is decreasing (improving) or accelerating (worsening)
- **FR-10:** Report generation: daily, weekly, monthly PDF-style summary
- **FR-11:** Clinical Override: disease-specific dietary constraints enforced in logging UI
- **FR-12:** Food Database API: OpenFoodFacts integration + local fallback for Indian staples

### **1.3.2  Next Steps (Post-MVP)**
- **FR-13:** Sleep data manual entry and pattern correlation with disease risk
- **FR-14:** Stress level self-reporting (1-10 scale, mood journaling)
- **FR-15:** Blood panel import: users manually enter lab values (glucose, HbA1c, lipids, etc.)
- **FR-16:** Multi-user household profiles with shared risk dashboards
- **FR-17:** Meal photo logging with portion-size estimation (YOLOv8 integration)
- **FR-18:** Doctor share: generate a patient-facing PDF report to share with clinician
- **FR-19:** Wearable sync: Apple Health / Google Fit OAuth (read heart rate, steps, sleep)

### **1.3.3  Future Plans**
- **FR-20:** Genetic predisposition module: family history + optional DNA markers as risk multipliers
- **FR-21:** RAG-based conversational health assistant grounded in user data
- **FR-22:** Clinical validation closed beta with dietitians and blood panel correlation
- **FR-23:** B2B API: licence risk engine to insurance, telehealth, corporate wellness providers
- **FR-24:** Deep neural network for personalised macro optimisation per disease trajectory

## **1.4  Non-Functional Requirements**

|**Category**|**Requirement**|**Target / Metric**|
| :- | :- | :- |
|Performance|API response time|< 300ms for 95th percentile|
|Performance|Risk score recalculation|< 2s for full 30-day analysis|
|Scalability|Concurrent users (MVP)|50 users localhost; 500 on Vercel free tier|
|Security|Password storage|bcrypt hash, min 12 rounds|
|Security|Data in transit|HTTPS enforced; HTTP redirects|
|Security|JWT token lifetime|Access: 15 min; Refresh: 7 days|
|Reliability|Uptime (post-Vercel)|99\.5% target|
|Usability|Onboarding to first insight|< 5 minutes for new user|
|Maintainability|Test coverage|> 70% unit test coverage at MVP|
|Accessibility|WCAG compliance|AA level for core flows|
|Portability|Browser support|Chrome, Firefox, Safari, Edge — latest 2 versions (no transpile needed for ES6 modules)|
|Data Retention|User data deletion|Full account wipe on request within 24h|

## **1.5  Constraints**
- Technology: Frontend — HTML5 + CSS3 + Vanilla JS (ES6 modules); Backend — Flask (Python); Database — MongoDB Atlas (free tier for development)
- Deployment: Localhost first → Vercel (frontend) + Render/Railway (backend) for production
- Regulatory: Not a medical device; must include disclaimer that output is informational only
- Team: Solo developer (MVP); all architecture must be maintainable by one person
- Budget: Zero cost at MVP stage; all services must have a usable free tier
- Timeline: MVP target — 8 weeks from kickoff

## **1.6  Requirement Priority Matrix (MoSCoW)**

|**Priority**|**Category**|**Requirements**|
| :- | :- | :- |
|**MUST**|Core MVP|FR-01 to FR-10 (Auth, Logging, Risk Engine, Countdown, Score)|
|**SHOULD**|Enhanced MVP|FR-11, FR-12 (Clinical Override, Food API), Report Export|
|**COULD**|Next Steps|FR-13 to FR-19 (Sleep, Blood Panel, Photo, Multi-profile, Wearable)|
|**WON'T NOW**|Future Plans|FR-20 to FR-24 (Genetics, RAG, B2B API, DNN)|


# **2. System Design**

## **2.1  High-Level Architecture**
NutriCore 2.0 follows a three-tier client-server architecture with a clear separation between the React SPA (presentation), Flask REST API (business logic), and MongoDB (persistence). The Risk Engine is an internal service module within Flask that can later be extracted to a microservice.

|**Tier 1 — Client**|Vanilla HTML5 + CSS3 + JavaScript (ES6 modules). No build step required. Modular JS files for each feature area. Fetch API for all server calls.|
| :- | :- |
|**Tier 2 — API Server**|Flask (Python 3.11). Blueprints for modular routing. Flask-JWT-Extended for auth. Pydantic/Marshmallow for validation. CORS managed by Flask-CORS.|
|**Tier 3 — Database**|MongoDB Atlas (free tier). Mongoose-style schemas via PyMongo / MongoEngine. Two logical DBs: nutricore\_users (structured) and nutricore\_logs (flexible logs).|
|**Risk Engine**|Internal Flask service module. Reads from both DBs. Produces disease\_risk\_scores per user. Runs on API call + scheduled nightly recalculation.|
|**External APIs**|OpenFoodFacts (food lookup). Optional: Apple Health / Google Fit OAuth (post-MVP).|

## **2.2  Low-Level Component Design**
### **2.2.1  Frontend File Structure (HTML/CSS/JS)**
- index.html — entry point, links all CSS and JS modules
- pages/
  - login.html, register.html
  - dashboard.html — risk countdown cards, overall score
  - tracker.html — meal logging, food search
  - report.html — charts, pattern analysis, PDF export
  - profile.html — health profile, conditions
- css/
  - base.css — reset, variables (CSS custom properties), typography
  - layout.css — grid, sidebar, responsive breakpoints
  - components.css — cards, modals, buttons, form elements
  - dashboard.css — countdown ring animations, score gauges
  - charts.css — chart container styles
- js/
  - api.js — central Fetch wrapper with JWT header injection and refresh logic
  - auth.js — login, register, logout, token storage (sessionStorage)
  - profile.js — load/save profile, BMI calculation, condition selector
  - tracker.js — food search, meal logging, live macro ticker
  - risk.js — fetch risk scores, render countdown cards, colour bands
  - charts.js — Chart.js wrappers for pattern + macro charts
  - report.js — weekly/monthly data fetch, jsPDF export
  - utils.js — date helpers, number formatters, DOM utilities
  - router.js — lightweight hash-based client router for SPA-like navigation

### **2.2.2  Backend Blueprint Structure**
- app.py — factory function, registers blueprints, CORS, JWT
- config.py — environment-based config (dev/prod)
- blueprints/
  - auth\_bp.py — /api/auth/\* endpoints
  - profile\_bp.py — /api/profile/\*
  - meals\_bp.py — /api/meals/\*
  - risk\_bp.py — /api/risk/\*
  - food\_bp.py — /api/food/\* (proxy to OpenFoodFacts + local fallback)
  - report\_bp.py — /api/report/\*
- services/
  - risk\_engine.py — core disease proximity calculation
  - pattern\_analyzer.py — rolling averages, trend detection
  - solution\_prescriber.py — maps risk flags to corrective plans
  - food\_resolver.py — OpenFoodFacts + local DB merge
- models/ — MongoEngine ODM models
- utils/ — validators, decorators, response helpers

## **2.3  Database Schema Design**
### **2.3.1  MongoDB Collections**
MongoDB is chosen for its document flexibility. User profiles have structured sub-documents while meal logs are schema-flexible to accommodate evolving food data models.

**Collection: users**

|**\_id**|ObjectId (primary key, auto)|
| :- | :- |
|**email**|String, unique, indexed|
|**password\_hash**|String (bcrypt)|
|**created\_at**|ISODate|
|**profile**|Embedded doc: { name, age, sex, weight\_kg, height\_cm, activity\_level, diet\_type, conditions: [String], bmi }|
|**goals**|Embedded doc: { target\_calories, target\_protein, target\_carbs, target\_fat }|
|**settings**|Embedded doc: { units: 'metric|imperial', notifications: Boolean }|

**Collection: meal\_logs**

|**\_id**|ObjectId|
| :- | :- |
|**user\_id**|ObjectId ref → users, indexed|
|**date**|ISODate (date portion, indexed)|
|**meal\_type**|String: breakfast | lunch | dinner | snack|
|**items**|Array of { food\_id, name, quantity\_g, calories, protein, carbs, fat, fiber, sugar, gi\_score, micronutrients: {} }|
|**total\_nutrients**|Embedded doc: computed sum of all items|
|**logged\_at**|ISODate (full timestamp)|

**Collection: risk\_scores**

|**\_id**|ObjectId|
| :- | :- |
|**user\_id**|ObjectId ref → users, indexed|
|**calculated\_at**|ISODate|
|**analysis\_window\_days**|Integer (7 or 30)|
|**scores**|Object: { diabetes: { score: 0-100, trend: 'up|down|stable', months\_to\_critical: Number, contributing\_factors: [String] }, hypertension: {...}, heart\_disease: {...}, ... }|
|**overall\_health\_score**|Number 0-100|
|**recommendations**|Array of { disease, priority, action, foods\_to\_add: [], foods\_to\_remove: [] }|

**Collection: foods (local fallback DB)**

|**\_id**|ObjectId|
| :- | :- |
|**name**|String, text-indexed for search|
|**category**|String|
|**per\_100g**|Embedded: { calories, protein, carbs, fat, fiber, sugar, sodium, potassium, ... }|
|**micronutrients**|Object: { vitamin\_a, vitamin\_c, iron, calcium, ... }|
|**gi\_index**|Number|
|**tags**|Array (e.g., 'Indian', 'vegan', 'low-gi')|

## **2.4  API Endpoint Design**

|**Method**|**Endpoint**|**Auth**|**Description**|
| :- | :- | :- | :- |
|**POST**|/api/auth/register|Public|Create new user account|
|**POST**|/api/auth/login|Public|Login, returns access + refresh JWT|
|**POST**|/api/auth/refresh|Refresh token|Get new access token|
|**GET**|/api/profile|JWT Required|Get current user profile|
|**PUT**|/api/profile|JWT Required|Update profile + conditions|
|**POST**|/api/meals|JWT Required|Log a meal|
|**GET**|/api/meals?date=YYYY-MM-DD|JWT Required|Get all meals for a date|
|**DELETE**|/api/meals/:id|JWT Required|Delete a logged meal|
|**GET**|/api/risk/scores|JWT Required|Get latest risk scores|
|**POST**|/api/risk/recalculate|JWT Required|Force risk recalculation|
|**GET**|/api/risk/history?days=30|JWT Required|Risk score history|
|**GET**|/api/food/search?q=dal|JWT Required|Search food (API + fallback)|
|**GET**|/api/food/:id|JWT Required|Get food details|
|**GET**|/api/report/weekly|JWT Required|Weekly health report|
|**GET**|/api/report/monthly|JWT Required|Monthly health report|

## **2.5  Data Flow Diagrams (DFD)**
### **2.5.1  Level-0 Context DFD**
External Entities: [User] ←→ [NutriCore System] ←→ [OpenFoodFacts API]

`  `• User sends: Health profile, Meal logs, Profile updates

`  `• System sends to User: Risk scores, Countdown timers, Corrective plans, Reports

`  `• System sends to OpenFoodFacts: Food search queries

`  `• OpenFoodFacts sends to System: Nutritional data

### **2.5.2  Level-1 DFD — Core Processes**
- P1: Authentication — User credentials → [User Store] → JWT tokens
- P2: Meal Logging — Food selection + portions → [Meal Log Store] → Confirmed log + live macro update
- P3: Risk Calculation — [Meal Log Store] + [User Profile] → Risk Engine → [Risk Score Store] → Countdown scores
- P4: Pattern Analysis — [Risk Score Store (30d)] → Pattern Analyzer → Trend data + trajectory
- P5: Solution Prescription — [Risk Scores] → Solution Prescriber → Corrective action plans
- P6: Report Generation — [Meal Logs + Risk Scores + Patterns] → Report Builder → Weekly/Monthly summaries

### **2.5.3  Risk Engine Data Flow (P3 Deep Dive)**
Input: user\_id → Queries: last 30 days of meal\_logs aggregated by nutrient → Computes rolling averages for: calories, sugar, sodium, saturated fat, fiber, processed food ratio, GI load → Compares against clinical thresholds per disease → Outputs: score (0-100), months\_to\_critical, contributing\_factors, trajectory (up/down/stable)


# **3. Risk Engine — Core Algorithm Design**
This section defines the mathematical model and logic for the disease risk calculation. This is the defining differentiator of NutriCore 2.0 from any existing app.

## **3.1  Disease Risk Model**
Each disease has a set of weighted risk factors derived from nutritional inputs. The risk score is computed as a weighted sum normalized to 0-100. A score above 70 is flagged as 'high', above 85 as 'critical'. The months\_to\_critical is estimated based on the velocity of change.

|**Disease**|**Primary Risk Factors (Inputs)**|**Clinical Thresholds**|
| :- | :- | :- |
|Type-2 Diabetes|Avg daily sugar, GI load, carb%, BMI|Sugar >50g/d, GI load >120, BMI >27|
|Hypertension|Sodium, saturated fat, alcohol, BMI, stress score|Sodium >2300mg/d, SatFat >20g/d|
|Heart Disease|Sat fat, trans fat, cholesterol, omega-3 deficit, fiber|SatFat >13g/d, fiber <15g/d|
|Obesity Risk|Caloric surplus (vs TDEE), activity level, ultra-processed ratio|Surplus >300kcal/d for 30 days|
|Chronic Kidney Disease|Protein excess, sodium, phosphorus, potassium extremes|Protein >2g/kg/d, sodium >3000mg/d|
|Iron Deficiency Anemia|Iron intake deficit, Vitamin C pairing score, red meat ratio|Iron <8mg/d with no pairing boosts|
|Thyroid Dysfunction|Iodine, selenium, zinc, soy over-consumption|Iodine <100mcg/d or soy >50g/d|
|Inflammatory Conditions|Omega-6:Omega-3 ratio, antioxidant score, sugar|Ratio >15:1, antioxidant score <30/100|
|Osteoporosis (future)|Calcium, Vitamin D, phosphorus, caffeine|Ca <700mg/d, Vit D <400IU/d|
|Metabolic Syndrome|Composite: waist, triglycerides (from sat fat), glucose load|3 or more sub-scores above threshold|

## **3.2  Scoring Algorithm**
**Step 1 — Compute 30-day rolling averages for each nutrient/factor**

avg\_sugar = sum(daily\_sugar[last\_30\_days]) / days\_with\_data

**Step 2 — Normalise each factor against threshold**

factor\_score = min(100, (actual\_value / threshold\_value) \* 100)

If actual < threshold: score is proportionally below 100 (lower = better)

If actual > threshold: score can exceed 100 but is capped at 100 for display

**Step 3 — Weighted sum per disease**

disease\_score = sum(factor\_score[i] \* weight[i] for all factors) / sum(weights)

**Step 4 — Compute months\_to\_critical**

velocity = (this\_week\_score - last\_week\_score) / 7  [score units per day]

months\_to\_critical = (85 - current\_score) / (velocity \* 30)  if velocity > 0 else infinity

If months\_to\_critical < 0: already critical. If velocity <= 0: score improving (flag green).

**Step 5 — Identify contributing factors**

Top 3 factors by normalised score are surfaced as 'contributing\_factors' strings for the UI.

## **3.3  Countdown Display Logic**
- Score 0-40: Green — 'Low Risk. Your pattern supports long-term health.'
- Score 41-60: Yellow — 'Moderate Risk. Monitor these habits.'
- Score 61-75: Orange — 'Elevated Risk. [N] months to critical if trend continues.'
- Score 76-85: Red — 'High Risk. Immediate dietary changes recommended.'
- Score 86-100: Critical Red (pulsing) — 'Critical Risk. Consult a health professional.'

The countdown timer is animated using CSS keyframes and React state. It ticks down daily on recalculation. If the user improves their pattern, the timer extends and the UI shows 'Your risk improved by X days' as positive reinforcement.


# **4. Test Design**

## **4.1  Testing Strategy Overview**

|**Test Level**|**Scope**|**Tools**|
| :- | :- | :- |
|Unit Tests|Individual functions, services, risk calculations|pytest (backend), Jest + jsdom (frontend JS modules)|
|Integration Tests|API endpoints + DB interaction|pytest with mongomock, Postman collections|
|Component Tests|JS module behaviour + DOM manipulation|Jest with jsdom, fetch-mock for API mocking|
|End-to-End Tests|Full user flows (register → log → risk view)|Playwright|
|Performance Tests|API response times under load|Locust (Python)|

## **4.2  Unit Test Design**
### **4.2.1  Risk Engine Unit Tests**
- test\_risk\_score\_range: Output of risk\_engine.calculate() is always 0 <= score <= 100
- test\_zero\_data\_returns\_neutral: User with no logs gets score = 0 (not error)
- test\_high\_sugar\_elevates\_diabetes\_score: Inject 80g/day sugar for 30 days → diabetes score > 70
- test\_good\_diet\_keeps\_score\_low: Inject a model diet (low GI, adequate fiber) → all scores < 40
- test\_months\_to\_critical\_positive: velocity > 0 always yields months\_to\_critical > 0
- test\_months\_to\_critical\_improving: velocity < 0 yields None / infinity (not negative number)
- test\_contributing\_factors\_length: Always returns exactly 3 factors

### **4.2.2  Pattern Analyzer Unit Tests**
- test\_rolling\_average\_7d: Correct average over exactly 7 days of data
- test\_rolling\_average\_partial: Only 3 days of data → average over 3, not 7
- test\_trend\_detection\_upward: Increasing scores over 14 days classified as 'up'
- test\_trend\_detection\_stable: Variance < 5 points classified as 'stable'

### **4.2.3  Auth Service Unit Tests**
- test\_register\_success: Valid input creates user, returns 201
- test\_register\_duplicate\_email: Second registration with same email returns 409
- test\_login\_correct\_password: Returns access\_token and refresh\_token
- test\_login\_wrong\_password: Returns 401
- test\_jwt\_protected\_route\_no\_token: Returns 401
- test\_jwt\_protected\_route\_expired\_token: Returns 401

### **4.2.4  Meal Logging Unit Tests**
- test\_log\_meal\_success: Valid meal body persists to DB, returns 201 with created doc
- test\_log\_meal\_missing\_items: Body without items array returns 422
- test\_get\_meals\_by\_date: Returns only meals for queried date, not others
- test\_delete\_meal\_own: User can delete their own meal, returns 200
- test\_delete\_meal\_others: User cannot delete another user's meal, returns 403

## **4.3  Integration Test Design**
- test\_register\_login\_get\_profile: Full flow — register → login → GET /profile returns user data
- test\_log\_meal\_then\_get\_risk: Log 7 days of high-sugar meals → GET /risk/scores → diabetes score > 50
- test\_recalculate\_after\_improvement: Log bad diet → get score → log good diet → recalculate → score improves
- test\_food\_search\_falls\_back: When OpenFoodFacts is mocked to fail → local DB results returned
- test\_report\_weekly: After logging 7 days → GET /report/weekly returns non-empty report

## **4.4  Frontend JS Module Test Design**
- auth.js — test that login() stores token in sessionStorage; test that logout() clears it
- tracker.js — addMealItem() updates running total correctly; removeMealItem() recalculates macros
- risk.js — getRiskColour() returns correct CSS class for each score band (green/yellow/orange/red)
- utils.js — formatDate() returns YYYY-MM-DD for a given Date object; calcBMI() correct for known values
- charts.js — buildPatternDataset() returns exactly 7 entries when given 7-day data array
- router.js — navigateTo() updates window.location.hash and calls correct page init function

## **4.5  Test Coverage Targets**

|**Module**|**Coverage Target**|
| :- | :- |
|Risk Engine (risk\_engine.py)|90%|
|Pattern Analyzer|85%|
|Auth Service + Blueprint|80%|
|Meal Logging Blueprint|80%|
|Frontend JS Modules (tracker, risk, auth)|75%|
|Frontend Utils + Router|80%|
|Overall Project|> 70%|


# **5. Coding Plan & Module Breakdown**

## **5.1  Repository Structure**
The project uses a monorepo with two top-level directories: /client (HTML/CSS/JS) and /server (Flask). No build tools are needed on the frontend — files are served directly.

- nutricore-v2/
  - client/ — Vanilla HTML/CSS/JS frontend
    - pages/ — dashboard.html, tracker.html, report.html, profile.html, login.html
    - css/ — base.css, layout.css, components.css, dashboard.css, charts.css
    - js/ — api.js, auth.js, tracker.js, risk.js, charts.js, report.js, utils.js, router.js
    - index.html — landing / redirect to login
  - server/ — Flask backend
    - app.py, config.py
    - blueprints/, services/, models/, utils/
    - tests/ — pytest test suite
    - requirements.txt, .env.example
  - .github/workflows/ — CI/CD pipelines
  - README.md, .gitignore, .env.example

## **5.2  Sprint Plan (8-Week MVP)**

|**Sprint**|**Focus**|**Deliverables**|**Git Tag**|
| :- | :- | :- | :- |
|**Week 1**|**Project Setup + Auth**|Repo init, Flask app factory, MongoDB connection, register/login endpoints, JWT setup, HTML login/register pages with CSS, auth.js + api.js|v0.1-auth|
|**Week 2**|**User Profile**|Profile model + CRUD endpoints, profile.html page, health conditions selector, BMI calculator in JS|v0.2-profile|
|**Week 3**|**Food DB + Meal Logging**|Local food collection seeding, OpenFoodFacts proxy, meal log endpoints, tracker.html with live macro ticker in vanilla JS|v0.3-logging|
|**Week 4**|**Risk Engine Core**|risk\_engine.py with 5 diseases (diabetes, hypertension, heart disease, obesity, anemia), /api/risk/scores endpoint, unit tests|v0.4-risk-engine|
|**Week 5**|**Risk Engine Full + Dashboard UI**|All 10 disease models, risk.js countdown card rendering, dashboard.html with animated countdown rings, colour-coded severity|v0.5-dashboard|
|**Week 6**|**Pattern Analyzer + Charts**|pattern\_analyzer.py, 7d/30d rolling averages, charts.js using Chart.js, trend arrows, trajectory messages|v0.6-patterns|
|**Week 7**|**Reports + Solution Prescriber**|solution\_prescriber.py, corrective plan section in report.html, weekly/monthly view, PDF export (jsPDF)|v0.7-reports|
|**Week 8**|**Polish + Testing + Deploy**|Full test suite (>70% coverage), bug fixes, Vercel static deploy (client/) + Render deploy (server/), README|v1.0-mvp|

## **5.3  Module Coding Guidelines**
### **5.3.1  Risk Engine (risk\_engine.py) — Implementation Notes**
- Each disease has its own function: calculate\_diabetes\_risk(averages, profile) → dict
- Disease functions are stateless pure functions — easier to test and reason about
- Weights are stored in a config dict at top of file, not hardcoded in functions
- Use dataclasses for RiskResult: score, trend, months\_to\_critical, factors
- Main entry: calculate\_all\_risks(user\_id, db) orchestrates all disease functions

### **5.3.2  Frontend JS Modules — Implementation Notes**
- api.js is the single gateway for all server calls — never use fetch() directly in page scripts
- Each page script (tracker.js, risk.js, etc.) has an init() function called on DOMContentLoaded
- State is held in plain JS module-level variables; DOM is updated directly via querySelector/innerHTML
- Debounce food search input with a 300ms setTimeout — cancel previous timer on each keystroke
- JWT access token stored in sessionStorage (cleared on tab close); refresh token handled server-side via httpOnly cookie
- CSS custom properties (--color-risk-high, --color-risk-low etc.) drive all theming — change the variable, not the class

### **5.3.3  Git Workflow**
- Every atomic change = one commit. Commit message format: type(scope): description
- Types: feat, fix, test, docs, refactor, chore
- Examples: feat(risk): add hypertension model with sodium weighting
- `           `test(auth): add duplicate email registration test
- `           `fix(ui): correct countdown timer negative display bug
- Push to main after each feature is tested. Use feature branches for experiments.
- Tag each sprint completion: git tag v0.1-auth && git push origin v0.1-auth


# **6. Implementation Plan**

## **6.1  Local Development Setup**
### **6.1.1  Prerequisites**
- Python 3.11+ and pip
- MongoDB Atlas free cluster (sign up at mongodb.com/cloud/atlas)
- Git 2.40+
- VS Code with Live Server, Pylance, and ESLint extensions
- A modern browser (Chrome or Firefox recommended for DevTools)
- No Node.js required for the frontend — plain HTML/CSS/JS, no build step

### **6.1.2  Initial Setup Commands**
\# Clone and setup

git clone https://github.com/your-username/nutricore-v2.git

cd nutricore-v2

\# Backend

cd server && python -m venv venv && source venv/bin/activate

pip install flask flask-jwt-extended flask-cors pymongo bcrypt marshmallow python-dotenv

cp .env.example .env  # fill in MONGO\_URI, JWT\_SECRET\_KEY

flask run --port 5000

\# Frontend — no install needed, just open with a static server

cd client && python3 -m http.server 8080

\# Or use VS Code Live Server extension (recommended for development)

\# Open http://localhost:8080 in browser

## **6.2  Environment Variables**

|**Variable**|**Where**|**Description**|
| :- | :- | :- |
|MONGO\_URI|Server .env|MongoDB Atlas connection string|
|JWT\_SECRET\_KEY|Server .env|Strong random string (min 32 chars)|
|JWT\_REFRESH\_SECRET|Server .env|Separate secret for refresh tokens|
|FLASK\_ENV|Server .env|development | production|
|OPENFOODFACTS\_BASE\_URL|Server .env|https://world.openfoodfacts.org/api/v2|
|API\_BASE\_URL|client/js/config.js|http://localhost:5000 (dev) — edit before deploy|
|APP\_NAME|client/js/config.js|NutriCore|

## **6.3  Deployment Strategy**
### **6.3.1  Phase 1 — Localhost**
- Flask on port 5000, static HTML/CSS/JS served via Python http.server or VS Code Live Server on port 8080
- MongoDB Atlas free cluster (M0) — no local MongoDB needed
- CORS configured to allow http://localhost:8080

### **6.3.2  Phase 2 — Vercel (Frontend) + Render (Backend)**
- Frontend: Push to GitHub → Connect Vercel → Set root to /client → Vercel serves static files automatically, no build step needed
- Backend: Connect Render to repo → Set root to /server → Add environment variables → Auto-deploy on push
- Update CORS to allow Vercel domain in Flask config
- Update API\_BASE\_URL in client/js/config.js to point to Render URL before final deploy commit
- MongoDB Atlas: Whitelist Render IP or use 0.0.0.0/0 for MVP

### **6.3.3  CI/CD with GitHub Actions**
Create .github/workflows/ci.yml with jobs:

- test-backend: Runs pytest on push to main and all PRs
- test-frontend: Runs Jest (jsdom) on JS module unit tests on push to main and all PRs
- deploy-preview: Vercel auto-preview for PRs (free on Vercel — static files deploy instantly)

## **6.4  Per-Step Git Push Protocol**
Following this protocol ensures the codebase is always in a deployable state and every change is traceable:

1. Complete one atomic unit of work (one function, one component, one test file)
1. Run relevant tests — all must pass before committing
1. Stage changes: git add -p  (interactive staging — never git add .)
1. Write meaningful commit: git commit -m 'feat(risk): add diabetes scoring function'
1. Push immediately: git push origin main
1. Verify CI passes on GitHub Actions before starting next unit

This creates a rich commit history that documents the system's evolution and makes bisecting bugs trivial.


# **7. Project Roadmap Summary**

|**Phase**|**Timeline**|**Deployment**|**Key Milestone**|
| :- | :- | :- | :- |
|**MVP Build**|Weeks 1-8|Localhost|Full risk engine + countdown dashboard working|
|**v1.0 Release**|Week 8|Vercel + Render|Public deployment, all 10 disease models live|
|**v1.1 — Sleep & Stress**|Weeks 9-12|Vercel + Render|Manual sleep/stress inputs, correlation analysis|
|**v1.2 — Blood Panel**|Weeks 13-16|Vercel + Render|Lab value import, direct clinical calibration|
|**v2.0 — Wearables**|Months 5-7|Vercel + Render|Apple Health / Google Fit OAuth sync|
|**v2.1 — Photo Logging**|Months 7-9|Vercel + Render + GPU service|YOLOv8 food recognition, portion estimation|
|**v3.0 — AI Assistant**|Months 10-14|Full cloud infra|RAG-based conversational health engine|
|**v4.0 — Genetics**|Year 2|HIPAA-ready infrastructure|Genetic predisposition module, B2B API|


*This document is a living specification. Update it as each sprint completes.*

NutriCore 2.0 SDLC · Version 1.0 · April 2026 · Team CodeFin
