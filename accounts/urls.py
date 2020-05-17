from django.conf.urls import url

from .views import my_profile

app_name = 'accounts'

urlpatterns = [
	url('profile/', my_profile, name='my_profile')
]