from HealthCheck_Pinger.core import PingHC
from functools import wraps

def pingDecor(uuid, server=None):
    """Custom decorator that pings HealthCheck Server"""
    def inner_function(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            if server:
                ping =PingHC(uuid, server)
            else:
                ping = PingHC(uuid)
            try:
                function(*args, **kwargs)
            except:
                ping.failure
            else:
                ping.success
        return wrapper
    return inner_function