from django.db import models


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255)


class Tag(models.Model):
    name = models.CharField(max_length=255)


class Product(models.Model):
    # TODO: Do we want just a description, both it and a name, or does name count as description?
    description = models.TextField()
    # link many-to-one relationship with categories. All products belong to one category.
    category = models.ForeignKey(Category, on_delete=models.CASCADE) # cascade to avoid orphan
    # link many-to-many relationship with tags. one product has many tags, tags reused across products.
    tags = models.ManyToManyField(Tag)