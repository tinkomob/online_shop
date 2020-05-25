from django.contrib import admin
from django.urls import path,include
from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [
    url(r'^jet/', include('jet.urls', 'jet')),
    path('admin/', admin.site.urls),
    path('', include('shop.urls', namespace='shop')),
    url(r'^profiles/', include('accounts.urls', namespace='accounts')),
    url(r'^cart/', include('shopping_cart.urls', namespace='shopping_cart')),
    url(r'^accounts/', include('allauth.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
