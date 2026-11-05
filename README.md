# DisasterGuard AI
## AI-Powered Adaptive Disaster Management and Intelligent Evacuation Route Recommendation System

An academic prototype that combines disaster monitoring, hazard-zone visualization, adaptive evacuation recommendations, and AI-assisted disaster analysis.

> **Disclaimer:** DisasterGuard AI is an educational simulation. Hazard locations, routes, shelter availability, and risk scores are illustrative. It must not be used for real emergency navigation or official disaster-response decisions.

## Team Details

**Team ID:** 2420030040

| Team Member | Student ID |
|---|---|
| Allam Greshmica | 2420030017 |
| Mikkineni Thanvitha | 2420030040 |
| Akshaya Vangalapudi | 2420090047 |

**Supervisor:** To be updated

## 1. Abstract

Disaster management requires decisions that can respond to changing environmental conditions. DisasterGuard AI is an academic prototype designed to demonstrate adaptive disaster monitoring and evacuation planning.

The system maintains disaster and hazard-zone records, evaluates simulated evacuation routes, and updates recommendations when road conditions or hazard exposure change. It also integrates a large language model through the Groq API to generate natural-language analysis of simulated disaster scenarios.

The project demonstrates Adaptive Software Engineering concepts through modular architecture, request-driven adaptation, risk-based decision-making, and automated backend testing.

## 2. Problem Statement

Traditional static evacuation recommendations may not account for changing conditions such as:

- Increasing hazard severity
- Blocked roads
- Crowd density
- Proximity to hazardous areas
- Shelter availability

This project explores how software can recalculate recommendations when these simulated conditions change.

## 3. Project Objectives

- Maintain disaster and hazard-zone records.
- Provide a unified disaster-monitoring website.
- Display hazard locations on an interactive map.
- Recommend evacuation routes using calculated risk scores.
- Adapt route recommendations when conditions change.
- Consider geographic hazard exposure and simulated shelter availability.
- Generate AI-assisted disaster explanations.
- Validate backend functionality using automated tests.

## 4. Implemented Features

### 4.1 Disaster Monitoring Dashboard

Displays recorded disasters, severity levels, locations, and current status.

### 4.2 Hazard Zone Monitoring

Displays recorded hazard zones, their severity, affected locations, radius, and status.

### 4.3 Emergency Reporting

Provides a web form for submitting disaster reports through the backend.

### 4.4 Adaptive Evacuation Recommendations

Evaluates simulated routes using factors including:

- Distance
- Hazard severity
- Crowd density
- Road blockage

The system calculates route risk scores and recommends the lowest-scoring eligible route.

When route conditions are modified and the recommendation is recalculated, the system reevaluates the available alternatives.

### 4.5 Geographic Hazard-Aware Routing

The geographic recommendation module considers the proximity of simulated routes to recorded hazard zones.

It uses geographic distance calculations and hazard penalties to compare candidate routes.

### 4.6 Shelter Availability

The routing simulation considers illustrative shelter capacities and excludes routes associated with full shelters.

Shelter data is currently simulated rather than sourced from a live shelter-management service.

### 4.7 Interactive Hazard Map

Uses Leaflet and OpenStreetMap to display:

- Simulated hazard zones
- Candidate evacuation routes
- Recommended route
- Shelter information
- Geographic risk information

The displayed route coordinates are illustrative and are not verified road-network directions.

### 4.8 AI Disaster Analysis

Integrates the **Groq API** with the **openai/gpt-oss-20b** language model.

The user enters a simulated disaster scenario, and the AI generates:

- Situation summary
- Potential hazards
- General safety precautions

**Important:** The LLM generates explanatory text. Evacuation routes are selected separately by the deterministic routing algorithms. The system does not train its own machine-learning model.

## 5. Adaptive Software Engineering

DisasterGuard AI demonstrates the MAPE-K adaptation concept.

| Stage | Implementation |
|---|---|
| Monitor | Read simulated disaster, hazard, and route-condition inputs |
| Analyze | Calculate route risk and geographic hazard exposure |
| Plan | Select the lowest-risk eligible evacuation route |
| Execute | Display the updated route recommendation |
| Knowledge | Use stored hazard records, routing rules, and parameters |

The current adaptation process is triggered by user requests and recalculation actions. It is not a continuously autonomous real-time monitoring system.

## 6. Technology Stack

| Layer | Technology |
|---|---|
| Programming language | Python |
| Frontend | HTML, CSS, JavaScript |
| Web application | Flask |
| Backend REST API | FastAPI |
| Database | PostgreSQL |
| AI integration | Groq API |
| Language model | openai/gpt-oss-20b |
| Interactive maps | Leaflet, OpenStreetMap |
| Testing | Pytest |
| Version control | Git, GitHub |
| CI configuration | GitHub Actions |

## 7. System Architecture

