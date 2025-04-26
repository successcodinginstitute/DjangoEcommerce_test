from .models import Cart, Category

def cart_count(request):
    if request.user.is_authenticated:
        count = Cart.objects.filter(user=request.user).count()
    else:
        count = 0
    return {'cart_count': count}

def categories_context(request):
    categories = Category.objects.all()
    print("Categories==>",categories)
    return {'nav_categories': categories}

def global_context(request):
    # Cart count
    if request.user.is_authenticated:
        cart_count = Cart.objects.filter(user=request.user).count()
    else:
        cart_count = 0

    # Categories
    categories = Category.objects.all()

    return {
        'cart_count': cart_count,
        'nav_categories': categories
    }
