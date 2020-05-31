from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.core.validators import RegexValidator

from shop.models import Product


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ebooks = models.ManyToManyField(Product, blank=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Формат: '+999999999'.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True) # validators should be a list
    delivery_address = models.CharField(blank=True, max_length=70)
    
    def __str__(self):
        return self.user.username
    class Meta:
        verbose_name = 'Профили'
        verbose_name_plural = 'Профили'

def post_save_profile_create(sender, instance, created, *args, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)

post_save.connect(post_save_profile_create, sender=settings.AUTH_USER_MODEL)