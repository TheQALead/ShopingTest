from django.contrib import admin
from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from app.core import views

urlpatterns = [
    path('', views.HomePageView.as_view()),
    path('login', views.LoginPageView.as_view()),
    path('cart', views.CartPageView.as_view()),
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/v1/auth/register', views.RegisterView.as_view()),
    path('api/v1/auth/login', views.LoginView.as_view()),
    path('api/v1/auth/refresh', views.RefreshView.as_view()),
    path('api/v1/auth/logout', views.LogoutView.as_view()),
    path('api/v1/auth/verify-email', views.VerifyEmailView.as_view()),
    path('api/v1/auth/password-reset/request', views.PasswordResetRequestView.as_view()),
    path('api/v1/auth/password-reset/confirm', views.PasswordResetConfirmView.as_view()),
    path('api/v1/products', views.ProductListView.as_view()),
    path('api/v1/products/<int:pk>', views.ProductDetailView.as_view()),
    path('api/v1/cart', views.CartView.as_view()),
    path('api/v1/cart/items', views.CartItemsView.as_view()),
    path('api/v1/cart/items/<int:pk>', views.CartItemDetailView.as_view()),
    path('api/v1/cards', views.CardListCreateView.as_view()),
    path('api/v1/cards/<int:pk>', views.CardDeleteView.as_view()),
    path('api/v1/cards/<int:pk>/make-default', views.CardMakeDefaultView.as_view()),
    path('api/v1/orders', views.OrderListCreateView.as_view()),
    path('api/v1/orders/<int:pk>', views.OrderDetailView.as_view()),
    path('api/v1/orders/<int:pk>/pay', views.OrderPayView.as_view()),
    path('api/v1/orders/<int:pk>/pay/3ds-confirm', views.OrderPay3DSConfirmView.as_view()),
    path('api/v1/admin/products', views.AdminProductCreateView.as_view()),
    path('api/v1/admin/products/<int:pk>', views.AdminProductPatchView.as_view()),
    path('api/v1/admin/categories', views.AdminCategoryCreateView.as_view()),
    path('api/v1/admin/categories/<int:pk>', views.AdminCategoryPatchView.as_view()),
    path('soap/v1/TrainingShopService', views.soap_endpoint),
    path('ui/api-logs', views.api_logs_page),
]
