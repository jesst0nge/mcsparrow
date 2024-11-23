from django.urls import path
from .views import new_sale
from . import views

app_name = 'sales'  # Make sure this matches the app's namespace if it's not global

urlpatterns = [
    path('new/', new_sale, name='new_sale'),
    path('search/', views.search_view, name='search'),  # Ensure you have this
]