from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('addtoshopcart/<int:id>',views.addToShopCart, name="addtoshopcart"),
    # path('shopcart/', views.shopcart, name="shopcart")
    path('deletefromcart/<int:id>',views.deletefromcart, name="deletefromcart"),
    path('orderdetail/',views.orderdetail, name="orderdetail"),
]