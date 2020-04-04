from django.db import models
from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=64)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=255)
    link = models.CharField(max_length=255)
    image = models.CharField(max_length=255)
    image_embedded = models.BinaryField()
    mallName = models.CharField(max_length=255)
    lprice = models.CharField(max_length=64, blank=True)
    hprice = models.CharField(max_length=64, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    shoppers = models.ManyToManyField(settings.AUTH_USER_MODEL)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title



