from django.urls import path
from products import views

app_name = "products"

# here, we are implicitly in the /products path.
urlpatterns = [
    path('', views.product_list, name="product_list"),
    path('api/', views.ProductListAPIView.as_view(), name="product_list_api"),
    path('api/<int:pk>/', views.ProductDetailsAPIView.as_view(), name="product_details_api"),
]
