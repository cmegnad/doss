from django.urls import path
from . import views
app_name = 'home'
urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.aboutUs, name='aboutus'),
    path('contact/', views.contact, name='contact'),
    path('category/<int:id>/<slug:slug>', views.category_products, name='category_products'),
    path('search/', views.search, name='search'),
    path('search_auto/', views.search_auto, name='search_auto'),
]   