from django.shortcuts import render
from .models import Product, Category
from django.db.models import Q

# Create your views here.
def product_list(request):
    # get all product objects using the Product model. 
    products = Product.objects.all().order_by('name')
    categories = Category.objects.all()
    
    # get the search query:
    search_term = request.GET.get("search")
    if search_term:
        products = products.filter(Q(name__icontains=search_term) | Q(description__icontains=search_term))
        
    category_id = request.GET.get("category")
    if category_id:
        # chain across relationships, from product to category to its name. 
        products = products.filter(category=category_id)
    
    tags = request.GET.get("tags")
    if tags:
        pass
    # params are the request, the template file, plus the Product data as a python dict.
    return render(request, 'products/product_list.html', {'products' : products, 'categories' : categories})