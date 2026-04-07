import json
from datetime import datetime


class ActionEngine:
    def __init__(self):
        self.blocked_ips = []
        self.monitored_ips = []
        self.log_file = "memory/incidents.json"

    def execute(self, decision_data):
        decision = decision_data.get("decision")
        ip = decision_data.get("target_ip", "unknown")

        action_result = {
            "timestamp": str(datetime.now()),
            "action_taken": decision,
            "target_ip": ip,
            "status": "success"
        }

        if decision == "block_ip":
            if ip not in self.blocked_ips:
                self.blocked_ips.append(ip)

        elif decision == "monitor":
            if ip not in self.monitored_ips:
                self.monitored_ips.append(ip)

        # Save to file
        self._log_incident(action_result)

        return action_result

    def _log_incident(self, data):
        try:
            with open(self.log_file, "r") as f:
                logs = json.load(f)
        except:
            logs = []

        logs.append(data)

        with open(self.log_file, "w") as f:
            json.dump(logs, f, indent=4)