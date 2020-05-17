def categories(request):
    from shop.models import Category, SubCategory
    return {'categories': Category.objects.all()}

def search_form(request):
    from shop.forms import SearchForm
    form  = SearchForm()
    return {'form': form}