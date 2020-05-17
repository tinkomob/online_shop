from django.contrib import admin
from django.views.generic import TemplateView
from django.urls import path,include
from . import views
app_name = 'shop'
urlpatterns = [
    path('', views.index, name="home"),
    path('catalog/<slug:category>', views.category_view, name='category'),
    path('catalog/<category>/<slug:subCategory>', views.subCategory_view, name='subCategory'),
    path('catalog/<category>/<subCategory>/<slug:product>', views.product_view, name='product'),
    path('search/', views.search_view, name='search'),
    path('help/about', TemplateView.as_view(template_name='main/about.html'), name='about'),
    path('help/delivery', TemplateView.as_view(template_name='main/delivery.html'), name='delivery'),
    path('help/payment', TemplateView.as_view(template_name='main/payment.html'), name='payment'),
    path('help/contacts', TemplateView.as_view(template_name='main/contacts.html'), name='contacts'),
]

