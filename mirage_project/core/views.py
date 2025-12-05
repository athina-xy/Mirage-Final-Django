from django.shortcuts import render
from .models import Item

# Create your views here.
def home(request):
    items = Item.objects.all().order_by('-created_at')
    context = {
        'items': items,
    }
    return render(request, 'core/home.html', context)
