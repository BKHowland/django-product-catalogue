from django.contrib import admin
from . import models


# since products have many relevant attributes, lets customize its view.
class ProductAdmin(admin.ModelAdmin):
    """
    Subclasses ModelAdmin to display product description and category,
    show filters for category and tags, and display a search bar for name/description.
    Improves usability and matches /products page functionality.
    """

    list_display = ("name", "description", "category")
    list_filter = ("category", "tags")
    search_fields = ("name", "description")


# Register your models here.
admin.site.register(models.Category)
admin.site.register(models.Tag)
admin.site.register(models.Product, ProductAdmin)
