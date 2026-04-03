# AI Smart Nutrition - Specification (Source of Truth)

## Overview
NutriCore is an AI-powered personalized nutrition and diet tracking application. The application is transitioning from a fragmented frontend prototype into a production-grade full-stack ecosystem using React, FastAPI, PostgreSQL, and MongoDB.

## Core Features
1. **User Authentication & Profiles**: Secure login/registration. User profiles track age, weight, health conditions, and diet preferences.
2. **Comprehensive Food Database**: 100+ foods including staples, dairy, vegetables, protein, snacks, and Indian staples. Extensive nutritional tracking (macros, micros, GI).
3. **Disease-Specific Diet Plans**: Customized meal targets for 9+ health conditions (Diabetes, Hypertension, Heart Disease, Weight Loss, Celiac, Kidney Disease, Thyroid, Anemia, Arthritis).
4. **Nutrition Tracking**: Real-time meal logging, nutrient analysis, and anomaly/gap detection.
5. **Health Scoring & AI Predictions**: Dynamic health score (0-100) based on dietary choices. Disease risk predictions and personalized recommendations using AI.

## Technical Architecture
- **Frontend**: React-based SPA. Logic is cleanly separated from UI via Custom Hooks (`useMealLog`, `useUserGoals`). Centralized API layer using Axios with JWT interceptors.
- **Backend**: FastAPI functional architecture:
  - `app/api`: Router definitions.
  - `app/core`: Security (JWT) and config.
  - `app/services`: Business logic (nutritional calculations, AI).
  - `app/db`: Data Access Layer.
- **Database (Multi-Modal)**:
  - **PostgreSQL**: Stores strictly structured, relational data (Users, Profiles, Goals).
  - **MongoDB**: Stores flexible, semi-structured data (Meal logs, Food items, AI-generated metadata).

## Security
- JWT Authentication with RS256 asymmetric signing.
- Dual-token strategy: short-lived access tokens, long-lived refresh tokens.
- Tokens securely stored in HttpOnly, Secure cookies.
- Strict PII encapsulation.

## AI Engine & Validation
- **Prediction Modules**: YOLOv8 (food recognition) and RAG (personalized advice).
- **Statistical Validation**: Algorithm caloric predictions must fall within ±5% of ground truth, verified via standard deviation testing.
