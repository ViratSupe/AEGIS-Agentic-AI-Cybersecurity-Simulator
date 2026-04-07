"""
red_team_agent.py
-----------------
A simulated Red Team Agent for educational and testing purposes.
Generates realistic attack logs (brute force, SQL injection, port scanning)
in JSON format. No real attacks are performed — this is a log simulator.
"""

import json
import random
import uuid
from datetime import datetime, timedelta


# ── Constants ─────────────────────────────────────────────────────────────────

ATTACK_TYPES = ["brute_force", "sql_injection", "port_scan"]

# Sample payloads per attack type
BRUTE_FORCE_PAYLOADS = [
    "admin:password123",
    "root:toor",
    "user:letmein",
    "admin:admin",
    "guest:guest123",
    "operator:pass@2024",
]

SQL_INJECTION_PAYLOADS = [
    "' OR '1'='1",
    "'; DROP TABLE users; --",
    "' UNION SELECT username, password FROM users --",
    "1' AND SLEEP(5) --",
    "' OR 1=1 LIMIT 1 --",
    "admin'--",
]

PORT_SCAN_PORTS = [21, 22, 23, 25, 53, 80, 110, 143, 443, 3306, 3389, 5432, 8080, 8443]


# ── Helper ────────────────────────────────────────────────────────────────────

def random_ip() -> str:
    """Generate a random public-looking IPv4 address."""
    # Avoid private ranges for realism
    first_octet = random.choice([5, 45, 91, 103, 185, 198, 203, 217])
    return f"{first_octet}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}"


def random_timestamp(within_hours: int = 24) -> str:
    """Return an ISO-8601 timestamp within the last N hours."""
    delta = timedelta(
        hours=random.randint(0, within_hours - 1),
        minutes=random.randint(0, 59),
        seconds=random.randint(0, 59),
    )
    ts = datetime.utcnow() - delta
    return ts.strftime("%Y-%m-%dT%H:%M:%SZ")


# ── Core Class ────────────────────────────────────────────────────────────────

class RedTeamAgent:
    """
    Simulates a red team agent that generates structured attack logs.
    All methods return Python dicts (easily serialisable to JSON).
    """

    def __init__(self, agent_id: str | None = None):
        self.agent_id = agent_id or str(uuid.uuid4())[:8]  # short readable ID

    # ── Individual attack simulators ──────────────────────────────────────────

    def simulate_brute_force(self, target_ip: str | None = None) -> dict:
        """Simulate a brute-force login attempt log entry."""
        return {
            "log_id": str(uuid.uuid4()),
            "agent_id": self.agent_id,
            "timestamp": random_timestamp(),
            "source_ip": random_ip(),
            "target_ip": target_ip or random_ip(),
            "attack_type": "brute_force",
            "payload": random.choice(BRUTE_FORCE_PAYLOADS),
            "status": random.choice(["failed", "failed", "failed", "success"]),  # mostly fail
            "attempts": random.randint(1, 500),
        }

    def simulate_sql_injection(self, target_ip: str | None = None) -> dict:
        """Simulate an SQL injection attempt log entry."""
        endpoints = ["/login", "/search", "/api/users", "/admin/query", "/products"]
        return {
            "log_id": str(uuid.uuid4()),
            "agent_id": self.agent_id,
            "timestamp": random_timestamp(),
            "source_ip": random_ip(),
            "target_ip": target_ip or random_ip(),
            "attack_type": "sql_injection",
            "endpoint": random.choice(endpoints),
            "payload": random.choice(SQL_INJECTION_PAYLOADS),
            "http_method": random.choice(["GET", "POST"]),
            "response_code": random.choice([200, 400, 403, 500]),
        }

    def simulate_port_scan(self, target_ip: str | None = None) -> dict:
        """Simulate a port scan log entry."""
        scanned = sorted(random.sample(PORT_SCAN_PORTS, k=random.randint(3, 8)))
        open_ports = random.sample(scanned, k=random.randint(0, min(3, len(scanned))))
        return {
            "log_id": str(uuid.uuid4()),
            "agent_id": self.agent_id,
            "timestamp": random_timestamp(),
            "source_ip": random_ip(),
            "target_ip": target_ip or random_ip(),
            "attack_type": "port_scan",
            "payload": None,                        # no payload for port scans
            "ports_scanned": scanned,
            "open_ports": open_ports,
            "scan_duration_ms": random.randint(120, 4500),
        }

    # ── Dispatcher ────────────────────────────────────────────────────────────

    def run_attack(self, attack_type: str, target_ip: str | None = None) -> dict:
        """
        Run a specific attack simulation.
        attack_type must be one of: brute_force | sql_injection | port_scan
        """
        dispatch = {
            "brute_force": self.simulate_brute_force,
            "sql_injection": self.simulate_sql_injection,
            "port_scan": self.simulate_port_scan,
        }
        if attack_type not in dispatch:
            raise ValueError(f"Unknown attack type '{attack_type}'. Choose from: {list(dispatch)}")
        return dispatch[attack_type](target_ip)

    # ── Bulk log generator ────────────────────────────────────────────────────

    def generate_random_logs(self, count: int = 10) -> list[dict]:
        """
        Generate `count` random attack log entries across all attack types.
        Useful for bulk testing or populating a SIEM with synthetic data.
        """
        logs = []
        for _ in range(count):
            attack = random.choice(ATTACK_TYPES)
            logs.append(self.run_attack(attack))
        return logs


# ── Entry Point ───────────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("  Red Team Agent — Simulation Log Generator")
    print("=" * 60)

    agent = RedTeamAgent(agent_id="RT-ALPHA")

    # 1. Run one of each attack type individually
    print("\n[+] Single attack simulations:\n")
    for attack in ATTACK_TYPES:
        log = agent.run_attack(attack)
        print(f"--- {attack.upper()} ---")
        print(json.dumps(log, indent=2))
        print()

    # 2. Generate a random batch of 5 logs
    print("[+] Random batch of 5 logs:\n")
    batch = agent.generate_random_logs(count=5)
    for entry in batch:
        print(json.dumps(entry, indent=2))

    print("=" * 60)
    print(f"  Total logs generated: {3 + len(batch)}")
    print("=" * 60)


if __name__ == "__main__":
    main()