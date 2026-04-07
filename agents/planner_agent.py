"""
planner_agent.py
----------------
Planner Agent for a cybersecurity multi-agent system.

Receives a Blue Team threat assessment and decides the next action:
  - block_ip  → HIGH threat
  - monitor   → MEDIUM threat
  - ignore    → LOW / unknown threat

No external dependencies — pure Python standard library.
"""

import json
from datetime import datetime


# ── Decision Rules ─────────────────────────────────────────────────────────────
# Maps threat level → (decision, explanation template).
# Edit here to change policy without touching core logic.

DECISION_RULES: dict[str, dict] = {
    "HIGH": {
        "decision": "block_ip",
        "explanation": (
            "Threat level is HIGH. Immediate action required — "
            "the source IP has been flagged for blocking to prevent "
            "further intrusion attempts or data compromise."
        ),
    },
    "MEDIUM": {
        "decision": "monitor",
        "explanation": (
            "Threat level is MEDIUM. Activity is suspicious but not "
            "immediately critical. The source IP will be added to the "
            "watchlist for continued observation."
        ),
    },
    "LOW": {
        "decision": "ignore",
        "explanation": (
            "Threat level is LOW. No significant risk detected. "
            "Log retained for audit purposes — no active response required."
        ),
    },
}

# Fallback if threat_level is missing or unrecognised
DEFAULT_RULE: dict = {
    "decision": "ignore",
    "explanation": (
        "Threat level is unrecognised or absent. Defaulting to ignore "
        "pending manual review of the source assessment."
    ),
}


# ── Planner Agent ──────────────────────────────────────────────────────────────

class PlannerAgent:
    """
    Evaluates Blue Team threat assessments and produces a structured
    action plan (decision + explanation).

    Usage:
        planner = PlannerAgent()
        plan    = planner.plan(blue_team_assessment)
    """

    def __init__(self, agent_id: str = "PLANNER-01"):
        self.agent_id = agent_id
        # Full audit trail of every decision made this session
        self._decision_log: list[dict] = []

    # ── Public API ─────────────────────────────────────────────────────────────

    def plan(self, assessment: dict | str) -> dict:
        """
        Main entry point.
        Accepts a Blue Team assessment dict (or JSON string) and returns
        a structured action plan.
        """
        # Accept raw JSON strings for pipeline convenience
        if isinstance(assessment, str):
            assessment = self._parse_json(assessment)

        self._validate(assessment)

        threat_level = assessment.get("threat_level", "").upper()
        rule = DECISION_RULES.get(threat_level, DEFAULT_RULE)

        # Build the action plan
        plan = {
            "decision":        rule["decision"],
            "explanation":     self._build_explanation(rule["explanation"], assessment),
            "threat_level":    threat_level or "UNKNOWN",
            "target_ip":       assessment.get("source_ip", "unknown"),
            "source_log_id":   assessment.get("source_log_id", "unknown"),
            "planned_by":      self.agent_id,
            "planned_at":      datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        }

        # Record in session audit log
        self._decision_log.append(plan)
        return plan

    def plan_batch(self, assessments: list[dict]) -> list[dict]:
        """Process a list of Blue Team assessments and return a list of plans."""
        return [self.plan(a) for a in assessments]

    def audit_log(self) -> list[dict]:
        """Return the full list of decisions made this session."""
        return self._decision_log.copy()

    def summary(self) -> dict:
        """
        High-level summary of all decisions made this session.
        Useful for dashboards and end-of-run reporting.
        """
        if not self._decision_log:
            return {"message": "No decisions recorded yet."}

        counts: dict[str, int] = {"block_ip": 0, "monitor": 0, "ignore": 0}
        for entry in self._decision_log:
            decision = entry.get("decision", "ignore")
            counts[decision] = counts.get(decision, 0) + 1

        return {
            "agent_id":          self.agent_id,
            "total_decisions":   len(self._decision_log),
            "decision_breakdown": counts,
            "blocked_ips":       self._ips_by_decision("block_ip"),
            "monitored_ips":     self._ips_by_decision("monitor"),
        }

    # ── Internal helpers ───────────────────────────────────────────────────────

    def _build_explanation(self, template: str, assessment: dict) -> str:
        """
        Enrich the base explanation with context from the assessment
        (e.g. attack type, recommended action from the Blue Team).
        """
        attack_hint = assessment.get("reason", "")
        bt_action   = assessment.get("recommended_action", "")

        extra_parts = []
        if attack_hint:
            extra_parts.append(f"Blue Team note: {attack_hint}")
        if bt_action:
            extra_parts.append(f"Blue Team recommended: '{bt_action}'.")

        if extra_parts:
            return template + " | " + " ".join(extra_parts)
        return template

    def _validate(self, assessment: dict) -> None:
        """Raise ValueError if the assessment is missing required fields."""
        required = {"threat_level", "source_ip", "source_log_id"}
        missing = required - assessment.keys()
        if missing:
            raise ValueError(f"Assessment is missing required fields: {missing}")

    @staticmethod
    def _parse_json(raw: str) -> dict:
        """Safely parse a JSON string into a dict."""
        try:
            return json.loads(raw)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSON input: {exc}") from exc

    def _ips_by_decision(self, decision: str) -> list[str]:
        """Return unique IPs associated with a specific decision type."""
        return list({
            entry["target_ip"]
            for entry in self._decision_log
            if entry.get("decision") == decision
        })


