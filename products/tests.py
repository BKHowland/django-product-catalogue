from django.test import TestCase
from django.urls import reverse

from .models import Category, Tag, Product


class ProductListViewTests(TestCase):
    """Test Cases for the products list view functionality."""

    def setUp(self):
        """Creates the test categories, tags, and products. Runs before every test! Reused ARRANGE step."""
        # Two categories so we can check that category filtering works
        self.electronics = Category.objects.create(name="Electronics")
        self.tools = Category.objects.create(name="Tools")

        # Two tags so that we can test OR logic on multiple
        self.tag_sale = Tag.objects.create(name="On Sale")
        self.tag_new = Tag.objects.create(name="New Arrival")

        # Create test products
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
        # hammer has no tags intentionally to test products with zero tags still show up

        # get the full url for for the products list page
        self.url = reverse("products:product_list")

    def test_no_filters_returns_all_products(self):
        """Test that every product is listed with no filters applied"""
        # ACT
        response = self.client.get(self.url)
        # ASSERT
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["products"]), 3)

    def test_search_matches_name(self):
        """Test that searching queries product names"""
        # ACT
        response = self.client.get(self.url, {"search": "Drill"})
        products = list(response.context["products"])
        # ASSERT
        self.assertEqual(products, [self.drill])

    def test_search_matches_description(self):
        """Test that search also match against description"""
        # ACT
        response = self.client.get(self.url, {"search": "LED"})
        products = list(response.context["products"])
        # ASSERT
        self.assertEqual(products, [self.lamp])

    def test_search_is_case_insensitive(self):
        """Ensure searching is not case sensitive"""
        # ACT
        response = self.client.get(self.url, {"search": "hammer"})
        products = list(response.context["products"])
        # ASSERT
        self.assertEqual(products, [self.hammer])

    def test_filter_by_category(self):
        """Test basic category filtering is working"""
        # ACT
        response = self.client.get(self.url, {"category": self.tools.id})
        products = list(response.context["products"])
        # ASSERT
        self.assertEqual(products, [self.hammer, self.drill])

    def test_filter_by_single_tag(self):
        """Test basic tag filtering is working"""
        # ACT
        response = self.client.get(self.url, {"tags": [self.tag_sale.id]})
        products = list(response.context["products"])
        # ASSERT
        self.assertEqual(products, [self.lamp])

    def test_filter_by_multiple_tags_uses_or_logic(self):
        """Test that selecting two tags should return products matching EITHER tag"""
        # ACT
        response = self.client.get(
            self.url, {"tags": [self.tag_sale.id, self.tag_new.id]}
        )
        products = list(response.context["products"])
        # ASSERT
        self.assertEqual(products, [self.drill, self.lamp])

    def test_combined_search_and_category_filter(self):
        """Test Search and category filters can be combined"""
        # ACT
        response = self.client.get(
            self.url, {"search": "hammer", "category": self.tools.id}
        )
        products = list(response.context["products"])
        # ASSERT
        self.assertEqual(products, [self.hammer])

    def test_combined_filters_with_no_matches(self):
        """Test that searches that match nothing return an empty list."""
        # ACT
        response = self.client.get(
            self.url, {"search": "Lamp", "category": self.tools.id}
        )
        # ASSERT
        self.assertEqual(list(response.context["products"]), [])

    def test_tag_filter_does_not_duplicate_products(self):
        """Test that a product matching multiple selected tags only appears once in the results"""
        # ARRANGE (plus the setup function)
        self.lamp.tags.add(self.tag_new)  # add second tag to lamp
        # ACT
        response = self.client.get(
            self.url, {"tags": [self.tag_sale.id, self.tag_new.id]}
        )
        products = list(response.context["products"])
        # ASSERT
        self.assertEqual(products.count(self.lamp), 1)
