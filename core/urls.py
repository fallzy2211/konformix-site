from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("solutions/", views.products, name="products"),
    path("solutions/<slug:key>/", views.product_detail, name="product_detail"),
    path("a-propos/", views.about, name="about"),
    path("ressources/", views.resources, name="resources"),
    path("ressources/<slug:slug>/", views.article_detail, name="article_detail"),
    path("contact/", views.contact, name="contact"),
    path("mentions-legales/", views.legal, name="legal"),
    path("donnees-personnelles/", views.privacy, name="privacy"),
]
