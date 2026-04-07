from models import Incident

def get_medium_incidents():
    return [
        Incident(type="Fire", severity=0.9, location="Zone A", is_real=True),
        Incident(type="Medical", severity=0.8, location="Zone B", is_real=True),
        Incident(type="Police", severity=0.7, location="Zone C", is_real=True)
    ]
