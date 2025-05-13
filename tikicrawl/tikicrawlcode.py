import os
import csv
import requests
import numpy as np

# URL API của Tiki
sach_page_url = "https://tiki.vn/api/v2/products"
product_id_file = "data/product_id.txt"


# Hàm crawl danh sách sản phẩm từ API
def crawl_product_id():
    product_list = []

    for i in range(1, 51):  # Lặp từ trang 1 đến 50
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Referer": "https://tiki.vn/",
        }
        params = {
            "limit": 40,
            "include": "advertisement",
            "aggregations": 2,
            "trackity_id": "36a2dfea-fc03-628a-4958-5b095bc0d894",
            "q": "sách",
            "page": i,
        }

        response = requests.get(sach_page_url, headers=headers, params=params)

        if response.status_code != 200:
            print(f"Lỗi API trang {i}: {response.status_code}")
            continue

        try:
            y = response.json()
            if "data" not in y or not isinstance(y["data"], list):
                print(f"Dữ liệu API không hợp lệ ở trang {i}")
                continue

            print(f"Trang {i}: {len(y['data'])} sản phẩm")
            for item in y["data"]:
                if "id" in item:
                    product_list.append(item["id"])
        except Exception as e:
            print(f"Lỗi JSON ở trang {i}: {e}")

    product_list = np.array(product_list, dtype=int)
    print("Danh sách product_id:", product_list)
    print("Tổng số sản phẩm:", len(product_list))
    return product_list


# Hàm ghi danh sách ID sản phẩm vào file
def write_csv_file(data, filename, mode="w"):
    folder = os.path.dirname(filename)
    if folder and not os.path.exists(folder):
        os.makedirs(folder)

    with open(filename, mode, newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["product_id"])
        for item in data:
            writer.writerow([item])


# Chạy chương trình
if __name__ == "__main__":
    product_list = crawl_product_id()
    write_csv_file(product_list, product_id_file, mode="w")
    print("✅ Dữ liệu đã được lưu vào", product_id_file)


import requests
import pandas as pd
import time


# Đọc danh sách ID sản phẩm từ file
def read_product_ids(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return [line.strip() for line in file.readlines() if line.strip()]


import requests
import pandas as pd
import time
import re
import os


# Hàm loại bỏ thẻ HTML
def clean_html(text):
    if text:
        clean_text = re.sub(r"<[^>]+>", " ", text)
        clean_text = re.sub(r"\s+", " ", clean_text).strip()
        return clean_text
    return ""


# Đọc danh sách ID sản phẩm từ file
def read_product_ids(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            lines = [line.strip() for line in file.readlines() if line.strip()]
            return lines[1:]  # Bỏ dòng tiêu đề "product_id"
    except FileNotFoundError:
        print(f"File {file_path} không tồn tại")
        return []


# Gọi API lấy thông tin sản phẩm
def get_product_data(product_id):
    url = f"https://tiki.vn/api/v2/products/{product_id}?platform=web&version=3"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://tiki.vn/",
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Lỗi API cho product_id {product_id}: {response.status_code}")
            return None

        data = response.json()

        # Trích xuất specifications
        specs = {}
        for spec in data.get("specifications", []):
            for attr in spec.get("attributes", []):
                specs[attr["code"]] = attr["value"]

        # Trích xuất images_url
        images_url = [img["base_url"] for img in data.get("images", [])]

        return {
            "id": data.get("id", ""),
            "name": data.get("name", ""),
            "price": data.get("price", ""),
            "original_price": data.get("list_price", ""),
            "discount": data.get("discount", ""),
            "discount_rate": data.get("discount_rate", ""),
            "short_description": clean_html(data.get("short_description", "")),
            "description": clean_html(data.get("description", "")),
            "thumbnail_url": data.get("thumbnail_url", ""),
            "images_url": (
                ";".join(images_url) if images_url else ""
            ),  # Gộp nhiều URL bằng dấu ;
            "rating_average": data.get("rating_average", ""),
            "review_count": data.get("review_count", ""),
            "inventory_status": data.get("inventory_status", ""),
            "inventory_type": data.get("inventory_type", ""),
            "all_time_quantity_sold": data.get("all_time_quantity_sold", ""),
            "current_seller_name": data.get("current_seller", {}).get("name", ""),
            "categories_name": (
                data.get("breadcrumbs", [])[-2].get("name", "")
                if data.get("categories", {}).get("name")
                in ["Root", "Product Line Root"]
                and len(data.get("breadcrumbs", [])) >= 2
                else data.get("categories", {}).get("name", "")
            ),
            "publisher_vn": specs.get("publisher_vn", ""),
            "book_cover": specs.get("book_cover", ""),
            "number_of_page": specs.get("number_of_page", ""),
            "manufacturer": specs.get("manufacturer", ""),
        }
    except Exception as e:
        print(f"Lỗi khi xử lý product_id {product_id}: {e}")
        return None


# Lưu dữ liệu vào file Excel
def save_to_excel(products, file_name="data/products_data.xlsx"):
    folder = os.path.dirname(file_name)
    if folder and not os.path.exists(folder):
        os.makedirs(folder)

    df = pd.DataFrame(products)
    df.to_excel(file_name, index=False, engine="openpyxl")
    print(f"✅ Dữ liệu đã được lưu vào '{file_name}'.")


# Chạy chương trình chính
def main():
    product_ids = read_product_ids("data/product_id.txt")
    all_products = []

    for idx, product_id in enumerate(product_ids, 1):
        print(f"Đang lấy dữ liệu sản phẩm {idx}/{len(product_ids)}: {product_id}")
        product_data = get_product_data(product_id)
        if product_data:
            all_products.append(product_data)
        time.sleep(1)  # Tránh bị chặn API

    if all_products:
        save_to_excel(all_products)
        print("✅ Hoàn thành! Dữ liệu đã được lưu vào file Excel.")
    else:
        print("⚠️ Không có dữ liệu nào được thu thập.")


if __name__ == "__main__":
    main()
