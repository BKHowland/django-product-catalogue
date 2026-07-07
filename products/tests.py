from django.test import TestCase
from django.urls import reverse

from .models import Category, Tag, Product


class TestProductList(TestCase):
    """Some sample tests for the products list view to ensure it works properly"""

    def setUp(self):
        """Creates categories, tags, and products. Runs before every test as a reused ARRANGE step"""
        # catagories
        self.electronics = Category.objects.create(name="Electronics")
        self.tools = Category.objects.create(name="Tools")

        # tags
        self.tag_sale = Tag.objects.create(name="On Sale")
        self.tag_new = Tag.objects.create(name="New Arrival")

        # products
        self.lamp = Product.objects.create(
            name="Desk Lamp",
            description="A bright LED lamp for your desk.",
            category=self.electronics,
        )
        self.lamp.tags.add(self.tag_sale)

        self.drill = Product.objects.create(
            name="Cordless Drill",
            description="Powerful drill for home projects.",
            category=self.tools,
        )
        self.drill.tags.add(self.tag_new)

        self.hammer = Product.objects.create(
            name="Claw Hammer",
            description="Its a hammer. What more do you want?",
            category=self.tools,
        )
        # no tag set

        # get the full url for for the products list page
        self.url = reverse("products:product_list")

    def test_all_products_returned_when_no_filter(self):
        """Test that every product is listed with no filters applied"""
        # ACT
        response = self.client.get(self.url)
        # ASSERT - we should see all 3 products
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["products"]), 3)

    def test_search_by_name(self):
        """Test that searching works on the product names"""
        # ACT
        response = self.client.get(self.url, {"search": "Drill"})
        products = list(response.context["products"])
        # ASSERT - we should only see drill since we searched for it
        self.assertEqual(products, [self.drill])

    def test_search_by_description(self):
        """Test that search also match against description"""
        # ACT
        response = self.client.get(self.url, {"search": "LED"})
        products = list(response.context["products"])
        # ASSERT - We should see only lamp since it is the only with LED tag
        self.assertEqual(products, [self.lamp])

    def test_case_insensitive_search(self):
        """Ensure searching is not case sensitive"""
        # ACT
        response = self.client.get(self.url, {"search": "hammer"})
        products = list(response.context["products"])
        # ASSERT - Should be only Hammer
        self.assertEqual(products, [self.hammer])

    def test_filter_by_category(self):
        """Test basic category filtering is working"""
        # ACT
        response = self.client.get(self.url, {"category": self.tools.id})
        products = list(response.context["products"])
        # ASSERT - The tools category contains hammer and drill, exclude lamp
        self.assertEqual(products, [self.hammer, self.drill])

    def test_filter_by_single_tag(self):
        """Test basic tag filtering is working"""
        # ACT
        response = self.client.get(self.url, {"tags": [self.tag_sale.id]})
        products = list(response.context["products"])
        # ASSERT - the only item on sale is the lamp
        self.assertEqual(products, [self.lamp])

    def test_filter_by_multiple_tags(self):
        """Test that selecting two tags should return products matching EITHER tag"""
        # ACT
        response = self.client.get(
            self.url, {"tags": [self.tag_sale.id, self.tag_new.id]}
        )
        products = list(response.context["products"])
        # ASSERT - new tag plus sale tag = items in either one.
        self.assertEqual(products, [self.drill, self.lamp])

    def test_combined_search_and_category_filter(self):
        """Test Search and category filters can be combined"""
        # ACT
        response = self.client.get(
            self.url, {"search": "hammer", "category": self.tools.id}
        )
        products = list(response.context["products"])
        # ASSERT - search for hammer within tools, returns hammer
        self.assertEqual(products, [self.hammer])

    def test_no_matches(self):
        """Test that searches that match nothing return an empty list."""
        # ACT
        response = self.client.get(
            self.url, {"search": "Lamp", "category": self.tools.id}
        )
        # ASSERT - there is no lamp related tool, so no results
        self.assertEqual(list(response.context["products"]), [])

    def test_tag_filter_does_not_show_duplicate_products(self):
        """Test that a product matching multiple selected tags only appears once in the results"""
        # ARRANGE (plus the setup function)
        self.lamp.tags.add(self.tag_new)  # add second tag to lamp
        # ACT
        response = self.client.get(
            self.url, {"tags": [self.tag_sale.id, self.tag_new.id]}
        )
        products = list(response.context["products"])
        # ASSERT - the lamp is sale and new, but should appear only once!
        self.assertEqual(products.count(self.lamp), 1)
