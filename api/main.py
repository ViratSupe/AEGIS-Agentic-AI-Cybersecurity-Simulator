"""
api/main.py
-----------
Production-ready FastAPI backend for the cybersecurity multi-agent system.

Endpoints:
  GET /            → health check
  GET /run         → full pipeline (attack → analyse → decide → act)
  GET /incidents   → all stored incidents
  GET /blocked     → all blocked IPs

Run:
    uvicorn api.main:app --reload
  or from the project root:
    uvicorn main:app --reload  (if running from inside api/)
"""

import uuid
from datetime import datetime
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# ── Agent imports ──────────────────────────────────────────────────────────────
# Adjust these import paths if your agents live in a sub-package.
from agents.red_agent import RedTeamAgent
from agents.blue_agent import BlueTeamAgent
from agents.planner_agent import PlannerAgent


# ══════════════════════════════════════════════════════════════════════════════
# In-process stores (replace with a real DB in production)
# ══════════════════════════════════════════════════════════════════════════════

class MemoryStore:
    """Lightweight in-memory incident + blocked-IP store."""

    def __init__(self) -> None:
        self._incidents: list[dict] = []
        self._blocked_ips: set[str] = set()

    # incidents
    def add_incident(self, incident: dict) -> None:
        self._incidents.append(incident)

    def get_incidents(self) -> list[dict]:
        return list(reversed(self._incidents))   # newest first

    # blocked IPs
    def block_ip(self, ip: str) -> None:
        self._blocked_ips.add(ip)

    def get_blocked_ips(self) -> list[str]:
        return sorted(self._blocked_ips)

    def is_blocked(self, ip: str) -> bool:
        return ip in self._blocked_ips


class ActionEngine:
    """Executes the action decided by the PlannerAgent."""

    def __init__(self, store: MemoryStore) -> None:
        self._store = store

    def execute(self, plan: dict) -> dict:
        decision  = plan.get("decision", "ignore")
        target_ip = plan.get("target_ip", "unknown")
        result    = {"action_taken": decision, "target_ip": target_ip}

        if decision == "block_ip":
            self._store.block_ip(target_ip)
            result["detail"] = f"IP {target_ip} added to blocklist."
        elif decision == "monitor":
            result["detail"] = f"IP {target_ip} added to watchlist."
        else:
            result["detail"] = "No active response required."

        return result


# ══════════════════════════════════════════════════════════════════════════════
# Pydantic response schemas
# ══════════════════════════════════════════════════════════════════════════════

class HealthResponse(BaseModel):
    status: str = "ok"
    service: str = "cybersecurity-multi-agent-api"
    version: str = "1.0.0"
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")


class AttackLog(BaseModel):
    log_id:      str
    agent_id:    str
    timestamp:   str
    source_ip:   str
    target_ip:   str
    attack_type: str
    payload:     Any = None


class ThreatAssessment(BaseModel):
    threat_level:       str
    reason:             str
    recommended_action: str
    source_ip:          str
    source_log_id:      str
    assessed_by:        str
    assessed_at:        str


class ActionPlan(BaseModel):
    decision:    str
    explanation: str
    target_ip:   str
    planned_by:  str
    planned_at:  str


class ActionResult(BaseModel):
    action_taken: str
    target_ip:    str
    detail:       str


class PipelineResponse(BaseModel):
    run_id:     str
    status:     str = "completed"
    ran_at:     str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    attack:     AttackLog
    assessment: ThreatAssessment
    plan:       ActionPlan
    action:     ActionResult


class IncidentsResponse(BaseModel):
    total:     int
    incidents: list[dict]


class BlockedResponse(BaseModel):
    total:      int
    blocked_ips: list[str]


# ══════════════════════════════════════════════════════════════════════════════
# Application factory
# ══════════════════════════════════════════════════════════════════════════════

def create_app() -> FastAPI:
    app = FastAPI(
        title="Cybersecurity Multi-Agent API",
        description="Red → Blue → Planner → ActionEngine pipeline exposed via REST.",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # ── CORS ───────────────────────────────────────────────────────────────────
    # Adjust allow_origins for your frontend domain in production.
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],          # tighten this in prod, e.g. ["https://yourdomain.com"]
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # ── Shared singletons (created once at startup) ────────────────────────────
    store         = MemoryStore()
    red_agent     = RedTeamAgent(agent_id="RT-API")
    blue_agent    = BlueTeamAgent(agent_id="BT-API")
    planner       = PlannerAgent(agent_id="PLANNER-API")
    action_engine = ActionEngine(store=store)

    # ══════════════════════════════════════════════════════════════════════════
    # Routes
    # ══════════════════════════════════════════════════════════════════════════

    @app.get(
        "/",
        response_model=HealthResponse,
        summary="Health check",
        tags=["System"],
    )
    def health_check() -> HealthResponse:
        """Returns service status and current UTC timestamp."""
        return HealthResponse()

    # ── ─────────────────────────────────────────────────────────────────────────

    @app.get(
        "/run",
        response_model=PipelineResponse,
        summary="Run full pipeline",
        tags=["Pipeline"],
    )
    def run_pipeline() -> PipelineResponse:
        """
        Executes one full attack → analysis → decision → action cycle.

        1. **RedTeamAgent**   generates a random attack log.
        2. **BlueTeamAgent**  assesses the threat level.
        3. **PlannerAgent**   decides the action (block / monitor / ignore).
        4. **ActionEngine**   executes the decision and stores the incident.
        """
        try:
            # Step 1 — generate attack
            attack_log = red_agent.generate_random_logs(count=1)[0]

            # Step 2 — analyse threat
            assessment = blue_agent.analyse(attack_log)

            # Step 3 — plan action
            plan = planner.plan(assessment)

            # Step 4 — execute action
            action_result = action_engine.execute(plan)

            # Build a unified incident record and persist it
            run_id = str(uuid.uuid4())
            incident = {
                "run_id":     run_id,
                "ran_at":     datetime.utcnow().isoformat() + "Z",
                "attack":     attack_log,
                "assessment": assessment,
                "plan":       plan,
                "action":     action_result,
            }
            store.add_incident(incident)

            return PipelineResponse(
                run_id     = run_id,
                attack     = AttackLog(**{k: attack_log.get(k) for k in AttackLog.model_fields}),
                assessment = ThreatAssessment(**{k: assessment.get(k) for k in ThreatAssessment.model_fields}),
                plan       = ActionPlan(**{k: plan.get(k) for k in ActionPlan.model_fields}),
                action     = ActionResult(**action_result),
            )

        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc)) from exc

    # ── ─────────────────────────────────────────────────────────────────────────

    @app.get(
        "/incidents",
        response_model=IncidentsResponse,
        summary="List all incidents",
        tags=["Data"],
    )
    def get_incidents() -> IncidentsResponse:
        """Returns all stored incidents (newest first)."""
        incidents = store.get_incidents()
        return IncidentsResponse(total=len(incidents), incidents=incidents)

    # ── ─────────────────────────────────────────────────────────────────────────

    @app.get(
        "/blocked",
        response_model=BlockedResponse,
        summary="List blocked IPs",
        tags=["Data"],
    )
    def get_blocked() -> BlockedResponse:
        """Returns all IPs that have been blocked by the ActionEngine."""
        blocked = store.get_blocked_ips()
        return BlockedResponse(total=len(blocked), blocked_ips=blocked)

    return app


# ── Instantiate the app (uvicorn entry point) ──────────────────────────────────
app = create_app()
