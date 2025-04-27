import pandas as pd
import re
from sqlalchemy import create_engine
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from django.conf import settings

# Danh sách stop words tiếng Việt (có thể mở rộng)
STOP_WORDS_VI = set([
    "và", "của", "là", "có", "trong", "cho", "với", "tại", "bởi", "để",
    "một", "các", "những", "này", "đó", "như", "thì", "được", "tôi", "bạn"
])

class Recommender:
    def __init__(self):
        self.df_sach = None
        self.tfidf_matrix = None
        self.similarity_matrix = None
        self.tfidf = TfidfVectorizer(
            stop_words=list(STOP_WORDS_VI),  # Sử dụng stop words tiếng Việt
            token_pattern=r"(?u)\b\w+\b"      # Chỉ lấy các từ (loại bỏ ký tự đặc biệt)
        )
        self.load_data()

    def clean_text(self, text):
        """Làm sạch văn bản: chuyển về chữ thường, loại bỏ ký tự đặc biệt và URL"""
        if not isinstance(text, str):
            return ""
        # Loại bỏ URL
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        # Loại bỏ ký tự đặc biệt, chỉ giữ chữ và số
        text = re.sub(r'[^\w\s]', '', text)
        # Chuyển về chữ thường và loại bỏ khoảng trắng thừa
        text = text.lower().strip()
        return text

    def load_data(self):
        """Tải dữ liệu từ cơ sở dữ liệu và tiền xử lý"""
        engine = create_engine(
            f"mysql+pymysql://{settings.DATABASES['default']['USER']}:"
            f"{settings.DATABASES['default']['PASSWORD']}@"
            f"{settings.DATABASES['default']['HOST']}:"
            f"{settings.DATABASES['default']['PORT']}/"
            f"{settings.DATABASES['default']['NAME']}"
        )
        self.df_sach = pd.read_sql("SELECT * FROM product", con=engine)

        # Làm sạch các cột văn bản
        for col in ['name', 'category', 'brand', 'description']:
            self.df_sach[col] = self.df_sach[col].apply(self.clean_text)

        # Tạo cột combinedFeatures với trọng số
        self.df_sach["combinedFeatures"] = self.df_sach.apply(self.combine_features, axis=1)

        # Tính TF-IDF và độ tương đồng
        self.tfidf_matrix = self.tfidf.fit_transform(self.df_sach["combinedFeatures"])
        self.similarity_matrix = cosine_similarity(self.tfidf_matrix)

    def combine_features(self, row):
        """Kết hợp các đặc trưng văn bản với trọng số"""
        # Trọng số: name và description quan trọng hơn, nên lặp lại để tăng ảnh hưởng
        return (
            f"{row['name']} {row['name']} "  # Trọng số x2 cho name
            f"{row['category']} "
            f"{row['description']} {row['description']}"  # Trọng số x2 cho description
        )

    def recommend_products(self, product_id, top_n=5, min_rating=3.0):
        """Gợi ý top N sản phẩm tương tự với các tiêu chí lọc"""
        # Lọc sách có sẵn và rating tối thiểu
        available_books = self.df_sach[
            (self.df_sach['inventory_status'] == 'available') &
            (self.df_sach['rating'].astype(float) >= min_rating)
        ]

        if product_id not in self.df_sach['id'].values:
            return []

        # Lấy chỉ số của sản phẩm
        product_index = self.df_sach[self.df_sach['id'] == product_id].index[0]

        # Tính độ tương đồng
        similar_products = list(enumerate(self.similarity_matrix[product_index]))
        sorted_similar_products = sorted(similar_products, key=lambda x: x[1], reverse=True)

        # Lấy top N sản phẩm tương tự
        recommended_ids = []
        for idx, score in sorted_similar_products[1:]:  # Bỏ sản phẩm gốc
            product_id = self.df_sach.iloc[idx]['id']
            # Chỉ thêm sản phẩm có sẵn và đạt yêu cầu rating
            if product_id in available_books['id'].values:
                recommended_ids.append(product_id)
            if len(recommended_ids) >= top_n:
                break

        return recommended_ids

# Sử dụng ví dụ
if __name__ == "__main__":
    recommender = Recommender()
    # Gợi ý dựa trên sách có id '22482263'
    recommendations = recommender.recommend_products('22482263', top_n=3)
    print("Sách được gợi ý:", recommendations)