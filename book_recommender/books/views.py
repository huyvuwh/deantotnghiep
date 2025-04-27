from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import JsonResponse
from .models import Product
from .recommender import Recommender
from django.db.models import Q

from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q, F
from .models import Product
from .recommender import Recommender

from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q, F
from .models import Product
from .recommender import Recommender

def index(request):
    # Lấy tất cả sản phẩm
    products = Product.objects.all()

    # Lấy danh sách thể loại duy nhất
    categories = Product.objects.values_list('category', flat=True).distinct()

    # Bộ lọc theo thể loại
    category = request.GET.get('category', '')
    if category:
        products = products.filter(category=category)

    # Bộ lọc theo giá
    price_order = request.GET.get('price_order', '')
    if price_order == 'asc':
        products = products.order_by('price')
    elif price_order == 'desc':
        products = products.order_by('-price')

    # Bộ lọc theo đánh giá
    rating_order = request.GET.get('rating_order', '')
    if rating_order == 'asc':
        products = products.order_by('rating')
    elif rating_order == 'desc':
        products = products.order_by('-rating')

    # Phân trang
    paginator = Paginator(products, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'index.html', {
        'page_obj': page_obj,
        'categories': categories
    })

def search(request):
    query = request.GET.get('q', '')
    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) |
            Q(category__icontains=query) |
            Q(description__icontains=query)
        )
    else:
        products = Product.objects.all()

    # Bộ lọc theo thể loại
    category = request.GET.get('category', '')
    if category:
        products = products.filter(category=category)

    # Bộ lọc theo giá
    price_order = request.GET.get('price_order', '')
    if price_order == 'asc':
        products = products.order_by('price')
    elif price_order == 'desc':
        products = products.order_by('-price')

    # Bộ lọc theo đánh giá
    rating_order = request.GET.get('rating_order', '')
    if rating_order == 'asc':
        products = products.order_by('rating')
    elif rating_order == 'desc':
        products = products.order_by('-rating')

    # Phân trang
    paginator = Paginator(products, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'search.html', {
        'page_obj': page_obj,
        'query': query,
        'categories': Product.objects.values_list('category', flat=True).distinct()
    })

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    recommender = Recommender()
    recommended_ids = recommender.recommend_products(product_id)
    # Sắp xếp recommended_products theo id để tránh cảnh báo
    recommended_products = Product.objects.filter(id__in=recommended_ids).order_by('id')
    
    # Phân trang cho sách gợi ý
    paginator = Paginator(recommended_products, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'product_detail.html', {
        'product': product,
        'page_obj': page_obj
    })

def recommend_api(request, product_id):
    recommender = Recommender()
    recommended_ids = recommender.recommend_products(product_id)
    recommended_products = Product.objects.filter(id__in=recommended_ids).values(
        'id', 'name', 'price', 'image_url'
    )
    return JsonResponse({'recommended_products': list(recommended_products)})