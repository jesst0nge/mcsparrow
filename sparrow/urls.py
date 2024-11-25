from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home', TemplateView.as_view(template_name='home.html'), name='home'),
    path('', include('store.urls')),
    path('inventory/', include('inventory.urls'), name='inventory'),
    path('sales/', include('sales.urls'), name='sales'),
    path('cart/', include('cart.urls'), name='cart'),
]
