from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search, name='search'),
    path('product/<str:product_id>/', views.product_detail, name='product_detail'),
    path('api/recommend/<str:product_id>/', views.recommend_api, name='recommend_api'),
]