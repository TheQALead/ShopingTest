import time
from .models import ApiLog

class ApiLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        started = time.time()
        response = self.get_response(request)
        try:
            headers = dict(request.headers)
            if 'Authorization' in headers:
                headers['Authorization'] = 'Bearer ***'
            ApiLog.objects.create(
                user=request.user if getattr(request, 'user', None) and request.user.is_authenticated else None,
                method=request.method,
                path=request.path,
                status=response.status_code,
                latency_ms=int((time.time() - started) * 1000),
                request_headers=headers,
                request_body=(request.body or b'')[:2000].decode('utf-8', errors='ignore'),
                response_body=getattr(response, 'content', b'')[:2000].decode('utf-8', errors='ignore'),
            )
        except Exception:
            pass
        return response