```text
                 USER
                   |
                   v
          Flask Web Application
           HTML / CSS / JS
                   |
                   v
             FastAPI Backend
                   |
       +-----------+-----------+
       |           |           |
       v           v           v
   PostgreSQL   Evacuation   Groq API
   Disaster &   Risk-Based   LLM Analysis
   Hazard Data  Algorithms
       |           |
       +-----+-----+
             |
             v
     Hazard Map / Dashboard
     Route Recommendations
```

The Flask frontend communicates with the FastAPI backend, which manages disaster information, hazard records, evacuation recommendations, and AI-analysis requests.

## 8. Project Structure

```text
DisasterManagementSystem/
├── .github/
│   └── workflows/
├── backend/
│   ├── app/
│   └── tests/
├── src/
│   ├── app.py
│   ├── templates/
│   └── static/
├── data/
├── docs/
├── reports/
├── results/
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## 9. Installation and Setup

### Prerequisites

- Python
- PostgreSQL
- Git
- Internet connection for AI requests and map tiles
- Groq API key for AI analysis

### Clone the Repository

```bash
git clone https://github.com/thanvitha-m/KLH-CSE-2026-27-2420030040-DisasterManagementSystem.git
cd KLH-CSE-2026-27-2420030040-DisasterManagementSystem
```

### Create a Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### Configure Environment Variables

Create a local `.env` file using `.env.example` as a reference.

Configure the PostgreSQL connection required by the backend and set:

```env
GROQ_API_KEY=your_groq_api_key_here
```

Never commit `.env`, passwords, or API keys to GitHub.

Ensure PostgreSQL is running and the required database configuration is available before starting the backend.

### Start FastAPI

In the first terminal:

```bash
python -m uvicorn backend.app.main:app --reload --port 8000
```

API documentation:

http://127.0.0.1:8000/docs

### Start Flask

In a second terminal:

```bash
source .venv/bin/activate
python src/app.py
```

Open:

http://127.0.0.1:5000

## 10. API Modules

The FastAPI backend provides endpoints for:

- Disaster creation, retrieval, updating, and deletion
- Hazard-zone management
- Evacuation route recommendations
- Geographic hazard-aware recommendations
- AI disaster analysis
- Backend health checks

Interactive API documentation is available through Swagger UI.

## 11. Screenshots

Add screenshots from the working application to `docs/screenshots/`.

Recommended screenshots:

1. Homepage
2. Disaster monitoring dashboard
3. Hazard-zone monitoring
4. Adaptive evacuation recommendation
5. Interactive hazard map
6. AI-generated disaster analysis
7. Emergency reporting page
8. Swagger API documentation
9. Automated test results

Screenshot links can be added here after the images are saved.

## 12. Testing

Automated backend tests are implemented using Pytest.

Run:

```bash
python -m pytest backend/tests -q
```

**Latest verified local result:**

```text
18 passed in 0.80s
```

A GitHub Actions CI workflow is also included in `.github/workflows/ci.yml`.

## 13. Development Methodology

The project follows an incremental development approach.

Implemented development activities include:

- Modular frontend and backend development
- REST API integration
- Database-backed disaster and hazard records
- Adaptive route-scoring logic
- Geographic hazard analysis
- LLM-based disaster explanations
- Automated backend tests
- Git-based version control

## 14. Current Project Status

**Phase:** Functional academic prototype

**Implemented:**

- Unified Flask website
- FastAPI backend
- PostgreSQL disaster and hazard-zone management
- Adaptive route recommendation
- Geographic hazard-aware routing
- Simulated shelter availability
- Interactive hazard map
- Groq LLM disaster analysis
- Automated backend tests

**Testing status:** 18 backend tests passed in the latest verified local run.

## 15. Limitations

- Disaster and hazard scenarios are simulated.
- No verified real-time official emergency feed is connected.
- Map routes are illustrative, not verified road-network paths.
- Shelter capacities are simulated.
- AI-generated explanations are not official emergency guidance.
- Route recalculation is request-driven rather than continuously autonomous.

## 16. Future Enhancements

- Integration with authorized real-time disaster data sources
- Verified road-network routing
- Live shelter-capacity management
- Automated hazard monitoring and adaptation
- More advanced route-risk evaluation
- Expanded integration and user-interface testing

## 17. Repository Guidelines

- Team members contribute using their own GitHub accounts.
- Maintain meaningful commits.
- Keep project documentation updated.
- Never commit API keys or confidential credentials.
- Use appropriate review and release tags for academic milestones.

## 18. Conclusion

DisasterGuard AI demonstrates how Adaptive Software Engineering can support dynamic decision-making in simulated emergency situations.

By combining risk-based evacuation algorithms, geographic hazard analysis, PostgreSQL-backed disaster records, interactive visualization, and Groq-powered AI explanations, the project provides an integrated educational prototype for adaptive disaster management.
