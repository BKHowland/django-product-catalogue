from django.shortcuts import render
from .models import Product, Category, Tag
from django.db.models import Q
from django.views.decorators.http import require_GET
from rest_framework.generics import ListAPIView, RetrieveAPIView
from .serializers import ProductSerializer, ProductSearchQuerySerializer
from rest_framework import status
from django.http import HttpResponseBadRequest

# Create your views here.
@require_GET
def product_list(request):
    """
    Handles requests to the product list page.
    Displays all products that match all applied user-configurable filters.
    Users can filter by searching for name/description matches, category, or associated tags.
    """
    # get all product objects using the Product model.
    # since we know we need categories and tags for each, telling django early to join reduces the query count.
    products = (
        Product.objects.all()
        .select_related("category")
        .prefetch_related("tags")
        .order_by("name")
    )
    categories = Category.objects.all()
    tags = Tag.objects.all()

    # check param values for correctness
    query_data = {
        "search": request.GET.get("search", ""),
        "category": request.GET.get("category") or None,
        "tags": request.GET.getlist("tags"),
    }
    serializer = ProductSearchQuerySerializer(data=query_data)
    if not serializer.is_valid():
        return HttpResponseBadRequest(
            f"Bad request parameters: {serializer.errors}"
        )
    filters = serializer.validated_data
    
    # get the search query:
    search_query = filters.get("search", "")
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | Q(description__icontains=search_query)
        )

    category_id = filters.get("category")
    if category_id:
        # chain across relationships, from product to category to its name.
        products = products.filter(category=category_id)

    tag_ids = filters.get("tags", [])
    if tag_ids:
        # we want to get all products where the tag id is in the tag ids requested.
        products = products.filter(tags__id__in=tag_ids).distinct()

    # params are the request, the template file, plus the catalogue data as a python dict.
    return render(
        request,
        "products/product_list.html",
        {
            "products": products,
            "categories": categories,
            "tags": tags,
            "search_query": search_query or "",  # avoid None appearing in search box
            "selected_category": int(category_id) if category_id else None,
            "selected_tags": list(map(int, tag_ids)),
        },
    )


class ProductListAPIView(ListAPIView):
    # list all products in JSON format
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
class ProductDetailsAPIView(RetrieveAPIView):
    # get info about specific product
    queryset = Product.objects.all() # specify full pool to search in, dont filter manually. 
    serializer_class = ProductSerializer