# ── Pretty printer ─────────────────────────────────────────────────────────────

def print_plan(plan: dict) -> None:
    """Render a single action plan with colour-coded decision label."""
    colour = {
        "block_ip": "\033[91m",   # red
        "monitor":  "\033[93m",   # yellow
        "ignore":   "\033[92m",   # green
    }.get(plan["decision"], "")
    reset = "\033[0m"

    print(f"\n{colour}{'─' * 55}")
    print(f"  DECISION : {plan['decision'].upper()}")
    print(f"{'─' * 55}{reset}")
    print(json.dumps(plan, indent=2))


# ── Example usage ──────────────────────────────────────────────────────────────

def main():
    # Simulated Blue Team assessments
    # (in production these come directly from BlueTeamAgent.analyse())
    sample_assessments = [
        {
            "threat_level":       "HIGH",
            "reason":             "Brute-force attack — 342 attempts recorded.",
            "recommended_action": "block_ip",
            "assessed_by":        "BT-SENTINEL",
            "assessed_at":        "2025-04-05T14:40:01Z",
            "source_log_id":      "a1b2c3d4-0001",
            "source_ip":          "185.44.23.101",
        },
        {
            "threat_level":       "HIGH",
            "reason":             "SQL injection payload detected on /api/users.",
            "recommended_action": "block_ip",
            "assessed_by":        "BT-SENTINEL",
            "assessed_at":        "2025-04-05T14:40:02Z",
            "source_log_id":      "a1b2c3d4-0002",
            "source_ip":          "91.120.55.18",
        },
        {
            "threat_level":       "MEDIUM",
            "reason":             "Port scan detected. Open ports: [80, 443].",
            "recommended_action": "monitor",
            "assessed_by":        "BT-SENTINEL",
            "assessed_at":        "2025-04-05T14:40:03Z",
            "source_log_id":      "a1b2c3d4-0003",
            "source_ip":          "198.0.22.7",
        },
        {
            "threat_level":       "LOW",
            "reason":             "No matching threat signature found.",
            "recommended_action": "ignore",
            "assessed_by":        "BT-SENTINEL",
            "assessed_at":        "2025-04-05T14:40:04Z",
            "source_log_id":      "a1b2c3d4-0004",
            "source_ip":          "203.55.12.9",
        },
    ]

    print("\n" + "=" * 55)
    print("   Planner Agent — Action Decision Engine")
    print("=" * 55)

    planner = PlannerAgent(agent_id="PLANNER-ALPHA")

    # Plan each assessment and print the result
    for assessment in sample_assessments:
        plan = planner.plan(assessment)
        print_plan(plan)

    # Session summary
    print("\n\n" + "=" * 55)
    print("  SESSION SUMMARY")
    print("=" * 55)
    print(json.dumps(planner.summary(), indent=2))
    print("=" * 55 + "\n")


if __name__ == "__main__":
    main()