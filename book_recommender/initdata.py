import os
import django
import pandas as pd

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'book_recommender.settings')  # thay 'your_project_name' bằng tên project thật
django.setup()

from books.models import Product  # thay 'your_app_name' bằng tên app thật

def load_data_from_excel(file_path):
    df = pd.read_excel(file_path)
    
# Nhập dữ liệu mới
    for index, row in df.iterrows():
        Product.objects.update_or_create(
            id=row['id'],
            defaults={
                'name': row.get('name'),
                'price': str(row.get('price')) if pd.notnull(row.get('price')) else None,
                'original_price': str(row.get('original_price')) if pd.notnull(row.get('original_price')) else None,
                'discount': str(row.get('discount')) if pd.notnull(row.get('discount')) else None,
                'discount_rate': str(row.get('discount_rate')) if pd.notnull(row.get('discount_rate')) else None,
                'short_description': row.get('short_description'),
                'description': row.get('description'),
                'thumbnail_url': row.get('thumbnail_url'),
                'images_url': row.get('images_url'),
                'rating': str(row.get('rating_average')) if pd.notnull(row.get('rating_average')) else None,
                'review_count': str(row.get('review_count')) if pd.notnull(row.get('review_count')) else None,
                'inventory_status': row.get('inventory_status'),
                'inventory_type': row.get('inventory_type'),
                'sold_quantity': str(row.get('all_time_quantity_sold')) if pd.notnull(row.get('all_time_quantity_sold')) else None,
                'current_seller_name': row.get('current_seller_name'),
                'category': row.get('categories_name'),
                'brand': row.get('publisher_vn'),
                'book_cover': row.get('book_cover'),
                'number_of_page': row.get('number_of_page'),
                'manufacturer': row.get('manufacturer')
            }
        )

    print(f"✅ Đã import xong {len(df)} sản phẩm vào database!")

if __name__ == "__main__":
    excel_file_path = 'D:/New folder (2)/BOOKRECOMMEND/tikicrawl/data/products_data.xlsx'
    load_data_from_excel(excel_file_path)


