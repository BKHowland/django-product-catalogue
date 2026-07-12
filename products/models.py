from django.db import models


# Create your models here.
class Category(models.Model):
    """
    Represents product categories. Each product belongs to exactly one category.
    """
    
    name = models.CharField(max_length=255)
    
    class Meta():
        # Correct default plural spelling
        verbose_name_plural = "Categories"
    
    # Allows the admin page to display name vs just its id:
    def __str__(self):
        return self.name


class Tag(models.Model):
    """
    Represents product 'tags' or themes. Each product may have multiple associated tags,
    and tags may be reused for any number of products.
    """
    
    name = models.CharField(max_length=255)
    
    # Allows the admin page to display name vs just its id:
    def __str__(self):
        return self.name


class Product(models.Model):
    """
    Represents a physical product in the catalogue. 
    Each product has a name, description, category, and associated tags.
    """
    
    name = models.CharField(max_length=255)
    description = models.TextField()
    # link many-to-one relationship with categories. All products belong to one category.
    category = models.ForeignKey(Category, on_delete=models.CASCADE) # cascade to avoid orphan
    # link many-to-many relationship with tags. one product has many tags, tags reused across products.
    tags = models.ManyToManyField(Tag, blank=True)
    
    # Allows the admin page to display name vs just its id:
    def __str__(self):
        return self.name