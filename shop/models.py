from django.db import models
from pytils.translit import slugify
from datetime import datetime
import statistics
# from accounts.models import Profile
# Create your models here.


class Category(models.Model):
    title = models.CharField(max_length=30)
    slug = models.SlugField(null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
    class Meta:
        verbose_name = 'Категории'
        verbose_name_plural = 'Категории'


class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=30)
    slug = models.SlugField(null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(SubCategory, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
    class Meta:
        verbose_name = 'Подкатегории'
        verbose_name_plural = 'Подкатегории'


class Product(models.Model):
    subCategory = models.ForeignKey(
        SubCategory, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=100)
    slug = models.SlugField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    articul = models.CharField(max_length=16, default="00000000")
    size = models.CharField(max_length=45, null=True, blank=True)
    material = models.CharField(max_length=30, null=True, blank=True)
    price = models.IntegerField()
    date_added = models.DateTimeField(default=datetime.now)
    rating = models.FloatField(default=0)
    image0 = models.ImageField(
        blank=True, upload_to='images/', verbose_name='Главное изображение')
    image1 = models.ImageField(
        blank=True, upload_to='images/', verbose_name='Доп Изображение 1')
    image2 = models.ImageField(
        blank=True, upload_to='images/', verbose_name='Доп Изображение 2')
    image3 = models.ImageField(
        blank=True, upload_to='images/', verbose_name='Доп Изображение 3')
    def getRevsRating(self):
        rates = self.review_set.filter(product_id=self.id)
        avg_rating = []
        for item in rates:
            avg_rating.append(item.rate)
        return statistics.mean(avg_rating)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        self.rating = self.getRevsRating()
        super(Product, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    class Meta:
        verbose_name = 'Товары'
        verbose_name_plural = 'Товары'
class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    author = models.ForeignKey('accounts.Profile', on_delete=models.SET_NULL, null=True)
    rate = models.FloatField(default=0)
    text = models.TextField()

    def __str__(self):
        return self.author.user.username + str(self.product.id)
    class Meta:
        verbose_name = 'Отзывы'
        verbose_name_plural = 'Отзывы'