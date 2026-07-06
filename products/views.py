from django.shortcuts import render
from .models import Product, Category, Tag
from django.db.models import Q


# Create your views here.
def product_list(request):
    # get all product objects using the Product model.
    products = Product.objects.all().order_by("name")
    categories = Category.objects.all()
    tags = Tag.objects.all()

    # get the search query:
    search_query = request.GET.get("search")
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | Q(description__icontains=search_query)
        )

    category_id = request.GET.get("category")
    if category_id:
        # chain across relationships, from product to category to its name.
        products = products.filter(category=category_id)

    tag_ids = request.GET.getlist("tags")
    if tag_ids:
        # we want to get all products where the tag id is in the tag ids requested.
        products = products.filter(tags__id__in=tag_ids).distinct()
    # params are the request, the template file, plus the Product data as a python dict.
    return render(
        request,
        "products/product_list.html",
        {
            "products": products,
            "categories": categories,
            "tags": tags,
            "search_query": search_query,
            "selected_category": category_id,
            "selected_tags": list(map(int, tag_ids)),
        },
    )
