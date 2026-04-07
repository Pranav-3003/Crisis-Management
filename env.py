from models import Incident, Resource

def generate_incidents():
    return [
        Incident(type="Fire", severity=0.8, location="Zone A", is_real=True),
        Incident(type="Medical", severity=0.6, location="Zone B", is_real=True),
        Incident(type="Robbery", severity=0.7, location="Zone C", is_real=False),
    ]

class CrisisEnv:
    def __init__(self):
        self.time = 0
        self.incidents = []
        self.resources = None

    def reset(self):
        self.time = 0
        self.incidents = generate_incidents()
        self.resources = Resource(ambulance=3, fire_truck=2, police=4)
        return self.state()

    def state(self):
        return {
            "time": self.time,
            "incidents": [
                {
                    "type": i.type,
                    "severity": i.severity,
                    "location": i.location,
                    "is_real": i.is_real
                } for i in self.incidents
            ],
            "resources": {
                "ambulance": self.resources.ambulance,
                "fire_truck": self.resources.fire_truck,
                "police": self.resources.police
            }
        }

    def step(self, action):
        reward = 0

        for incident in self.incidents:
            if incident.location == action.target:
                if action.action_type == "dispatch":
                    if incident.is_real:
                        reward += 10
                    else:
                        reward -= 5
                    self.incidents.remove(incident)
                    break

        self.time += 1
        done = self.time > 10 or len(self.incidents) == 0

        return self.state(), float(reward), bool(done), {}