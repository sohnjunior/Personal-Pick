from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=64)
    link = models.CharField(max_length=256)
    image = models.CharField(max_length=256)
    image_embedded = models.BinaryField()
    mallName = models.CharField(max_length=256)
    lprice = models.CharField(max_length=64, blank=True)
    hprice = models.CharField(max_length=64, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.title



