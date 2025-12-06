from django.shortcuts import render
from .models import Item
from .models import Item, Category, SubCategory
from django.db.models import Q

# Create your views here.
def home(request):
    query = request.GET.get('q', '').strip()
    category_slug = request.GET.get('category', '').strip()
    subcategory_slug = request.GET.get('subcategory', '').strip()
    rarity = request.GET.get('rarity', '').strip()
    min_price = request.GET.get('min_price', '').strip()
    max_price = request.GET.get('max_price', '').strip()

    items = Item.objects.all().order_by('-created_at')

    if query:
        items = items.filter(
            Q(label__icontains=query) |
            Q(description__icontains=query) |
            Q(element__icontains=query) |
            Q(reality_fragment__icontains=query)
        )

    if category_slug:
        items = items.filter(category__url_name=category_slug)

    if subcategory_slug:
        items = items.filter(subcategory__url_name=subcategory_slug)

    if rarity:
        items = items.filter(rarity=rarity)

    if min_price:
        try:
            items = items.filter(price__gte=float(min_price))
        except ValueError:
            pass

    if max_price:
        try:
            items = items.filter(price__lte=float(max_price))
        except ValueError:
            pass

    categories = Category.objects.all().order_by('label')
    subcategories = SubCategory.objects.all().order_by('label')

    context = {
        'items': items,
        'categories': categories,
        'subcategories': subcategories,
        'selected_category': category_slug,
        'selected_subcategory': subcategory_slug,
        'selected_rarity': rarity,
        'query': query,
        'min_price': min_price,
        'max_price': max_price,
    }
    return render(request, 'core/home.html', context)
