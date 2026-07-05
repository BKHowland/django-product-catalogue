from django.shortcuts import render
from .models import Product

# Create your views here.
def product_list(request):
    # get all product objects using the Product model. 
    products = Product.objects.all().order_by('name')
    
    # get the search query:
    search_term = request.GET.get("search")
    
    products = products.filter(name__icontains=search_term)
    # params are the request, the template file, plus the Product data as a python dict.
    return render(request, 'products/product_list.html', {'products' : products})