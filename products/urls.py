from django.urls import path
from products import views

# here, we are implicitly in the /posts path.
urlpatterns = [
    path('', views.product_list),
]
