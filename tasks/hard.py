from models import Incident

def get_hard_incidents():
    return [
        Incident(type="Fire", severity=0.9, location="Zone A", is_real=True),
        Incident(type="Medical", severity=0.5, location="Zone B", is_real=False), # Fake alert
        Incident(type="Police", severity=0.8, location="Zone A", is_real=True), # Conflicting
        Incident(type="Fire", severity=0.6, location="Zone C", is_real=False), # Fake alert
        Incident(type="Medical", severity=0.9, location="Zone D", is_real=True)
    ]
