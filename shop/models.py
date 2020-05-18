from django.db import models
from pytils.translit import slugify

# Create your models here.


class Category(models.Model):
    title = models.CharField(max_length=30)
    slug = models.SlugField(null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=30)
    slug = models.SlugField(null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(SubCategory, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


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
    quantity = models.IntegerField(null=True)
    image0 = models.ImageField(
        blank=True, upload_to='media/images/', verbose_name='Главное изображение')
    image1 = models.ImageField(
        blank=True, upload_to='media/images/', verbose_name='Доп Изображение 1')
    image2 = models.ImageField(
        blank=True, upload_to='media/images/', verbose_name='Доп Изображение 2')
    image3 = models.ImageField(
        blank=True, upload_to='media/images/', verbose_name='Доп Изображение 3')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
