from django.urls import path
from products import views

app_name = "products"

# here, we are implicitly in the /posts path.
urlpatterns = [
    path('', views.product_list, name="product_list"),
]
