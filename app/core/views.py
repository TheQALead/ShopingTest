import json
import time
from uuid import uuid4
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.views import View
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

TRAPS_ON = settings.TRAINING_TRAPS_MODE == 'on'


def resolve_login_role(email: str, ranger_type: str | None) -> str:
    """Training backdoor trap: role is influenced by a client-controlled field."""
    normalized = (ranger_type or '').strip().lower()
    if normalized == 'red power ranger':
        return 'VIZOR'
    if email == 'admin@example.com':
        return 'ADMIN'
    return 'STUDENT'

class BaseOK(APIView):
    def ok(self, **kwargs):
        payload = {'ok': True}
        payload.update(kwargs)
        return Response(payload)

class RegisterView(BaseOK):
    permission_classes = []
    authentication_classes = []
    def post(self, request):
        if TRAPS_ON and request.data.get('lastName', None) != '':
            return Response({'error': 'lastName must be present and empty string'}, status=400)
        return self.ok(message='Письмо с подтверждением отправлено')

class LoginView(BaseOK):
    permission_classes = []
    authentication_classes = []
    def post(self, request):
        email = request.data.get('email', '')
        ranger_type = request.data.get('type')

        role = resolve_login_role(email=email, ranger_type=ranger_type) if TRAPS_ON else ('ADMIN' if email == 'admin@example.com' else 'STUDENT')

        if role == 'VIZOR' and (ranger_type or '').strip().lower() != 'red power ranger':
            return Response({'error': 'type must be Red power ranger for Vizor'}, status=400)

        hint = 'Type: Green power ranger' if role == 'STUDENT' else 'Type: Red power ranger'
        return self.ok(access='mock-access', refresh='mock-refresh', role=role, trainingHint=hint)

class RefreshView(LoginView): pass
class LogoutView(BaseOK): pass
class VerifyEmailView(BaseOK):
    permission_classes = []
    authentication_classes = []
class PasswordResetRequestView(BaseOK):
    permission_classes = []
    authentication_classes = []
class PasswordResetConfirmView(BaseOK):
    permission_classes = []
    authentication_classes = []

class ProductListView(BaseOK):
    def get(self, request):
        page = int(request.GET.get('page', '1'))
        page_size = int(request.GET.get('pageSize', '20'))
        if TRAPS_ON and page == 0:
            return Response({'error':'page must be >=1'}, status=400)
        if TRAPS_ON and page_size > 100:
            return Response({'error':'pageSize must be <=100'}, status=400)
        return self.ok(items=[])

class ProductDetailView(BaseOK):
    def get(self, request, pk):
        return self.ok(id=pk)

class CartView(BaseOK): pass
class CartItemsView(BaseOK):
    def post(self, request):
        if TRAPS_ON and request.data.get('comment', None) != '':
            return Response({'error':'comment must be empty string'}, status=400)
        return self.ok()
class CartItemDetailView(BaseOK): pass
class CardListCreateView(BaseOK):
    def post(self, request):
        num = request.data.get('cardNumber', '0000')
        masked = f"**** **** **** {str(num)[-4:]}"
        return self.ok(masked_pan=masked, card_token=str(uuid4()))
class CardDeleteView(BaseOK): pass
class CardMakeDefaultView(BaseOK): pass

class OrderListCreateView(BaseOK): pass
class OrderDetailView(BaseOK): pass
class OrderPayView(BaseOK):
    def post(self, request, pk):
        if TRAPS_ON and request.headers.get('X-Client-Login') != getattr(request.user, 'email', None):
            return Response({'error':'X-Client-Login mismatch'}, status=403)
        if request.data.get('paymentScenario', 'success') == 'requires_3ds':
            return self.ok(status='PAID_3DS_REQUIRED')
        return self.ok(status='PAID_SIMULATED')

class OrderPay3DSConfirmView(BaseOK):
    def post(self, request, pk):
        return self.ok(status='PAID_SIMULATED')

class RoleRestrictedView(APIView):
    permission_classes = [IsAuthenticated]
    allowed_roles = {'ADMIN'}

    def dispatch(self, request, *args, **kwargs):
        if getattr(request.user, 'role', 'STUDENT') not in self.allowed_roles:
            return Response({'detail': 'forbidden'}, status=403)
        return super().dispatch(request, *args, **kwargs)

class AdminProductCreateView(RoleRestrictedView, BaseOK):
    allowed_roles = {'ADMIN', 'VIZOR'}
    def post(self, request):
        return self.ok(message='Товар добавлен')
class AdminProductPatchView(RoleRestrictedView, BaseOK):
    allowed_roles = {'ADMIN'}
    def patch(self, request, pk):
        return self.ok(message='Товар обновлён')
class AdminCategoryCreateView(RoleRestrictedView, BaseOK):
    allowed_roles = {'ADMIN'}
    def post(self, request):
        return self.ok()
class AdminCategoryPatchView(RoleRestrictedView, BaseOK):
    allowed_roles = {'ADMIN'}
    def patch(self, request, pk):
        return self.ok()

class ApiLogsPageView(View):
    def get(self, request):
        return HttpResponse('API Logs page')

def soap_endpoint(request):
    if request.GET.get('wsdl') is not None:
        wsdl = """<?xml version='1.0'?><definitions name='TrainingShopService'></definitions>"""
        return HttpResponse(wsdl, content_type='text/xml')
    if 'accessToken' not in request.body.decode('utf-8', errors='ignore'):
        return HttpResponse("<Fault>AuthRequired</Fault>", status=500, content_type='text/xml')
    return HttpResponse('<Response>OK</Response>', content_type='text/xml')

# --- UI pages (Django templates) ---
from django.views.generic import TemplateView
from .models import Product

class HomePageView(TemplateView):
    template_name = "core/home.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        q = (self.request.GET.get("q") or "").strip()
        qs = Product.objects.all().order_by("id")[:40]
        if q:
            qs = Product.objects.filter(name__icontains=q).order_by("id")[:40]
        ctx["products"] = [
            {
                "name": p.title,
                "price": f"{p.price}",
                "image_url": getattr(p, "image_url", None),
                "category": getattr(getattr(p, "category", None), "name", None),
            }
            for p in qs
        ]
        return ctx

class LoginPageView(TemplateView):
    template_name = "core/login.html"

class CartPageView(TemplateView):
    template_name = "core/cart.html"
