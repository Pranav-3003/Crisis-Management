from models import Incident

def get_easy_incidents():
    return [
        Incident(type="Fire", severity=0.8, location="Zone A", is_real=True)
    ]
