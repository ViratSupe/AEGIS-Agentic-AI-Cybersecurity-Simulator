<div align="center">

# ⚡ AEGIS
### Agentic AI Cybersecurity Simulator

**AI-powered Red Team vs Blue Team Cybersecurity Simulator with Real Log Analysis**

<br/>

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Gemini AI](https://img.shields.io/badge/Gemini-AI-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev)
[![JavaScript](https://img.shields.io/badge/JavaScript-ES2024-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)](https://developer.mozilla.org)
[![Render](https://img.shields.io/badge/Backend-Render-46E3B7?style=for-the-badge&logo=render&logoColor=white)](https://render.com)
[![Vercel](https://img.shields.io/badge/Frontend-Vercel-000000?style=for-the-badge&logo=vercel&logoColor=white)](https://vercel.com)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-22c55e?style=for-the-badge)]()

<br/>

> *A fully autonomous, multi-agent AI system that simulates real-world cyberattacks,*
> *detects threats using LLM + rule-based fallback, makes decisions, and executes responses — all in real time.*

<br/>

[🔗 Live Demo](#-live-demo) &nbsp;·&nbsp; [✨ Features](#-features) &nbsp;·&nbsp; [🏗 Architecture](#-architecture) &nbsp;·&nbsp; [🛠 Installation](#-installation) &nbsp;·&nbsp; [📡 API Docs](#-api-endpoints)

</div>

---



## 🔗 Live Demo

<div align="center">

### [**▶ Try the Live Application →**](https://ai-blue-red-simulator.vercel.app)

<!-- 🔁 Replace the URL above with your deployed Vercel / Render / GitHub Pages link -->

</div>

---

## 🧠 What is AEGIS?

AEGIS (**A**gentic **E**ngagement & **G**uardian **I**ntelligence **S**ystem) is a **full-stack, multi-agent AI cybersecurity platform** that mirrors how real Security Operations Centers (SOCs) operate.

Four specialised agents collaborate in sequence:

- 🔴 **Red Team Agent** — generates realistic attack logs (brute force, SQL injection, port scans)
- 🔵 **Blue Team Agent** — analyses threats using **Gemini AI**, with a keyword + rule-based fallback when the API is unavailable
- 🟡 **Planner Agent** — maps assessed threat severity to a concrete action decision
- 🟢 **Action Engine** — executes the decision, blocks IPs, and persists all incidents

All of this is visualised live in a **SOC-style cyberpunk dashboard** with animated card transitions, a log-upload drop zone, and real-time pipeline status indicators.

---

## ✨ Features

| | Feature | Details |
|---|---|---|
| 🤖 | **Agentic AI Pipeline** | Four agents collaborate autonomously — no human in the loop |
| 📁 | **Real Log Ingestion** | Upload `.log` / `.txt` files; each line is parsed and processed individually |
| 🧠 | **LLM + Fallback Detection** | Gemini AI primary; rule-based keyword detection as a zero-dependency fallback |
| 🎯 | **Threat Classification** | `LOW` / `MEDIUM` / `HIGH` severity with a natural-language justification |
| ⚡ | **Automated Response** | `block_ip`, `monitor`, or `ignore` — executed and logged as incidents |
| 🖥️ | **SOC Dashboard UI** | Dark-theme cyberpunk UI with animated card reveals and live status tickers |
| 🔒 | **Rate Limiting** | Per-IP rate limiting on sensitive endpoints to prevent API abuse |
| ☁️ | **Cloud Deployed** | Backend on Render · Frontend on Vercel · accessible with zero setup |
| 🧩 | **Modular Architecture** | Every agent is independently testable, replaceable, and extensible |

---

## 🏗 Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          AEGIS Pipeline                                 │
│                                                                         │
│    ┌─────────────┐      ┌─────────────────┐      ┌──────────────────┐  │
│    │    INPUT    │      │  RED TEAM AGENT  │      │ BLUE TEAM AGENT  │  │
│    │             │─────▶│                  │─────▶│                  │  │
│    │  GET /run   │      │  Generates       │      │  Gemini AI       │  │
│    │  POST /upload│     │  attack logs     │      │  + Rule Fallback │  │
│    └─────────────┘      └─────────────────┘      └────────┬─────────┘  │
│                                                            │            │
│                                                            ▼            │
│    ┌─────────────┐      ┌─────────────────┐      ┌──────────────────┐  │
│    │  AEGIS UI   │      │  ACTION ENGINE   │      │  PLANNER AGENT   │  │
│    │             │◀─────│                  │◀─────│                  │  │
│    │  Dashboard  │      │  block_ip        │      │  HIGH → block    │  │
│    │  Incidents  │      │  monitor         │      │  MED  → monitor  │  │
│    │  Blocked IPs│      │  ignore          │      │  LOW  → ignore   │  │
│    └─────────────┘      └─────────────────┘      └──────────────────┘  │
│                                   │                                     │
│                                   ▼                                     │
│                          ┌─────────────────┐                           │
│                          │   MEMORY STORE   │                           │
│                          │  Incidents  ·    │                           │
│                          │  Blocked IPs     │                           │
│                          └─────────────────┘                           │
└─────────────────────────────────────────────────────────────────────────┘
```

### Detection Tiers

```
Tier 1 (Primary)   →  Gemini 1.5 Flash   →  LLM-powered contextual analysis
                          │ (timeout / error / no key)
                          ▼
Tier 2 (Fallback)  →  Rule Engine        →  Attack-type lookup + keyword scan
                          │ (no match)
                          ▼
Tier 3 (Default)   →  LOW / ignore       →  Safe no-action baseline
```

---

## 🛠 Installation

### Prerequisites

- Python **3.11+**
- A [Google Gemini API key](https://ai.google.dev) *(optional — rule-based fallback works without it)*

---

### Step 1 — Clone the repository

```bash
git clone https://github.com/ViratSpe/AI-RED-BLUE-SIMULATOR.git
cd AI-RED-BLUE-SIMULATOR
```

### Step 2 — Create a virtual environment

```bash
python -m venv .venv

# macOS / Linux
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

### Step 3 — Install dependencies

```bash
pip install -r api/requirements.txt
```

### Step 4 — Configure environment variables

Edit `.env` in the project root:

```env
# Gemini AI — optional (rule-based fallback activates if absent)
GEMINI_API_KEY=your_gemini_api_key_here

# Optional tuning
GEMINI_MODEL=gemini-1.5-flash
GEMINI_TIMEOUT_SECS=8
```

### Step 5 — Start the backend

```bash
# Option A — use the entry point
python run.py

# Option B — start FastAPI directly
uvicorn api.main:app --reload
```

| URL | Description |
|---|---|
| `http://127.0.0.1:8000` | Backend API root |
| `http://127.0.0.1:8000/docs` | Interactive Swagger UI |
| `http://127.0.0.1:8000/redoc` | ReDoc documentation |

### Step 6 — Open the frontend

```bash
# Option A — open directly (no build step needed)
open frontend/index.html          # macOS
start frontend/index.html         # Windows
xdg-open frontend/index.html      # Linux

# Option B — serve with a static server
npx serve frontend/
```

---

## 📡 API Endpoints

| Method | Endpoint | Description | Auth | Rate Limit |
|--------|----------|-------------|:----:|:---:|
| `GET` | `/` | Health check + version info | ❌ | ❌ |
| `GET` | `/run` | Run full simulation pipeline | ❌ | ✅ 5/min |
| `POST` | `/upload` | Upload `.log`/`.txt` for analysis | ❌ | ❌ |
| `GET` | `/incidents` | All stored incidents (newest first) | ❌ | ❌ |
| `GET` | `/blocked` | All blocked IPs | ❌ | ❌ |

> Full interactive documentation available at `/docs` when the backend is running.

---

## 💡 Example Usage

### GET /run — Simulated Pipeline

```bash
curl http://localhost:8000/run
```

<details>
<summary>📋 View full response</summary>

```json
{
  "run_id": "f3a1b2c4-9d3e-4f1c-a2b8-7e6d5c4b3a21",
  "status": "completed",
  "ran_at": "2025-04-05T14:32:07Z",
  "attack": {
    "log_id": "a1b2c3d4-0001",
    "attack_type": "sql_injection",
    "source_ip": "185.44.23.101",
    "target_ip": "10.0.0.5",
    "payload": "' UNION SELECT username, password FROM users --",
    "timestamp": "2025-04-05T14:32:05Z"
  },
  "assessment": {
    "threat_level": "HIGH",
    "reason": "SQL injection payload identified. Attacker may be attempting unauthorised data access.",
    "recommended_action": "block_ip",
    "source_ip": "185.44.23.101",
    "assessed_by": "BT-API",
    "assessed_at": "2025-04-05T14:32:06Z",
    "detection_source": "gemini"
  },
  "plan": {
    "decision": "block_ip",
    "explanation": "Threat level is HIGH. Immediate action required — source IP flagged for blocking.",
    "target_ip": "185.44.23.101",
    "planned_by": "PLANNER-API",
    "planned_at": "2025-04-05T14:32:06Z"
  },
  "action": {
    "action_taken": "block_ip",
    "target_ip": "185.44.23.101",
    "detail": "IP 185.44.23.101 added to blocklist."
  }
}
```

</details>

---

### POST /upload — Log File Ingestion

**Sample `attack.log`:**

```
185.44.23.101 - - [05/Apr/2025] "POST /login HTTP/1.1" 401 failed password attempts
{"log_id":"abc-001","attack_type":"port_scan","source_ip":"91.120.55.18","target_ip":"10.0.0.5","timestamp":"2025-04-05T14:00:00Z","open_ports":[80,443,3306]}
10.33.22.99 - SQL error: unauthorized ' OR 1=1 -- access attempt on /api/users
```

```bash
curl -X POST http://localhost:8000/upload \
  -F "file=@attack.log"
```

<details>
<summary>📋 View full response</summary>

```json
{
  "filename": "attack.log",
  "lines_found": 3,
  "lines_processed": 3,
  "processed_at": "2025-04-05T14:35:00Z",
  "results": [
    {
      "line_index": 0,
      "raw_log": "185.44.23.101 - - POST /login 401 failed password attempts",
      "analysis": {
        "threat_level": "HIGH",
        "reason": "Log contains failed authentication indicators.",
        "recommended_action": "block_ip",
        "detection_source": "rule-based-fallback"
      },
      "decision": { "decision": "block_ip", "target_ip": "185.44.23.101" },
      "action":   { "action_taken": "block_ip", "detail": "IP added to blocklist." }
    }
  ]
}
```

</details>

---

## 📁 Project Structure

```
AI-RED-BLUE-SIMULATOR/
│
├── 📂 actions/
│   └── action_engine.py         # Executes block / monitor / ignore decisions
│
├── 📂 agents/
│   ├── blue_agent.py            # Gemini AI + rule-based fallback detection
│   ├── planner_agent.py         # Threat level → action decision mapper
│   └── red_agent.py             # Brute force, SQL injection, port scan simulator
│
├── 📂 api/
│   ├── main.py                  # FastAPI app — all endpoints + app factory
│   ├── rate_limiter.py          # Per-IP rate limiting middleware
│   └── requirements.txt         # Python dependencies
│
├── 📂 core/
│   └── main.py                  # Pipeline orchestrator — wires all agents together
│
├── 📂 frontend/
│   └── index.html               # Single-file SOC dashboard UI
│
├── 📂 memory/
│   ├── incidents.json           # Persisted incident log
│   └── memory_store.py          # In-memory + file-backed incident store
│
├── .env                         # Environment variables (GEMINI_API_KEY etc.)
├── .gitignore
└── run.py                       # Entry point — starts the full stack
```

---

## 🔮 Future Improvements

| Priority | Feature | Description |
|:---:|---|---|
| 🔴 | **Real-time log streaming** | WebSocket-based live log tail with instant agent analysis |
| 🔴 | **Authentication & RBAC** | JWT auth for API endpoints + role-based dashboard access |
| 🟡 | **SIEM Integration** | Export incidents to Splunk, Elastic Stack, or Datadog |
| 🟡 | **IP Geolocation Map** | Visualise attack origins on a live world map |
| 🟡 | **Custom Rule Builder** | UI to define detection rules without modifying code |
| 🟢 | **Slack / Discord Alerts** | Webhook notifications for HIGH-severity incidents |
| 🟢 | **Historical Analytics** | Incident trends, attack-type breakdowns, timeline charts |
| 🟢 | **Docker Support** | Single `docker compose up` for full-stack local deployment |

---

## 🧰 Tech Stack

<div align="center">

| Layer | Technology |
|---|---|
| **Backend Framework** | FastAPI · Pydantic v2 · Uvicorn |
| **AI / LLM** | Google Gemini 1.5 Flash (`google-generativeai`) |
| **Fallback Detection** | Custom rule engine — zero extra dependencies |
| **Frontend** | Vanilla JS (ES2024) · HTML5 · CSS3 |
| **Typography** | Orbitron · Rajdhani · Share Tech Mono |
| **Backend Hosting** | Render |
| **Frontend Hosting** | Vercel |
| **Runtime** | Python 3.11+ |

</div>

---

## 👨‍💻 Author

<div align="center">

<img src="https://avatars.githubusercontent.com/ViratSpe" width="96" style="border-radius:50%" alt="Virat Solanki"/>

### Virat Solanki

*Building intelligent systems at the intersection of AI and cybersecurity*

[![GitHub](https://img.shields.io/badge/GitHub-ViratSolanki-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/ViratSpe)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Virat%20Solanki-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/virat-solanki-b1a820293/)

</div>

---

## ⭐ Support

If AEGIS helped you learn, inspired a project, or impressed you — a ⭐ on GitHub costs nothing and means everything.

---

<div align="center">

*"Security is not a product, but a process."* — **Bruce Schneier**

<br/>

**Built with 🤖 autonomous agents · ☕ late nights · and genuine respect for the craft of security engineering.**

<br/>

`Red Team attacks. Blue Team defends. AEGIS never sleeps.`

</div>
