from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.shortcuts import render
from django.core.paginator import Paginator

from .models import Product, SubCategory, Category
# Create your views here.

def index(request):
    products = Product.objects.all()
    context = {'products' : products}
    return render(request, 'main/index.html', context)

def category_view(request, category):
    i_category = Category.objects.get(slug = category)
    sub_categories = SubCategory.objects.filter(category__slug=category)
    subCat_ids = [o.id for o in sub_categories]
    products = Product.objects.filter(subCategory__id__in = subCat_ids)
    paginator = Paginator(products, 15)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'sub_categories' : sub_categories, 'products' : products, 'category' : i_category, 'page_obj': page_obj}
    return render(request, 'main/category_view.html', context)

def subCategory_view(request, category, subCategory):
    i_category = Category.objects.get(slug = category)
    i_subCategory = SubCategory.objects.get(slug = subCategory)
    products = Product.objects.filter(subCategory__slug = subCategory)
    paginator = Paginator(products, 15)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'products' : products, 'category' : i_category, 'subCategory' : i_subCategory, 'page_obj': page_obj}
    return render(request, 'main/subCategory_view.html', context)
    
def product_view(request, category, subCategory, product):
    i_product = Product.objects.get(slug = product)
    context = {'product' : i_product}
    return render(request, 'main/product_view.html', context)

def search_view(request):
    if request.method == 'POST':
        search_query = request.POST['search_query']
        search_products = Product.objects.filter(title__icontains = search_query) 
        context = {'result_products' : search_products}
        return render(request, 'main/search_result.html', context)