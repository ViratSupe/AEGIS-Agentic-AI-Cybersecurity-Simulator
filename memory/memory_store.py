import json


class MemoryStore:
    def __init__(self, file_path="memory/incidents.json"):
        self.file_path = file_path

    def save_incident(self, incident):
        try:
            with open(self.file_path, "r") as f:
                data = json.load(f)
        except:
            data = []

        data.append(incident)

        with open(self.file_path, "w") as f:
            json.dump(data, f, indent=4)

    def get_all_incidents(self):
        try:
            with open(self.file_path, "r") as f:
                return json.load(f)
        except:
            return []

    def get_incidents_by_ip(self, ip):
        data = self.get_all_incidents()
        return [i for i in data if i.get("target_ip") == ip]