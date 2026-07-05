from django.db import models


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255)
    
    # Allows the admin page to display name vs just its id:
    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=255)
    
    # Allows the admin page to display name vs just its id:
    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    # link many-to-one relationship with categories. All products belong to one category.
    category = models.ForeignKey(Category, on_delete=models.CASCADE) # cascade to avoid orphan
    # link many-to-many relationship with tags. one product has many tags, tags reused across products.
    tags = models.ManyToManyField(Tag)
    
    # Allows the admin page to display name vs just its id:
    def __str__(self):
        return self.name