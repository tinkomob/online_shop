from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404,redirect
from django.core.paginator import Paginator
from django.contrib import messages

from .models import Product, SubCategory, Category, Review
from accounts.models import Profile
# Create your views here.


def index(request):
    products = Product.objects.all()
     
    if request.method == 'GET' and 'sort' in request.GET and 'ord' in request.GET:
        sort = request.GET['sort']
        ord = request.GET['ord']
        if sort == 'price' and ord == 'desc':
            products = Product.objects.order_by('-price')
        if sort == 'price' and ord == 'asc':
            products = Product.objects.order_by('price')
        if sort == 'date' and ord == 'new':
            products = Product.objects.order_by('-date_added')
        if sort == 'date' and ord == 'old':
            products = Product.objects.order_by('date_added')
        if sort == 'rating' and ord == 'big':
            products = Product.objects.order_by('-rating')
        if sort == 'rating' and ord == 'small':
            products = Product.objects.order_by('rating')

    context = {'products' : products}
    return render(request, 'main/index.html', context)

def category_view(request, category):
    i_category = Category.objects.get(slug = category)
    sub_categories = SubCategory.objects.filter(category__slug=category)
    subCat_ids = [o.id for o in sub_categories]
    products = Product.objects.filter(subCategory__id__in = subCat_ids)
    
    if request.method == 'GET' and 'sort' in request.GET and 'ord' in request.GET:
        sort = request.GET['sort']
        ord = request.GET['ord']
        if sort == 'price' and ord == 'desc':
            products = Product.objects.filter(subCategory__id__in = subCat_ids).order_by('-price')
        if sort == 'price' and ord == 'asc':
            products = Product.objects.filter(subCategory__id__in = subCat_ids).order_by('price')
        if sort == 'date' and ord == 'new':
            products = Product.objects.filter(subCategory__id__in = subCat_ids).order_by('-date_added')
        if sort == 'date' and ord == 'old':
            products = Product.objects.filter(subCategory__id__in = subCat_ids).order_by('date_added')
        if sort == 'rating' and ord == 'big':
            products = Product.objects.filter(subCategory__id__in = subCat_ids).order_by('-rating')
        if sort == 'rating' and ord == 'small':
            products = Product.objects.filter(subCategory__id__in = subCat_ids).order_by('rating')
        

    context = {'sub_categories' : sub_categories, 'products' : products, 'category' : i_category}
    return render(request, 'main/category_view.html', context)

def subCategory_view(request, category, subCategory):
    i_category = Category.objects.get(slug = category)
    i_subCategory = SubCategory.objects.get(slug = subCategory)
    products = Product.objects.filter(subCategory__slug = subCategory)
    if request.method == 'GET' and 'sort' in request.GET and 'ord' in request.GET:
        sort = request.GET['sort']
        ord = request.GET['ord']
        if sort == 'price' and ord == 'desc':
            products = Product.objects.filter(subCategory__slug = subCategory).order_by('-price')
        if sort == 'price' and ord == 'asc':
            products = Product.objects.filter(subCategory__slug = subCategory).order_by('price')
        if sort == 'date' and ord == 'new':
            products = Product.objects.filter(subCategory__slug = subCategory).order_by('-date_added')
        if sort == 'date' and ord == 'old':
            products = Product.objects.filter(subCategory__slug = subCategory).order_by('date_added')
        if sort == 'rating' and ord == 'big':
            products = Product.objects.filter(subCategory__slug = subCategory).order_by('-rating')
        if sort == 'rating' and ord == 'small':
            products = Product.objects.filter(subCategory__slug = subCategory).order_by('rating')
    context = {'products' : products, 'category' : i_category, 'subCategory' : i_subCategory}
    return render(request, 'main/subCategory_view.html', context)
    
def product_view(request, category, subCategory, product):
    i_product = Product.objects.get(slug = product)
    reviews = Review.objects.filter(product=i_product)
    context = {'product' : i_product, 'reviews' : reviews}
    return render(request, 'main/product_view.html', context)

def search_view(request):
    if request.method == 'POST':
        search_query = request.POST['search_query']
        search_products = Product.objects.filter(title__icontains = search_query) 
        context = {'result_products' : search_products}
        return render(request, 'main/search_result.html', context)
def add_rev(request, product_id):
    if request.method == 'POST':
        text = request.POST['text']
        rate = request.POST['rate']
        author = get_object_or_404(Profile, user=request.user)
        product = Product.objects.get(id=product_id)

        review = Review()
        review.product = product
        review.author = author
        review.rate = rate
        review.text = text
        review.save()
        product.save()
    messages.info(request, "Вы успешно оставили отзыв!")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
def del_rev(request, rev_id,product_id):
    product = Product.objects.get(id=product_id)
    review = Review.objects.get(id=rev_id)
    review.delete()
    product.save()
    messages.info(request, "Отзыв успешно удалён!")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
def upd_rev(request, rev_id,product_id):
    if request.method == 'POST':
        text = request.POST['text']
        rate = request.POST['rate']
        author = get_object_or_404(Profile, user=request.user)
        product = Product.objects.get(id=product_id)

        review = Review.objects.get(id=rev_id)
        review.product = product
        review.author = author
        review.rate = rate
        review.text = text
        review.save()
        product.save()
        messages.info(request, "Отзыв успешно изменён!")
        return redirect(reverse_lazy('accounts:my_profile'))
        
    else:    
        product = Product.objects.get(id=product_id)
        review = Review.objects.get(id=rev_id)
        context = {'review' : review, 'product':product}
        return render(request, 'main/update_review.html', context)
