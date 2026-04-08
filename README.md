# 🚑 TriageOS — Multi-Agent Emergency Routing

<div align="center">

![TriageOS Banner](https://img.shields.io/badge/Status-Live%20Demo-brightgreen?style=for-the-badge)
[![Live Demo](https://img.shields.io/badge/🔴%20Live%20Demo-Google%20Cloud%20Run-blue?style=for-the-badge)](https://triageos-mvp-337328557825.europe-west1.run.app/)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Google Cloud Run](https://img.shields.io/badge/Google%20Cloud%20Run-Deployed-4285F4?style=for-the-badge&logo=googlecloud&logoColor=white)](https://cloud.google.com/run)
[![Gemini](https://img.shields.io/badge/Gemini%202.5%20Flash-AI%20Engine-8E24AA?style=for-the-badge&logo=google&logoColor=white)](https://deepmind.google/gemini)

**An autonomous, API-based multi-agent AI system that eliminates manual data entry during critical medical emergencies — bridging field paramedics and hospital command centers before the ambulance arrives.**

[🔴 Live Demo](https://triageos-mvp-337328557825.europe-west1.run.app/) · [🐛 Report Bug](https://github.com/Sanwar09/TriageOS-MVP/issues) · [✨ Request Feature](https://github.com/Sanwar09/TriageOS-MVP/issues)

</div>

---

## 📋 Table of Contents

- [The Problem](#-the-problem)
- [The Solution](#-the-solution)
- [Live Demo](#-live-demo)
- [Architecture](#️-architecture)
- [Multi-Agent Workflow](#-multi-agent-workflow)
- [Tech Stack](#️-tech-stack)
- [Getting Started](#-getting-started)
- [API Reference](#-api-reference)
- [Hackathon Criteria](#-hackathon-criteria-met)
- [Roadmap](#-roadmap)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🛑 The Problem

Every minute in a trauma emergency costs lives. Yet hospital emergency teams routinely face:

- **Chaotic radio communication** between paramedics and hospital dispatch
- **Manual data entry** of patient vitals during the most critical minutes of care
- **Unprepared receiving teams** — wrong beds, missing specialists, unassembled surgical kits
- **Wasted golden-hour minutes** on administrative handoffs instead of treatment

The result: avoidable delays in patient handover, misallocated resources, and unprepared surgical teams.

---

## 💡 The Solution

TriageOS acts as an **autonomous AI orchestrator** that captures raw, unstructured field reports from paramedics and instantly:

1. **Categorizes** the emergency type and severity (CRITICAL / MODERATE / STABLE)
2. **Calculates** ETAs and resource requirements
3. **Triggers** parallel hospital preparations — ward assignments, nursing task checklists, and specialist scheduling — *before the ambulance arrives*

Zero manual data entry. Zero delay.

---

## 🔴 Live Demo

> **Try it now:** [https://triageos-mvp-337328557825.europe-west1.run.app/](https://triageos-mvp-337328557825.europe-west1.run.app/)

The demo includes two role-based portals:

| Portal | Role | Description |
|--------|------|-------------|
| 🚑 **EMS Uplink** | Paramedic | Submit unstructured field reports on patient vitals and conditions |
| 🏥 **Hospital Command Roster** | Hospital Staff | Live dashboard with bed assignments, ETA alerts, and prep checklists |

**Sample Input to try:**
```
Male, ~45yrs. Unresponsive after MVA. GCS 6. BP 80/50, HR 130 thready.
Suspected TBI + internal bleed. ETA 8 mins. Need trauma bay + neurosurgeon NOW.
```

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    TRIAGEOS ARCHITECTURE                     │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│   🚑 EMS Portal          🏥 Hospital Portal                 │
│   (Paramedic Input)      (Staff Dashboard)                  │
│         │                        ▲                          │
│         ▼                        │                          │
│   ┌─────────────────────────────────────────┐               │
│   │        FastAPI  /api/dispatch            │               │
│   └───────────────────┬─────────────────────┘               │
│                        │                                     │
│                        ▼                                     │
│   ┌─────────────────────────────────────────┐               │
│   │     PRIMARY ORCHESTRATOR                 │               │
│   │     (Gemini 2.5 Flash)                   │               │
│   │     NLP Parsing → JSON Triage Plan       │               │
│   └──────────┬──────────┬──────────┬────────┘               │
│               │           │          │                       │
│               ▼           ▼          ▼                       │
│   ┌──────────────┐ ┌───────────┐ ┌──────────────┐          │
│   │  Database    │ │  Task     │ │  Calendar    │          │
│   │  Sub-Agent   │ │  Sub-Agent│ │  Sub-Agent   │          │
│   │  (Bed/Ward   │ │  (Nursing │ │  (Specialist │          │
│   │  Assignment) │ │  Checklist│ │  Scheduling) │          │
│   └──────────────┘ └───────────┘ └──────────────┘          │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔄 Multi-Agent Workflow

```
Field Input → AI NLP Analysis → Parallel Tool Execution → Live UI Update
```

**Step-by-step:**

1. **EMS Transmission Uplink** — Paramedic submits rapid, unstructured text on patient vitals and condition
2. **API Ingestion** — FastAPI backend receives the payload at `/api/dispatch` and triggers the Primary Orchestrator
3. **AI Triage** — Gemini 2.5 Flash analyzes clinical text to extract severity, resource requirements, and ETA
4. **Sub-Agent Delegation** — Orchestrator sends a structured JSON plan to three parallel sub-agents:
   - **Database Agent** → Logs structured patient record, assigns Trauma Bay or ER bed
   - **Task Agent** → Creates high-priority nursing prep checklist (simulated Jira/Task Manager MCP)
   - **Calendar Agent** → Blocks on-call specialist schedules (simulated Google Workspace Calendar MCP)
5. **Hospital Command Roster** — Staff dashboard updates in real-time with bed assignment, ETA, and all prep tasks — **zero manual entry**

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **AI Engine** | Google Gemini 2.5 Flash API |
| **Backend** | Python 3.11 / FastAPI |
| **Frontend** | HTML5, Vanilla JavaScript, Tailwind CSS |
| **Deployment** | Google Cloud Run (Serverless) / Docker |
| **Containerization** | Docker |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- A Google Gemini API key ([get one here](https://aistudio.google.com/app/apikey))
- Docker (optional, for containerized runs)

### Local Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Sanwar09/TriageOS-MVP.git
   cd TriageOS-MVP
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate        # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env and add your GEMINI_API_KEY
   ```

   ```env
   GEMINI_API_KEY=your_api_key_here
   ```

5. **Run the development server:**
   ```bash
   uvicorn main:app --reload --port 8000
   ```

6. **Open in browser:**
   ```
   http://localhost:8000
   ```

### Docker (Optional)

```bash
# Build the image
docker build -t triageos-mvp .

# Run the container
docker run -p 8000:8000 -e GEMINI_API_KEY=your_key_here triageos-mvp
```

---

## 📡 API Reference

### `POST /api/dispatch`

Accepts a raw paramedic field report and returns a structured triage plan with sub-agent execution results.

**Request Body:**
```json
{
  "report": "Male, ~45yrs. Unresponsive after MVA. GCS 6. BP 80/50, HR 130 thready. Suspected TBI + internal bleed. ETA 8 mins.",
  "unit_id": "AMB-04",
  "eta_minutes": 8
}
```

**Response:**
```json
{
  "patient_id": "PT-20240615-001",
  "severity": "CRITICAL",
  "triage_summary": "Suspected TBI with hemodynamic instability. Requires immediate trauma bay.",
  "bed_assignment": "Trauma Bay 1",
  "agents": {
    "database": { "status": "success", "record_id": "PT-20240615-001" },
    "tasks": { "status": "success", "checklist_items": 7 },
    "calendar": { "status": "success", "specialists_alerted": ["Neurosurgeon", "General Surgeon"] }
  },
  "eta_minutes": 8
}
```

---

## ✅ Hackathon Criteria Met

| Requirement | Implementation |
|-------------|---------------|
| **Primary Agent Coordinating Sub-Agents** | Gemini 2.5 Flash as Primary Orchestrator parses raw text into a strict JSON plan to delegate to 3 sub-agents |
| **Store & Retrieve Structured Data** | Database Sub-Agent logs structured patient records and autonomously assigns Trauma Bay / ER beds |
| **Multiple MCP Tool Integrations** | Simulated MCP integrations: Jira (nursing checklists) + Google Workspace Calendar (specialist scheduling) |
| **Multi-Step Workflow** | Field Input → AI Analysis → Parallel Tool Execution → Live UI Update |
| **API-Based System Deployment** | Decoupled FastAPI backend on `/api/dispatch`, containerized on Google Cloud Run |

---

## 🗺️ Roadmap

- [ ] Real Jira MCP integration for live task creation
- [ ] Real Google Calendar MCP for actual specialist blocking
- [ ] FHIR-compliant patient data export
- [ ] Multi-hospital routing and bed availability API
- [ ] SMS/push alerts to on-call staff
- [ ] Voice input support for hands-free paramedic reporting
- [ ] Analytics dashboard for response time metrics

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 👤 Author

**Sanwar** — [@Sanwar09](https://github.com/Sanwar09)

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**Built for the Gen AI Academy Hackathon**

⭐ Star this repo if TriageOS could save lives!

</div>
