from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name='index'),
    path("cart", views.cart, name='cart'),
    path("about", views.about, name='about'),
    path("contact", views.contact, name='contact'),
    path("electronics", views.electronics, name='electronics'),
    path("cloths", views.cloths, name='cloths'),
    path("shoes", views.shoes, name='shoes'),
    path("product/<int:myid>/", views.prodView, name="prodView"),
    path("cart", views.cart, name="cart"),
    path("search", views.search, name="search"),
    path("checkout", views.checkout, name="checkout"),
    path("signup", views.handleSignup, name="handleSignup"),
    path("login", views.handleLogin, name="handleLogin"),
    path("logout", views.handleLogout, name="handleLogout"),
]
