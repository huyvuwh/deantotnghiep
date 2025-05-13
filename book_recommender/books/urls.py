from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search, name='search'),
    path('product/<str:product_id>/', views.product_detail, name='product_detail'),
    path('api/recommend/<str:product_id>/', views.recommend_api, name='recommend_api'),
    path('cart/', views.cart_view, name='cart'),
    path('thank-you/', views.thank_you, name='thank_you'),
    path('favorites/', views.favorites_view, name='favorites'),
    path('about/', views.about, name='about'),
]