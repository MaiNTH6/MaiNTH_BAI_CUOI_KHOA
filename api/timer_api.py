# api/timer_api.py
import time

class APITimer:
    @staticmethod
    def measure(api_call, payload=None,**kwargs):
        start = time.perf_counter()
        response = api_call(payload, **kwargs) if payload is not None else api_call(**kwargs)
        duration = round(time.perf_counter() - start, 3)
        return response, duration
