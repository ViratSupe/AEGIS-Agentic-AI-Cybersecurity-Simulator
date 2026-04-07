"""
main.py
-------
Orchestrator for the cybersecurity multi-agent pipeline.

Flow per iteration:
  1. RedTeamAgent   → generates a random attack log
  2. BlueTeamAgent  → analyses the log and assesses threat level
  3. PlannerAgent   → decides the action to take

Run:
    python main.py
"""

import json
import time

from agents.red_agent import RedTeamAgent
from agents.blue_agent import BlueTeamAgent
from agents.planner_agent import PlannerAgent
from actions.action_engine import ActionEngine
from memory.memory_store import MemoryStore

# ── ANSI colour helpers ────────────────────────────────────────────────────────

RESET  = "\033[0m"
BOLD   = "\033[1m"
RED    = "\033[91m"
YELLOW = "\033[93m"
GREEN  = "\033[92m"
CYAN   = "\033[96m"
WHITE  = "\033[97m"
DIM    = "\033[2m"

def colour_for_threat(level: str) -> str:
    return {"HIGH": RED, "MEDIUM": YELLOW, "LOW": GREEN}.get(level, WHITE)

def colour_for_decision(decision: str) -> str:
    return {"block_ip": RED, "monitor": YELLOW, "ignore": GREEN}.get(decision, WHITE)


# ── Printer helpers ────────────────────────────────────────────────────────────

def print_header(text: str, width: int = 58) -> None:
    print(f"\n{BOLD}{CYAN}{'═' * width}")
    print(f"  {text}")
    print(f"{'═' * width}{RESET}")

def print_step(number: int, label: str, agent_name: str) -> None:
    print(f"\n{BOLD}{WHITE}  STEP {number} ─── {label}  {DIM}({agent_name}){RESET}")
    print(f"  {'─' * 50}")

def print_field(key: str, value, indent: int = 4) -> None:
    pad = " " * indent
    if value is None:
        value = "—"
    print(f"{pad}{DIM}{key:<22}{RESET}{WHITE}{value}{RESET}")

def print_attack_log(log: dict) -> None:
    fields = ["log_id", "attack_type", "source_ip", "target_ip",
              "timestamp", "payload", "attempts", "open_ports"]
    for f in fields:
        if f in log:
            print_field(f, log[f])

def print_assessment(a: dict) -> None:
    level = a.get("threat_level", "?")
    c = colour_for_threat(level)
    print(f"    {DIM}{'threat_level':<22}{RESET}{c}{BOLD}{level}{RESET}")
    print_field("reason",             a.get("reason", "—"))
    print_field("recommended_action", a.get("recommended_action", "—"))
    print_field("source_ip",          a.get("source_ip", "—"))

def print_plan(p: dict) -> None:
    decision = p.get("decision", "?")
    c = colour_for_decision(decision)
    print(f"    {DIM}{'decision':<22}{RESET}{c}{BOLD}{decision.upper()}{RESET}")
    print_field("explanation",  p.get("explanation", "—"))
    print_field("target_ip",    p.get("target_ip",   "—"))
    print_field("planned_at",   p.get("planned_at",  "—"))

def print_summary(summary: dict) -> None:
    breakdown = summary.get("decision_breakdown", {})
    print(f"\n{BOLD}{CYAN}{'═' * 58}")
    print("  PIPELINE SUMMARY — ALL ITERATIONS")
    print(f"{'═' * 58}{RESET}")
    print_field("total decisions",  summary.get("total_decisions"))
    print_field("block_ip",         f"{RED}{breakdown.get('block_ip', 0)}{RESET}")
    print_field("monitor",          f"{YELLOW}{breakdown.get('monitor', 0)}{RESET}")
    print_field("ignore",           f"{GREEN}{breakdown.get('ignore', 0)}{RESET}")
    blocked  = summary.get("blocked_ips",   [])
    monitored = summary.get("monitored_ips", [])
    if blocked:
        print_field("blocked IPs",   ", ".join(blocked))
    if monitored:
        print_field("monitored IPs", ", ".join(monitored))
    print(f"{BOLD}{CYAN}{'═' * 58}{RESET}\n")


# ── Pipeline ───────────────────────────────────────────────────────────────────

def run_pipeline(iterations: int = 5, delay: float = 0.4) -> None:
    """
    Run the full multi-agent pipeline for `iterations` cycles.

    Args:
        iterations: Number of attack cycles to simulate.
        delay:      Pause between iterations (seconds) for readability.
    """
    # Initialise agents once — they accumulate session history across runs
    red_agent     = RedTeamAgent(agent_id="RT-ALPHA")
    blue_agent    = BlueTeamAgent(agent_id="BT-SENTINEL")
    planner_agent = PlannerAgent(agent_id="PLANNER-ALPHA")
    action_engine = ActionEngine()
    memory_store = MemoryStore()

    print_header(f"CYBERSECURITY MULTI-AGENT PIPELINE  ·  {iterations} iterations")

    for i in range(1, iterations + 1):

        # ── Iteration banner ───────────────────────────────────────────────────
        print(f"\n\n{BOLD}{WHITE}{'▓' * 58}")
        print(f"  ITERATION {i} of {iterations}")
        print(f"{'▓' * 58}{RESET}")

        # ── Step 1 : Red Team generates attack log ─────────────────────────────
        print_step(1, "ATTACK GENERATED", "RedTeamAgent")
        attack_log = red_agent.generate_random_logs(count=1)[0]
        print_attack_log(attack_log)

        # ── Step 2 : Blue Team analyses the log ───────────────────────────────
        print_step(2, "THREAT ASSESSMENT", "BlueTeamAgent")
        assessment = blue_agent.analyse(attack_log)
        print_assessment(assessment)

        # ── Step 3 : Planner decides the action ───────────────────────────────
        print_step(3, "ACTION DECISION", "PlannerAgent")
        plan = planner_agent.plan(assessment)
        print_plan(plan)

        # Step 4: Execute action
        print_step(4, "ACTION EXECUTION", "ActionEngine")
        action_result = action_engine.execute(plan)
        print(action_result)

        # Step 5: Store in memory
        print_step(5, "MEMORY UPDATE", "MemoryStore")
        memory_store.save_incident({
            "attack": attack_log,
            "assessment": assessment,
            "plan": plan,
            "action": action_result
        })
        print("Incident stored successfully")

        # Small pause between iterations so output is easy to follow
        if i < iterations:
            time.sleep(delay)

    # ── End-of-run summary ─────────────────────────────────────────────────────
    print_summary(planner_agent.summary())


# ── Entry point ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    run_pipeline(iterations=5)