from django.urls import path
from .views import new_sale

urlpatterns = [
    path('new/', new_sale, name='new_sale'),
]
