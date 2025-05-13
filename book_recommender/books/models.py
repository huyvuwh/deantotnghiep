from django.db import models

# Create your models here.
from django.db import models

from django.db import models

class Product(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=1024, blank=True, null=True)
    price = models.CharField(max_length=255, blank=True, null=True)
    original_price = models.CharField(max_length=255, blank=True, null=True)
    discount = models.CharField(max_length=255, blank=True, null=True)
    discount_rate = models.CharField(max_length=255, blank=True, null=True)  # Thêm trường discount_rate
    short_description = models.TextField(blank=True, null=True)  # Thêm trường short_description
    description = models.TextField(blank=True, null=True)
    thumbnail_url = models.CharField(max_length=255, blank=True, null=True)  # Đổi tên image_url thành thumbnail_url
    images_url = models.TextField(blank=True, null=True)  # Thêm trường images_url (lưu nhiều URL)
    rating = models.FloatField(max_length=255, blank=True, null=True)  # Đổi tên rating_average thành rating
    review_count = models.CharField(max_length=255, blank=True, null=True)
    inventory_status = models.CharField(max_length=255, blank=True, null=True)
    inventory_type = models.CharField(max_length=255, blank=True, null=True)  # Thêm trường inventory_type
    sold_quantity = models.CharField(max_length=255, blank=True, null=True)  # Đổi tên all_time_quantity_sold thành sold_quantity
    current_seller_name = models.CharField(max_length=255, blank=True, null=True)  # Thêm trường current_seller_name
    category = models.CharField(max_length=255, blank=True, null=True)  # Đổi tên categories_name thành category
    brand = models.CharField(max_length=255, blank=True, null=True)  # Đổi tên publisher_vn thành brand
    book_cover = models.CharField(max_length=255, blank=True, null=True)
    number_of_page = models.CharField(max_length=255, blank=True, null=True)
    manufacturer = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'product'