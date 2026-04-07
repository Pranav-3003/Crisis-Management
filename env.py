from models import Incident, Resource, Observation, Action

def generate_incidents():
    return [
        Incident(type="Fire", severity=0.8, location="Zone A", is_real=True),
        Incident(type="Medical", severity=0.6, location="Zone B", is_real=True),
        Incident(type="Robbery", severity=0.7, location="Zone C", is_real=False), # Fake alert
    ]

class CrisisEnv:
    def __init__(self):
        self.time = 0
        self.incidents = []
        self.resources = None

    def reset(self):
        self.time = 0
        self.incidents = generate_incidents()
        # Initial resources
        self.resources = Resource(ambulance=3, fire_truck=2, police=4)
        return self.state()

    def state(self):
        return Observation(
            time=self.time,
            incidents=self.incidents,
            resources=self.resources
        )

    def step(self, action: Action):
        reward = 0
        optimal_allocation = False
        correct_response = False
        delayed = False
        resource_wasted = False
        ignored_real_emergency = False

        if action.action_type == "dispatch":
            for incident in self.incidents:
                if incident.location == action.target:
                    if incident.is_real:
                        reward += 10
                        correct_response = True
                        if action.resource == "ambulance" and incident.type == "Medical":
                            optimal_allocation = True
                            self.resources.ambulance -= 1
                        elif action.resource == "fire_truck" and incident.type == "Fire":
                            optimal_allocation = True
                            self.resources.fire_truck -= 1
                        elif action.resource == "police" and incident.type == "Robbery":
                            optimal_allocation = True
                            self.resources.police -= 1
                        else:
                            resource_wasted = True
                        self.incidents.remove(incident)
                    else:
                        reward -= 5
                        resource_wasted = True
                        self.incidents.remove(incident)
                    break

        elif action.action_type == "ignore":
            for incident in self.incidents:
                if incident.location == action.target:
                    if incident.is_real:
                        ignored_real_emergency = True
                        reward -= 10
                        self.incidents.remove(incident)
                    else:
                        reward += 5 # Correctly ignoring a fake alert
                        self.incidents.remove(incident)

        elif action.action_type == "verify":
            # Just spends time but we gain knowledge maybe?
            delayed = True

        # Custom smart rewards
        if optimal_allocation:
            reward += 5
        if delayed:
            reward -= 2
        if resource_wasted:
            reward -= 5
        
        self.time += 1
        done = self.time > 20 or len(self.incidents) == 0

        # Phase 4 smarter reward
        return self.state(), reward, done, {}
