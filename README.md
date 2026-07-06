# Product Catalogue

A Django project that models a product catalogue. It includes products, categories, and tags, with a front-end page for searching and filtering the catalogue.

## Features

- A single-page product list view (`/products/`) that supports:
  - Text search across product name and description
  - Filtering by category
  - Filtering by one or more tags
  - Any combination of the above at the same time
  - resetting all applied filters
- **Products** are stored with a name, description, category, and associated tags.
- **Category** (one per product) and **Tag** (many-to-many, reusable across products) models.
- Django admin page can be used to populate sample data, and has been adjusted to match products page behaviour.


## Tech Stack

- Python 3.11.9
- Django 5.2.15
- SQLite (default Django database)

## Setup

1. **Clone the repo and create a virtual environment**

   ```bash
   git clone <this-repo-url>
   cd django-product-catalogue
   python -m venv .venv
   .\venv\Scripts\activate
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run migrations**

   ```bash
   python manage.py migrate
   ```

4. **Load the sample data**

   The database itself isn't committed to the repo (bad practice to commit), but a fixture with the sample categories, tags, and products is included so you don't have to re-enter data by hand:

   ```bash
   python manage.py loaddata sample_data.json
   ```

   This loads the same data used to test the search/filter functionality locally (created via the Django admin).

5. **(Optional) Create a superuser to browse the admin**

   ```bash
   python manage.py createsuperuser
   ```

6. **Run the dev server**

   ```bash
   python manage.py runserver
   ```

   - Product list / search / filter page: http://127.0.0.1:8000/products/
   - Admin: http://127.0.0.1:8000/admin/

## Regenerating the Sample Data Fixture

If you add or edit data through the admin and want to refresh the fixture
(e.g. after adding more products), run:

```bash
python manage.py dumpdata products --indent 2 > products/fixtures/sample_data.json
```

## Assumptions & Notes

In the making of this project, I made several assumptions based on ambiguity in the instructions and what would make sense for real-world use cases. These are listed below.

- A product belongs to **exactly one** category (using foreign keys), while tags are many-to-many relationship given they can be reused across products and one product may have multiple associated tags.
- Search matches based on a case-insensitive partial match against both the product **name** and **description**. 
    - While the instructions only mention description, I assumed this was not the same as a product's name, and searching should work on both. 
- Selecting multiple tags returns products that have **at least one** of the selected tags (OR logic), not products that have all of them. This felt like the more natural interpretation of "filter by tags" for a commercial catalogue page.
- Styling was intentionally kept minimal per the assignment instructions, which state that design/styling are not the focus of the evaluation.
- Tests were not included in the repo as they are not the focus of the assignment, but features were tested thoroughly.

## AI Usage Disclosure

In compliance with the assignment instructions, AI was used to help with:
- Drafting the initial revision of this readme file
- Acting as a supplement to regular web searches for questions 
    - Guiding learning on best practices
    - Explaining Django features
    - Debugging support
- Assisting in generating sample data for products in the relevant domain
- Pointing out possible optimizations
- CSS adjustments

**All code was written, modified, and reviewed by hand.**
