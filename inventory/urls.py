from django.urls import path
from .views import inventory_home, product_search, product_page, add_item,  api_get_variants
from . import views

app_name = 'inventory'

urlpatterns = [
    path('', inventory_home, name='inventory_home'),  # Default inventory route
    path('<int:product_id>/', views.product_page, name='product_page'),
    #path('search/', product_search, name='search'),
    #path('<int:product_id>/', product_page, name='product'),
    path('add-item/', add_item, name='add_item'),
    path('api/variants/<int:product_id>/', api_get_variants, name='api_get_variants'),
    path('search/', views.search_view, name='search'),
]

